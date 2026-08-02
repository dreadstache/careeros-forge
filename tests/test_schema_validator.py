import pytest

from careeros_forge.schema_validator import (
    SchemaValidationError,
    validate_json_text,
)


def test_resume_schema_accepts_generated_shape() -> None:
    content = """{
      "basics": {"name": "", "headline": "", "summary": ""},
      "experience": [],
      "education": [],
      "skills": [],
      "projects": []
    }"""

    validate_json_text(content, "resume")


def test_resume_schema_rejects_missing_sections() -> None:
    with pytest.raises(SchemaValidationError, match="education.*required"):
        validate_json_text(
            '{"basics":{"name":"","headline":"","summary":""},'
            '"experience":[],"skills":[],"projects":[]}',
            "resume",
        )


def test_resume_schema_rejects_invalid_json() -> None:
    with pytest.raises(SchemaValidationError, match="invalid JSON at line 1"):
        validate_json_text("{broken", "resume")
