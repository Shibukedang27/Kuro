from pathlib import Path

from compiler.self_host import native_compiler_source


ROOT = Path(__file__).resolve().parents[2]


def test_checked_in_native_compiler_source_matches_current_composition():
    artifact = ROOT / "dist" / "kuro-compiler.source.kuro"

    assert artifact.read_text(encoding="utf-8") == native_compiler_source()
