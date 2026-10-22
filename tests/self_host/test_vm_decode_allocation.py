"""Parity tests pinning VM constant decoding around allocation optimizations.

The reference decoder is the exact VMDecodeDigit/Number/Constant implementation
from parent 1dc7eebadd042175eb9bd54eba824ead545601df. Keeping it inline makes the
compatibility oracle independent of Git and of any baseline checkout path.
"""
from __future__ import annotations

import platform
import subprocess
from pathlib import Path

import pytest

from compiler.native import build_native
from compiler.pipeline import compile_source, run_source
from compiler.self_host import native_artifact_launcher_source


PARENT_SHA = "1dc7eebadd042175eb9bd54eba824ead545601df"

# Exact decoder actions from self_host/vm.kuro at PARENT_SHA (including the
# decoder's shared status global). Do not replace this with a second copy of
# the working-tree implementation: this literal is the independent oracle.
_PARENT_DECODER = '''VMNumericOk = 1;

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
    # Keep the recursive accumulator and decimal divisor as integers. The
    # decoder converts them to floating point only at the final division, so
    # native integer literals and decimal literals share no ambiguous ABI.
    If VMDecodeConstant_Count is equal to 1;
        Get Value 0;
        Call VMDecodeDigit @_;
        If VMNumericOk is equal to 1;
            Return @_;
        Done.
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
Done.
'''

# Every required edge class is represented, with a few nearby numeric cases to
# check successful paths and the decimal display spelling as well.
_INPUTS = (
    "",
    *tuple(str(digit) for digit in range(10)),
    ".",
    "x",
    "é",
    "0007",
    "001.50",
    ".7",
    "12.3",
    "12..3",
    "12.3x",
    "7x.",
    "x.5",
)


def _working_tree_decoder() -> str:
    root = Path(__file__).resolve().parents[2]
    source = (root / "self_host" / "vm.kuro").read_text(encoding="utf-8")
    start = source.index("VMNumericOk = 1;\n\nAction VMDecodeDigit Char;")
    end = source.index("\nAction VMStep;", start)
    return source[start:end]


def _probe_source(decoder: str, *, print_results: bool = False, values=_INPUTS) -> str:
    lines = ["VMDecodedFloat = 0;", 'VMDecodedDisplay = "";', decoder]
    for index, value in enumerate(values):
        # Inputs intentionally avoid quotes and backslashes, so the literal is
        # also valid in the Kuro source grammar without host-specific escaping.
        lines.extend(
            [
                f'ProbeInput{index} = "{value}";',
                f"Call VMDecodeConstant ProbeInput{index};",
                f"ProbeValue{index} = @_;",
                f"ProbeOk{index} = VMNumericOk;",
                f"ProbeFloat{index} = VMDecodedFloat;",
                f"ProbeDisplay{index} = VMDecodedDisplay;",
            ]
        )
        if print_results:
            lines.extend(
                [
                    f"Print ProbeOk{index}.",
                    f"Print ProbeFloat{index}.",
                ]
            )
    return "\n".join(lines)


def _hosted_probe(decoder: str):
    result = run_source(_probe_source(decoder))
    assert result.ok, result.compile.diags.render_all()
    env = result.interpreter.env
    return {
        index: (
            env[f"ProbeValue{index}"],
            env[f"ProbeOk{index}"],
            env[f"ProbeFloat{index}"],
            env[f"ProbeDisplay{index}"],
        )
        for index in range(len(_INPUTS))
    }, env


def test_vm_decode_constant_matches_parent_for_valid_and_malformed_text():
    reference, _ = _hosted_probe(_PARENT_DECODER)
    current, env = _hosted_probe(_working_tree_decoder())
    assert current == reference

    # Pin representative semantics in addition to the full parent comparison.
    assert current[0] == ("", 1, 0, "")  # empty input is returned untouched
    assert current[1] == (0, 1, 0, "")
    assert current[11] == (".", 0, 0, "")  # single dot is malformed
    assert current[12] == ("x", 0, 0, "")
    assert current[13] == ("é", 0, 0, "")
    assert current[14] == (7, 1, 0, "")  # leading zeroes
    assert current[15] == (1.5, 1, 1, "001.50")
    assert current[17] == (12.3, 1, 1, "12.3")
    assert current[18] == (12.3, 1, 1, "12..3")  # parent accepts repeated dots
    for index in (19, 20, 21):
        assert current[index] == (_INPUTS[index], 0, 0, "")

    # Each source string remains unchanged, and every malformed return retains
    # its own string after all subsequent decodes have run. Decimal display
    # strings likewise remain the spelling captured at their own decode.
    for index, original in enumerate(_INPUTS):
        assert env[f"ProbeInput{index}"] == original
        if current[index][1] == 0 or original == "":
            assert current[index][0] == original
    assert current[15][3] == env["ProbeInput15"] == "001.50"


requires_x86_64_linux = pytest.mark.skipif(
    platform.system() != "Linux" or platform.machine().lower() not in {"x86_64", "amd64"},
    reason="requires executable x86-64 Linux native images",
)


@requires_x86_64_linux
def test_fresh_native_vm_decoder_probe_matches_parent(tmp_path):
    # Use the production artifact-loader + VM + runtime composition, replacing
    # only the decoder actions in the parent build.  Each process receives one
    # BC_CONST so native action-frame reuse across decoder calls cannot obscure
    # a decoder parity failure.
    native_values = (
        "", "0", "9", ".", "001.50", "12..3", "12.3x", "ab",
        "é", "e\u0301", "猫語", "🙂猫",
    )

    def build(decoder: str, name: str) -> Path:
        launcher_source = native_artifact_launcher_source()
        candidate_decoder = _working_tree_decoder()
        assert launcher_source.count(candidate_decoder) == 1
        launcher_source = launcher_source.replace(candidate_decoder, decoder, 1)
        # VM bytecode has its own variable store, so observe the decoder's Kuro
        # globals in the composed launcher after RuntimeRun has printed the VM
        # result.  This leaves the framed program itself as a raw BC_CONST
        # probe, while making all decoder state visible as exact native bytes.
        launcher_source += (
            '\nPrint VMNumericOk.\n'
            'Print VMDecodedFloat.\n'
            'Print VMDecodedDisplay.\n'
        )
        compiled = compile_source(launcher_source)
        assert compiled.ok, compiled.diags.render_all()
        image = tmp_path / name
        build_native(compiled.ir, image, target="x86_64-linux")
        return image

    def framed_probe(value: str) -> bytes:
        # Artifact tokens use a small backslash escape alphabet.  The probe
        # values below contain no control characters or backslashes; the empty
        # constant is represented by the loader's explicit empty-token escape.
        encoded = value if value else "\\e"
        tokens = [
            "BC_CONST", encoded, "BC_PRINT",
            "BC_CONST_TEXT", encoded, "BC_PRINT",
        ]
        return ("kuro.bytecode/1\n" + "\n".join(tokens) + "\n").encode("utf-8")

    parent_image = build(_PARENT_DECODER, "parent-artifact-launcher")
    current_image = build(_working_tree_decoder(), "current-artifact-launcher")

    # Pin the entire native byte stream, not only status flags.  The first line
    # is the actual BC_CONST return printed by the production VM; the remaining
    # lines expose its status, float marker, retained display spelling, and the
    # original input bytes (including multi-byte and combining UTF-8 text).
    expected = {
        "": ("", 1, 0, ""),
        "0": ("0", 1, 0, ""),
        "9": ("9", 1, 0, ""),
        ".": (".", 0, 0, ""),
        "001.50": ("001.50", 1, 1, "001.50"),
        "12..3": ("12..3", 1, 1, "12..3"),
        "12.3x": ("12.3x", 0, 0, ""),
        "ab": ("ab", 0, 0, ""),
        "é": ("é", 0, 0, ""),
        "e\u0301": ("e\u0301", 0, 0, ""),
        "猫語": ("猫語", 0, 0, ""),
        "🙂猫": ("🙂猫", 0, 0, ""),
    }

    for value in native_values:
        expected_value, numeric_ok, decoded_float, display = expected[value]
        expected_stdout = (
            f"{expected_value}\n{value}\n{numeric_ok}\n{decoded_float}\n{display}\n"
        ).encode("utf-8")
        reference = subprocess.run(
            [str(parent_image)], input=framed_probe(value), capture_output=True,
            check=False, timeout=30, cwd=tmp_path,
        )
        current = subprocess.run(
            [str(current_image)], input=framed_probe(value), capture_output=True,
            check=False, timeout=30, cwd=tmp_path,
        )
        assert (reference.returncode, reference.stderr) == (0, b"")
        assert (current.returncode, current.stderr) == (0, b"")
        assert reference.stdout == expected_stdout
        assert current.stdout == expected_stdout
