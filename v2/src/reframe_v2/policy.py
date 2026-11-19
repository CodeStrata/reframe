"""Data policy and Claude backend destination rules (specification section 11, NFR-01, NFR-10, NFR-12).

Before any source leaves the workspace, the project's data policy decides
where it may go. The claude-cli backend is refused for customer source. A
Bedrock inference profile whose destinations fall outside the allowed
processing regions is refused before anything is sent, never swapped. The
backend and model ids are pinned per run; a missing model is never replaced.
Each request is budgeted in full against the pinned context limit, and work
that does not fit is split along dependency-safe units, never truncated.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


class PolicyRefusal(Exception):
    """The policy does not allow this. Nothing was sent."""


class OversizedUnit(PolicyRefusal):
    """One dependency-safe unit is larger than the context allows; it cannot be split further and is never truncated."""


DESTINATIONS = ("aws", "claude_backend", "github", "engineer_machine")
BACKENDS = ("claude-cli", "bedrock")


@dataclass(frozen=True)
class Backend:
    kind: str
    generation_model: str
    review_model: str
    inference_profile: str | None
    invocation_region: str | None
    allowed_processing_regions: tuple[str, ...]
    cli_version: str | None

    @classmethod
    def from_policy(cls, body: dict[str, Any]) -> Backend:
        b = body["claude_backend"]
        return cls(b["kind"], b["generation_model"], b["review_model"], b["inference_profile"], b["invocation_region"],
                   tuple(b["allowed_processing_regions"]), b["cli_version"])


def check_destination(policy: dict[str, Any], destination: str) -> None:
    """Refuse a destination the policy does not list as allowed."""
    if destination not in DESTINATIONS:
        raise PolicyRefusal(f"unknown destination {destination!r}")
    for entry in policy["data_policy"]["destinations"]:
        if entry["destination"] == destination:
            if not entry["allowed"]:
                raise PolicyRefusal(f"the data policy does not allow sending anything to {destination}")
            return
    raise PolicyRefusal(f"the data policy does not list {destination}; nothing is sent to an unlisted destination")


def check_backend(policy: dict[str, Any], profile_destinations: tuple[str, ...] | list[str] | None = None) -> Backend:
    """Check the policy's Claude backend before any source is sent.

    profile_destinations are the regions the Bedrock inference profile can
    route to, as AWS reports them; they must all be allowed.
    """
    check_destination(policy, "claude_backend")
    backend = Backend.from_policy(policy)
    if backend.kind not in BACKENDS:
        raise PolicyRefusal(f"unknown Claude backend {backend.kind!r}")
    if backend.kind == "claude-cli":
        if policy["data_policy"]["customer_source"]:
            raise PolicyRefusal("the claude-cli backend is for internal testing; it is refused for customer source")
        if not backend.cli_version:
            raise PolicyRefusal("the claude-cli backend pins a CLI version")
        return backend
    if not backend.invocation_region:
        raise PolicyRefusal("the bedrock backend records its invocation region")
    if not backend.allowed_processing_regions:
        raise PolicyRefusal("the bedrock backend lists the processing regions the policy allows")
    destinations = set(profile_destinations) if profile_destinations is not None else {backend.invocation_region}
    if backend.inference_profile and profile_destinations is None:
        raise PolicyRefusal("an inference profile's destination regions must be known before anything is sent")
    outside = sorted(destinations - set(backend.allowed_processing_regions))
    if outside:
        raise PolicyRefusal(f"the inference profile can route to {', '.join(outside)}, outside the policy; refused, not swapped")
    return backend


def provenance(backend: Backend, configured_destinations: tuple[str, ...] | list[str], reported_region: str | None) -> dict[str, Any]:
    """What provenance records about where a call was processed."""
    return {
        "backend": backend.kind,
        "model_or_profile": backend.inference_profile or backend.generation_model,
        "configured_destinations": sorted(configured_destinations),
        "processing_region": reported_region or "unknown",
    }


@dataclass(frozen=True)
class ModelPin:
    model: str
    context_tokens: int
    max_output_tokens: int


def pin_models(backend: Backend, discovered: dict[str, dict[str, int]]) -> dict[str, ModelPin]:
    """Pin the generation and review models with their context limits. A missing model is refused, never replaced."""
    pins = {}
    for role, model in (("generation", backend.generation_model), ("review", backend.review_model)):
        if model not in discovered:
            raise PolicyRefusal(f"the {role} model {model} is not available on {backend.kind}; it is never silently replaced")
        limits = discovered[model]
        pins[role] = ModelPin(model, limits["context_tokens"], limits["max_output_tokens"])
    return pins


@dataclass(frozen=True)
class Request:
    instructions: int
    tools: int
    history: int
    evidence: int
    reserved_output: int

    @property
    def total(self) -> int:
        return self.instructions + self.tools + self.history + self.evidence + self.reserved_output


def fits(pin: ModelPin, request: Request) -> bool:
    if request.reserved_output > pin.max_output_tokens:
        return False
    return request.total <= pin.context_tokens


@dataclass(frozen=True)
class Unit:
    """A dependency-safe piece of evidence: a group whose members must travel together."""

    id: str
    tokens: int
    members: tuple[str, ...] = field(default=())


def split(pin: ModelPin, fixed: Request, units: list[Unit]) -> list[list[Unit]]:
    """Pack units into requests that each fit, in the given order. A unit is never cut; one that cannot fit is refused."""
    room = pin.context_tokens - (fixed.instructions + fixed.tools + fixed.history + fixed.reserved_output)
    if fixed.reserved_output > pin.max_output_tokens or room <= 0:
        raise OversizedUnit("instructions, tools, history and reserved output alone exceed the context")
    batches: list[list[Unit]] = []
    current: list[Unit] = []
    used = 0
    for unit in units:
        if unit.tokens > room:
            raise OversizedUnit(f"{unit.id} needs {unit.tokens} tokens but a request has room for {room}; it is not truncated")
        if used + unit.tokens > room:
            batches.append(current)
            current, used = [], 0
        current.append(unit)
        used += unit.tokens
    if current:
        batches.append(current)
    return batches


@dataclass(frozen=True)
class BackendChange:
    before: str
    after: str
    by: str
    reason: str
    reruns: tuple[str, ...] = ()


def change_backend(current: Backend, new: Backend, by: str, reason: str) -> BackendChange:
    """A backend change is a recorded policy change. It reruns nothing by itself; outputs keep the backend that produced them."""
    if not by or not reason:
        raise PolicyRefusal("a backend change records who made it and why")
    if current == new:
        raise PolicyRefusal("the backend is unchanged")
    return BackendChange(f"{current.kind}:{current.generation_model}", f"{new.kind}:{new.generation_model}", by, reason)
