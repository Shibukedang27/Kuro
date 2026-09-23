from compiler.pipeline import compile_source, run_source


def test_relative_imports_are_compiled_as_one_kuro_program(tmp_path):
    lib = tmp_path / "lib.kuro"
    app = tmp_path / "app.kuro"
    lib.write_text('Greeting = "hello";\n', encoding="utf-8")
    app.write_text('Import "lib.kuro";\nPrint Greeting.', encoding="utf-8")
    result = run_source(app.read_text(), filename=str(app))
    assert result.ok
    assert result.stdout == "hello\n"


def test_missing_import_is_a_module_diagnostic(tmp_path):
    app = tmp_path / "app.kuro"
    app.write_text('Import "missing.kuro";\nPrint "x".', encoding="utf-8")
    result = compile_source(app.read_text(), filename=str(app))
    assert not result.ok
    assert any(d.code == "E5001" for d in result.diags.diagnostics)


def test_import_cycles_are_rejected(tmp_path):
    a = tmp_path / "a.kuro"
    b = tmp_path / "b.kuro"
    a.write_text('Import "b.kuro";\nPrint "a".', encoding="utf-8")
    b.write_text('Import "a.kuro";\nPrint "b".', encoding="utf-8")
    result = compile_source(a.read_text(), filename=str(a))
    assert not result.ok
    assert any(d.code == "E5002" for d in result.diags.diagnostics)


def test_import_cannot_escape_project_root(tmp_path):
    outside = tmp_path.parent / "outside.kuro"
    outside.write_text('Print "outside".', encoding="utf-8")
    app = tmp_path / "app.kuro"
    app.write_text('Import "../outside.kuro";\nPrint "safe".', encoding="utf-8")
    result = compile_source(app.read_text(encoding="utf-8"), filename=str(app))
    assert not result.ok
    assert any(d.code == "E5003" for d in result.diags.diagnostics)
