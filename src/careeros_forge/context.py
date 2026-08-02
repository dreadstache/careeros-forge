from dataclasses import dataclass, field
from pathlib import Path

from .config import ForgeConfig
from .filesystem import ensure_directory, write_text
from .template_renderer import TemplateRenderer


@dataclass(frozen=True)
class GenerationContext:
    """Shared state and filesystem helpers available to Forge modules."""

    config: ForgeConfig
    root: Path
    renderer: TemplateRenderer = field(
        default_factory=TemplateRenderer,
        repr=False,
        compare=False,
    )

    def ensure_directory(self, relative_path: str | Path) -> Path:
        path = self.root / relative_path
        ensure_directory(path)
        return path

    def write_text(self, relative_path: str | Path, content: str) -> Path:
        path = self.root / relative_path
        write_text(path, content)
        return path

    def render_template(
        self,
        template_name: str,
        relative_path: str | Path,
        **values: object,
    ) -> Path:
        content = self.renderer.render(template_name, **values)
        return self.write_text(relative_path, content)
