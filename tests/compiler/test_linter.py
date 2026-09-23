from compiler.linter import lint_source
from cli.kuro import cmd_lint


def test_linter_reports_unused_declarations():
    diags = lint_source("Unused is Integers;\nPrint 1.")
    assert any(d.code == "W7001" for d in diags.diagnostics)


def test_linter_reports_tabs_and_trailing_whitespace(tmp_path):
    path = tmp_path / "main.kuro"
    path.write_text("If 1 is equal to 1;\n\tPrint 1.  \nDone.\n")
    assert cmd_lint(str(path)) == 0
    diags = lint_source(path.read_text(), str(path))
    assert {d.code for d in diags.diagnostics} >= {"W7002", "W7003"}
    assert cmd_lint(str(path), strict=True) == 1
