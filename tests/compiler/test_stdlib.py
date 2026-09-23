from compiler.pipeline import run_source


def test_kuro_authored_core_and_math_library_are_importable(tmp_path):
    app = tmp_path / "app.kuro"
    app.write_text(
        'Import "stdlib/core.kuro";\n'
        'Import "stdlib/math.kuro";\n'
        'Call KuroMax 4, 9;\nPrint @_.\n'
        'Call KuroAdd 2, 3;\nPrint @_.\n',
        encoding="utf-8",
    )
    # The imports are resolved relative to the application, so expose the
    # repository stdlib through a symlink-like copied directory in the test.
    import shutil
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    shutil.copytree(root / "stdlib", tmp_path / "stdlib")
    result = run_source(app.read_text(encoding="utf-8"), filename=str(app))
    assert result.ok
    assert result.stdout == "9\n5\n"


def test_all_current_stdlib_modules_compile_as_kuro_source(tmp_path):
    from pathlib import Path
    import shutil

    root = Path(__file__).resolve().parents[2]
    shutil.copytree(root / "stdlib", tmp_path / "stdlib")
    imports = "\n".join(f'Import "stdlib/{name}";' for name in (
        "core.kuro", "text.kuro", "collections.kuro", "math.kuro", "io.kuro"
    ))
    result = run_source(imports + '\nPrint "stdlib".', filename=str(tmp_path / "main.kuro"))
    assert result.ok
    assert result.stdout == "stdlib\n"


def test_kuro_standard_library_algorithms_run_in_kuro(tmp_path):
    import shutil
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    shutil.copytree(root / "stdlib", tmp_path / "stdlib")
    source = (
        'Import "stdlib/math.kuro";\n'
        'Import "stdlib/collections.kuro";\n'
        'Import "stdlib/text.kuro";\n'
        'Values = "a", "b", "c";\n'
        'Call KuroCollectionContains Values, "b";\nPrint @_.\n'
        'Call KuroCollectionIndexOf Values, "c";\nPrint @_.\n'
        'Call KuroPower 2, 5;\nPrint @_.\n'
        'Call KuroFactorial 5;\nPrint @_.\n'
        'Call KuroTextStartsWith "kuro", "ku";\nPrint @_.\n'
        'Call KuroTextEndsWith "kuro", "ro";\nPrint @_.\n'
    )
    result = run_source(source, filename=str(tmp_path / "main.kuro"))
    assert result.ok
    assert result.stdout == "1\n2\n32\n120\n1\n1\n"


def test_kuro_io_standard_library_uses_explicit_runtime_capabilities(tmp_path):
    import shutil
    from pathlib import Path

    root = Path(__file__).resolve().parents[2]
    shutil.copytree(root / "stdlib", tmp_path / "stdlib")
    target = str(tmp_path / "note.txt").replace("\\", "\\\\").replace('"', '\\"')
    directory = str(tmp_path).replace("\\", "\\\\").replace('"', '\\"')
    source = (
        'Import "stdlib/io.kuro";\n'
        f'Call KuroWriteFile "{target}", "hello";\nPrint @_.\n'
        f'Call KuroFileExists "{target}";\nPrint @_.\n'
        f'Call KuroReadFile "{target}";\nPrint @_.\n'
        f'Call KuroListDirectory "{directory}";\nPrint @_.\n'
    )
    result = run_source(source, filename=str(tmp_path / "main.kuro"))
    assert result.ok
    assert result.stdout.startswith("5\nTrue\nhello\n")
    assert "note.txt" in result.stdout
