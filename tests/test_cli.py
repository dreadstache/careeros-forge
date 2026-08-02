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

    main()

    output = capsys.readouterr().out
    assert "Generated modules: base, resume" in output
    assert "Unknown modules: future-module" in output
