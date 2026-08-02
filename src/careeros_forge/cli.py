from pathlib import Path
from .config import load_config
from .generator import generate_project_with_report

def main():
    path = Path("forge.json")
    if not path.exists():
        raise SystemExit("forge.json not found.")
    config = load_config(path)
    report = generate_project_with_report(config)
    print(f"Created: {report.root}")
    print(f"Generated modules: {', '.join(report.generated)}")
    if report.skipped:
        print(f"Skipped modules: {', '.join(report.skipped)}")
    if report.unknown:
        print(f"Unknown modules: {', '.join(report.unknown)}")
