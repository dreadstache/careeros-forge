from abc import ABC, abstractmethod

from .context import GenerationContext


class ForgeModule(ABC):
    """Interface implemented by every discoverable Forge module."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the module name used in forge.json."""

    @abstractmethod
    def generate(self, context: GenerationContext) -> None:
        """Generate this module's files inside the project root."""
