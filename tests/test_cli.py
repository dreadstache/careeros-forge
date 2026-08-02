import json
from pathlib import Path

from careeros_forge.cli import main


def test_cli_reports_module_outcomes(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    config = {
        "project_name": "Demo",
        "output_directory": str(tmp_path / "generated"),
        "modules": ["resume", "future-module"],
    }
    (tmp_path / "forge.json").write_text(json.dumps(config), encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    main([])

    output = capsys.readouterr().out
    assert "Generated modules: base, resume" in output
    assert "Unknown modules: future-module" in output


def test_cli_can_preview_populated_example(tmp_path: Path, monkeypatch, capsys) -> None:
    repository_root = Path(__file__).parents[1]
    source_config = json.loads(
        (repository_root / "examples" / "forge.example.json").read_text(
            encoding="utf-8"
        )
    )
    source_config["output_directory"] = str(tmp_path / "generated")
    source_config["module_options"]["resume"]["data_file"] = str(
        repository_root / "examples" / "career-data.example.json"
    )
    config_path = tmp_path / "forge.example.json"
    config_path.write_text(json.dumps(source_config), encoding="utf-8")
    opened: list[str] = []
    monkeypatch.setattr("careeros_forge.cli.webbrowser.open", opened.append)

    main(["--config", str(config_path), "--preview"])

    output = capsys.readouterr().out
    assert "Generated modules: base, resume" in output
    assert "Preview:" in output
    assert opened and opened[0].startswith("file:")
