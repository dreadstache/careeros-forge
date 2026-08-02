import json
from pathlib import Path

from ..context import GenerationContext
from ..module import ForgeModule
from ..schema_validator import validate_json_text


class ResumeModule(ForgeModule):
    name = "resume"

    def generate(self, context: GenerationContext) -> None:
        resume_json, resume_data, source_name = self._load_data(context)
        context.render_template(
            "resume/README.md.j2",
            "resume/README.md",
            project_name=context.config.project_name,
            source_name=source_name,
        )
        context.write_text("resume/resume.json", resume_json)
        context.render_template(
            "resume/index.html.j2",
            "resume/index.html",
            resume=resume_data,
        )

    def _load_data(
        self, context: GenerationContext
    ) -> tuple[str, object, str | None]:
        options = context.config.module_options.get(self.name, {})
        configured_path = options.get("data_file")
        if configured_path is None:
            content = context.renderer.render("resume/resume.json.j2")
            return content, validate_json_text(content, "resume"), None

        source = Path(str(configured_path))
        if not source.is_absolute():
            source = context.config.config_directory / source
        if not source.is_file():
            raise ValueError(f"resume data file not found: {source}")

        content = source.read_text(encoding="utf-8")
        data = validate_json_text(content, "resume")
        canonical_content = json.dumps(data, indent=2, ensure_ascii=False) + "\n"
        return canonical_content, data, str(configured_path)


MODULE = ResumeModule()
