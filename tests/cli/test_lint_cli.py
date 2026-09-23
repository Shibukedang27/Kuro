from cli.kuro import main


def test_lint_command_is_reachable_through_cli(tmp_path, capsys):
    path = tmp_path / "main.kuro"
    path.write_text('Print "clean".', encoding="utf-8")
    assert main(["kuro", "lint", str(path)]) == 0
    assert capsys.readouterr().err == ""


def test_lint_strict_command_reports_diagnostics(tmp_path, capsys):
    path = tmp_path / "main.kuro"
    path.write_text("Unused is Integers;\nPrint 1.", encoding="utf-8")
    assert main(["kuro", "lint", str(path), "--strict"]) == 1
    assert capsys.readouterr().err
