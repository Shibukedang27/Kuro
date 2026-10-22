"""Frozen bootstrap observations, not a request to change the oracle.

Use its own parenthesized syntax; strip only its known IR debug trailer.
The modern frontend's closure/runtime policies cannot be inferred from it.
"""

from pathlib import Path
import subprocess
import sys

import pytest


ROOT = Path(__file__).resolve().parents[2]
BOOTSTRAP = ROOT / "bootstrap" / "python" / "kuro.py"


@pytest.mark.parametrize("source, status, output, error", [
    pytest.param("Print @_.", 1, "", "undefined value '_'", id="absent-result-errors"),
    pytest.param(
        "Action Seed(); Return 17; Done. Action Read(); Return @_; Done. "
        "Call Seed(); Call Read(); Print @_.",
        0, "17\n", "", id="direct-entry-live-global",
    ),
    pytest.param(
        "Action Answer(); Return 42; Done. "
        "Action Outer(_); Call Answer(); Print @_. Return @_; Done. "
        "Call Outer(17); Print @_.",
        0, "17\n17\n", "", id="parameter-overlay-hides-producer",
    ),
    pytest.param(
        "Action Answer(); Return 42; Done. "
        "Action Outer(); Call Answer(); Done. Call Outer(); Print @_.",
        0, "None\n", "", id="implicit-return-none",
    ),
])
def test_frozen_bootstrap_result_boundary(tmp_path, source, status, output, error):
    path = tmp_path / "result.kuro"
    path.write_text(source, encoding="utf-8")
    completed = subprocess.run(
        [sys.executable, str(BOOTSTRAP), str(path)],
        capture_output=True, text=True, timeout=5,
    )
    assert completed.returncode == status, completed.stderr
    if status == 0:
        before, marker, _ir = completed.stdout.partition("\nKURO IR v0.4\n")
        assert marker, "bootstrap debug trailer missing"
        assert before == output
        assert completed.stderr == ""
    else:
        assert completed.stdout == output
        assert error in completed.stderr
        assert "Traceback" not in completed.stderr
