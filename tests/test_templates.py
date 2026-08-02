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
