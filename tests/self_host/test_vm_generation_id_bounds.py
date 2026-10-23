"""Seeded boundary probes, not claims of naturally reaching 2**63 resets.

Complete production helpers remain unchanged. The driver deliberately assigns
VMNextCollectionId near the signed boundary using small runtime literals.
These tests document today's backend difference, not an approved wrap policy.
"""
from pathlib import Path
import platform
import subprocess

import pytest

from compiler.native import build_native
from compiler.pipeline import compile_source, run_source

ROOT = Path(__file__).resolve().parents[2]
LINUX_X86 = platform.system() == "Linux" and platform.machine().lower() in {"x86_64", "amd64"}


def _source():
    return (ROOT / "self_host/vm.kuro").read_text(encoding="utf-8") + '''
# Test-only boundary injection; no production helper is edited.
GenerationBoundary = 1;
GenerationBit = 0;
While GenerationBit is less than 62;
    GenerationBoundary = GenerationBoundary * 2;
    Add 1 to GenerationBit;
Done.
VMNextCollectionId = GenerationBoundary - 1;
VMNextCollectionId = VMNextCollectionId + GenerationBoundary;
Call VMResetCollection "LastPositive";
Call VMFindCollection "LastPositive", 0;
Print @_.
Call VMResetCollection "AfterBoundary";
Call VMFindCollection "AfterBoundary", 0;
Print @_.
VMAppendCollectionDisplay = "0007";
Call VMAppendCollectionItem "LastPositive", "raw-seven";
Call VMGetCollectionItem "LastPositive", 0;
Print @_.
Print VMGetCollectionDisplay.
Call VMAppendCollectionItem "AfterBoundary", "other";
Print VMCollectionEntryCount.
Print VMFailed.
'''


def test_hosted_generation_ids_continue_past_signed_native_boundary():
    result = run_source(_source())
    assert result.compile.ok, result.compile.diags.render_all()
    assert result.runtime_error is None, result.runtime_error
    assert result.stdout == "0\n1\nraw-seven\n0007\n2\n0\n"
    env = result.interpreter.env
    assert env["VMCollectionIds"][:2] == [2**63 - 1, 2**63]
    assert env["VMNextCollectionId"] == 2**63 + 1


@pytest.mark.skipif(not LINUX_X86, reason="native helper witness requires Linux x86-64")
def test_native_signed_wrap_makes_new_generation_inactive(tmp_path):
    compiled = compile_source(_source())
    assert compiled.ok, compiled.diags.render_all()
    image = tmp_path / "generation-id-boundary"
    build_native(compiled.ir, image, target="x86_64-linux")
    result = subprocess.run([str(image)], capture_output=True, text=True,
                            check=False, timeout=60, cwd=tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (
        0, "0\n-1\nraw-seven\n0007\n1\n1\n", "")
