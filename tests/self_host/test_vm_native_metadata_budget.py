"""Actual native-emitter allocation cost for four integer metadata arrays.

This is an allocation-budget witness only. It is not a full metadata ledger,
RSS/commit measurement, system-allocation-failure compatibility proof, speedup
claim, or alias-lifetime proof. ELF SHT_NOBITS/PT_LOAD accounting measures
reserved zero-fill, not pages committed or touched at runtime.
"""
from __future__ import annotations

import platform
import re
import struct
import subprocess
from pathlib import Path

import pytest

from compiler.native import (
    NATIVE_COLLECTION_BYTES,
    NATIVE_COLLECTION_CAPACITY,
    build_native,
    emit_x86_64_linux,
)
from compiler.pipeline import compile_source, run_source
from compiler.self_host import native_artifact_launcher_source

LINUX_X86 = platform.system() == "Linux" and platform.machine().lower() in {
    "x86_64", "amd64"
}
EXTRA_ARRAYS = ("BudgetHead", "BudgetTail", "BudgetLength", "BudgetNext")


def _metadata_declarations() -> str:
    # Identical two-value initializers keep metadata integer arrays and their
    # scalar globals aligned between the baseline and candidate source.
    return "".join(f"{name} = 0, 0;\n" for name in EXTRA_ARRAYS)


def _compiled_assembly(source: str) -> str:
    result = compile_source(source)
    assert result.ok, result.diags.render_all()
    # Deliberately call the unchanged production emitter (not a model or mock).
    return emit_x86_64_linux(result.ir)


def _assembly_bss_census(assembly: str) -> dict:
    """Count emitted BSS bytes including every explicit alignment directive."""
    lines = assembly.splitlines()
    start = lines.index(".section .bss") + 1
    end = next(i for i in range(start, len(lines)) if lines[i].startswith(".section "))
    offset = 0
    allocations: list[tuple[str, int]] = []
    alignments = 0
    for line in lines[start:end]:
        match = re.fullmatch(r"\s*\.p2align\s+(\d+)\s*", line)
        if match:
            alignment = 1 << int(match.group(1))
            offset = (offset + alignment - 1) & -alignment
            alignments += 1
            continue
        match = re.fullmatch(r"\s*([^\s:]+):\s*\.zero\s+(\d+)\s*", line)
        if match:
            size = int(match.group(2))
            allocations.append((match.group(1), size))
            offset += size
    return {"size": offset, "allocations": allocations, "alignments": alignments}


def _elf_census(path: Path) -> dict:
    """Read ELF64 section and PT_LOAD sizes using only Python's stdlib."""
    data = path.read_bytes()
    assert data[:4] == b"\x7fELF" and data[4] == 2 and data[5] == 1
    header = struct.unpack_from("<HHIQQQIHHHHHH", data, 16)
    phoff, shoff = header[4], header[5]
    phentsize, phnum = header[8], header[9]
    shentsize, shnum, shstrndx = header[10], header[11], header[12]
    section_format = "<IIQQQQIIQQ"
    sections = [
        struct.unpack_from(section_format, data, shoff + index * shentsize)
        for index in range(shnum)
    ]
    names_section = sections[shstrndx]
    names = data[names_section[4]: names_section[4] + names_section[5]]
    by_name = {}
    for section in sections:
        name_offset = section[0]
        name = names[name_offset:names.find(b"\0", name_offset)].decode("ascii")
        by_name[name] = {"type": section[1], "size": section[5]}
    load_format = "<IIQQQQQQ"
    loads = [
        struct.unpack_from(load_format, data, phoff + index * phentsize)
        for index in range(phnum)
    ]
    loads = [segment for segment in loads if segment[0] == 1]  # PT_LOAD
    file_backed = sum(segment[5] for segment in loads)
    memory = sum(segment[6] for segment in loads)
    return {
        "file_size": len(data),
        "bss": by_name[".bss"],
        "load_file_bytes": file_backed,
        "load_memory_bytes": memory,
        "load_zero_fill_bytes": sum(max(segment[6] - segment[5], 0) for segment in loads),
    }


def _launcher_source(with_metadata: bool) -> str:
    source = native_artifact_launcher_source()
    return source + ("\n" + _metadata_declarations() if with_metadata else "")


def _append_to_capacity_source(*, invalid_access: bool) -> str:
    # Dynamic APPEND reaches the backend's real native capacity without a
    # capacity override or a huge generated initializer. All four additional
    # candidate integer arrays are present in this executable control.
    source = _metadata_declarations() + (
        f"BudgetIndex = 2;\n"
        f"While BudgetIndex is less than {NATIVE_COLLECTION_CAPACITY};\n"
        "    Append BudgetIndex to BudgetHead;\n"
        "    Add 1 to BudgetIndex;\n"
        "Done.\n"
    )
    if invalid_access:
        # Fail-stop on the one-past store must occur before the subsequent
        # tail-column store/publication. This says nothing about VM ordering.
        source += (
            "Print 777.\n"
            f"Set BudgetHead {NATIVE_COLLECTION_CAPACITY} to 900;\n"
            "Set BudgetTail 0 to 900;\n"
            "Print 888.\n"
        )
    else:
        source += (
            "Get BudgetHead 0; Print @_.\n"
            f"Get BudgetHead {NATIVE_COLLECTION_CAPACITY - 1}; Print @_.\n"
        )
    return source


def test_actual_emitter_accounts_for_four_full_integer_arrays_and_length_cells():
    baseline = _assembly_bss_census(_compiled_assembly(_launcher_source(False)))
    candidate = _assembly_bss_census(_compiled_assembly(_launcher_source(True)))
    base_labels = dict(baseline["allocations"])
    candidate_labels = dict(candidate["allocations"])

    base_buffers = {name for name in base_labels if re.fullmatch(r"\.Lkuro_collection_\d+", name)}
    candidate_buffers = {name for name in candidate_labels if re.fullmatch(r"\.Lkuro_collection_\d+", name)}
    base_item_lengths = {name for name in base_labels if re.fullmatch(r"\.Lkuro_collection_item_len_\d+", name)}
    candidate_item_lengths = {name for name in candidate_labels if re.fullmatch(r"\.Lkuro_collection_item_len_\d+", name)}
    base_lengths = {name for name in base_labels if re.fullmatch(r"\.Lkuro_collection_len_\d+", name)}
    candidate_lengths = {name for name in candidate_labels if re.fullmatch(r"\.Lkuro_collection_len_\d+", name)}

    assert len(candidate_buffers) - len(base_buffers) == len(EXTRA_ARRAYS)
    assert len(candidate_item_lengths) - len(base_item_lengths) == len(EXTRA_ARRAYS)
    assert len(candidate_lengths) - len(base_lengths) == len(EXTRA_ARRAYS)
    added = set(candidate_labels) - set(base_labels)
    assert sum(candidate_labels[label] for label in added) == (
        len(EXTRA_ARRAYS) * (2 * NATIVE_COLLECTION_BYTES + 8)
    )
    assert all(candidate_labels[label] == NATIVE_COLLECTION_BYTES for label in candidate_buffers)
    assert all(candidate_labels[label] == NATIVE_COLLECTION_BYTES for label in candidate_item_lengths)
    assert all(candidate_labels[label] == 8 for label in candidate_lengths)
    # All current VM globals remain identical: only four collection declarations
    # were added, not extra scalar temporaries that could pollute the delta.
    base_globals = {name for name in base_labels if name.startswith(".Lkuro_global_")}
    candidate_globals = {name for name in candidate_labels if name.startswith(".Lkuro_global_")}
    assert candidate_globals == base_globals
    assert candidate["size"] - baseline["size"] == len(EXTRA_ARRAYS) * (
        2 * NATIVE_COLLECTION_BYTES + 8
    )


def test_hosted_small_metadata_array_grows_without_native_capacity_assumption():
    # This hosted control is intentionally small and does not use/import the
    # backend capacity constant as an expected limit.
    result = run_source(
        "HostedMeta = 0; HostedIndex = 0;\n"
        "While HostedIndex is less than 64;\n"
        "    Append HostedIndex to HostedMeta;\n"
        "    Add 1 to HostedIndex;\n"
        "Done.\n"
        "Get HostedMeta 0; Print @_.\n"
        "Get HostedMeta -1; Print @_.\n"
    )
    assert result.compile.ok, result.compile.diags.render_all()
    assert result.runtime_error is None, result.runtime_error
    assert result.stdout == "0\n63\n"


@pytest.mark.skipif(not LINUX_X86, reason="linked native ELF census requires Linux x86-64")
def test_linked_launcher_elf_shows_zero_fill_delta_separate_from_file_backing(tmp_path):
    images = {}
    for label, with_metadata in (("baseline", False), ("candidate", True)):
        compiled = compile_source(_launcher_source(with_metadata))
        assert compiled.ok, compiled.diags.render_all()
        output = tmp_path / f"launcher-{label}"
        # No capacity override: build the actual unchanged Linux native backend.
        build_native(compiled.ir, output, target="x86_64-linux")
        images[label] = _elf_census(output)

    baseline, candidate = images["baseline"], images["candidate"]
    expected = len(EXTRA_ARRAYS) * (2 * NATIVE_COLLECTION_BYTES + 8)
    assert baseline["bss"]["type"] == candidate["bss"]["type"] == 8  # SHT_NOBITS
    assert candidate["bss"]["size"] - baseline["bss"]["size"] == expected
    assert candidate["load_zero_fill_bytes"] - baseline["load_zero_fill_bytes"] == expected
    assert baseline["load_file_bytes"] > 0 and candidate["load_file_bytes"] > 0
    assert baseline["load_memory_bytes"] >= baseline["load_file_bytes"]
    assert candidate["load_memory_bytes"] >= candidate["load_file_bytes"]
    assert baseline["load_zero_fill_bytes"] == baseline["bss"]["size"]
    assert candidate["load_zero_fill_bytes"] == candidate["bss"]["size"]


@pytest.mark.skipif(not LINUX_X86, reason="native execution bounds require Linux x86-64")
def test_native_metadata_array_first_last_slot_and_one_past_fail_stop(tmp_path):
    valid_ir = compile_source(_append_to_capacity_source(invalid_access=False))
    assert valid_ir.ok, valid_ir.diags.render_all()
    valid_image = tmp_path / "metadata-capacity-valid"
    build_native(valid_ir.ir, valid_image, target="x86_64-linux")
    valid = subprocess.run(
        [str(valid_image)], capture_output=True, text=True, check=False, timeout=90
    )
    assert (valid.returncode, valid.stdout, valid.stderr) == (0, "0\n65535\n", "")

    invalid_ir = compile_source(_append_to_capacity_source(invalid_access=True))
    assert invalid_ir.ok, invalid_ir.diags.render_all()
    invalid_image = tmp_path / "metadata-capacity-one-past"
    build_native(invalid_ir.ir, invalid_image, target="x86_64-linux")
    invalid = subprocess.run(
        [str(invalid_image)], capture_output=True, text=True, check=False, timeout=90
    )
    assert (invalid.returncode, invalid.stdout, invalid.stderr) == (1, "777\n", "")
