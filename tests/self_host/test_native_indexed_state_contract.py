"""Reference subset and semantic blockers, NOT Kuro-owned collection lowering."""
import hashlib
import json
import platform
import subprocess

import pytest

from compiler.native import build_native
from compiler.pipeline import compile_source, run_source
from compiler.self_host import compile_with_kuro_driver
from test_native_codegen import x86_linux_codegen  # shared fresh-image fixture
from test_vm_cross import run_kuro_vm_environment


LINUX_X86 = platform.system() == "Linux" and platform.machine().lower() in {"x86_64", "amd64"}
requires_linux_x86 = pytest.mark.skipif(not LINUX_X86, reason="executes Linux x86-64 images")


def indexed_state_source(slot, frame):
    # A test-local contract: 16 numeric lanes and 16 flattened snapshots.
    # Guards constrain logical length, not merely allocated backing storage.
    return f"""Masks = 1, 1;
Snapshots = 1, 1;
Repeat 14;
    Append 1 to Masks;
Done.
Repeat 254;
    Append 1 to Snapshots;
Done.
Slot = {slot};
Frame = {frame};
If Slot is less than 0 or Slot is greater than or equal to 16 or Frame is less than 0 or Frame is greater than or equal to 16;
    Print "REJECT".
Else;
    Position = Frame * 16 + Slot;
    Set Masks Slot to 4;
    Set Snapshots Position to 2;
    Get Masks Slot;
    Print @_.
    Get Snapshots Position;
    Print @_.
    Other = 15 - Slot;
    Get Masks Other;
    Print @_.
    OtherPosition = 255 - Position;
    Get Snapshots OtherPosition;
    Print @_.
Done.
"""


REFERENCE_CASES = [
    ("first", indexed_state_source(0, 0), "4\n2\n1\n1\n"),
    ("last", indexed_state_source(15, 15), "4\n2\n1\n1\n"),
    ("interior", indexed_state_source(7, 8), "4\n2\n1\n1\n"),
    ("negative-slot", indexed_state_source(-1, 0), "REJECT\n"),
    ("slot-overflow", indexed_state_source(16, 0), "REJECT\n"),
    ("negative-frame", indexed_state_source(0, -1), "REJECT\n"),
    ("frame-overflow", indexed_state_source(0, 16), "REJECT\n"),
    ("text-names", 'Names is Text;\nAppend "slot00" to Names;\nAppend "slot15" to Names;\n'
     'Set Names 0 to "changed";\nGet Names 0;\nPrint @_.\nGet Names 1;\nPrint @_.\n'
     'Length Names;\nPrint @_.\n', "changed\nslot15\n2\n"),
]


def compiler_tokens(source):
    compiled = compile_with_kuro_driver(source)
    assert compiled["CompilerFailed"] == 0
    tokens = [str(token) for token in compiled["CompilerOutput"]]
    assert compiled["CompilerInstructionCount"] == len(tokens)
    assert 0 < len(tokens) < 4096  # isolate these witnesses from program size
    return tokens


def frame_artifact(tokens):
    def encode(token):
        if token == "":
            return r"\e"
        if token == "kuro.input/1":
            return r"\i"
        return token.replace("\\", "\\\\").replace("\n", r"\n").replace("\r", r"\r").replace("\t", r"\t")
    return "kuro.bytecode/1\n" + "\n".join(encode(token) for token in tokens) + "\n"


@pytest.mark.parametrize("name, source, expected", REFERENCE_CASES, ids=[c[0] for c in REFERENCE_CASES])
def test_guarded_indexed_state_reference_parity(name, source, expected):
    host = run_source(source)
    assert host.ok, (host.compile.diags.render_all(), host.runtime_error)
    assert host.stdout == expected
    # Kuro compiler + Kuro VM, hosted in the IR interpreter; not native codegen.
    vm = run_kuro_vm_environment(source)
    assert vm["VMFailed"] == 0
    assert "\n".join(str(value) for value in vm["VMOutput"]) + "\n" == expected


@requires_linux_x86
@pytest.mark.parametrize("name, source, expected", REFERENCE_CASES, ids=[c[0] for c in REFERENCE_CASES])
def test_guarded_indexed_state_hosted_native_parity(tmp_path, name, source, expected):
    compiled = compile_source(source)
    assert compiled.ok, compiled.diags.render_all()
    image = tmp_path / name
    # Python-authored backend. This is explicitly NOT Kuro generator output.
    build_native(compiled.ir, image, target="x86_64-linux")
    executed = subprocess.run([str(image)], text=True, capture_output=True, timeout=10)
    assert (executed.returncode, executed.stdout, executed.stderr) == (0, expected, "")


@requires_linux_x86
def test_real_generator_indexed_state_contract_boundary(tmp_path, x86_linux_codegen):
    """Live scalar control; every complete collection witness rejects below ceiling."""
    manifest = {
        "scope": "reference parity and rejection boundary; no collection lowering",
        "generator_image_sha256": hashlib.sha256(x86_linux_codegen.read_bytes()).hexdigest(),
        "generator_bootstrap": "hosted Python compile_source/build_native",
        "compiler_path": "Kuro stages in hosted interpreter",
        "cases": {},
    }
    scalar = 'Slot = 15;\nFrame = 15;\nPosition = Frame * 16 + Slot;\nPrint Position.\n'
    cases = [("scalar-control", scalar, "255\n"), *REFERENCE_CASES]
    for name, source, expected in cases:
        tokens = compiler_tokens(source)
        wire = frame_artifact(tokens)
        generated = subprocess.run([str(x86_linux_codegen)], input=wire, text=True,
                                   capture_output=True, timeout=30)
        (tmp_path / f"{name}.kuro").write_text(source, encoding="utf-8")
        (tmp_path / f"{name}.bc").write_text(wire, encoding="utf-8")
        (tmp_path / f"{name}.s").write_text(generated.stdout, encoding="utf-8")
        record = {
            "token_count": len(tokens),
            "source_sha256": hashlib.sha256(source.encode()).hexdigest(),
            "artifact_sha256": hashlib.sha256(wire.encode()).hexdigest(),
            "assembly_sha256": hashlib.sha256(generated.stdout.encode()).hexdigest(),
            "generator_exit": generated.returncode,
            "submitted_program_executed": False,
        }
        if name == "scalar-control":
            assert generated.returncode == 0 and generated.stderr == ""
            image = tmp_path / name
            subprocess.run(["clang", "-target", "x86_64-unknown-linux-gnu", "-nostdlib",
                            "-Wl,-e,_start", "-x", "assembler", "-", "-o", str(image)],
                           input=generated.stdout, text=True, capture_output=True, check=True)
            executed = subprocess.run([str(image)], text=True, capture_output=True, timeout=5)
            assert (executed.returncode, executed.stdout, executed.stderr) == (0, expected, "")
            undefined = subprocess.run(["nm", "-u", str(image)], text=True, capture_output=True, check=True)
            assert undefined.stdout.strip() == ""
            record.update(submitted_program_executed=True, stdout=executed.stdout,
                          executed_image_sha256=hashlib.sha256(image.read_bytes()).hexdigest())
        else:
            assert {"BC_APPEND", "BC_GET", "BC_SET"} <= set(tokens)
            if name == "text-names":
                assert {"BC_DECLTYPE", "BC_LENGTH"} <= set(tokens)
            else:
                assert "BC_MULTI_BEGIN" in tokens
            assert (generated.returncode, generated.stdout, generated.stderr) == (1, "", "")
        manifest["cases"][name] = record
    (tmp_path / "indexed-state-boundary.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


def test_negative_collection_get_is_an_unresolved_semantic_boundary():
    # Observational regression, NOT approval of either behavior for new lowering.
    source = 'Items = 10, 20;\nGet Items -1;\nPrint @_.\n'
    host = run_source(source)
    assert host.ok and host.stdout == "20\n"
    vm = run_kuro_vm_environment(source)
    assert vm["VMFailed"] == 1


@requires_linux_x86
@pytest.mark.parametrize("operation", ["Get Items 2;\nPrint @_.", 'Set Items 2 to 7;\nPrint "continued".'])
def test_logical_length_is_not_hosted_native_storage_capacity(tmp_path, operation):
    # Both accesses are outside the two-element logical collection. The hosted
    # backend checks backing capacity instead. Keep the discrepancy visible;
    # never use that backend as the oracle for new unguarded collection lowering.
    source = "Items = 10, 20;\n" + operation + "\n"
    host = run_source(source)
    assert host.compile.ok and host.runtime_error is not None
    assert host.runtime_error.code == "E6001"
    vm = run_kuro_vm_environment(source)
    assert vm["VMFailed"] == 1
    image = tmp_path / "logical-length-probe"
    build_native(host.compile.ir, image, target="x86_64-linux")
    executed = subprocess.run([str(image)], text=True, capture_output=True, timeout=5)
    # Existing behavior is recorded, not characterized as bounds-safe parity.
    expected = "0\n" if operation.startswith("Get") else "continued\n"
    assert (executed.returncode, executed.stdout, executed.stderr) == (0, expected, "")
