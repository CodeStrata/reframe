"""Resource manifest, tags and deletion rules (specification section 8).

Reframe can only ever delete what it created. A resource is eligible for
clean start or teardown only when it is in the project's resource manifest
and, where AWS supports tags, carries ManagedBy=reframe and the matching
ReframeProject tag. A tag alone never authorizes deletion: a tagged resource
missing from the manifest is listed for review. Resources AWS cannot tag are
tracked, and deleted, by the manifest alone. Client-owned resources are never
tagged or deleted. Every deletion is listed with its estimated cost and
needs a person's confirmation of exactly that list.
"""

from __future__ import annotations

import enum
from dataclasses import dataclass, field
from decimal import Decimal

MANAGED_BY = "ManagedBy"
PROJECT_TAG = "ReframeProject"
RUN_TAG = "ReframeRun"


class LifecycleOwner(enum.Enum):
    TERRAFORM = "terraform"
    TRANSFORM_ADAPTER = "transform_adapter"


class ResourceError(Exception):
    """A resource rule would be broken. Nothing was changed."""


def default_tags(project: str, run: str) -> dict[str, str]:
    """The tags on every resource Reframe creates: Terraform default tags, and the Transform adapter where AWS supports tags."""
    if not project or not run:
        raise ResourceError("tags name the project and the run")
    return {MANAGED_BY: "reframe", PROJECT_TAG: project, RUN_TAG: run}


@dataclass(frozen=True)
class ManifestEntry:
    resource_id: str
    resource_type: str
    owner: LifecycleOwner
    taggable: bool
    project: str
    run: str


@dataclass
class Manifest:
    project: str
    entries: dict[str, ManifestEntry] = field(default_factory=dict)

    def record(self, entry: ManifestEntry) -> None:
        if entry.project != self.project:
            raise ResourceError(f"{entry.resource_id} belongs to project {entry.project}, not {self.project}")
        existing = self.entries.get(entry.resource_id)
        if existing and existing.owner is not entry.owner:
            raise ResourceError(f"{entry.resource_id} already has lifecycle owner {existing.owner.value}; each resource has one")
        self.entries[entry.resource_id] = entry


@dataclass(frozen=True)
class Observed:
    """A resource as read-only checks see it in the account."""

    resource_id: str
    resource_type: str
    tags: dict[str, str] | None
    """None when AWS does not support tags on this resource type."""
    client_owned: bool = False
    active_jobs: tuple[str, ...] = ()
    used_by: tuple[str, ...] = ()
    """Projects or stacks outside this project that depend on it."""
    estimated_monthly_usd: Decimal = Decimal(0)


class Verdict(enum.Enum):
    ELIGIBLE = "ELIGIBLE"
    REVIEW = "REVIEW"
    REFUSED = "REFUSED"


@dataclass(frozen=True)
class PlanItem:
    resource_id: str
    verdict: Verdict
    reason: str
    estimated_monthly_usd: Decimal


@dataclass(frozen=True)
class DeletionPlan:
    project: str
    items: tuple[PlanItem, ...]

    @property
    def eligible(self) -> tuple[str, ...]:
        return tuple(item.resource_id for item in self.items if item.verdict is Verdict.ELIGIBLE)

    @property
    def estimated_monthly_usd(self) -> Decimal:
        return sum((item.estimated_monthly_usd for item in self.items if item.verdict is Verdict.ELIGIBLE), Decimal(0))


def plan_deletion(manifest: Manifest, observed: list[Observed]) -> DeletionPlan:
    """Sort every observed resource into eligible, for review, or refused. Nothing is deleted here."""
    items = []
    for resource in sorted(observed, key=lambda r: r.resource_id):
        entry = manifest.entries.get(resource.resource_id)
        items.append(PlanItem(resource.resource_id, *_verdict(manifest.project, entry, resource), resource.estimated_monthly_usd))
    seen = {resource.resource_id for resource in observed}
    for resource_id in sorted(set(manifest.entries) - seen):
        items.append(PlanItem(resource_id, Verdict.REVIEW, "in the manifest but not found in the account; nothing to delete, check the manifest", Decimal(0)))
    return DeletionPlan(manifest.project, tuple(items))


def _verdict(project: str, entry: ManifestEntry | None, resource: Observed) -> tuple[Verdict, str]:
    if resource.client_owned:
        return Verdict.REFUSED, "client-owned; never tagged or deleted"
    tagged_ours = resource.tags is not None and resource.tags.get(MANAGED_BY) == "reframe" and resource.tags.get(PROJECT_TAG) == project
    if entry is None:
        if tagged_ours:
            return Verdict.REVIEW, "tagged for this project but missing from the manifest; a tag alone never authorizes deletion"
        return Verdict.REFUSED, "not in the manifest; Reframe did not create it"
    if resource.active_jobs:
        return Verdict.REFUSED, f"active jobs use it: {', '.join(resource.active_jobs)}"
    if resource.used_by:
        return Verdict.REFUSED, f"shared: also used by {', '.join(resource.used_by)}"
    if resource.tags is None:
        if entry.taggable:
            return Verdict.REVIEW, "the manifest says it is taggable but no tags could be read"
        return Verdict.ELIGIBLE, "in the manifest; AWS cannot tag this resource, so the manifest alone decides"
    if not tagged_ours:
        return Verdict.REVIEW, "in the manifest but missing the ManagedBy and ReframeProject tags for this project"
    return Verdict.ELIGIBLE, "in the manifest and tagged for this project"


@dataclass(frozen=True)
class Confirmation:
    by: str
    resource_ids: tuple[str, ...]
    estimated_monthly_usd: Decimal


def confirm(plan: DeletionPlan, by: str, resource_ids: list[str] | tuple[str, ...], estimated_monthly_usd: Decimal) -> Confirmation:
    """A person confirms exactly the eligible list and the cost they were shown."""
    if not by:
        raise ResourceError("a deletion is confirmed by a named person")
    if not plan.eligible:
        raise ResourceError("nothing in the plan is eligible for deletion")
    if tuple(sorted(resource_ids)) != tuple(sorted(plan.eligible)):
        raise ResourceError("the confirmation must name exactly the eligible items it was shown")
    if estimated_monthly_usd != plan.estimated_monthly_usd:
        raise ResourceError("the confirmation must acknowledge the estimated cost it was shown")
    return Confirmation(by, tuple(sorted(resource_ids)), estimated_monthly_usd)


def teardown_order(include_data: bool, export_verified: bool) -> list[str]:
    """Teardown keeps project data unless asked; with --include-data a verified export comes first."""
    if not include_data:
        return ["delete manifest-owned resources", "keep project data"]
    if not export_verified:
        raise ResourceError("--include-data needs a verified reframe export before any data is deleted")
    return ["verified export written", "delete manifest-owned resources", "delete project data after confirmation"]


def adopt(manifest: Manifest, stack: list[Observed], run: str, owner: LifecycleOwner, by: str) -> list[ManifestEntry]:
    """reframe resources adopt: bring a stack created outside Reframe into the manifest, after checks and confirmation.

    Refuses a client-owned, shared or busy stack even after confirmation. The
    caller applies the returned entries' tags.
    """
    if not by:
        raise ResourceError("adopting a stack needs its own confirmation by a named person")
    if not stack:
        raise ResourceError("an empty or unknown stack is refused")
    problems = []
    for resource in stack:
        if resource.client_owned:
            problems.append(f"{resource.resource_id} is client-owned")
        if resource.used_by:
            problems.append(f"{resource.resource_id} is shared with {', '.join(resource.used_by)}")
        if resource.active_jobs:
            problems.append(f"{resource.resource_id} has active jobs")
        if resource.tags and resource.tags.get(PROJECT_TAG) not in (None, manifest.project):
            problems.append(f"{resource.resource_id} is tagged for project {resource.tags[PROJECT_TAG]}")
    if problems:
        raise ResourceError("adopt refused: " + "; ".join(problems))
    entries = [ManifestEntry(r.resource_id, r.resource_type, owner, r.tags is not None, manifest.project, run) for r in stack]
    for entry in entries:
        manifest.record(entry)
    return entries
