from compiler.formatter import format_source
from cli.kuro import cmd_fmt


def test_formatter_indents_and_normalizes_blocks():
    source = 'N=0;\nIf N is less than 2;\nPrint "x".\nElse;\nPrint "y".\nDone.'
    assert format_source(source) == (
        'N=0;\nIf N is less than 2;\n    Print "x".\nElse;\n'
        '    Print "y".\nDone.\n'
    )


def test_formatter_write_mode_updates_file(tmp_path):
    path = tmp_path / "main.kuro"
    path.write_text("If 1 is equal to 1;\nPrint 1.\nDone.", encoding="utf-8")
    assert cmd_fmt(str(path), write=True) == 0
    assert path.read_text(encoding="utf-8") == "If 1 is equal to 1;\n    Print 1.\nDone.\n"
