from dataclasses import dataclass
from pathlib import Path
import json

from .schema_validator import validate_data

@dataclass(frozen=True)
class ForgeConfig:
    project_name: str
    output_directory: Path
    modules: tuple[str, ...]

def load_config(path: Path) -> ForgeConfig:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ValueError(
            f"forge-config contains invalid JSON at line {error.lineno}, "
            f"column {error.colno}: {error.msg}"
        ) from error
    validate_data(data, "forge-config")
    name = str(data.get("project_name","")).strip()
    if not name:
        raise ValueError("project_name is required")
    return ForgeConfig(name, Path(data.get("output_directory","./generated")), tuple(data.get("modules",["base"])))
