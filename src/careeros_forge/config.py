from dataclasses import dataclass
from pathlib import Path
import json

@dataclass(frozen=True)
class ForgeConfig:
    project_name: str
    output_directory: Path
    modules: tuple[str, ...]

def load_config(path: Path) -> ForgeConfig:
    data = json.loads(path.read_text(encoding="utf-8"))
    name = str(data.get("project_name","")).strip()
    if not name:
        raise ValueError("project_name is required")
    return ForgeConfig(name, Path(data.get("output_directory","./generated")), tuple(data.get("modules",["base"])))
