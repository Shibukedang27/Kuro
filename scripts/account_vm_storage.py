#!/usr/bin/env python3
"""Measure unchanged Linux VM storage at exit using symbol-only GDB exposure.

Requires gdb, clang, and an artifact input (including kuro.input/1 for a
compiler self-reproduction). No VM source, instructions or limits are changed.
The report is a final retained allocation census, not a general GC liveness proof.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from compiler.native import emit_x86_64_linux
from compiler.pipeline import compile_source
from compiler.self_host import native_artifact_launcher_source


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    if not re.fullmatch(r"[A-Za-z0-9_./-]+", str(out)):
        raise ValueError("GDB evidence paths must contain only safe shell characters")
    input_bytes = args.input.read_bytes()
    snapshot = out / 'input.kurobc'
    snapshot.write_bytes(input_bytes)
    source = native_artifact_launcher_source()
    compiled = compile_source(source)
    if not compiled.ok:
        raise RuntimeError(compiled.diags.render_all())
    mapping = {}

    def trace(frame, event, arg):
        if frame.f_code is emit_x86_64_linux.__code__ and event == "return":
            for key in ("collection_buffers", "collection_lengths", "global_labels"):
                mapping[key] = dict(frame.f_locals[key])
        return trace

    sys.setprofile(trace)
    try:
        original = emit_x86_64_linux(compiled.ir)
    finally:
        sys.setprofile(None)
    # Only assembler-local symbol spelling changes. Instructions, operands,
    # data bytes, capacities and control flow are preserved modulo relocation.
    exposed = original.replace(".Lkuro_", "audit_kuro_")
    assert exposed.replace("audit_kuro_", ".Lkuro_") == original
    (out / "original.s").write_text(original)
    asm = out / "symbolized.s"
    asm.write_text(exposed)
    mapping = {key: {name: label.replace(".Lkuro_", "audit_kuro_")
                     for name, label in values.items()}
               for key, values in mapping.items()}
    (out / "labels.json").write_text(json.dumps(mapping, indent=2) + "\n")
    image = out / "launcher"
    subprocess.run(["clang", "-g", "-target", "x86_64-unknown-linux-gnu",
                    "-nostdlib", "-static", "-Wl,-e,_start", str(asm),
                    "-o", str(image)], check=True)
    gdb_python = r'''
import gdb, json, collections
from pathlib import Path
out = Path(OUTPUT)
labels = json.loads((out / "labels.json").read_text())
def address(label):
    return int(gdb.parse_and_eval("&" + label))
def words(label, count):
    data = bytes(gdb.selected_inferior().read_memory(address(label), count * 8))
    return [int.from_bytes(data[i:i+8], "little", signed=True) for i in range(0, len(data), 8)]
def scalar(name):
    return words(labels['global_labels'][name], 1)[0]
def vector(name):
    count = words(labels['collection_lengths'][name], 1)[0]
    return words(labels['collection_buffers'][name], count)
def text(pointer):
    if not pointer:
        return ""
    return gdb.Value(pointer).cast(gdb.lookup_type('char').pointer()).string(encoding='utf-8', errors='strict')
names = [text(p) for p in vector('VMCollectionNames')][:scalar('VMCollectionCount')]
ids = vector('VMCollectionIds')[:len(names)]
counts = collections.Counter(vector('VMCollectionOwners')[:scalar('VMCollectionEntryCount')])
active = {owner: name for name, owner in zip(names, ids) if owner >= 0}
report = {
    'stop': gdb.newest_frame().name(),
    'stop_reason': 'normal_epilogue' if int(gdb.parse_and_eval('$audit_stop')) == 1 else 'generic_overflow',
    'vm_failed': scalar('VMFailed'),
    'runtime_exit_code': scalar('RuntimeExitCode'),
    'entry_count': scalar('VMCollectionEntryCount'),
    'column_lengths': {name: len(vector(name)) for name in ('VMCollectionOwners', 'VMCollectionItems', 'VMCollectionItemDisplay')},
    'char_bytes': words('audit_kuro_char_heap_cursor', 1)[0],
    'text_join_bytes': words('audit_kuro_text_heap_cursor', 1)[0],
    'owners': [{'id': owner, 'name': active.get(owner), 'entries': count, 'currently_named': owner in active} for owner, count in sorted(counts.items())],
    'named_entries': sum(count for owner, count in counts.items() if owner in active),
    'unnamed_entries': sum(count for owner, count in counts.items() if owner not in active),
    'active_names': dict(zip(names, ids)),
}
(out / 'census.json').write_text(json.dumps(report, indent=2) + '\n')
'''.replace("OUTPUT", repr(str(out)))
    commands = ("set pagination off\nset confirm off\n"
                "break audit_kuro_main_epilogue\nbreak audit_kuro_overflow\n"
                "commands 1\nsilent\nset $audit_stop = 1\nend\n"
                "commands 2\nsilent\nset $audit_stop = 2\nend\n"
                f"run < {snapshot} > {out / 'stdout'} 2> {out / 'stderr'}\n"
                "python\n" + gdb_python + "\nend\ncontinue\n"
                "python\n"
                "report['inferior_exit_code'] = int(gdb.parse_and_eval('$_exitcode'))\n"
                "(out / 'census.json').write_text(json.dumps(report, indent=2) + '\\n')\n"
                "end\n")
    cmd = out / "commands.gdb"
    cmd.write_text(commands)
    result = subprocess.run(["gdb", "-nx", "-iex", "set auto-load off", "-q", "-batch", "-x", str(cmd), str(image)],
                            capture_output=True, timeout=300)
    (out / "gdb.log").write_bytes(result.stdout + result.stderr)
    if result.returncode or not (out / "census.json").exists():
        raise RuntimeError(f"GDB accounting failed; inspect {out / 'gdb.log'}")
    report = json.loads((out / "census.json").read_text())
    if 'inferior_exit_code' not in report:
        raise RuntimeError(f"Missing inferior exit status; inspect {out / 'gdb.log'}")
    report.update({"input_sha256": hashlib.sha256(input_bytes).hexdigest(),
                   "launcher_source_sha256": hashlib.sha256(source.encode()).hexdigest(),
                   "original_assembly_sha256": hashlib.sha256(original.encode()).hexdigest(),
                   "symbolized_assembly_sha256": hashlib.sha256(exposed.encode()).hexdigest(),
                   "diagnostic_image_sha256": hashlib.sha256(image.read_bytes()).hexdigest(),
                   "stdout_sha256": hashlib.sha256((out / "stdout").read_bytes()).hexdigest(),
                   "symbol_only_roundtrip": True})
    count = report['entry_count']
    report['invariants_passed'] = (
        0 <= count <= 65536
        and all(length == max(2, count) for length in report['column_lengths'].values())
        and report['named_entries'] + report['unnamed_entries'] == count
    )
    report['successful_exit_census'] = (
        report['stop_reason'] == 'normal_epilogue'
        and report['vm_failed'] == report['runtime_exit_code'] == report['inferior_exit_code'] == 0
        and report['invariants_passed']
        and not (out / 'stderr').read_bytes()
    )
    (out / "census.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps(report, indent=2))
    if not report['successful_exit_census']:
        raise RuntimeError('Not a consistent successful-exit census; inspect report and GDB log')


if __name__ == "__main__":
    main()
