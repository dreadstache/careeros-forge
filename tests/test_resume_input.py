import json
from pathlib import Path

import pytest

from careeros_forge.config import ForgeConfig
from careeros_forge.generator import generate_project
from careeros_forge.schema_validator import SchemaValidationError


def resume_data() -> dict[str, object]:
    return {
        "basics": {
            "name": "Ada Lovelace",
            "headline": "Computing Pioneer",
            "summary": "Turns ideas into instructions.",
        },
        "experience": [
            {
                "organization": "Analytical Engine",
                "position": "Programmer",
                "start_date": "1842",
                "highlights": ["Published the first algorithm"],
            }
        ],
        "education": [],
        "skills": [{"name": "Mathematics", "keywords": ["Algorithms"]}],
        "projects": [],
    }


def configured_project(tmp_path: Path, data_file: str) -> ForgeConfig:
    return ForgeConfig(
        "Demo",
        tmp_path / "output",
        ("resume",),
        {"resume": {"data_file": data_file}},
        tmp_path,
    )


def test_resume_module_generates_from_relative_data_file(tmp_path: Path) -> None:
    source = tmp_path / "career.json"
    source.write_text(json.dumps(resume_data()), encoding="utf-8")

    root = generate_project(configured_project(tmp_path, "career.json"))

    html = (root / "resume" / "index.html").read_text(encoding="utf-8")
    generated_data = json.loads(
        (root / "resume" / "resume.json").read_text(encoding="utf-8")
    )
    instructions = (root / "resume" / "README.md").read_text(encoding="utf-8")
    assert "Ada Lovelace" in html
    assert "Published the first algorithm" in html
    assert generated_data == resume_data()
    assert "career.json" in instructions


def test_resume_module_rejects_missing_data_file(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="resume data file not found"):
        generate_project(configured_project(tmp_path, "missing.json"))


def test_resume_module_rejects_invalid_input_before_resume_output(
    tmp_path: Path,
) -> None:
    source = tmp_path / "career.json"
    source.write_text('{"basics": {}}', encoding="utf-8")

    with pytest.raises(SchemaValidationError):
        generate_project(configured_project(tmp_path, "career.json"))

    assert not (tmp_path / "output" / "Demo" / "resume").exists()


def test_resume_module_generates_filtered_profiles(tmp_path: Path) -> None:
    data = resume_data()
    data["experience"][0]["id"] = "experience-engine"
    data["skills"][0]["id"] = "skills-math"
    source = tmp_path / "career.json"
    source.write_text(json.dumps(data), encoding="utf-8")
    config = ForgeConfig(
        "Demo",
        tmp_path / "output",
        ("resume",),
        {"resume": {"data_file": "career.json", "profiles": [{
            "slug": "computing",
            "title": "Computing Resume",
            "headline": "Algorithm Designer",
            "experience_ids": ["experience-engine"],
            "skill_ids": ["skills-math"],
            "project_ids": [],
        }]}},
        tmp_path,
    )

    root = generate_project(config)

    profile = json.loads((root / "resume" / "computing" / "resume.json").read_text(encoding="utf-8"))
    html = (root / "resume" / "computing" / "index.html").read_text(encoding="utf-8")
    assert profile["basics"]["headline"] == "Algorithm Designer"
    assert [item["id"] for item in profile["experience"]] == ["experience-engine"]
    assert profile["projects"] == []
    assert "Computing Resume" in html
