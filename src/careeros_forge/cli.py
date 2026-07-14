from pathlib import Path
from .config import load_config
from .generator import generate_project

def main():
    path = Path("forge.json")
    if not path.exists():
        raise SystemExit("forge.json not found.")
    config = load_config(path)
    print(f"Created: {generate_project(config)}")
