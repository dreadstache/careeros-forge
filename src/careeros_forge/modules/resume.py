from ..context import GenerationContext
from ..module import ForgeModule
from ..schema_validator import validate_json_text


class ResumeModule(ForgeModule):
    name = "resume"

    def generate(self, context: GenerationContext) -> None:
        context.render_template(
            "resume/README.md.j2",
            "resume/README.md",
            project_name=context.config.project_name,
        )
        resume_json = context.renderer.render("resume/resume.json.j2")
        validate_json_text(resume_json, "resume")
        context.write_text("resume/resume.json", resume_json)


MODULE = ResumeModule()
