from importlib import import_module
from pkgutil import iter_modules

from .module import ForgeModule


class ModuleRegistry:
    """Registry of modules available to the project generator."""

    def __init__(self) -> None:
        self._modules: dict[str, ForgeModule] = {}

    def register(self, module: ForgeModule) -> None:
        if not module.name:
            raise ValueError("module name is required")
        if module.name in self._modules:
            raise ValueError(f"module already registered: {module.name}")
        self._modules[module.name] = module

    def get(self, name: str) -> ForgeModule | None:
        return self._modules.get(name)

    @property
    def names(self) -> tuple[str, ...]:
        return tuple(sorted(self._modules))


def discover_modules() -> ModuleRegistry:
    """Import bundled module packages and register their MODULE instances."""

    from . import modules

    registry = ModuleRegistry()
    for module_info in iter_modules(modules.__path__, f"{modules.__name__}."):
        discovered = import_module(module_info.name)
        module = getattr(discovered, "MODULE", None)
        if isinstance(module, ForgeModule):
            registry.register(module)
    return registry
