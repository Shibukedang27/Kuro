"""Assembly-generation regressions; these do not claim ARM64 execution parity."""
from copy import deepcopy

import pytest

from compiler.native import NativeBackendError, emit_macos_arm64
from compiler.pipeline import compile_source
from compiler.self_host import native_compiler_source


def _cursor_source(declaration="Integers", value="2", increment="1"):
    # A variable APPEND (not a literal STORE_LIST) is the owning scanner path.
    return (
        f"LCFrameAction is {declaration};\n"
        f"LCActionStart = {value};\n"
        "Append LCActionStart to LCFrameAction;\n"
        "Get LCFrameAction 0; LCActionStart = @_;\n"
        "LCParamPos = LCActionStart;\n"
        f"Add {increment} to LCParamPos; Print LCParamPos.\n"
    )


def _compile(source):
    result = compile_source(source)
    assert result.ok, result.diags.render_all()
    return result.ir


def test_arm64_declared_integer_append_get_preserves_numeric_cursor():
    ir = _compile(_cursor_source())
    assert ir.symbol_types["LCFrameAction"] == "Integers"
    assert any(i.op == "APPEND" and i.args[0] == "LCFrameAction" for i in ir.main)
    assert any(i.op == "GET" and i.args[0] == "LCFrameAction" for i in ir.main)
    assert any(i.op == "ADD" and i.args[0] == "LCParamPos" for i in ir.main)
    assembly = emit_macos_arm64(ir)
    assert "    add x0, x0, x1" in assembly
    assert "    ldr x0, [x2, x1]" in assembly
    assert "b.ge L_kuro_collection_overflow" in assembly
    assert "b.hs L_kuro_collection_bounds" in assembly
    assert "L_kuro_collection_bounds:" in assembly


@pytest.mark.parametrize("declaration,value,increment", [
    ("Text", '"two"', "1"),
    ("Integers", "2", '"one"'),
    ("Decimals", "2", "1"),
])
def test_arm64_cursor_increment_still_requires_two_integer_operands(
    declaration, value, increment
):
    ir = _compile(_cursor_source(declaration, value, increment))
    with pytest.raises(NativeBackendError, match="dynamic ADD requires numeric operands"):
        emit_macos_arm64(ir)


def test_arm64_untyped_append_does_not_gain_numeric_admission():
    ir = _compile(_cursor_source())
    del ir.symbol_types["LCFrameAction"]
    with pytest.raises(NativeBackendError, match="dynamic ADD requires numeric operands"):
        emit_macos_arm64(ir)


def test_arm64_full_authored_compiler_integer_frame_and_guarded_cursor():
    ir = _compile(native_compiler_source())
    assert ir.symbol_types["LCFrameAction"] == "Integers"
    assert any(i.op == "GET" and i.args[0] == "LCFrameAction" for i in ir.main)
    assert any(i.op == "ADD" and i.args[0] == "LCParamPos" for i in ir.main)
    assembly = emit_macos_arm64(ir)
    assert ".globl _main" in assembly
    assert "L_kuro_collection_bounds:" in assembly

    # The declaration, not the variable's spelling or an ADD bypass, carries
    # the kind. Losing it recreates the exact parent's assembly-time failure.
    missing_declaration = deepcopy(ir)
    del missing_declaration.symbol_types["LCFrameAction"]
    with pytest.raises(NativeBackendError, match="dynamic ADD requires numeric operands"):
        emit_macos_arm64(missing_declaration)

    # Keep the owner Integer but make the actual increment Text: still reject.
    text_increment = deepcopy(ir)
    cursor_add = next(
        i for i in text_increment.main
        if i.op == "ADD" and i.args[0] == "LCParamPos"
    )
    operand = cursor_add.args[1]
    constant = next(i for i in text_increment.main if i.dest == operand)
    assert constant.op == "CONST"
    constant.args = ("one",)
    with pytest.raises(NativeBackendError, match="dynamic ADD requires numeric operands"):
        emit_macos_arm64(text_increment)


@pytest.mark.parametrize("source", [
    'Bag is Integers; X = "bad"; Append X to Bag; Get Bag 0; Cursor = @_; Add 1 to Cursor;',
    'Bag is Integers; X = "bad"; Set Bag 0 to X; Get Bag 0; Cursor = @_; Add 1 to Cursor;',
    # A linear last-definition check would miss the Text path at this join.
    'Bag is Integers; Words = "bad", "worse"; Get Words 0; X = @_; '
    'Flag = 0; If Flag is equal to 1; X = 2; Done. '
    'Append X to Bag; Get Bag 0; Cursor = @_; Add 1 to Cursor;',
    # A later write must invalidate an earlier read too (e.g. inside a loop).
    'Bag is Integers; Get Bag 0; Cursor = @_; Add 1 to Cursor; '
    'Set Bag 0 to "bad";',
    'Bag is Integers; '
    'Action Poison Value; Set Bag 0 to Value; Done. Call Poison "bad"; '
    'Get Bag 0; Cursor = @_; Add 1 to Cursor;',
    # Return inference must not guess numeric just from a parameter's name.
    'Bag is Integers; Action Identity Index; Return Index; Done. '
    'Call Identity "bad"; X = @_; Append X to Bag; '
    'Get Bag 0; Cursor = @_; Add 1 to Cursor;',
    'Bag is Integers; '
    'Action Poison Value; Set Bag 0 to Value; Done. Call Poison 1; '
    'Call MakeClosure "Poison"; Setter = @_; Call Invoke Setter, "bad"; '
    'Get Bag 0; Cursor = @_; Add 1 to Cursor;',
    'Bag is Integers; X is Text; Take user X; Append X to Bag; Get Bag 0; Cursor = @_; Add 1 to Cursor;',
], ids=["text-append", "text-set", "branch-join", "later-write", "action-set", "action-return", "indirect-action", "input"])
def test_arm64_integer_collection_rejects_unproven_or_text_writes(source):
    source = source.replace("Bag is Integers;", "Bag is Integers; Append 0 to Bag;", 1)
    ir = _compile(source)
    from compiler.native import _arm64_integer_collections

    assert _arm64_integer_collections(ir, {"Bag"}) == set()
    with pytest.raises(NativeBackendError, match="dynamic ADD requires numeric operands"):
        emit_macos_arm64(ir)


def test_arm64_provenance_recognizes_both_integer_scanner_frame_owners():
    from compiler.native import _arm64_integer_collections

    ir = _compile(native_compiler_source())
    owners = {i.args[0] for i in ir.main if i.op == "APPEND"}
    assert _arm64_integer_collections(ir, owners) == {"LCFrameAction", "LCFrameRepeat"}


@pytest.mark.parametrize("mixed_write", [False, True], ids=["numeric", "text-write"])
def test_arm64_inferred_integer_literal_owner_requires_the_same_write_proof(mixed_write):
    from compiler.native import _arm64_integer_collections

    # symbol_types contains inferred types too. This ordinary literal owner was
    # already numeric after STORE_LIST in the parent; it is not new admission.
    source = 'Bag = 1, 2; Append 3 to Bag; '
    if mixed_write:
        source += 'Append "bad" to Bag; '
    ir = _compile(source + 'Get Bag 0; Cursor = @_; Add 1 to Cursor; Print Cursor.')
    assert ir.symbol_types["Bag"] == "Integers"
    if mixed_write:
        assert _arm64_integer_collections(ir, {"Bag"}) == set()
        # No new seed is inferred. The legacy literal STORE_LIST refinement
        # is intentionally outside this repair, not a new global write policy.
    else:
        assert _arm64_integer_collections(ir, {"Bag"}) == {"Bag"}
        assert "    add x0, x0, x1" in emit_macos_arm64(ir)


@pytest.mark.parametrize("image", ["runtime", "compiler", "bytecode", "codegen"])
def test_arm64_production_image_sources_preserve_unrelated_collection_fallback(image):
    from compiler.self_host import (
        native_runtime_source, native_artifact_launcher_source, native_codegen_source,
    )

    sources = {
        "runtime": native_runtime_source,
        "compiler": native_compiler_source,
        "bytecode": native_artifact_launcher_source,
        "codegen": native_codegen_source,
    }
    # A proof that cannot classify an unrelated VM collection must retain the
    # parent fallback, not reject the entire image. No linking/execution claim.
    assembly = emit_macos_arm64(_compile(sources[image]()))
    assert ".globl _main" in assembly
    assert "L_kuro_collection_bounds:" in assembly
