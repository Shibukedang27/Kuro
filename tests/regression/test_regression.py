"""Regression suite: every `.kuro` fixture from the frozen bootstrap
implementation (bootstrap/python/tests/) still behaves the same way under
the new compiler/, with two documented, deliberate exceptions.

This is the "regression suite" milestone from spec section 61: it exists so
a future change to compiler/ that silently breaks a program the bootstrap
interpreter used to run correctly is caught immediately, not discovered
later.
"""
from pathlib import Path

import pytest

from compiler.pipeline import run_source

FIXTURES = sorted((Path(__file__).resolve().parent.parent.parent / "bootstrap" / "python" / "tests").glob("*.kuro"))

# name -> (bootstrap exit code, bootstrap stdout) captured in this session
# from `python3 bootstrap/python/kuro.py <file>` before any new code existed
# (see docs/architecture/current-state.md section 1). The bootstrap engine
# also always appended a "KURO IR v0.4" debug trailer to stdout on success;
# that trailer is bootstrap-only debug output; it is stripped here because
# the new pipeline's `run_source` does not print it (`kuro emit-ir` is the
# real equivalent — see cli/kuro.py).
BOOTSTRAP_STDOUT_ON_SUCCESS = {
    "actions": "Kuro\n",
    "comments": "Kuro\n",
    "compare": "True\n",
    "get": "K\n",         # bootstrap auto-printed via Get; see divergence below
    "legacy_if": "Old\n",
    "length": "4\n",      # bootstrap auto-printed via Length; see divergence below
    "nested": "zero\none\n",
    "repeat_index": "0\n1\n2\n",
    "set_list": "A\nX\nC\n",
    "set_text": "kuro\n",
    "typed": "21\n",
}

BOOTSTRAP_EXIT_1 = {
    "add_text", "bad_call", "bad_get", "error_add_text", "error_bad_call",
    "error_bad_get", "error_return_top", "error_unknown_type", "return_top",
    "unknown_type",
}

# ADR-0007: `Get`/`Length` no longer print as a side effect (spec has no
# statement that says "print"; it was a bootstrap debug convenience, not a
# designed feature — see docs/architecture/current-state.md section 7). The
# two fixtures that relied purely on that side effect now produce no
# output under the new pipeline; this is a deliberate, documented breaking
# change, not a regression.
KNOWN_DIVERGENCES = {"get", "length"}


@pytest.mark.parametrize("path", FIXTURES, ids=lambda p: p.stem)
def test_fixture_matches_bootstrap_behavior(path: Path):
    name = path.stem
    source = path.read_text(encoding="utf-8")
    result = run_source(source, filename=str(path))

    if name in BOOTSTRAP_EXIT_1:
        assert not result.ok, f"{name}: expected a compile/runtime error, new pipeline accepted it"
        return

    assert result.ok, (
        f"{name}: expected success, got "
        + (result.compile.diags.render_all() if not result.compile.ok else str(result.runtime_error))
    )
    if name in KNOWN_DIVERGENCES:
        assert result.stdout == "", f"{name}: expected no output post-ADR-0007, got {result.stdout!r}"
        return
    expected = BOOTSTRAP_STDOUT_ON_SUCCESS.get(name)
    if expected is not None:
        assert result.stdout == expected, f"{name}: stdout diverged from bootstrap golden output"


def test_every_fixture_is_accounted_for():
    known = set(BOOTSTRAP_STDOUT_ON_SUCCESS) | BOOTSTRAP_EXIT_1
    names = {p.stem for p in FIXTURES}
    missing = names - known
    assert not missing, f"fixtures with no golden expectation recorded: {missing}"
