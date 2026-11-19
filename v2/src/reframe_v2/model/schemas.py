"""Load and apply the published record schemas in reframe_v2/schemas."""

from __future__ import annotations

import json
from functools import lru_cache
from importlib import resources
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource

SCHEMA_PACKAGE = "reframe_v2.schemas"


class SchemaError(ValueError):
    """A record does not match its published schema."""


@lru_cache(maxsize=1)
def _load() -> dict[str, dict[str, Any]]:
    schemas = {}
    for entry in resources.files(SCHEMA_PACKAGE).iterdir():
        if entry.name.endswith(".schema.json"):
            schemas[entry.name.removesuffix(".schema.json")] = json.loads(entry.read_text(encoding="utf-8"))
    return schemas


@lru_cache(maxsize=1)
def _registry() -> Registry:
    return Registry().with_resources((schema["$id"], Resource.from_contents(schema)) for schema in _load().values())


def catalog() -> dict[str, str]:
    """Each published schema's name and $id, for the package manifest."""
    return {name: schema["$id"] for name, schema in sorted(_load().items())}


def schema_for(record_type: str) -> dict[str, Any]:
    try:
        return _load()[record_type]
    except KeyError:
        raise SchemaError(f"no published schema for record type {record_type!r}") from None


def validate(record_json: dict[str, Any]) -> None:
    """Raise SchemaError listing every way the record breaks its schema."""
    record_type = record_json.get("record_type")
    validator = Draft202012Validator(schema_for(str(record_type)), registry=_registry())
    errors = sorted(validator.iter_errors(record_json), key=lambda error: list(error.absolute_path))
    if errors:
        lines = [f"{'/'.join(map(str, error.absolute_path)) or '(record)'}: {error.message}" for error in errors]
        raise SchemaError(f"{record_type} record does not match its schema:\n" + "\n".join(lines))


DOCUMENT_SCHEMAS = ("package_manifest", "provenance", "resources_file")


def validate_document(name: str, document: dict[str, Any]) -> None:
    """Validate a document that is not a record (package manifest, provenance, resources file) against its published schema."""
    if name not in DOCUMENT_SCHEMAS:
        raise SchemaError(f"{name!r} is not a document schema")
    validator = Draft202012Validator(schema_for(name), registry=_registry())
    errors = sorted(validator.iter_errors(document), key=lambda error: list(error.absolute_path))
    if errors:
        lines = [f"{'/'.join(map(str, error.absolute_path)) or '(document)'}: {error.message}" for error in errors]
        raise SchemaError(f"{name} does not match its schema:\n" + "\n".join(lines))
