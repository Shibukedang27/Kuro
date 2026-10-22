"""Lifetime and publication contracts for self-hosted VM storage.

The decode oracle below is copied from the exact #110 parent VM at
0b2a3fdfc1ffcafff519f69265ab85d30eee9d52, including #108's optimization.
It is deliberately an embedded source oracle: CI does not need Git or a
baseline checkout. Production sources are unchanged in this increment.
"""
from __future__ import annotations

import hashlib
import platform
import subprocess
from pathlib import Path

import pytest

from compiler.native import build_native
from compiler.pipeline import compile_source, run_source
from compiler.self_host import native_artifact_launcher_source


PARENT_SHA = "0b2a3fdfc1ffcafff519f69265ab85d30eee9d52"
_PARENT_DECODER_SHA256 = "885bd5c6f53a7d713d871e815eef31c4bbabb48577152a788f97e5feea46cadb"

# Exact VMDecodeDigit/Number/Constant source from PARENT_SHA. The digest pins
# the literal to the source slice extracted when this fixture was recorded.
_PARENT_DECODER = r'''VMNumericOk = 1;

Action VMDecodeDigit Char;
    If Char is equal to "0";
        Return 0;
    Else;
        If Char is equal to "1";
            Return 1;
        Else;
            If Char is equal to "2";
                Return 2;
            Else;
                If Char is equal to "3";
                    Return 3;
                Else;
                    If Char is equal to "4";
                        Return 4;
                    Else;
                        If Char is equal to "5";
                            Return 5;
                        Else;
                            If Char is equal to "6";
                                Return 6;
                            Else;
                                If Char is equal to "7";
                                    Return 7;
                                Else;
                                    If Char is equal to "8";
                                        Return 8;
                                    Else;
                                        If Char is equal to "9";
                                            Return 9;
                                        Else;
                                            VMNumericOk = 0;
                                            Return 0;
                                        Done.
                                    Done.
                                Done.
                            Done.
                        Done.
                    Done.
                Done.
            Done.
        Done.
    Done.
Done.

Action VMDecodeNumber Value, Pos, Count, Accumulated, DecimalDivisor, DecimalMode;
    If Pos is less than Count;
        Get Value Pos;
        VMDecodeNumber_Char = @_;
        If VMDecodeNumber_Char is equal to ".";
            VMDecodedFloat = 1;
            VMDecodeNumber_Next = Pos + 1;
            Call VMDecodeNumber Value, VMDecodeNumber_Next, Count, Accumulated, DecimalDivisor, 1;
            Return @_;
        Else;
            Call VMDecodeDigit VMDecodeNumber_Char;
            VMDecodeNumber_Digit = @_;
            VMDecodeNumber_NextAcc = Accumulated * 10 + VMDecodeNumber_Digit;
            If DecimalMode is equal to 1;
                VMDecodeNumber_NextDivisor = DecimalDivisor * 10;
            Else;
                VMDecodeNumber_NextDivisor = DecimalDivisor;
            Done.
            VMDecodeNumber_Next = Pos + 1;
            Call VMDecodeNumber Value, VMDecodeNumber_Next, Count, VMDecodeNumber_NextAcc, VMDecodeNumber_NextDivisor, DecimalMode;
            Return @_;
        Done.
    Else;
        If DecimalMode is equal to 1;
            VMDecodeNumber_FloatAcc = Accumulated * 1.0;
            VMDecodeNumber_FloatDivisor = DecimalDivisor * 1.0;
            Return VMDecodeNumber_FloatAcc / VMDecodeNumber_FloatDivisor;
        Else;
            Return Accumulated;
        Done.
    Done.
Done.

Action VMDecodeConstant Value;
    VMDecodedFloat = 0;
    VMDecodedDisplay = "";
    Length Value;
    VMDecodeConstant_Count = @_;
    If VMDecodeConstant_Count is equal to 0;
        Return Value;
    Done.
    VMNumericOk = 1;
    # Keep the recursive accumulator and decimal divisor as integers.  The
    # decoder converts them to floating point only at the final division, so
    # native integer literals and decimal literals share no ambiguous ABI.
    If VMDecodeConstant_Count is equal to 1;
        # Value already is the complete one-character Text. Do not allocate
        # a second copy with Get, or decode a failed digit a second time.
        Call VMDecodeDigit Value;
        If VMNumericOk is equal to 1;
            Return @_;
        Done.
        Return Value;
    Done.
    Call VMDecodeNumber Value, 0, VMDecodeConstant_Count, 0, 1, 0;
    VMDecodeConstant_Number = @_;
    If VMNumericOk is equal to 1;
        If VMDecodedFloat is equal to 1;
            VMDecodedDisplay = Value;
        Done.
        Return VMDecodeConstant_Number;
    Else;
        VMDecodedFloat = 0;
        VMDecodedDisplay = "";
        Return Value;
    Done.
Done.'''


requires_x86_64_linux = pytest.mark.skipif(
    platform.system() != "Linux" or platform.machine().lower() not in {"x86_64", "amd64"},
    reason="requires executable x86-64 Linux native images",
)


def _working_tree_decoder() -> str:
    root = Path(__file__).resolve().parents[2]
    source = (root / "self_host" / "vm.kuro").read_text(encoding="utf-8")
    start = source.index("VMNumericOk = 1;\n\nAction VMDecodeDigit Char;")
    end = source.index("\nAction VMStep;", start)
    return source[start:end]


def _launcher_source(decoder: str, *, expose_decoder_state: bool = False) -> str:
    source = native_artifact_launcher_source()
    current = _working_tree_decoder()
    assert source.count(current) == 1
    source = source.replace(current, decoder, 1)
    if expose_decoder_state:
        source += "\nPrint VMNumericOk.\nPrint VMDecodedFloat.\nPrint VMDecodedDisplay.\nPrint ArtifactSource.\n"
    return source


def _artifact(tokens: list[str]) -> str:
    return "kuro.bytecode/1\n" + "\n".join(tokens) + "\n"


def _decode_lifetime_artifact() -> str:
    tokens = [
        "BC_CONST", "12.3x", "BC_STORE_LIST", "RetainedMalformed",
        "BC_CONST", "001.50", "BC_STORE_LIST", "RetainedDecimal",
    ]
    # Later decodes repeatedly exercise numeric, decimal, malformed, and
    # multi-character paths before either retained value is observed again.
    for value in ("7", "12.3x", "4.25", "ab", "001.50", "0", "x", "0009.00"):
        tokens.extend(("BC_CONST", value, "BC_PRINT"))
    tokens.extend(
        (
            "BC_LOADVAR", "RetainedMalformed", "BC_PRINT",
            "BC_LOADVAR", "RetainedDecimal", "BC_PRINT",
        )
    )
    return _artifact(tokens)


def _run_hosted(source: str, payload: str):
    result = run_source(source, input_fn=lambda _prompt: payload)
    assert result.compile.ok, result.compile.diags.render_all()
    assert result.runtime_error is None, result.runtime_error
    env = result.interpreter.env
    assert env["ArtifactFailed"] == 0
    assert env["RuntimeExitCode"] == 0
    assert env["ArtifactSource"] == payload
    return result.stdout or ""


def _build_native_launcher(source: str, output: Path) -> None:
    compiled = compile_source(source)
    assert compiled.ok, compiled.diags.render_all()
    build_native(compiled.ir, output, target="x86_64-linux")


def _run_native(executable: Path, payload: str, cwd: Path):
    completed = subprocess.run(
        [str(executable)],
        input=payload.encode("utf-8"),
        capture_output=True,
        check=False,
        timeout=60,
        cwd=cwd,
    )
    return completed.returncode, completed.stdout, completed.stderr


def test_repeated_vm_decodes_preserve_earlier_malformed_and_decimal_values_hosted():
    assert hashlib.sha256(_PARENT_DECODER.encode("utf-8")).hexdigest() == _PARENT_DECODER_SHA256
    payload = _decode_lifetime_artifact()
    parent = _run_hosted(_launcher_source(_PARENT_DECODER, expose_decoder_state=True), payload)
    current = _run_hosted(_launcher_source(_working_tree_decoder(), expose_decoder_state=True), payload)

    expected = "7\n12.3x\n4.25\nab\n001.50\n0\nx\n0009.00\n12.3x\n001.50\n1\n1\n0009.00\n" + payload + "\n"
    assert parent == expected
    assert current == expected


@requires_x86_64_linux
def test_repeated_vm_decodes_preserve_earlier_values_native_bytes(tmp_path):
    assert hashlib.sha256(_PARENT_DECODER.encode("utf-8")).hexdigest() == _PARENT_DECODER_SHA256
    payload = _decode_lifetime_artifact()
    parent_image = tmp_path / "parent-decoder-launcher"
    current_image = tmp_path / "current-decoder-launcher"
    _build_native_launcher(
        _launcher_source(_PARENT_DECODER, expose_decoder_state=True), parent_image
    )
    _build_native_launcher(
        _launcher_source(_working_tree_decoder(), expose_decoder_state=True), current_image
    )

    expected_stdout = (
        "7\n12.3x\n4.25\nab\n001.50\n0\nx\n0009.00\n"
        "12.3x\n001.50\n1\n1\n0009.00\n" + payload + "\n"
    ).encode("utf-8")
    parent = _run_native(parent_image, payload, tmp_path)
    current = _run_native(current_image, payload, tmp_path)
    assert parent == (0, expected_stdout, b"")
    assert current == (0, expected_stdout, b"")


def _collection_copy_artifact() -> str:
    # Keep a destination collection reference on the VM stack while mutating,
    # resetting, and then deactivating the source collection.
    return _artifact(
        [
            "BC_MULTI_BEGIN", "BC_CONST_TEXT", "original", "BC_CONST", "001.50",
            "BC_STORE_MULTI", "Source",
            "BC_LOADVAR", "Source", "BC_STORE_LIST", "Destination",
            "BC_LOADVAR", "Destination",
            "BC_CONST", "0", "BC_CONST_TEXT", "mutated", "BC_SET", "Source",
            "BC_LOADVAR", "Source", "BC_PRINT",
            "BC_MULTI_BEGIN", "BC_CONST_TEXT", "replacement", "BC_CONST_TEXT", "extra",
            "BC_STORE_MULTI", "Source",
            # Scalar publication deactivates Source's collection ID.
            "BC_CONST_TEXT", "scalar", "BC_STORE_LIST", "Source",
            # The preserved stack reference and the named destination both survive.
            "BC_PRINT", "BC_LOADVAR", "Destination", "BC_PRINT",
        ]
    )


def test_vm_collection_copy_is_independent_across_source_mutation_and_reset_hosted():
    output = _run_hosted(_launcher_source(_working_tree_decoder()), _collection_copy_artifact())
    assert output == "mutated\n001.50\noriginal\n001.50\noriginal\n001.50\n"


@requires_x86_64_linux
def test_vm_collection_copy_is_independent_after_source_deactivation_native_bytes(tmp_path):
    executable = tmp_path / "collection-copy-launcher"
    _build_native_launcher(_launcher_source(_working_tree_decoder()), executable)
    completed = _run_native(executable, _collection_copy_artifact(), tmp_path)
    assert completed == (
        0,
        b"mutated\n001.50\noriginal\n001.50\noriginal\n001.50\n",
        b"",
    )
