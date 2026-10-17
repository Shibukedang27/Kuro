"""Conformance checks for the freestanding binary64 decimal formatter."""
from __future__ import annotations

import ctypes
import hashlib
import json
import math
import platform
import random
import re
import shutil
import struct
import subprocess
from pathlib import Path

import pytest


ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / "self_host" / "decimal_formatter.c"
CODEGEN = ROOT / "self_host" / "native_codegen.kuro"
FROZEN_START = "# BEGIN FROZEN ARM64 DECIMAL FORMATTER"
FROZEN_END = "# END FROZEN ARM64 DECIMAL FORMATTER"


def _float_from_bits(bits: int) -> float:
    return struct.unpack(">d", bits.to_bytes(8, "big"))[0]


def _bits_from_float(value: float) -> int:
    return int.from_bytes(struct.pack(">d", value), "big")


def _edge_bits() -> list[int]:
    """Boundary values stressing binary64 rounding and notation transitions."""
    values = {
        0x0000000000000000,  # +0
        0x8000000000000000,  # -0
        0x0000000000000001,  # smallest subnormal
        0x0000000000000002,
        0x000FFFFFFFFFFFFF,  # largest subnormal
        0x0010000000000000,  # smallest normal
        0x7FEFFFFFFFFFFFFF,  # largest finite
        0x7FF0000000000000,  # +inf
        0xFFF0000000000000,  # -inf
        0x7FF8000000000001,  # NaN payload
        0xFFF8000000001234,  # signed NaN payload
    }
    # Every normal power of two and its immediate neighbors, plus powers of ten
    # near both formatting cutoffs and across the finite decimal range.
    for exponent in range(0, 2047):
        bits = exponent << 52
        if exponent:
            values.update((bits - 1, bits, bits + 1))
    for exponent in range(-323, 309):
        try:
            value = float(10.0**exponent)
        except OverflowError:
            continue
        if math.isfinite(value) and value != 0.0:
            values.add(_bits_from_float(value))
            values.add(_bits_from_float(math.nextafter(value, 0.0)))
            values.add(_bits_from_float(math.nextafter(value, math.inf)))
    for boundary in (1e-4, 1e16):
        values.update(
            _bits_from_float(math.nextafter(boundary, direction))
            for direction in (0.0, math.inf)
        )
        values.add(_bits_from_float(boundary))
    return sorted(values)


def _test_bits() -> list[int]:
    bits = set(_edge_bits())
    rng = random.Random(0x4B55524F)
    bits.update(rng.getrandbits(64) for _ in range(2048))
    return sorted(bits)


def _expected_text(bits: int) -> str:
    value = _float_from_bits(bits)
    text = repr(value)
    # Python canonicalizes every NaN payload/sign to "nan"; the formatter's
    # contract likewise ignores NaN sign, while preserving infinities' signs.
    if math.isnan(value):
        text = "nan"
    return text + "\n"


def _frozen_assembly() -> str:
    text = CODEGEN.read_text(encoding="utf-8")
    start = text.find(FROZEN_START)
    end = text.find(FROZEN_END)
    assert start >= 0 and end > start, "embedded ARM64 formatter action markers missing"
    region = text[start:end]
    action = re.search(
        r"(?ms)^Action NativeEmitArmDecimalFormatter;\s*(.*?)^Done\.\s*$", region
    )
    assert action, "NativeEmitArmDecimalFormatter action missing from frozen region"
    chunks = re.findall(
        r"(?m)^\s*NativeOut\s*=\s*NativeOut\s*\+\s*(\"(?:\\.|[^\"\\])*\")\s*;\s*$",
        action.group(1),
    )
    assert chunks, "no JSON-quoted NativeOut text chunks in frozen formatter action"
    return "".join(json.loads(chunk) for chunk in chunks)


def _elfize_macho_assembly(assembly: str) -> str:
    """Translate only section declarations/directives needed by frozen output."""
    lines = []
    for line in assembly.splitlines():
        stripped = line.strip()
        if stripped.startswith((".subsections_via_symbols", ".build_version", ".file", ".loh")):
            continue
        section = re.match(r"^\s*\.section\s+([^,]+),([^,]+)(?:,.*)?$", line)
        if section:
            segment, name = section.group(1).strip(), section.group(2).strip()
            if name == "__text":
                line = ".text"
            elif segment == "__TEXT":
                line = ".section .rodata,\"a\",%progbits"
            elif segment == "__DATA" and name == "__bss":
                line = ".bss"
            elif segment == "__DATA":
                line = ".data"
            else:
                line = ".section .rodata,\"a\",%progbits"
        # Translate Darwin's page relocations to ELF's AArch64 relocation
        # modifiers (the source may address a compiler-emitted constant table).
        line = re.sub(r"([,\s])([^,\s]+)@PAGEOFF\b", r"\1:lo12:\2", line)
        line = re.sub(r"([,\s])([^,\s]+)@PAGE\b", r"\1\2", line)
        # Only used for the full generated-program test; the standalone driver
        # above already uses Linux syscalls. Keep the formatter itself intact.
        line = re.sub(r"\bmov\s+x16,\s*#4\b", "mov x8, #64", line)
        line = re.sub(r"\bmov\s+x16,\s*#1\b", "mov x8, #93", line)
        line = re.sub(r"\bsvc\s+#0x80\b", "svc #0", line)
        assert "@PAGE" not in line, line
        lines.append(line)
    return "\n".join(lines) + "\n"


def test_c_formatter_matches_python_repr_and_roundtrips(tmp_path: Path) -> None:
    clang = shutil.which("clang")
    if not clang:
        pytest.skip("clang is required to build the freestanding formatter")
    darwin = platform.system() == "Darwin"
    library_path = tmp_path / ("libdecimal_formatter.dylib" if darwin else "libdecimal_formatter.so")
    link_flags = ["-dynamiclib", "-Wl,-undefined,error", "-lSystem"] if darwin else ["-shared", "-Wl,--no-undefined"]
    subprocess.run(
        [
            clang,
            *link_flags,
            "-fPIC",
            "-O2",
            "-ffreestanding",
            "-fno-builtin",
            "-fno-stack-protector",
            "-nostdlib",
            str(SOURCE),
            "-o",
            str(library_path),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    library = ctypes.CDLL(str(library_path))
    formatter = library.kuro_decimal_format
    formatter.argtypes = (ctypes.c_ulonglong, ctypes.POINTER(ctypes.c_char))
    formatter.restype = ctypes.c_uint

    for bits in _test_bits():
        output = ctypes.create_string_buffer(64)
        length = formatter(bits, output)
        actual = output.raw[:length].decode("ascii")
        expected = _expected_text(bits)
        assert length == len(actual), f"reported wrong output length for 0x{bits:016x}"
        assert actual == expected, f"0x{bits:016x}: expected {expected!r}, got {actual!r}"
        assert length > 0 and actual.endswith("\n"), f"missing newline for 0x{bits:016x}"
        value = _float_from_bits(bits)
        if not math.isnan(value):
            parsed = float(actual[:-1])
            assert _bits_from_float(parsed) == bits, f"roundtrip mismatch for 0x{bits:016x}"


def test_embedded_arm_formatter_hash_matches_c_source() -> None:
    source_hash = hashlib.sha256(SOURCE.read_bytes()).hexdigest()
    text = CODEGEN.read_text(encoding="utf-8")
    start = text.find(FROZEN_START)
    end = text.find(FROZEN_END)
    assert start >= 0 and end > start, "embedded ARM64 formatter action markers missing"
    region = text[start:end]
    match = re.search(r"(?m)^# C source SHA256: ([0-9a-f]{64})\s*$", region)
    assert match, "embedded formatter source SHA256 header missing"
    assert match.group(1) == source_hash, "embedded ARM64 formatter is stale for decimal_formatter.c"
    assert re.search(r"(?m)^Action NativeEmitArmDecimalFormatter;\s*$", region)


@pytest.mark.skipif(
    not (shutil.which("qemu-aarch64") and shutil.which("ld.lld") and shutil.which("clang")),
    reason="requires clang, ld.lld, and qemu-aarch64 for ARM64 execution",
)
def test_frozen_arm_formatter_executes_on_aarch64(tmp_path: Path) -> None:
    bits = _edge_bits()
    assembly = _elfize_macho_assembly(_frozen_assembly())
    assembly_path = tmp_path / "formatter.s"
    object_path = tmp_path / "formatter.o"
    driver_path = tmp_path / "driver.s"
    driver_object = tmp_path / "driver.o"
    executable = tmp_path / "formatter-arm64"

    # The driver exercises only the formatter function and Linux write/exit
    # syscalls; it deliberately does not use the frozen Darwin print wrapper.
    table = "\n".join(f"    .quad 0x{value:016x}" for value in bits)
    driver_path.write_text(
        ".text\n.global _start\n_start:\n"
        f"    adr x21, input_bits\n    mov x20, #{len(bits)}\n"
        "    sub sp, sp, #96\n"
        "1:\n    ldr x0, [x21], #8\n    mov x1, sp\n"
        "    bl _kuro_decimal_format\n"
        "    mov x2, x0\n    mov x0, #1\n    mov x1, sp\n"
        "    mov x8, #64\n    svc #0\n"
        "    subs x20, x20, #1\n    b.ne 1b\n"
        "    mov x0, #0\n    mov x8, #93\n    svc #0\n"
        ".section .rodata,\"a\",%progbits\ninput_bits:\n"
        + table
        + "\n",
        encoding="utf-8",
    )
    assembly_path.write_text(assembly, encoding="utf-8")
    clang = shutil.which("clang")
    subprocess.run(
        [clang, "--target=aarch64-linux-gnu", "-c", str(assembly_path), "-o", str(object_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    subprocess.run(
        [clang, "--target=aarch64-linux-gnu", "-c", str(driver_path), "-o", str(driver_object)],
        check=True,
        capture_output=True,
        text=True,
    )
    ld = shutil.which("ld.lld")
    subprocess.run(
        [ld, "-m", "aarch64elf", "-static", "-e", "_start", str(driver_object), str(object_path), "-o", str(executable)],
        check=True,
        capture_output=True,
        text=True,
    )
    nm = shutil.which("nm")
    if nm:
        undefined = subprocess.run([nm, "-u", str(executable)], check=True, capture_output=True, text=True)
        assert not undefined.stdout.strip(), f"unexpected undefined symbols (libc dependency?): {undefined.stdout}"

    run = subprocess.run(
        [shutil.which("qemu-aarch64"), str(executable)],
        check=True,
        capture_output=True,
        timeout=30,
    )
    expected = "".join(_expected_text(value) for value in bits).encode("ascii")
    assert run.stdout == expected


@pytest.mark.skipif(
    not (shutil.which("qemu-aarch64") and shutil.which("ld.lld") and shutil.which("clang")),
    reason="requires clang, ld.lld, and qemu-aarch64 for ARM64 execution",
)
def test_generated_arm_decimal_printing_program_executes_on_aarch64(tmp_path: Path) -> None:
    """Exercise native codegen's complete emitted program and print wrapper."""
    import importlib.util
    import sys

    module_path = ROOT / "tests" / "self_host" / "test_native_codegen.py"
    spec = importlib.util.spec_from_file_location("kuro_native_codegen_test_helpers", module_path)
    assert spec and spec.loader
    helpers = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = helpers
    spec.loader.exec_module(helpers)

    tokens = helpers.decimal_printing_bytecode()
    env = helpers.run_codegen(", ".join(json.dumps(token) for token in tokens))
    assert env["NativeFailed"] == 0
    assert "bl _kuro_decimal_format" in env["NativeOut"]
    # The emitted assembly is the Darwin output; translate its syntax and the
    # two wrapper syscall numbers only for Linux ELF/qemu execution.
    assembly = _elfize_macho_assembly(env["NativeOut"])
    assembly = re.sub(r"(?m)^\s*\.globl _main\s*$", ".global _start", assembly)
    assembly = re.sub(r"(?m)^_main:\s*$", "_start:", assembly)
    assembly_path = tmp_path / "generated-program.s"
    object_path = tmp_path / "generated-program.o"
    executable = tmp_path / "generated-program-arm64"
    assembly_path.write_text(assembly, encoding="utf-8")
    clang = shutil.which("clang")
    subprocess.run(
        [clang, "--target=aarch64-linux-gnu", "-c", str(assembly_path), "-o", str(object_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    ld = shutil.which("ld.lld")
    subprocess.run(
        [ld, "-m", "aarch64elf", "-static", "-e", "_start", str(object_path), "-o", str(executable)],
        check=True,
        capture_output=True,
        text=True,
    )
    nm = shutil.which("nm")
    if nm:
        undefined = subprocess.run([nm, "-u", str(executable)], check=True, capture_output=True, text=True)
        assert not undefined.stdout.strip(), f"unexpected undefined symbols (libc dependency?): {undefined.stdout}"

    run = subprocess.run(
        [shutil.which("qemu-aarch64"), str(executable)],
        check=True,
        capture_output=True,
        timeout=30,
    )
    assert run.stdout.decode("ascii") == helpers.DECIMAL_PRINTING_OUTPUT
