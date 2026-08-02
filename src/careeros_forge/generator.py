from dataclasses import dataclass
from pathlib import Path

from .context import GenerationContext
from .registry import discover_modules


@dataclass(frozen=True)
class GenerationReport:
    root: Path
    generated: tuple[str, ...]
    skipped: tuple[str, ...]
    unknown: tuple[str, ...]


def generate_project_with_report(config) -> GenerationReport:
    output_directory = config.output_directory
    if not output_directory.is_absolute():
        output_directory = config.config_directory / output_directory
    root = output_directory / config.project_name
    context = GenerationContext(config=config, root=root)
    registry = discover_modules()

    requested = tuple(dict.fromkeys(config.modules))
    generated = ["base"]
    base_module = registry.get("base")
    if base_module is None:
        raise RuntimeError("required base module was not discovered")
    base_module.generate(context)

    for module_name in requested:
        if module_name == "base":
            continue
        module = registry.get(module_name)
        if module is not None:
            module.generate(context)
            generated.append(module_name)

    unknown = tuple(name for name in requested if registry.get(name) is None)
    skipped = tuple(name for name in registry.names if name not in generated)
    return GenerationReport(root, tuple(generated), skipped, unknown)


def generate_project(config):
    """Generate a project and return its root, preserving the original API."""

    return generate_project_with_report(config).root
