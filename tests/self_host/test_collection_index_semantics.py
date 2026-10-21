"""Collection index behavior against the frozen oracle and execution paths.

README identifies ``bootstrap/python/kuro.py`` as the frozen compatibility
oracle, and ADR-0012's Golden Rule requires self-hosted implementations to
reproduce its semantics. The oracle unambiguously allows negative GET indices
in ``-len(collection) <= i < len(collection)`` and restricts SET to
``0 <= i < len(collection)``. Native fixed-capacity storage is a separate,
storage-aware concern, not an alternative logical collection contract.
"""
from __future__ import annotations

from contextlib import redirect_stdout
import io
import json
import platform
import runpy
import subprocess
from pathlib import Path

import pytest

from compiler.bytecode import BytecodeProgram, BytecodeVM, encode_ir
from compiler.native import NATIVE_COLLECTION_CAPACITY, build_native
from compiler.pipeline import compile_source, run_source
from compiler.interpreter import KuroRuntimeException
from test_vm_cross import run_kuro_vm_environment

LINUX_X86 = platform.system() == "Linux" and platform.machine().lower() in {"x86_64", "amd64"}
FROZEN_ORACLE = Path(__file__).resolve().parents[2] / "bootstrap" / "python" / "kuro.py"


def _source(operation: str, index: int, *, append: bool = False) -> str:
    prefix = 'Items = 11, 22;\n'
    if append:
        prefix += 'Append 33 to Items;\n'
    prefix += f"Index = {index};\n"
    if operation == "get":
        return prefix + 'Get Items Index;\nPrint @_.\nPrint "continued".'
    return (
        prefix
        + 'Set Items Index to 99;\n'
        + 'Get Items 0;\nPrint @_.\nGet Items 1;\nPrint @_.\n'
        + ('Get Items 2;\nPrint @_.\n' if append else '')
        + 'Print "continued".'
    )


def _hosted(source: str) -> dict:
    result = run_source(source)
    assert result.compile.ok, result.compile.diags.render_all()
    error = result.runtime_error
    return {
        "stdout": result.stdout or "",
        "error": None if error is None else (error.code, error.message),
        "env": result.interpreter.env.copy(),
        "returncode": None,
    }


def _python_bytecode(source: str) -> dict:
    compiled = compile_source(source)
    assert compiled.ok, compiled.diags.render_all()
    serialized = json.dumps(encode_ir(compiled.ir).to_data())
    program = BytecodeProgram.from_data(json.loads(serialized))
    output = io.StringIO()
    vm = BytecodeVM(program, output=output)
    error = None
    try:
        vm.run()
    except KuroRuntimeException as exc:
        error = (exc.code, exc.message)
    return {"stdout": output.getvalue(), "error": error, "returncode": None}


def _kuro_vm(source: str) -> dict:
    env = run_kuro_vm_environment(source)
    values = env.get("VMOutput", [])
    displays = env.get("VMOutputDisplay", [])
    # The authored VM exposes a value/display log rather than a subprocess
    # stream. Preserve exact printed values and display strings separately.
    return {
        "stdout": "".join(
            (display if display else str(value)) + "\n"
            for value, display in zip(values, displays)
        ),
        "values": values,
        "displays": displays,
        "failed": env.get("VMFailed", 0),
        "returncode": None,
    }


def _native(source: str, tmp_path) -> dict:
    compiled = compile_source(source)
    assert compiled.ok, compiled.diags.render_all()
    executable = tmp_path / "collection-index"
    build_native(compiled.ir, executable, target="x86_64-linux")
    completed = subprocess.run(
        [str(executable)], text=True, capture_output=True, check=False, timeout=15
    )
    return {
        "stdout": completed.stdout,
        "stderr": completed.stderr,
        "returncode": completed.returncode,
    }


def _frozen_oracle(source: str, indices: tuple[int, ...] = ()) -> dict:
    """Run the frozen Engine AST directly, ignoring its bootstrap print/IR output."""
    oracle = runpy.run_path(str(FROZEN_ORACLE), run_name="frozen_collection_oracle")
    ast = oracle["Parser"](oracle["lex"](source)).parse()
    # The frozen lexer predates unary-minus syntax, but its Engine accepts
    # negative integer index values. Inject these directly into its parsed AST.
    access_nodes = [node for node in ast if type(node).__name__ in {"Get", "Set"}]
    assert len(access_nodes) == len(indices)
    for node, index in zip(access_nodes, indices):
        node.index = ("lit", index)
    engine = oracle["Engine"](ast)
    exception = None
    # Engine.run() prints both language output and bootstrap IR. Those effects
    # are deliberately excluded; compare resulting environment/exception only.
    with redirect_stdout(io.StringIO()):
        try:
            engine.run()
        except oracle["KuroRuntimeError"] as exc:
            exception = exc
    return {"env": engine.env.copy(), "exception": exception}


def _expected(operation: str, index: int, path: str, *, append: bool = False) -> tuple[str, bool]:
    """Return expected visible stdout and failure state for one observed path."""
    logical_length = 3 if append else 2
    valid_get = -logical_length <= index < logical_length
    valid_set = 0 <= index < logical_length

    valid = valid_get if operation == "get" else valid_set
    if not valid:
        # Native bounds checks terminate with an OS status, not a Kuro
        # RuntimeException object.
        return "", True

    if operation == "get":
        value = [11, 22, 33][:logical_length][index]
        return f"{value}\ncontinued\n", False

    items = [11, 22, 33][:logical_length]
    if 0 <= index < logical_length:
        items[index] = 99
    return "".join(f"{item}\n" for item in items) + "continued\n", False


def _assert_negative_get_parity(observations: dict) -> None:
    """The three logical runtimes must agree on negative GET output and failure."""
    host = observations["host"]
    bytecode = observations["bytecode"]
    kuro_vm = observations["kuro_vm"]
    assert host["stdout"] == bytecode["stdout"] == kuro_vm["stdout"]
    assert (host["error"] is not None) == (bytecode["error"] is not None) == bool(
        kuro_vm["failed"]
    )


@pytest.mark.parametrize("operation", ["get", "set"])
@pytest.mark.parametrize("index", [-3, -2, -1, 0, 1, 2, 3, NATIVE_COLLECTION_CAPACITY - 1, NATIVE_COLLECTION_CAPACITY])
def test_two_item_collection_index_observations(operation, index, tmp_path):
    source = _source(operation, index)
    observations = {
        "host": _hosted(source),
        "bytecode": _python_bytecode(source),
        "kuro_vm": _kuro_vm(source),
    }
    if LINUX_X86:
        observations["native"] = _native(source, tmp_path)

    if operation == "get" and index < 0:
        _assert_negative_get_parity(observations)

    for path, observation in observations.items():
        expected_stdout, failed = _expected(operation, index, path)
        assert observation["stdout"] == expected_stdout, (path, operation, index, observation)
        if path == "native":
            assert observation["returncode"] == (1 if failed else 0), (path, operation, index, observation)
            assert observation["stderr"] == ""
            if failed:
                assert "continued\n" not in observation["stdout"]
            continue
        if path == "kuro_vm":
            assert observation["failed"] == int(failed), (path, operation, index, observation)
            if failed:
                assert "continued\n" not in observation["stdout"]
            continue
        if failed:
            assert observation["error"] is not None, (path, operation, index, observation)
            assert observation["error"][0] == "E6001"
            assert "continued\n" not in observation["stdout"]
        else:
            assert observation["error"] is None


@pytest.mark.parametrize("operation,index", [("get", 2), ("get", 3), ("set", 2), ("set", 3)])
def test_append_changes_logical_index_boundary(operation, index, tmp_path):
    source = _source(operation, index, append=True)
    observations = {
        "host": _hosted(source),
        "bytecode": _python_bytecode(source),
        "kuro_vm": _kuro_vm(source),
    }
    if LINUX_X86:
        observations["native"] = _native(source, tmp_path)

    for path, observation in observations.items():
        expected_stdout, failed = _expected(operation, index, path, append=True)
        assert observation["stdout"] == expected_stdout, (path, operation, index, observation)
        if path == "kuro_vm":
            assert observation["failed"] == int(failed), (path, operation, index, observation)
        elif path == "native":
            assert observation["returncode"] == (1 if failed else 0), (path, operation, index, observation)
            assert observation["stderr"] == ""
        elif failed:
            assert observation["error"] is not None
            assert observation["error"][0] == "E6001"
        else:
            assert observation["error"] is None
        if failed:
            assert "continued\n" not in observation["stdout"]


@pytest.mark.parametrize("index,expected_stdout,failed", [(-3, "11\ncontinued\n", False), (-4, "", True)])
def test_appended_collection_negative_get_boundary(index, expected_stdout, failed):
    source = _source("get", index, append=True)
    observations = {
        "host": _hosted(source),
        "bytecode": _python_bytecode(source),
        "kuro_vm": _kuro_vm(source),
    }
    _assert_negative_get_parity(observations)
    for path, observation in observations.items():
        assert observation["stdout"] == expected_stdout, (path, observation)
        if path == "kuro_vm":
            assert observation["failed"] == int(failed)
        elif failed:
            assert observation["error"] is not None
            assert observation["error"][0] == "E6001"
        else:
            assert observation["error"] is None


@pytest.mark.parametrize(
    "source,oracle_source,indices,expected_stdout,failed",
    [
        (
            'Items = 11, 22, 33;\nGet Items -2;\nPrint @_.',
            'Items = 11, 22, 33;\nGet Items 2;\nPrint @_.',
            (-2,),
            "22\n",
            False,
        ),
        (
            'Items = 11, 22, 33;\nGet Items -4;\nPrint @_.',
            'Items = 11, 22, 33;\nGet Items 1;\nPrint @_.',
            (-4,),
            "",
            True,
        ),
        (
            'Items = 11, 22, 33;\nSet Items -1 to 99;',
            'Items = 11, 22, 33;\nSet Items 1 to 99;',
            (-1,),
            "",
            True,
        ),
        (
            'Items = 11, 22, 33;\nItems = 44, 55;\n'
            'Get Items -2;\nPrint @_.\nGet Items -1;\nPrint @_.',
            'Items = 11, 22, 33;\nItems = 44, 55;\n'
            'Get Items 2;\nPrint @_.\nGet Items 1;\nPrint @_.',
            (-2, -1),
            "44\n55\n",
            False,
        ),
        (
            'Items = 11, 22, 33;\nOthers = 7, 8;\n'
            'Get Items -3;\nPrint @_.\nGet Others -2;\nPrint @_.\n'
            'Get Items -1;\nPrint @_.',
            'Items = 11, 22, 33;\nOthers = 7, 8;\n'
            'Get Items 1;\nPrint @_.\nGet Others 1;\nPrint @_.\n'
            'Get Items 1;\nPrint @_.',
            (-3, -2, -1),
            "11\n7\n33\n",
            False,
        ),
    ],
)
def test_frozen_oracle_environment_and_exception(
    source, oracle_source, indices, expected_stdout, failed
):
    """Validate direct frozen Engine AST behavior without its CLI auto-print path."""
    oracle = _frozen_oracle(oracle_source, indices)
    hosted = _hosted(source)
    assert hosted["stdout"] == expected_stdout
    assert oracle["env"] == hosted["env"]
    assert (oracle["exception"] is not None) == failed
    assert (hosted["error"] is not None) == failed
    observations = {"host": hosted, "bytecode": _python_bytecode(source),
                    "kuro_vm": _kuro_vm(source)}
    _assert_negative_get_parity(observations)
    if failed:
        assert type(oracle["exception"]).__name__ == "KuroRuntimeError"
        assert hosted["error"][0] == "E6001"


@pytest.mark.parametrize("index,expected,failed", [(-2, "44\n", False), (-3, "", True)])
def test_reassigned_collection_ignores_historical_entries(index, expected, failed):
    source = f'Items = 11, 22, 33;\nItems = 44, 55;\nGet Items {index};\nPrint @_.\n'
    observations = {"host": _hosted(source), "bytecode": _python_bytecode(source),
                    "kuro_vm": _kuro_vm(source)}
    _assert_negative_get_parity(observations)
    assert observations["host"]["stdout"] == expected
    assert observations["kuro_vm"]["failed"] == int(failed)


def test_negative_get_counts_only_current_owner_with_interleaved_appends():
    source = ('Items = 11, 22;\nOthers = 7, 8;\nAppend 33 to Items;\n'
              'Get Items -3;\nPrint @_.\nGet Others -2;\nPrint @_.\n'
              'Get Items -1;\nPrint @_.\n')
    observations = {"host": _hosted(source), "bytecode": _python_bytecode(source),
                    "kuro_vm": _kuro_vm(source)}
    _assert_negative_get_parity(observations)
    assert observations["host"]["stdout"] == "11\n7\n33\n"
    assert observations["kuro_vm"]["failed"] == 0


@pytest.mark.skipif(not LINUX_X86, reason="native Kuro VM runtime regression targets Linux x86_64")
def test_native_runtime_vm_negative_get_and_owner_lengths(tmp_path):
    """Exercise build_native_runtime's native backend running Kuro VM source, not generator collection lowering."""
    from compiler.self_host import build_native_runtime

    source = (
        'Items = 11, 22, 33;\n'
        'Get Items -3;\nPrint @_.\nGet Items -1;\nPrint @_.\n'
        'Append 44 to Items;\nGet Items -4;\nPrint @_.\n'
        'Get Items -1;\nPrint @_.\n'
        'Others = 7, 8;\nGet Others -2;\nPrint @_.\n'
        'Get Items -4;\nPrint @_.\n'
    )
    executable = tmp_path / "native-kuro-vm-negative-get"
    build_native_runtime(source, executable, target="x86_64-linux")
    completed = subprocess.run(
        [str(executable)], text=True, capture_output=True, check=False, timeout=30
    )
    assert completed.returncode == 0, completed.stderr
    assert completed.stdout == "11\n33\n11\n44\n7\n11\n"
    assert completed.stderr == ""
