from pathlib import Path

from careeros_forge.config import ForgeConfig
from careeros_forge.generator import generate_project, generate_project_with_report
from careeros_forge.registry import discover_modules

def test_generate_project(tmp_path: Path):
    root = generate_project(ForgeConfig("Demo", tmp_path, ("base",)))
    assert (root / "README.md").exists()
    assert (root / "backend").is_dir()
    assert "- base" in (root / "README.md").read_text(encoding="utf-8")


def test_discovers_bundled_modules():
    assert discover_modules().names == ("base", "resume")


def test_generate_resume_module(tmp_path: Path):
    root = generate_project(ForgeConfig("Demo", tmp_path, ("base", "resume")))

    assert (root / "resume" / "README.md").exists()
    assert (root / "resume" / "resume.json").exists()
    assert (root / "resume" / "index.html").exists()
    assert '"experience": []' in (
        root / "resume" / "resume.json"
    ).read_text(encoding="utf-8")
    assert "Add verified experience records" in (
        root / "resume" / "index.html"
    ).read_text(encoding="utf-8")


def test_does_not_generate_unselected_resume_module(tmp_path: Path):
    root = generate_project(ForgeConfig("Demo", tmp_path, ("base",)))

    assert not (root / "resume").exists()


def test_unknown_modules_preserve_base_generation(tmp_path: Path):
    root = generate_project(ForgeConfig("Demo", tmp_path, ("future-module",)))

    assert (root / "README.md").exists()


def test_generation_report_tracks_generated_skipped_and_unknown(tmp_path: Path):
    report = generate_project_with_report(
        ForgeConfig("Demo", tmp_path, ("resume", "future-module", "resume"))
    )

    assert report.generated == ("base", "resume")
    assert report.skipped == ()
    assert report.unknown == ("future-module",)


def test_generation_report_tracks_unselected_modules(tmp_path: Path):
    report = generate_project_with_report(ForgeConfig("Demo", tmp_path, ("base",)))

    assert report.generated == ("base",)
    assert report.skipped == ("resume",)
    assert report.unknown == ()
