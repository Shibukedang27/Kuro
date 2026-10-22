"""Owned fixed-integer collection length support in the Kuro native generator."""
from __future__ import annotations

import json

import pytest

from test_native_codegen import run_codegen, x86_linux_codegen
from test_native_integer_storage import execute, generate, requires_linux
from test_native_integer_storage_capacity import (
    _run_authored_vm,
    _values,
    native_compiler,
    native_compiler_image,
)


INITIAL_ITEMS = [
    "BC_MULTI_BEGIN", "BC_CONST", "11", "BC_CONST", "22",
    "BC_STORE_MULTI", "Items",
]


def _wire(tokens):
    return ", ".join(json.dumps(token) for token in tokens)


def _assert_authored_vm(tokens, expected, *, failed=False):
    # The reference frontend currently rejects integer Length with E3009.
    # Compare the existing Kuro-authored bytecode VM, not a bypassed typecheck.
    env = _run_authored_vm(tokens)
    stdout = "".join(
        (display if display else str(value)) + "\n"
        for value, display in zip(env.get("VMOutput", []), env.get("VMOutputDisplay", []))
    )
    assert stdout == expected
    assert bool(env["VMFailed"]) == failed


def _raw_length(tokens=INITIAL_ITEMS, owner="Items"):
    return [*tokens, "BC_LENGTH", owner, "BC_STORE_LIST", "_"]


@requires_linux
@pytest.mark.parametrize("count", [2, 272], ids=["minimum", "maximum"])
def test_fresh_native_compiler_generator_and_linked_image_report_owner_length(
    count, tmp_path, x86_linux_codegen, native_compiler
):
    source = f"Items = {_values(count)};\nLength Items;\nPrint @_.\n"
    expected = f"{count}\n"
    tokens = native_compiler(source, tmp_path)
    _assert_authored_vm(tokens, expected)
    assert "BC_LENGTH" in tokens
    length_at = tokens.index("BC_LENGTH")
    assert tokens[length_at + 1:length_at + 4] == ["Items", "BC_STORE_LIST", "_"]
    result = execute(x86_linux_codegen, source, tmp_path, tokens=tokens)
    assert (result.returncode, result.stdout, result.stderr) == (0, expected, "")


@requires_linux
def test_length_is_owner_local_not_total_cell_budget(
    tmp_path, x86_linux_codegen, native_compiler
):
    source = (
        f"Left = {_values(200)};\nRight = {_values(72, 1000)};\n"
        "Length Left; Print @_.\nLength Right; Print @_.\n"
    )
    expected = "200\n72\n"
    tokens = native_compiler(source, tmp_path)
    _assert_authored_vm(tokens, expected)
    assert tokens.count("BC_LENGTH") == 2
    result = execute(x86_linux_codegen, source, tmp_path, tokens=tokens)
    assert (result.returncode, result.stdout, result.stderr) == (0, expected, "")


@requires_linux
def test_sixteen_owners_at_aggregate_cell_budget_have_distinct_lengths(
    tmp_path, x86_linux_codegen, native_compiler
):
    source = "".join(
        f"Owner{owner} = {_values(2 if owner == 0 else 32 if owner == 15 else 17, owner * 100)};\n"
        for owner in range(16)
    )
    source += "Length Owner0; Print @_.\nLength Owner15; Print @_.\n"
    expected = "2\n32\n"
    tokens = native_compiler(source, tmp_path)
    _assert_authored_vm(tokens, expected)
    assert tokens.count("BC_LENGTH") == 2
    result = execute(x86_linux_codegen, source, tmp_path, tokens=tokens)
    assert (result.returncode, result.stdout, result.stderr) == (0, expected, "")


@requires_linux
def test_mutating_collection_cells_does_not_change_logical_length(
    tmp_path, x86_linux_codegen, native_compiler
):
    source = (
        "Items = 11, 22;\nSet Items 0 to 777;\nSet Items 1 to 888;\n"
        "Length Items; Print @_.\nGet Items 0; Print @_.\nGet Items 1; Print @_.\n"
    )
    expected = "2\n777\n888\n"
    tokens = native_compiler(source, tmp_path)
    _assert_authored_vm(tokens, expected)
    result = execute(x86_linux_codegen, source, tmp_path, tokens=tokens)
    assert (result.returncode, result.stdout, result.stderr) == (0, expected, "")


@requires_linux
def test_length_result_computes_valid_last_index(
    tmp_path, x86_linux_codegen, native_compiler
):
    source = "Items = 11, 22, 33;\nLength Items;\nIndex = @_ - 1;\nGet Items Index;\nPrint @_.\n"
    tokens = native_compiler(source, tmp_path)
    _assert_authored_vm(tokens, "33\n")
    result = execute(x86_linux_codegen, source, tmp_path, tokens=tokens)
    assert (result.returncode, result.stdout, result.stderr) == (0, "33\n", "")


@requires_linux
def test_length_result_as_out_of_bounds_index_preserves_failstop_prefix(
    tmp_path, x86_linux_codegen, native_compiler
):
    source = (
        "Items = 11, 22, 33;\nLength Items;\nIndex = @_;\nPrint 777.\n"
        "Get Items Index;\nPrint @_.\nPrint 888.\n"
    )
    tokens = native_compiler(source, tmp_path)
    _assert_authored_vm(tokens, "777\n", failed=True)
    result = execute(x86_linux_codegen, source, tmp_path, tokens=tokens)
    assert (result.returncode, result.stdout, result.stderr) == (1, "777\n", "")


@requires_linux
def test_repeated_lengths_replace_the_published_result(
    tmp_path, x86_linux_codegen, native_compiler
):
    source = (
        "Short = 11, 22;\nLong = 1, 2, 3, 4;\n"
        "Length Long; Length Short; Print @_.\n"
        "Length Long; Print @_.\nLength Short; Print @_.\n"
    )
    expected = "2\n4\n2\n"
    tokens = native_compiler(source, tmp_path)
    _assert_authored_vm(tokens, expected)
    assert tokens.count("BC_LENGTH") == 4
    result = execute(x86_linux_codegen, source, tmp_path, tokens=tokens)
    assert (result.returncode, result.stdout, result.stderr) == (0, expected, "")


def test_raw_length_preserves_lower_operand_stack_items_portably():
    tokens = [
        *INITIAL_ITEMS, "BC_CONST", "40", "BC_LENGTH", "Items",
        "BC_BINOP", "+", "BC_PRINT",
    ]
    env = run_codegen(_wire(tokens), target="x86_64-linux", execution_target="x86_64-linux")
    assert env["NativeFailed"] == 0
    assert env["NativeOut"]


@requires_linux
def test_raw_length_stack_effect_preserves_lower_values_in_linked_execution(
    tmp_path, x86_linux_codegen
):
    tokens = [
        *INITIAL_ITEMS, "BC_CONST", "40", "BC_LENGTH", "Items",
        "BC_BINOP", "+", "BC_PRINT",
    ]
    result = execute(x86_linux_codegen, "raw bytecode operand-stack witness", tmp_path, tokens=tokens)
    assert (result.returncode, result.stdout, result.stderr) == (0, "42\n", "")


@pytest.mark.parametrize(
    "tokens",
    [
        [*INITIAL_ITEMS, "BC_LENGTH"],
        [*INITIAL_ITEMS, "BC_LENGTH", "BC_STORE_LIST", "_"],
        [*INITIAL_ITEMS, "BC_LENGTH", "Unknown", "BC_STORE_LIST", "_"],
        [*INITIAL_ITEMS, "BC_CONST", "2", "BC_STORE_LIST", "Scalar", "BC_LENGTH", "Scalar", "BC_STORE_LIST", "_"],
        [*INITIAL_ITEMS, "BC_LOADVAR", "Items", "BC_STORE_LIST", "Alias", "BC_LENGTH", "Alias", "BC_STORE_LIST", "_"],
        [*INITIAL_ITEMS, "BC_CONST_TEXT", "abc", "BC_STORE_LIST", "TextValue", "BC_LENGTH", "TextValue", "BC_STORE_LIST", "_"],
        ["BC_MULTI_BEGIN", "BC_CONST", "1.5", "BC_CONST", "2.5", "BC_STORE_MULTI", "Decimals", "BC_LENGTH", "Decimals", "BC_STORE_LIST", "_"],
        [*INITIAL_ITEMS, "BC_CONST", "33", "BC_APPEND", "Items", "BC_LENGTH", "Items", "BC_STORE_LIST", "_"],
        [*INITIAL_ITEMS, "BC_FUNC_BEGIN", "Read", "BC_LENGTH", "Items", "BC_STORE_LIST", "_", "BC_FUNC_END"],
        [*INITIAL_ITEMS, "BC_CONST", "1", "BC_CONST", "1", "BC_CMP", "eq", "BC_IF_BEGIN", "BC_LENGTH", "Items", "BC_STORE_LIST", "_", "BC_ELSE_BEGIN", "BC_IF_END"],
    ],
    ids=["truncated", "missing-owner", "unknown-owner", "scalar-owner", "alias-owner", "text-owner", "decimal-owner", "growth", "action", "control-flow"],
)
def test_portable_raw_codegen_rejects_out_of_scope_length_owners_and_contexts(tokens):
    # A completed print prevents the separate mandatory-print rule masking the
    # invalid operand/opcode. It does not initialize any scalar or owner.
    if tokens[:len(INITIAL_ITEMS)] == INITIAL_ITEMS:
        tokens = [*INITIAL_ITEMS, "BC_CONST", "777", "BC_PRINT", *tokens[len(INITIAL_ITEMS):]]
    env = run_codegen(_wire(tokens), target="x86_64-linux", execution_target="x86_64-linux")
    assert (env["NativeFailed"], env["NativeOut"]) == (1, "")


@pytest.mark.parametrize("tokens", [
    [*INITIAL_ITEMS, "BC_LENGTH", "Items", "BC_BINOP", "+", "BC_PRINT"],
    [*INITIAL_ITEMS, "BC_LENGTH", "Items"],
], ids=["underflow", "unconsumed-length"])
def test_portable_raw_codegen_rejects_length_stack_underflow_or_residue(tokens):
    tokens = [*INITIAL_ITEMS, "BC_CONST", "777", "BC_PRINT", *tokens[len(INITIAL_ITEMS):]]
    env = run_codegen(_wire(tokens), target="x86_64-linux", execution_target="x86_64-linux")
    assert (env["NativeFailed"], env["NativeOut"]) == (1, "")


@pytest.mark.parametrize("output_target", ["aarch64-macos", "x86_64-macos", "x86_64-linux"])
@pytest.mark.parametrize("execution_target", ["unverified", "aarch64-macos", "x86_64-macos", "x86_64-linux"])
def test_raw_length_requires_both_linux_execution_and_output_qualification(
    output_target, execution_target
):
    env = run_codegen(
        _wire([*_raw_length(), "BC_LOADVAR", "_", "BC_PRINT"]),
        target=output_target, execution_target=execution_target
    )
    if output_target == execution_target == "x86_64-linux":
        assert env["NativeFailed"] == 0 and env["NativeOut"]
    else:
        assert (env["NativeFailed"], env["NativeOut"]) == (1, "")


def test_reference_frontend_integer_length_boundary_is_not_silently_bypassed():
    from compiler.pipeline import compile_source

    compiled = compile_source("Items = 11, 22; Length Items; Print @_.")
    assert not compiled.ok
    assert "error[E3009]: Length target must be Text, found Integers" in compiled.diags.render_all()


@requires_linux
@pytest.mark.parametrize("expression,expected", [("0 - 1", "33\n"), ("0 - @_", "11\n")])
def test_length_derived_negative_indices_keep_logical_end_semantics(
    expression, expected, tmp_path, x86_linux_codegen, native_compiler
):
    source = (
        "Items = 11, 22, 33;\nLength Items;\n"
        f"Index = {expression};\nGet Items Index;\nPrint @_.\n"
    )
    tokens = native_compiler(source, tmp_path)
    _assert_authored_vm(tokens, expected)
    result = execute(x86_linux_codegen, source, tmp_path, tokens=tokens)
    assert (result.returncode, result.stdout, result.stderr) == (0, expected, "")


@requires_linux
def test_raw_length_does_not_publish_without_the_lowered_store(tmp_path, x86_linux_codegen):
    tokens = [
        *INITIAL_ITEMS, "BC_CONST", "9", "BC_STORE_LIST", "_",
        "BC_LENGTH", "Items", "BC_PRINT", "BC_LOADVAR", "_", "BC_PRINT",
    ]
    result = execute(x86_linux_codegen, "raw explicit-publication witness", tmp_path, tokens=tokens)
    assert (result.returncode, result.stdout, result.stderr) == (0, "2\n9\n", "")


@requires_linux
@pytest.mark.parametrize("suffix", [
    ["BC_LENGTH"],
    ["BC_LENGTH", "Unknown", "BC_PRINT"],
    ["BC_CONST", "2", "BC_STORE_LIST", "Scalar", "BC_LENGTH", "Scalar", "BC_PRINT"],
    ["BC_LOADVAR", "Items", "BC_STORE_LIST", "Alias", "BC_LENGTH", "Alias"],
    ["BC_CONST", "33", "BC_APPEND", "Items", "BC_LENGTH", "Items"],
    ["BC_LENGTH", "Items", "BC_BINOP", "+"],
    ["BC_LENGTH", "Items"],
], ids=["truncated", "unknown", "scalar", "alias", "growth", "underflow", "residue"])
def test_actual_generator_length_failure_emits_no_partial_assembly(
    suffix, tmp_path, x86_linux_codegen
):
    tokens = [*INITIAL_ITEMS, "BC_CONST", "777", "BC_PRINT", *suffix]
    generated = generate(x86_linux_codegen, tokens, tmp_path)
    assert (generated.returncode, generated.stdout, generated.stderr) == (1, "", "")
