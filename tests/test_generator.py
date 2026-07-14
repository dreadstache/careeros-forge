from pathlib import Path
from careeros_forge.config import ForgeConfig
from careeros_forge.generator import generate_project

def test_generate_project(tmp_path: Path):
    root = generate_project(ForgeConfig("Demo", tmp_path, ("base",)))
    assert (root / "README.md").exists()
    assert (root / "backend").is_dir()
