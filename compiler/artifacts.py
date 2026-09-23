"""Versioned Kuro IR artifact loading and execution."""
from __future__ import annotations

import json
import hashlib
import struct
from pathlib import Path

from .bytecode import BytecodeProgram, BytecodeVM
from .interpreter import KuroRuntimeException


class ArtifactError(ValueError):
    """Raised when a file is not a valid Kuro executable artifact."""


ARTIFACT_SCHEMA = "kuro.artifact/1"
BINARY_MAGIC = b"KRA\x01"
BINARY_HEADER = struct.Struct(">4sI32s")


def make_artifact_document(program: BytecodeProgram, *, kind: str = "kuro.ir/1", entry: str = "main") -> dict:
    """Create the canonical, integrity-checked Kuro artifact envelope."""
    payload = program.to_data()
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    if kind not in {"kuro.ir/1", "kuro.app/1"}:
        raise ArtifactError(f"unsupported Kuro artifact format {kind!r}")
    return {
        "schema": ARTIFACT_SCHEMA,
        "format": kind,
        "language": "kuro",
        "entry": entry,
        "bytecode_sha256": hashlib.sha256(canonical).hexdigest(),
        "bytecode": payload,
    }


def write_artifact(path: str | Path, program: BytecodeProgram, *, kind: str = "kuro.ir/1", entry: str = "main") -> Path:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    document = make_artifact_document(program, kind=kind, entry=entry)
    destination.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return destination


def write_binary_artifact(path: str | Path, program: BytecodeProgram, *, kind: str = "kuro.ir/1", entry: str = "main") -> Path:
    """Write the stable Kuro artifact envelope in a framed binary container.

    The JSON envelope remains the canonical semantic representation.  The
    binary wrapper adds a magic/version marker, an explicit payload length,
    and a digest over the exact serialized envelope so launchers can reject
    truncation or corruption before parsing it.
    """
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    document = make_artifact_document(program, kind=kind, entry=entry)
    payload = json.dumps(document, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    header = BINARY_HEADER.pack(BINARY_MAGIC, len(payload), hashlib.sha256(payload).digest())
    destination.write_bytes(header + payload)
    return destination


def _read_document(path: str | Path) -> dict:
    raw = Path(path).read_bytes()
    if raw.startswith(BINARY_MAGIC):
        if len(raw) < BINARY_HEADER.size:
            raise ArtifactError("truncated Kuro binary artifact header")
        magic, length, digest = BINARY_HEADER.unpack(raw[:BINARY_HEADER.size])
        payload = raw[BINARY_HEADER.size:]
        if len(payload) != length:
            raise ArtifactError("Kuro binary artifact payload length mismatch")
        if hashlib.sha256(payload).digest() != digest:
            raise ArtifactError("Kuro binary artifact integrity check failed")
        try:
            document = json.loads(payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ArtifactError("Kuro binary artifact contains invalid metadata") from error
    else:
        try:
            document = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            message = error.msg if isinstance(error, json.JSONDecodeError) else "file is not UTF-8"
            raise ArtifactError(f"invalid Kuro artifact JSON: {message}") from error
    if not isinstance(document, dict):
        raise ArtifactError("Kuro artifact must contain a JSON object")
    if document.get("schema") != ARTIFACT_SCHEMA:
        raise ArtifactError(f"unsupported or missing Kuro artifact schema {document.get('schema')!r}")
    if document.get("format") not in {"kuro.ir/1", "kuro.app/1"}:
        raise ArtifactError("unsupported Kuro artifact format")
    if document.get("language") != "kuro":
        raise ArtifactError("Kuro artifact language marker must be 'kuro'")
    if not isinstance(document.get("entry"), str) or not document["entry"]:
        raise ArtifactError("Kuro artifact is missing a valid entry")
    return document


def read_artifact_document(path: str | Path) -> dict:
    """Return validated envelope metadata without executing its program."""
    document = _read_document(path)
    payload = document.get("bytecode") or document.get("program")
    if not isinstance(payload, dict):
        raise ArtifactError("Kuro artifact is missing its serialized program")
    try:
        program = BytecodeProgram.from_data(payload)
    except ValueError as error:
        raise ArtifactError(str(error)) from error
    digest = document.get("bytecode_sha256")
    if digest is not None:
        canonical = json.dumps(program.to_data(), ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
        if digest != hashlib.sha256(canonical).hexdigest():
            raise ArtifactError("Kuro artifact bytecode integrity check failed")
    return document


def read_program(path: str | Path) -> BytecodeProgram:
    document = read_artifact_document(path)
    payload = document.get("bytecode") or document.get("program")
    return BytecodeProgram.from_data(payload)


def run_artifact(path: str | Path, *, input_fn=input, output=None) -> tuple[BytecodeProgram, str | None, KuroRuntimeException | None]:
    import io

    program = read_program(path)
    stream = output if output is not None else io.StringIO()
    interpreter = BytecodeVM(program, input_fn=input_fn, output=stream)
    try:
        interpreter.run()
    except KuroRuntimeException as error:
        return program, stream.getvalue() if hasattr(stream, "getvalue") else None, error
    return program, stream.getvalue() if hasattr(stream, "getvalue") else None, None
