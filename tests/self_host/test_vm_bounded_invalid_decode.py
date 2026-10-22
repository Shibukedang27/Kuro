"""Differential contracts for the VM's bounded invalid-number decode path.

The parent decoder is the hash-pinned literal from test_vm_storage_lifetime;
using it as the unchanged oracle keeps this test independent of Git state.
"""
from __future__ import annotations

import itertools
import hashlib
import platform
import re

import pytest

from compiler.pipeline import run_source
from test_vm_storage_lifetime import (
    _PARENT_DECODER,
    _PARENT_DECODER_SHA256,
    _artifact,
    _build_native_launcher,
    _launcher_source,
    _run_hosted,
    _run_native,
    _working_tree_decoder,
)


requires_x86_64_linux = pytest.mark.skipif(
    platform.system() != "Linux"
    or platform.machine().lower() not in {"x86_64", "amd64"},
    reason="requires executable x86-64 Linux native images",
)


def _inputs() -> tuple[str, ...]:
    # All short strings over a compact alphabet exercise digit, decimal, and
    # invalid-character recursion interactions without launching per value.
    values = [""]
    alphabet = ("0", "1", ".", "x")
    for length in range(1, 4):
        values.extend("".join(chars) for chars in itertools.product(alphabet, repeat=length))

    # Put an invalid character at each representative position around the
    # Count < 19 cutoff. Zero prefixes prevent integer overflow on the legacy
    # path before an end-position invalid character is encountered.
    for length in (17, 18, 19, 20):
        values.extend((
            "x" + "0" * (length - 1),
            "0" * (length // 2) + "x" + "0" * (length - length // 2 - 1),
            "0" * (length - 1) + "x",
        ))
        values.append("1." + "0" * (length - 3) + "x")
        values.append("0.." + "0" * (length - 3) + "x")

    values.extend((
        "é", "猫", "🙂", "0" * 8 + "猫" + "0" * 8,
        "🙂" + "0" * 18,
        ".", "..", "....", "1..2", "0...0", "12.3x", "x.5", "7x.",
        "0" * 18 + "1",                    # valid 19-character integer
        "0" * 19 + "1",                    # valid 20-character integer
        "1234567890123456789",             # 19 digits, within signed int64
        "0." + "0" * 16 + "1",             # safe 17-place fraction
        "0." + "0" * 17 + "1",             # safe 18-place fraction
        "0" * 16 + "..1",                  # repeated-dot legacy behavior
    ))
    return tuple(dict.fromkeys(values))


_INPUTS = _inputs()


def _probe_source(decoder: str) -> str:
    lines = [
        'VMDecodedFloat = 0;',
        'VMDecodedDisplay = "";',
        "VMNumericOk = 1;",
        decoder,
    ]
    for index, value in enumerate(_INPUTS):
        # The fixture alphabet excludes quotes/backslashes, so these literals
        # are unambiguous in Kuro source while still including Unicode cases.
        lines.extend((
            f'ProbeInput{index} = "{value}";',
            "VMNumericOk = 1;",
            "VMDecodedFloat = 0;",
            'VMDecodedDisplay = "";',
            f"Call VMDecodeConstant ProbeInput{index};",
            f"ProbeValue{index} = @_;",
            f"ProbeOk{index} = VMNumericOk;",
            f"ProbeFloat{index} = VMDecodedFloat;",
            f"ProbeDisplay{index} = VMDecodedDisplay;",
        ))

    # Emit every result/state tuple, followed by all original inputs again.
    # The second pass detects accidental mutation or invalidation of retained
    # text after later recursive decodes have executed.
    for index in range(len(_INPUTS)):
        lines.extend((
            f"Print ProbeValue{index}.",
            f"Print ProbeOk{index}.",
            f"Print ProbeFloat{index}.",
            f"Print ProbeDisplay{index}.",
        ))
    for index in range(len(_INPUTS)):
        lines.append(f"Print ProbeInput{index}.")
    return "\n".join(lines)


def _expected_decode(value: str):
    """Small independent semantic oracle for the decoder's public contract."""
    if value == "":
        return value, 1, 0, ""
    if len(value) == 1:
        if value in "0123456789":
            return int(value), 1, 0, ""
        return value, 0, 0, ""

    accumulated = 0
    divisor = 1
    decimal_mode = False
    for char in value:
        if char == ".":
            decimal_mode = True
            continue
        if char not in "0123456789":
            return value, 0, 0, ""
        accumulated = accumulated * 10 + int(char)
        if decimal_mode:
            divisor *= 10

    if decimal_mode:
        return accumulated / divisor, 1, 1, value
    return accumulated, 1, 0, ""


def _hosted(source: str):
    result = run_source(source)
    assert result.compile.ok, result.compile.diags.render_all()
    assert result.runtime_error is None, result.runtime_error
    env = result.interpreter.env
    observed = {
        index: (
            env[f"ProbeValue{index}"],
            env[f"ProbeOk{index}"],
            env[f"ProbeFloat{index}"],
            env[f"ProbeDisplay{index}"],
        )
        for index in range(len(_INPUTS))
    }
    assert tuple(env[f"ProbeInput{index}"] for index in range(len(_INPUTS))) == _INPUTS
    return result.stdout or "", observed


def _artifact_probe(decoder: str) -> tuple[str, str]:
    """Build one launcher that reports state after each batched BC_CONST."""
    source = _launcher_source(decoder)
    call = "Call VMDecodeConstant @_;"
    assert source.count(call) == 1
    source = source.replace(
        call,
        "VMNumericOk = 1;\n        "
        + call
        + "\n        Print VMNumericOk.\n"
        + "        Print VMDecodedFloat.\n"
        + "        Print VMDecodedDisplay.",
        1,
    )
    tokens: list[str] = []
    for index, value in enumerate(_INPUTS):
        tokens.extend((
            "BC_CONST",
            "\\e" if value == "" else value,
            "BC_STORE_LIST",
            f"DecodeResult{index}",
        ))
    # Load the results only after every decode; malformed values therefore
    # exercise the retained original Text across the complete call sequence.
    for index in range(len(_INPUTS)):
        tokens.extend(("BC_LOADVAR", f"DecodeResult{index}", "BC_PRINT"))
    return source, _artifact(tokens)


def test_invalid_decode_guard_is_after_digit_and_strictly_below_19():
    decoder = _working_tree_decoder()
    assert hashlib.sha256(_PARENT_DECODER.encode("utf-8")).hexdigest() == _PARENT_DECODER_SHA256
    executable_lines = "\n".join(
        line for line in decoder.splitlines() if not line.lstrip().startswith("#")
    )
    match = re.search(
        r"Call VMDecodeDigit VMDecodeNumber_Char;\s*"
        r"VMDecodeNumber_Digit = @_;\s*"
        r"If VMNumericOk is equal to 0 and Count is less than 19;\s*"
        r"Return 0;\s*"
        r"Done\.",
        executable_lines,
    )
    assert match is not None, (
        "VMDecodeNumber must immediately return zero after a failed digit only "
        "when the original Count is strictly less than 19"
    )


def test_hosted_exhaustive_and_boundary_decodes_match_parent_and_contract():
    assert hashlib.sha256(_PARENT_DECODER.encode("utf-8")).hexdigest() == _PARENT_DECODER_SHA256
    source_parent = _probe_source(_PARENT_DECODER)
    source_current = _probe_source(_working_tree_decoder())
    parent_stdout, parent_values = _hosted(source_parent)
    current_stdout, current_values = _hosted(source_current)

    assert current_stdout == parent_stdout
    assert current_values == parent_values
    assert len(_INPUTS) >= 100
    for index, value in enumerate(_INPUTS):
        expected = _expected_decode(value)
        assert parent_values[index] == expected, (value, parent_values[index], expected)
        assert current_values[index] == expected, (value, current_values[index], expected)

    # Invalid inputs always publish their original retained Text and clear both
    # float metadata fields; long invalid strings retain those same semantics.
    for index, value in enumerate(_INPUTS):
        decoded, ok, is_float, display = current_values[index]
        if ok == 0:
            assert (decoded, is_float, display) == (value, 0, "")


@requires_x86_64_linux
def test_native_exhaustive_and_boundary_decodes_match_parent_bytes(tmp_path):
    assert hashlib.sha256(_PARENT_DECODER.encode("utf-8")).hexdigest() == _PARENT_DECODER_SHA256
    parent_source, payload = _artifact_probe(_PARENT_DECODER)
    current_source, current_payload = _artifact_probe(_working_tree_decoder())
    assert current_payload == payload
    parent_image = tmp_path / "parent-decoder-probe"
    current_image = tmp_path / "current-decoder-probe"
    _build_native_launcher(parent_source, parent_image)
    _build_native_launcher(current_source, current_image)

    parent = _run_native(parent_image, payload, tmp_path)
    current = _run_native(current_image, payload, tmp_path)
    assert current == parent
    assert parent[0] == 0
    assert parent[2] == b""

    # Hosted and native stdout must agree too, not only the two native builds.
    hosted_parent = _run_hosted(parent_source, payload)
    hosted_current = _run_hosted(current_source, payload)
    assert parent[1].decode("utf-8") == hosted_parent
    assert current[1].decode("utf-8") == hosted_current
    assert current == parent
