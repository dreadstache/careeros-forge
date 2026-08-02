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


def test_resume_schema_accepts_typed_records() -> None:
    content = """{
      "basics": {"name": "Ada", "headline": "Engineer", "summary": "Builds."},
      "experience": [{
        "organization": "Example Studio",
        "position": "Developer",
        "start_date": "2025-01",
        "highlights": ["Shipped a project"]
      }],
      "education": [{
        "institution": "Example College",
        "credential": "Certificate",
        "start_date": "2024"
      }],
      "skills": [{"name": "Python", "keywords": ["Automation"]}],
      "projects": [{"name": "Forge", "summary": "Generator", "highlights": []}]
    }"""

    validate_json_text(content, "resume")


def test_resume_schema_rejects_incomplete_experience_record() -> None:
    content = """{
      "basics": {"name": "", "headline": "", "summary": ""},
      "experience": [{"organization": "Example Studio"}],
      "education": [], "skills": [], "projects": []
    }"""

    with pytest.raises(SchemaValidationError, match="position.*required"):
        validate_json_text(content, "resume")


def test_resume_schema_rejects_invalid_project_url() -> None:
    content = """{
      "basics": {"name": "", "headline": "", "summary": ""},
      "experience": [], "education": [], "skills": [],
      "projects": [{
        "name": "Forge", "summary": "Generator", "highlights": [],
        "url": "not a URL"
      }]
    }"""

    with pytest.raises(SchemaValidationError, match="projects.0.url"):
        validate_json_text(content, "resume")


def test_resume_schema_accepts_record_metadata() -> None:
    content = """{
      "schema_version": "1.0",
      "basics": {"name": "", "headline": "", "summary": ""},
      "experience": [{
        "id": "city-of-casper-2015",
        "status": "archived",
        "provenance": {"source": "career-data.xlsx", "source_type": "spreadsheet"},
        "organization": "City of Casper",
        "position": "Systems Analyst",
        "start_date": "2015",
        "highlights": []
      }],
      "education": [], "skills": [], "projects": []
    }"""

    validate_json_text(content, "resume")
