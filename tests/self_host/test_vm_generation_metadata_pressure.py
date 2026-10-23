"""A per-generation table cannot inherit the eager row buffer's capacity.

The native witness calls unchanged production helpers with more fresh empty
IDs than the real native row limit. It does not prove unbounded IDs, metadata
reclamation, authored-codegen parity, or an asynchronous reader protocol.
"""
from pathlib import Path
import platform
import subprocess

import pytest

from compiler.native import NATIVE_COLLECTION_CAPACITY, build_native
from compiler.pipeline import compile_source, run_source


ROOT = Path(__file__).resolve().parents[2]
LINUX_X86 = platform.system() == "Linux" and platform.machine().lower() in {"x86_64", "amd64"}


def _source(resets):
    return (ROOT / "self_host/vm.kuro").read_text(encoding="utf-8") + f'''
GenerationChurnIndex = 0;
While GenerationChurnIndex is less than {resets};
    Call VMResetCollection "Churn";
    Add 1 to GenerationChurnIndex;
Done.
Print VMNextCollectionId.
Print VMCollectionEntryCount.
Call VMCopyCollection "Churn", "EmptyCopy";
Print VMNextCollectionId.
Print VMCollectionEntryCount.
VMAppendCollectionDisplay = "0007";
Call VMAppendCollectionItem "Churn", "raw-seven";
Call VMCopyCollection "Churn", "Published";
Print VMNextCollectionId.
Print VMCollectionEntryCount.
Print VMFailed.
Call VMGetCollectionItem "Published", 0;
Print @_.
Print VMGetCollectionDisplay.
Call VMLengthCollection "Churn";
Print @_.
'''


def _expected(resets):
    return f"{resets}\n0\n{resets + 1}\n0\n{resets + 2}\n2\n0\nraw-seven\n0007\n1\n"


def test_hosted_empty_generation_churn_and_later_publication():
    result = run_source(_source(7))
    assert result.compile.ok, result.compile.diags.render_all()
    assert result.runtime_error is None, result.runtime_error
    assert result.stdout == _expected(7)
    env = result.interpreter.env
    assert env["VMCollectionCount"] == 3
    assert env["VMCollectionIds"][:3] == [6, 7, 8]
    assert env["VMCollectionOwners"][:2] == [6, 8]


@pytest.mark.skipif(not LINUX_X86, reason="native helper witness requires Linux x86-64")
def test_native_empty_generation_churn_exceeds_real_row_capacity(tmp_path):
    assert NATIVE_COLLECTION_CAPACITY == 65_536
    resets = NATIVE_COLLECTION_CAPACITY + 1
    compiled = compile_source(_source(resets))
    assert compiled.ok, compiled.diags.render_all()
    image = tmp_path / "empty-generation-churn"
    build_native(compiled.ir, image, target="x86_64-linux")
    result = subprocess.run([str(image)], capture_output=True, text=True,
                            check=False, timeout=60, cwd=tmp_path)
    assert (result.returncode, result.stdout, result.stderr) == (0, _expected(resets), "")
