from ..context import GenerationContext
from ..module import ForgeModule


DEFAULT_DIRECTORIES = (
    "backend",
    "frontend",
    "database",
    "docs",
    "templates",
    "assets",
    "scripts",
    "exports",
)


class BaseModule(ForgeModule):
    name = "base"

    def generate(self, context: GenerationContext) -> None:
        context.ensure_directory(".")
        for name in DEFAULT_DIRECTORIES:
            context.ensure_directory(name)
            context.write_text(f"{name}/.gitkeep", "")
        context.render_template(
            "base/README.md.j2",
            "README.md",
            project_name=context.config.project_name,
            modules=context.config.modules,
        )
        context.render_template("base/gitignore.template", ".gitignore")


MODULE = BaseModule()
