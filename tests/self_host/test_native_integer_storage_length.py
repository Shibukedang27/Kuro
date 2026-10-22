"""Text-only source Length frontend gate and fail-closed integer generation.

Unknown alias tokens and the raw VM remain lower-level capabilities, not proof
of complete source validation.
"""
from __future__ import annotations

import json
import subprocess

import pytest

from compiler.pipeline import compile_source, run_source
from compiler.self_host import SelfHostError, compile_with_kuro_driver
from test_native_codegen import run_codegen, x86_linux_codegen
from test_native_integer_storage import execute, generate, requires_linux
from test_native_integer_storage_capacity import (
    _run_authored_vm,
    _values,
    native_compiler,
    native_compiler_image,
)
from test_typecheck_cross import kuro_semantic, python_semantic


INITIAL_ITEMS = [
    "BC_MULTI_BEGIN", "BC_CONST", "11", "BC_CONST", "22",
    "BC_STORE_MULTI", "Items",
]


def _wire(tokens):
    return ", ".join(json.dumps(token) for token in tokens)


INTEGER_SOURCES = [
    pytest.param("Items = 11, 22;\nLength Items;\nPrint @_.\n", id="minimum-owner"),
    pytest.param(f"Items = {_values(32)};\nLength Items;\nPrint @_.\n", id="larger-owner"),
    pytest.param("Items = 11, 22;\nSet Items 0 to 777;\nLength Items;\nPrint @_.\n", id="cell-mutation"),
    pytest.param("Items = 11, 22;\nOther = 1, 2, 3, 4;\nLength Other;\nLength Items;\nPrint @_.\n", id="repeated-publication"),
    pytest.param("Items = 11, 22;\nLength Items;\nIndex = @_ - 1;\nGet Items Index;\nPrint @_.\n", id="derived-index"),
    pytest.param("Items = 11, 22;\nAlias is Integers;\nAlias = Items;\nLength Alias;\nPrint @_.\n", id="typed-alias"),
    pytest.param("Items = 11, 22;\nAppend 33 to Items;\nLength Items;\nPrint @_.\n", id="growth"),
    pytest.param("Items = 11, 22;\nIf 1 is equal to 1;\nLength Items;\nPrint @_.\nDone.\n", id="control-flow"),
    pytest.param("Items = 11, 22;\nAction Read;\nLength Items;\nPrint @_.\nDone.\nCall Read;\n", id="action"),
]


@pytest.mark.parametrize("source", INTEGER_SOURCES)
def test_reference_and_authored_semantic_pass_reject_integer_collection_length(source):
    compiled = compile_source(source)
    assert not compiled.ok
    assert "error[E3009]: Length target must be Text, found Integers" in compiled.diags.render_all()
    reference = python_semantic(source)
    authored = kuro_semantic(source)
    assert authored == reference
    assert reference["diagnostics"]
    assert all(code == "E3009" for code, _ in reference["diagnostics"])


def test_maximal_initializer_reference_rejection_without_claiming_hosted_semantic_capacity():
    # The recursive hosted authored semantic pass has an existing large-list
    # recursion limit. Do not raise it or imply this maximum ran through it.
    source = f"Items = {_values(272)};\nLength Items;\nPrint @_.\n"
    compiled = compile_source(source)
    assert not compiled.ok
    assert [diag.code for diag in compiled.diags.diagnostics] == ["E3009"]


def test_unknown_alias_type_is_not_misrepresented_as_static_length_rejection():
    # Existing inference records literal types, not VarRef assignment types.
    # Both semantic passes therefore accept this unknown target; native owner
    # aliasing remains independently closed by the generator, tested below.
    source = "Items = 11, 22;\nAlias = Items;\nLength Alias;\nPrint @_.\n"
    assert compile_source(source).ok
    assert kuro_semantic(source) == python_semantic(source)
    assert python_semantic(source)["diagnostics"] == []


@requires_linux
@pytest.mark.parametrize("source", INTEGER_SOURCES + [
    pytest.param(f"Items = {_values(272)};\nLength Items;\nPrint @_.\n", id="maximum-owner"),
])
def test_known_integer_length_is_rejected_before_native_artifact_publication(
    source, native_compiler_image
):
    completed = subprocess.run(
        [str(native_compiler_image)], input=source, text=True,
        capture_output=True, check=False, timeout=30,
    )
    assert (completed.returncode, completed.stdout, completed.stderr) == (
        1, "kuro.compile-error/1\n", "",
    )
    with pytest.raises(SelfHostError):
        compile_with_kuro_driver(source)


@requires_linux
def test_unknown_alias_tokens_do_not_authorize_integer_length_native_output(
    tmp_path, native_compiler, x86_linux_codegen
):
    # The bounded frontend rule deliberately does not infer VarRef aliases.
    # Generator rejection remains independent defense for that unknown route.
    source = "Items = 11, 22;\nAlias = Items;\nLength Alias;\nPrint @_.\n"
    tokens = native_compiler(source, tmp_path)
    assert "BC_LENGTH" in tokens
    generated = generate(x86_linux_codegen, tokens, tmp_path)
    assert (generated.returncode, generated.stdout, generated.stderr) == (1, "", "")


@pytest.mark.parametrize("source", [
    "Items is Integers;\nItems = 5;\nLength Items;",
    "Items = 5;\nLength Items;",
    "Items = 1.5, 2.5;\nLength Items;",
])
def test_non_text_scalar_and_decimal_length_remain_semantic_errors(source):
    assert not compile_source(source).ok
    assert kuro_semantic(source) == python_semantic(source)
    assert ("E3009", 3 if "is Integers" in source else 2) in python_semantic(source)["diagnostics"]


@pytest.mark.parametrize("source,expected", [
    ('Items = "Kuro";\nLength Items;\nPrint @_.\n', "4\n"),
    ('Items = "a", "bb";\nLength Items;\nPrint @_.\n', "2\n"),
])
def test_text_source_contract_keeps_reference_and_authored_semantic_runtime_parity(source, expected):
    assert kuro_semantic(source) == python_semantic(source)
    assert python_semantic(source)["diagnostics"] == []
    result = run_source(source)
    assert result.ok and result.stdout == expected
    compiled = compile_with_kuro_driver(source)
    assert compiled["CompilerFailed"] == 0
    env = _run_authored_vm(compiled["CompilerOutput"])
    assert not env["VMFailed"]
    assert env["VMOutput"] == [int(expected.strip())]


@pytest.mark.parametrize("suffix", [
    ["BC_LENGTH", "Items", "BC_STORE_LIST", "_", "BC_LOADVAR", "_", "BC_PRINT"],
    ["BC_LENGTH", "Items", "BC_PRINT"],
    ["BC_CONST", "40", "BC_LENGTH", "Items", "BC_BINOP", "+", "BC_PRINT"],
    ["BC_LENGTH"],
    ["BC_LENGTH", "BC_STORE_LIST", "_"],
    ["BC_LENGTH", "Unknown", "BC_PRINT"],
    ["BC_CONST", "2", "BC_STORE_LIST", "Scalar", "BC_LENGTH", "Scalar", "BC_PRINT"],
    ["BC_LOADVAR", "Items", "BC_STORE_LIST", "Alias", "BC_LENGTH", "Alias"],
    ["BC_CONST", "33", "BC_APPEND", "Items", "BC_LENGTH", "Items"],
    ["BC_FUNC_BEGIN", "Read", "BC_LENGTH", "Items", "BC_PRINT", "BC_FUNC_END"],
    ["BC_CONST", "1", "BC_CONST", "1", "BC_CMP", "eq", "BC_IF_BEGIN", "BC_LENGTH", "Items", "BC_PRINT", "BC_ELSE_BEGIN", "BC_IF_END"],
    ["BC_LENGTH", "Items", "BC_BINOP", "+", "BC_PRINT"],
    ["BC_LENGTH", "Items"],
], ids=["published", "direct", "lower-stack", "truncated", "missing-owner", "unknown-owner", "scalar", "alias", "growth", "action", "control-flow", "underflow", "residue"])
def test_portable_integer_length_rejection_emits_no_partial_assembly(suffix):
    # A complete print satisfies the independent mandatory-print requirement.
    tokens = [*INITIAL_ITEMS, "BC_CONST", "777", "BC_PRINT", *suffix]
    env = run_codegen(_wire(tokens), target="x86_64-linux", execution_target="x86_64-linux")
    assert (env["NativeFailed"], env["NativeOut"]) == (1, "")


@requires_linux
@pytest.mark.parametrize("suffix", [
    ["BC_LENGTH", "Items", "BC_STORE_LIST", "_", "BC_LOADVAR", "_", "BC_PRINT"],
    ["BC_LENGTH", "Items", "BC_PRINT"],
    ["BC_CONST", "40", "BC_LENGTH", "Items", "BC_BINOP", "+", "BC_PRINT"],
    ["BC_LENGTH"],
    ["BC_LENGTH", "Unknown", "BC_PRINT"],
    ["BC_LENGTH", "Items", "BC_BINOP", "+"],
    ["BC_LENGTH", "Items"],
], ids=["published", "direct", "lower-stack", "truncated", "unknown", "underflow", "residue"])
def test_actual_generator_integer_length_failure_emits_no_partial_assembly(
    suffix, tmp_path, x86_linux_codegen
):
    tokens = [*INITIAL_ITEMS, "BC_CONST", "777", "BC_PRINT", *suffix]
    generated = generate(x86_linux_codegen, tokens, tmp_path)
    assert (generated.returncode, generated.stdout, generated.stderr) == (1, "", "")


@pytest.mark.parametrize("output_target", ["aarch64-macos", "x86_64-macos", "x86_64-linux"])
@pytest.mark.parametrize("execution_target", ["unverified", "aarch64-macos", "x86_64-macos", "x86_64-linux"])
def test_no_platform_qualification_authorizes_integer_owner_length(output_target, execution_target):
    tokens = [*INITIAL_ITEMS, "BC_LENGTH", "Items", "BC_STORE_LIST", "_", "BC_LOADVAR", "_", "BC_PRINT"]
    env = run_codegen(_wire(tokens), target=output_target, execution_target=execution_target)
    assert (env["NativeFailed"], env["NativeOut"]) == (1, "")


def test_raw_authored_vm_collection_length_primitive_is_not_removed():
    # Raw BC_LENGTH publishes in this VM; compiler lowering adds STORE_LIST _.
    # That pre-existing low-level capability is not an exception to ADR-0013.
    tokens = [*INITIAL_ITEMS, "BC_LENGTH", "Items", "BC_STORE_LIST", "_", "BC_LOADVAR", "_", "BC_PRINT"]
    env = _run_authored_vm(tokens)
    assert not env["VMFailed"]
    assert env["VMOutput"] == [2]


@requires_linux
@pytest.mark.parametrize("count", [2, 272])
def test_integer_storage_get_and_logical_bounds_survive_length_admission_restriction(
    count, tmp_path, x86_linux_codegen, native_compiler
):
    source = f"Items = {_values(count)};\nGet Items -1;\nPrint @_.\n"
    assert compile_source(source).ok
    tokens = native_compiler(source, tmp_path)
    result = execute(x86_linux_codegen, source, tmp_path, tokens=tokens)
    assert (result.returncode, result.stdout, result.stderr) == (0, f"{count - 1}\n", "")
