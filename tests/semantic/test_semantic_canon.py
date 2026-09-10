"""Unit tests for the canonical semantic representation (compiler/
semantic_canon.py) that Stage 7's differential test relies on.
"""
from compiler.pipeline import compile_source
from compiler.semantic_canon import canon_semantic


def canon(src: str) -> dict:
    r = compile_source(src)
    return canon_semantic(r.symbols, r.diags)


def test_valid_program_has_no_diagnostics():
    c = canon('Name = "Kuro";\nPrint Name.')
    assert c["diagnostics"] == []
    assert ("Name", "Text") in c["symbols"]


def test_action_recorded_with_arity():
    c = canon("Action Add A, B;\nReturn A + B;\nDone.")
    assert ("Add", 2) in c["actions"]


def test_diagnostics_are_code_and_location_only():
    c = canon("Print Missing.")
    assert c["diagnostics"] == [("E4001", 1, 7)]


def test_result_is_deterministic():
    src = 'Name = "Kuro";\nAge is Integers;\nAge = 5;\nPrint Name.'
    assert canon(src) == canon(src)
