import json
from pathlib import Path

import pytest

from careeros_forge.config import load_config
from careeros_forge.schema_validator import SchemaValidationError


def write_config(tmp_path: Path, data: object) -> Path:
    path = tmp_path / "forge.json"
    path.write_text(json.dumps(data), encoding="utf-8")
    return path


def test_load_config_applies_defaults(tmp_path: Path) -> None:
    config = load_config(write_config(tmp_path, {"project_name": "Demo"}))

    assert config.output_directory == Path("./generated")
    assert config.modules == ("base",)
    assert config.module_options == {}
    assert config.config_directory == tmp_path.resolve()


def test_load_config_reads_module_options(tmp_path: Path) -> None:
    config = load_config(
        write_config(
            tmp_path,
            {
                "project_name": "Demo",
                "modules": ["resume"],
                "module_options": {"resume": {"data_file": "career.json"}},
            },
        )
    )

    assert config.module_options["resume"]["data_file"] == "career.json"


@pytest.mark.parametrize(
    "data, expected",
    [
        ({}, "project_name.*required"),
        ({"project_name": "Demo", "modules": "resume"}, "modules.*array"),
        ({"project_name": "Demo", "extra": True}, "(?i)additional properties"),
        (
            {"project_name": "Demo", "modules": ["resume", "resume"]},
            "non-unique",
        ),
        (
            {
                "project_name": "Demo",
                "module_options": {"resume": {"unknown": True}},
            },
            "(?i)additional properties",
        ),
    ],
)
def test_load_config_rejects_invalid_schema(
    tmp_path: Path, data: object, expected: str
) -> None:
    with pytest.raises(SchemaValidationError, match=expected):
        load_config(write_config(tmp_path, data))


def test_load_config_rejects_invalid_json(tmp_path: Path) -> None:
    path = tmp_path / "forge.json"
    path.write_text("{broken", encoding="utf-8")

    with pytest.raises(ValueError, match="invalid JSON at line 1"):
        load_config(path)
