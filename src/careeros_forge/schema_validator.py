import json
from functools import lru_cache
from importlib.resources import files
from typing import Any

from jsonschema import Draft202012Validator


class SchemaValidationError(ValueError):
    """Raised when Forge data does not match its declared JSON Schema."""


@lru_cache(maxsize=None)
def load_schema(schema_name: str) -> dict[str, Any]:
    resource = files("careeros_forge.schemas").joinpath(f"{schema_name}.schema.json")
    if not resource.is_file():
        raise ValueError(f"schema not found: {schema_name}")
    schema = json.loads(resource.read_text(encoding="utf-8"))
    Draft202012Validator.check_schema(schema)
    return schema


def validate_data(data: object, schema_name: str) -> None:
    validator = Draft202012Validator(load_schema(schema_name))
    errors = sorted(validator.iter_errors(data), key=lambda error: list(error.path))
    if not errors:
        return

    error = errors[0]
    location = ".".join(str(part) for part in error.absolute_path) or "root"
    raise SchemaValidationError(
        f"{schema_name} validation failed at {location}: {error.message}"
    )


def validate_json_text(content: str, schema_name: str) -> object:
    try:
        data = json.loads(content)
    except json.JSONDecodeError as error:
        raise SchemaValidationError(
            f"{schema_name} contains invalid JSON at line {error.lineno}, "
            f"column {error.colno}: {error.msg}"
        ) from error
    validate_data(data, schema_name)
    return data
