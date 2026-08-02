import argparse
from pathlib import Path
import webbrowser
from .config import load_config
from .generator import generate_project_with_report

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Generate a CareerOS Forge project.")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("forge.json"),
        help="Path to a Forge configuration file (default: forge.json).",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Open the generated resume HTML when available.",
    )
    return parser


def main(argv: list[str] | None = None):
    args = build_parser().parse_args(argv)
    path = args.config
    if not path.exists():
        raise SystemExit(f"configuration file not found: {path}")
    config = load_config(path)
    report = generate_project_with_report(config)
    print(f"Created: {report.root}")
    print(f"Generated modules: {', '.join(report.generated)}")
    if report.skipped:
        print(f"Skipped modules: {', '.join(report.skipped)}")
    if report.unknown:
        print(f"Unknown modules: {', '.join(report.unknown)}")
    preview = report.root / "resume" / "index.html"
    if args.preview:
        if not preview.is_file():
            raise SystemExit("resume preview was not generated")
        webbrowser.open(preview.resolve().as_uri())
        print(f"Preview: {preview}")
