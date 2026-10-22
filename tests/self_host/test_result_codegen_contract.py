"""Exercise the Kuro-authored compiler-to-native-codegen result boundary."""

import json
import platform
from pathlib import Path
import subprocess

import pytest

from compiler import self_host
from compiler.pipeline import run_source


ROOT = Path(__file__).resolve().parents[2]
INSTRUCTION_LIMIT = 2_000_000
WHILE_LIMIT = 10_000
PROCESS_TIMEOUT = 30


class _InstructionBudgetExceeded(RuntimeError):
    pass


class _SharedInstructionBudget:
    """Share one trace allowance across the hosted compiler and codegen runs."""

    def __init__(self):
        self.count = 0

    def trace(self, *_):
        self.count += 1
        if self.count > INSTRUCTION_LIMIT:
            raise _InstructionBudgetExceeded(
                f"hosted compiler plus generator exceeded {INSTRUCTION_LIMIT} instructions"
            )

    def run_source(self, source):
        result = run_source(
            source,
            max_while_iterations=WHILE_LIMIT,
            trace=self.trace,
        )
        assert result.ok, result.compile.diags.render_all() if not result.compile.ok else result.runtime_error
        assert result.interpreter.frames == []
        return result


FIXTURES = [
    pytest.param(
        "Action Read _; Return @_; Done. Call Read 17; Print @_.",
        [
            "BC_FUNC_BEGIN", "Read", "BC_PARAM", "_", "NONE", "BC_LOADVAR", "_",
            "BC_RETURN", "BC_FUNC_END", "BC_CALL_BEGIN", "Read", "BC_CONST", "17",
            "BC_CALL_END", "BC_STORE_LIST", "_", "BC_LOADVAR", "_", "BC_PRINT",
        ],
        "17\n",
        id="direct-result",
    ),
    pytest.param(
        "Action Answer; Return 42; Done. Action Read _; Call Answer; Return @_; Done. Call Read 17; Print @_.",
        [
            "BC_FUNC_BEGIN", "Answer", "BC_CONST", "42", "BC_RETURN", "BC_FUNC_END",
            "BC_FUNC_BEGIN", "Read", "BC_PARAM", "_", "NONE", "BC_CALL_BEGIN", "Answer",
            "BC_CALL_END", "BC_STORE_LIST", "_", "BC_LOADVAR", "_", "BC_RETURN",
            "BC_FUNC_END", "BC_CALL_BEGIN", "Read", "BC_CONST", "17", "BC_CALL_END",
            "BC_STORE_LIST", "_", "BC_LOADVAR", "_", "BC_PRINT",
        ],
        "42\n",
        id="nested-result",
    ),
]


def _native_target_for_this_host():
    system = platform.system()
    machine = platform.machine().lower()
    if system == "Linux" and machine in {"x86_64", "amd64"}:
        return "x86_64-linux"
    if system == "Darwin" and machine in {"arm64", "aarch64"}:
        return "aarch64-macos"
    pytest.skip("native result execution is supported only on Linux x86-64 and Darwin arm64")


def _compile_and_run_native(assembly_text, target, tmp_path):
    assembly = tmp_path / "result-contract.s"
    executable = tmp_path / "result-contract"
    assembly.write_text(assembly_text, encoding="utf-8")
    if target == "x86_64-linux":
        command = [
            "clang", "-target", "x86_64-unknown-linux-gnu", "-nostdlib",
            "-Wl,-e,_start", "-x", "assembler", str(assembly), "-o", str(executable),
        ]
    else:
        command = ["clang", str(assembly), "-o", str(executable)]
    subprocess.run(
        command,
        check=True,
        capture_output=True,
        text=True,
        timeout=PROCESS_TIMEOUT,
    )
    return subprocess.run(
        [str(executable)],
        check=True,
        capture_output=True,
        text=True,
        timeout=PROCESS_TIMEOUT,
    )


@pytest.mark.parametrize("typed", [False, True], ids=["untyped-rejected", "typed-executed"])
@pytest.mark.parametrize(("source", "expected_bytecode", "native_output"), FIXTURES)
def test_kuro_result_codegen_contract(source, expected_bytecode, native_output, typed, tmp_path, monkeypatch):
    target = _native_target_for_this_host()
    budget = _SharedInstructionBudget()
    if typed:
        source = source.replace("Action Read _;", "Action Read _: Integers;", 1)
        expected_bytecode = ["Integers" if token == "NONE" else token for token in expected_bytecode]

    # This is the language-level reference result. Both fixtures currently
    # resolve the action's `_` read to its argument, yielding 17.
    reference = budget.run_source(source)
    assert reference.ok, reference.runtime_error
    assert reference.stdout == "17\n"

    # compile_with_kuro_driver calls this module-level run_source; patch it so
    # the hosted compiler and the generator share the same instruction budget.
    monkeypatch.setattr(self_host, "run_source", budget.run_source)
    compiled = self_host.compile_with_kuro_driver(source)
    tokens = [str(token) for token in compiled["CompilerOutput"]]
    assert compiled["CompilerFailed"] == 0
    assert tokens == expected_bytecode

    codegen = (ROOT / "self_host" / "native_codegen.kuro").read_text(encoding="utf-8")
    codegen = codegen.replace(
        'NativeTarget = "aarch64-macos";', f'NativeTarget = "{target}";', 1
    )
    generator_source = (
        "BytecodeOut = " + ", ".join(json.dumps(token) for token in tokens) + ";\n" + codegen
    )
    generated = budget.run_source(generator_source)
    assert generated.ok, generated.runtime_error
    env = generated.interpreter.env

    if not typed:
        # Current Kuro generator boundary: these fixtures encode `_` as a
        # parameter of type NONE, which native_codegen rejects before emitting
        # assembly. Do not execute empty/partial output or infer a value from it.
        assert env.get("NativeFailed") == 1
        assert env.get("NativePrepareParamType") == "NONE"
        assert env.get("NativeOut") == ""
        return

    assert env.get("NativeFailed") == 0
    assert env.get("NativeOut"), "successful native generation must publish assembly"
    native = _compile_and_run_native(env["NativeOut"], target, tmp_path)
    assert native.stdout == native_output
    assert native.stderr == ""
