from pathlib import Path

import pytest
from jinja2 import UndefinedError

from careeros_forge.config import ForgeConfig
from careeros_forge.context import GenerationContext
from careeros_forge.template_renderer import TemplateRenderer


def test_renders_packaged_template() -> None:
    content = TemplateRenderer().render(
        "base/README.md.j2",
        project_name="Demo",
        modules=("base", "resume"),
    )

    assert content.startswith("# Demo\n")
    assert "- resume" in content


def test_missing_template_has_clear_error() -> None:
    with pytest.raises(ValueError, match="template not found: missing.j2"):
        TemplateRenderer().render("missing.j2")


def test_missing_template_value_fails_loudly() -> None:
    with pytest.raises(UndefinedError, match="project_name.*undefined"):
        TemplateRenderer().render("resume/README.md.j2")


def test_context_renders_template_to_project(tmp_path: Path) -> None:
    config = ForgeConfig("Demo", tmp_path, ("base",))
    context = GenerationContext(config, tmp_path / "Demo")

    output = context.render_template(
        "resume/README.md.j2",
        "custom/resume.md",
        project_name=config.project_name,
    )

    assert output.read_text(encoding="utf-8").startswith("# Demo Resume")


def test_html_templates_escape_resume_data() -> None:
    resume = {
        "basics": {"name": "<script>alert(1)</script>", "headline": "", "summary": ""},
        "experience": [],
        "education": [],
        "skills": [],
        "projects": [],
    }

    content = TemplateRenderer().render("resume/index.html.j2", resume=resume)

    assert "&lt;script&gt;alert(1)&lt;/script&gt;" in content
    assert "<script>alert(1)</script>" not in content


def test_html_templates_hide_archived_records() -> None:
    resume = {
        "basics": {"name": "Demo", "headline": "", "summary": ""},
        "experience": [{
            "id": "old-role",
            "status": "archived",
            "organization": "Hidden Company",
            "position": "Old Role",
            "start_date": "2020",
            "highlights": [],
        }],
        "education": [],
        "skills": [],
        "projects": [],
    }

    content = TemplateRenderer().render("resume/index.html.j2", resume=resume)

    assert "Hidden Company" not in content
    assert "Add verified experience records" in content
