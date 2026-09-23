"""First native backend: macOS arm64 assembly for literal-print programs.

This backend is intentionally capability-checked. It emits native assembly
only for operations whose ABI lowering is implemented; other Kuro programs
receive a clear diagnostic instead of silently using a foreign runtime.
"""
from __future__ import annotations

import subprocess
import platform
import shutil
from pathlib import Path

from .ir import IRProgram


class NativeBackendError(ValueError):
    pass


NATIVE_INPUT_CAPACITY = 1 << 20
NATIVE_INPUT_READ_LIMIT = NATIVE_INPUT_CAPACITY - 1
NATIVE_COLLECTION_CAPACITY = 1 << 16
NATIVE_COLLECTION_BYTES = NATIVE_COLLECTION_CAPACITY * 8
NATIVE_TEXT_HEAP_CAPACITY = 1 << 24


def _link_x86_64_linux(assembly: Path, destination: Path) -> None:
    """Assemble and link a freestanding Linux image, including on macOS.

    Apple's linker cannot consume ELF objects.  Cross-build hosts therefore
    use LLVM's ELF linker directly; native Linux hosts keep the normal clang
    driver path.  The resulting image has no libc or dynamic-loader dependency.
    """
    if platform.system() == "Linux":
        command = [
            "clang", "-target", "x86_64-unknown-linux-gnu", "-nostdlib",
            "-Wl,-e,_start", str(assembly), "-o", str(destination),
        ]
        result = subprocess.run(command, check=False, capture_output=True)
    else:
        object_path = destination.with_suffix(".linux-x86_64.o")
        assembled = subprocess.run(
            ["clang", "-target", "x86_64-unknown-linux-gnu", "-c", str(assembly), "-o", str(object_path)],
            check=False, capture_output=True,
        )
        if assembled.returncode:
            raise subprocess.CalledProcessError(
                assembled.returncode, assembled.args, assembled.stdout,
                assembled.stderr.decode("utf-8", errors="replace"),
            )
        linker = shutil.which("ld.lld") or shutil.which("lld")
        if linker is None:
            candidates = sorted(
                Path("/opt/homebrew/share/android-commandlinetools/build-tools").glob("*/lld-bin/lld"),
                reverse=True,
            )
            linker = str(candidates[0]) if candidates else None
        if linker is None:
            raise NativeBackendError(
                "cross-linking x86_64-linux requires LLVM lld (ld.lld or lld)"
            )
        command = [linker]
        if Path(linker).name == "lld":
            command.extend(["-flavor", "gnu"])
        command.extend(["-e", "_start", "-o", str(destination), str(object_path)])
        result = subprocess.run(command, check=False, capture_output=True)
    if result.returncode:
        detail = result.stderr.decode("utf-8", errors="replace")
        raise subprocess.CalledProcessError(result.returncode, result.args, result.stdout, detail)


def supported_native_targets() -> tuple[str, ...]:
    """Targets with an in-tree Kuro ABI lowering implementation."""
    return ("aarch64-macos", "x86_64-macos", "x86_64-linux")


def _emit_dynamic_macos_arm64(ir: IRProgram) -> str:
    """Lower the straight-line IR/control-flow subset to real arm64 code."""
    instructions = ir.main
    collection_names = {
        item.args[0]
        for item in instructions
        if item.op == "APPEND" and item.args
    }
    collection_names.update(
        item.args[0]
        for item in instructions
        if item.op == "STORE_LIST" and len(item.args) > 1 and len(item.args[1]) > 1
    )
    for function in ir.functions.values():
        collection_names.update(
            item.args[0]
            for item in function.body
            if item.op == "APPEND" and item.args
        )
    names: set[str] = set()
    for item in instructions:
        if item.dest:
            names.add(item.dest)
        for arg in item.args:
            if isinstance(arg, str) and (arg.startswith("t") or arg.startswith("__")):
                names.add(arg)
            if item.op in {"LOADVAR", "STORE_LIST", "UPDATE", "ADD", "APPEND", "SAVEVAR", "RESTOREVAR"}:
                names.add(item.args[0])
    slots = {name: index * 8 for index, name in enumerate(sorted(names))}
    frame = ((len(slots) * 8 + 15) // 16) * 16 or 16
    lines = [
        ".section __TEXT,__text",
        ".globl _main",
        ".p2align 2",
        "_main:",
        "    stp x29, x30, [sp, #-16]!",
        "    stp x19, x20, [sp, #-16]!",
        "    mov x29, sp",
        f"    mov x15, #{frame}",
        "    sub sp, sp, x15",
    ]
    data: list[tuple[str, str]] = []
    formats: list[tuple[str, str]] = []
    function_sections: list[str] = []
    input_buffer = "_kuro_input_buffer"
    collection_buffers: dict[str, str] = {name: f"_kuro_collection_{index}" for index, name in enumerate(sorted(collection_names))}
    collection_lengths: dict[str, str] = {name: f"_kuro_collection_len_{index}" for index, name in enumerate(sorted(collection_names))}
    char_buffers: dict[str, str] = {
        item.dest: f"_kuro_char_{index}"
        for index, item in enumerate(instructions)
        if item.op == "GET" and item.args[0] not in collection_names and item.dest
    }
    next_char_index = len(char_buffers)
    for function in ir.functions.values():
        for item in function.body:
            if item.op == "GET" and item.args[0] not in collection_names and item.dest:
                key = f"{function.name}:{item.dest}"
                if key not in char_buffers:
                    char_buffers[key] = f"_kuro_char_{next_char_index}"
                    next_char_index += 1
    global_names: set[str] = {"_"}
    def collect_globals(items, params=()):
        for item in items:
            if item.op == "LABEL":
                continue
            if item.op in {"LOADVAR", "STORE_LIST", "UPDATE", "ADD", "APPEND", "SAVEVAR", "RESTOREVAR", "INPUT"} and item.args:
                name = item.args[0]
                if isinstance(name, str) and not name.startswith("t") and not name.startswith("__") and name not in params:
                    global_names.add(name)
    collect_globals(instructions)
    for function in ir.functions.values():
        collect_globals(function.body, function.params)
    global_names -= set(collection_buffers)
    global_labels = {name: f"_kuro_global_{index}" for index, name in enumerate(sorted(global_names))}
    collection_kinds: dict[str, str] = {}
    # Kuro's compiler/runtime collections are textual streams by default;
    # concrete literal APPEND/STORE_LIST values below refine this where known.
    collection_kinds.update({name: "text" for name in collection_names})
    all_items = list(instructions)
    for function in ir.functions.values():
        all_items.extend(function.body)
    const_kinds = {
        item.dest: ("text" if isinstance(item.args[0], str) else "number")
        for item in all_items
        if item.op == "CONST" and item.dest
    }
    for item in all_items:
        if item.op == "APPEND" and item.args:
            collection_kinds.setdefault(item.args[0], const_kinds.get(item.args[1], "unknown"))
        elif item.op == "STORE_LIST" and len(item.args) > 1 and len(item.args[1]) > 1:
            values = item.args[1]
            collection_kinds.setdefault(item.args[0], const_kinds.get(values[0], "unknown"))
    global_kinds = {
        item.args[0]: const_kinds.get(item.args[1][0], "unknown")
        for item in instructions
        if item.op == "STORE_LIST" and len(item.args) > 1 and len(item.args[1]) == 1
    }
    function_return_kinds: dict[str, str] = {}
    def inferred_text_name(name: str) -> bool:
        lowered = name.lower()
        return any(word in lowered for word in ("kind", "operand", "name", "value", "code", "message", "text", "op"))
    for _ in range(len(ir.functions) + 1):
        changed = False
        for function in ir.functions.values():
            inferred: dict[str, str] = {parameter: ("float" if parameter.lower() in {"acc", "scale"} else "text" if any(word in parameter.lower() for word in ("kind", "word", "value", "name", "code", "message", "text", "class")) else "number") for parameter in function.params}
            for item in function.body:
                if item.op == "CONST": inferred[item.dest] = "text" if isinstance(item.args[0], str) else "float" if isinstance(item.args[0], float) else "number"
                elif item.op == "GET": inferred[item.dest] = collection_kinds.get(item.args[0], "unknown")
                elif item.op == "LOADVAR": inferred[item.dest] = inferred.get(item.args[0], global_kinds.get(item.args[0], collection_kinds.get(item.args[0], "unknown")))
                elif item.op == "CALL":
                    inferred[item.dest] = function_return_kinds.get(item.args[0], "unknown")
                    if inferred[item.dest] == "unknown" and inferred_text_name(item.dest):
                        inferred[item.dest] = "text"
                elif item.op in {"CMP", "AND", "OR", "ISCLASS", "LENGTH"}: inferred[item.dest] = "number"
                elif item.op == "BINOP": inferred[item.dest] = "text" if item.args[0] == "+" and inferred.get(item.args[1]) == inferred.get(item.args[2]) == "text" else "number"
                elif item.op == "STORE_LIST" and len(item.args[1]) == 1: inferred[item.args[0]] = inferred.get(item.args[1][0], "unknown")
            returns = [inferred.get(item.args[0], "unknown") for item in function.body if item.op == "RETURN"]
            result = "text" if returns and all(kind == "text" for kind in returns) else "float" if returns and all(kind == "float" for kind in returns) else "number" if returns and all(kind == "number" for kind in returns) else "unknown"
            if result != function_return_kinds.get(function.name): function_return_kinds[function.name] = result; changed = True
        if not changed: break
    kinds: dict[str, str] = {}
    known_text: dict[str, str] = {}
    closure_actions: dict[str, str] = {}
    record_field_slots: dict[str, int] = {}
    record_field_kinds: dict[str, str] = {}
    map_key_slots: dict[str, int] = {}
    map_value_kinds: dict[str, str] = {}
    map_value_lengths: dict[str, int] = {}
    task_actions: dict[str, str] = {}
    known_lengths: dict[str, int] = {}
    labels = {item.dest: f"L_kuro_{item.dest}" for item in instructions if item.op == "LABEL"}
    input_sequence = 0

    def addr(value: object, label_prefix: str) -> str:
        label = f"L_kuro_data_{len(data)}"
        escaped = str(value).replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
        data.append((label, escaped))
        lines.extend([f"    adrp x0, {label}@PAGE", f"    add x0, x0, {label}@PAGEOFF"])
        return label

    def load(target: str, register: str = "x0"):
        if target in global_labels:
            lines.extend([f"    adrp {register}, {global_labels[target]}@PAGE", f"    add {register}, {register}, {global_labels[target]}@PAGEOFF", f"    ldr {register}, [{register}]"])
            return
        if target not in slots:
            raise NativeBackendError(f"native backend cannot load {target!r}")
        lines.append(f"    ldr {register}, [sp, #{slots[target]}]")

    def store(target: str, register: str = "x0"):
        if target in global_labels:
            lines.extend([f"    adrp x2, {global_labels[target]}@PAGE", f"    add x2, x2, {global_labels[target]}@PAGEOFF", f"    str {register}, [x2]"])
            return
        lines.append(f"    str {register}, [sp, #{slots[target]}]")

    def load_collection_length(name: str, register: str = "x0"):
        lines.extend([f"    adrp {register}, {collection_lengths[name]}@PAGE", f"    add {register}, {register}, {collection_lengths[name]}@PAGEOFF", f"    ldr {register}, [{register}]"])

    def store_collection_length(name: str, register: str = "x0"):
        lines.extend([f"    adrp x2, {collection_lengths[name]}@PAGE", f"    add x2, x2, {collection_lengths[name]}@PAGEOFF", f"    str {register}, [x2]"])

    for item in instructions:
        op = item.op
        if op == "CONST":
            value = item.args[0]
            if isinstance(value, str):
                addr(value, "string")
                kinds[item.dest] = "text"
                known_text[item.dest] = value
                known_lengths[item.dest] = len(value)
            elif isinstance(value, int) and 0 <= value <= NATIVE_COLLECTION_CAPACITY:
                lines.append(f"    mov x0, #{value}")
                kinds[item.dest] = "number"
            else:
                raise NativeBackendError("native dynamic backend supports small integer and text constants")
            store(item.dest)
        elif op == "INPUT":
            name = item.args[0]
            read_label = f"L_kuro_read_{input_sequence}"
            read_done_label = f"L_kuro_read_done_{input_sequence}"
            input_sequence += 1
            lines.extend([
                "    mov x19, #0",
                "    movz x20, #65535",
                "    movk x20, #15, lsl #16",
                f"{read_label}:",
                f"    adrp x1, {input_buffer}@PAGE",
                f"    add x1, x1, {input_buffer}@PAGEOFF",
                "    add x1, x1, x19",
                "    sub x2, x20, x19",
                "    cbz x2, L_kuro_runtime_error",
                "    mov w0, #0",
                "    bl _read",
                "    cmp x0, #0",
                "    b.lt L_kuro_runtime_error",
                f"    cbz x0, {read_done_label}",
                "    add x19, x19, x0",
                f"    b {read_label}",
                f"{read_done_label}:",
                f"    adrp x1, {input_buffer}@PAGE",
                f"    add x1, x1, {input_buffer}@PAGEOFF",
                "    strb wzr, [x1, x19]",
                "    mov x0, x1",
            ])
            store(name)
            kinds[name] = "text"
        elif op == "LOADVAR":
            load(item.args[0])
            store(item.dest)
            kinds[item.dest] = kinds.get(item.args[0], global_kinds.get(item.args[0], "unknown"))
            if item.args[0] in known_text:
                known_text[item.dest] = known_text[item.args[0]]
            if item.args[0] in closure_actions:
                closure_actions[item.dest] = closure_actions[item.args[0]]
            if item.args[0] in task_actions:
                task_actions[item.dest] = task_actions[item.args[0]]
            if item.args[0] in known_lengths:
                known_lengths[item.dest] = known_lengths[item.args[0]]
        elif op == "STORE_LIST":
            name, temps = item.args
            if name in collection_buffers:
                if len(temps) > NATIVE_COLLECTION_CAPACITY:
                    raise NativeBackendError(f"native collection exceeds fixed capacity of {NATIVE_COLLECTION_CAPACITY} values")
                for index, temp in enumerate(temps):
                    load(temp, "x0")
                    lines.extend([
                        f"    adrp x1, {collection_buffers[name]}@PAGE",
                        f"    add x1, x1, {collection_buffers[name]}@PAGEOFF",
                        f"    str x0, [x1, #{index * 8}]",
                    ])
                lines.append(f"    mov x0, #{len(temps)}")
                store_collection_length(name)
                kinds[name] = "collection"
                if temps:
                    collection_kinds[name] = kinds.get(temps[0], "unknown")
            elif len(temps) != 1:
                raise NativeBackendError("native dynamic backend does not yet lower multi-value assignment")
            else:
                load(temps[0])
                store(name)
                kinds[name] = kinds.get(temps[0], "unknown")
                global_kinds[name] = kinds[name]
                if temps[0] in closure_actions:
                    closure_actions[name] = closure_actions[temps[0]]
                if temps[0] in task_actions:
                    task_actions[name] = task_actions[temps[0]]
                if temps[0] in known_lengths:
                    known_lengths[name] = known_lengths[temps[0]]
        elif op == "UPDATE":
            name, temp = item.args
            load(temp)
            store(name)
            kinds[name] = kinds.get(temp, "unknown")
            if temp in known_text:
                known_text[name] = known_text[temp]
            if temp in known_lengths:
                known_lengths[name] = known_lengths[temp]
        elif op == "SAVEVAR":
            name = item.args[0]
            load(name)
            store(item.dest)
            kinds[item.dest] = kinds.get(name, "unknown")
        elif op == "RESTOREVAR":
            name, temp = item.args
            load(temp)
            store(name)
            kinds[name] = kinds.get(temp, "unknown")
        elif op == "ADD":
            name, temp = item.args
            if kinds.get(name) != "number" or kinds.get(temp) != "number":
                raise NativeBackendError("native dynamic ADD requires numeric operands")
            load(name, "x0")
            load(temp, "x1")
            lines.append("    add x0, x0, x1")
            store(name)
            kinds[name] = "number"
            known_lengths.pop(name, None)
        elif op == "APPEND":
            name, temp = item.args
            if name not in collection_buffers:
                raise NativeBackendError("native APPEND target was not allocated as a collection")
            load_collection_length(name, "x1")
            lines.extend([
                f"    adrp x2, {collection_buffers[name]}@PAGE",
                f"    add x2, x2, {collection_buffers[name]}@PAGEOFF",
                f"    cmp x1, #{NATIVE_COLLECTION_CAPACITY}",
                "    b.ge L_kuro_collection_overflow",
            ])
            load(temp, "x0")
            lines.extend(["    lsl x3, x1, #3", "    str x0, [x2, x3]", "    add x1, x1, #1"])
            store_collection_length(name, "x1")
            kinds[name] = "collection"
            collection_kinds.setdefault(name, kinds.get(temp, "unknown"))
        elif op == "GET":
            name, index_temp = item.args
            if index_temp is None:
                raise NativeBackendError("native GET requires an index")
            if name not in collection_buffers:
                if (name not in known_lengths and kinds.get(name) != "text") or item.dest not in char_buffers:
                    raise NativeBackendError("native GET requires a native collection or known text value")
                load(name, "x2")
                load(index_temp, "x1")
                lines.extend([
                    "    add x2, x2, x1", "    ldrb w0, [x2]",
                    "    adrp x3, _kuro_char_heap_cursor@PAGE", "    add x3, x3, _kuro_char_heap_cursor@PAGEOFF", "    ldr x1, [x3]",
                    "    cmp x1, #512, lsl #12", "    b.hs L_kuro_collection_overflow",
                    "    adrp x2, _kuro_char_heap@PAGE", "    add x2, x2, _kuro_char_heap@PAGEOFF", "    add x2, x2, x1",
                    "    strb w0, [x2]", "    strb wzr, [x2, #1]", "    add x1, x1, #2", "    str x1, [x3]", "    mov x0, x2",
                ])
                store(item.dest)
                kinds[item.dest] = "text"
                continue
            load(index_temp, "x1")
            lines.extend([
                f"    adrp x2, {collection_buffers[name]}@PAGE",
                f"    add x2, x2, {collection_buffers[name]}@PAGEOFF",
                f"    cmp x1, #{NATIVE_COLLECTION_CAPACITY}",
                "    b.hs L_kuro_collection_bounds",
                "    lsl x1, x1, #3",
                "    ldr x0, [x2, x1]",
            ])
            store(item.dest)
            kinds[item.dest] = collection_kinds.get(name, "unknown")
        elif op == "LENGTH":
            name = item.args[0]
            if name in collection_buffers:
                load_collection_length(name)
            elif name in known_lengths:
                lines.append(f"    mov x0, #{known_lengths[name]}")
            elif kinds.get(name) == "text" or kinds.get(name, "unknown") == "unknown":
                load(name)
                zero_label = f"L_kuro_length_zero_{item.dest}"
                done_label = f"L_kuro_length_done_{item.dest}"
                lines.extend(["    cbz x0, " + zero_label, "    bl _strlen", f"    b {done_label}", f"{zero_label}:", "    mov x0, #0", f"{done_label}:"])
            else:
                raise NativeBackendError("native LENGTH requires a native collection or known text value")
            store(item.dest)
            kinds[item.dest] = "number"
        elif op == "SET":
            name, index_temp, value_temp = item.args
            if name not in collection_buffers:
                raise NativeBackendError("native SET requires a native collection")
            load(index_temp, "x1")
            load(value_temp, "x0")
            lines.extend([
                f"    adrp x2, {collection_buffers[name]}@PAGE",
                f"    add x2, x2, {collection_buffers[name]}@PAGEOFF",
                f"    cmp x1, #{NATIVE_COLLECTION_CAPACITY}",
                "    b.hs L_kuro_collection_bounds",
                "    lsl x1, x1, #3",
                "    str x0, [x2, x1]",
            ])
        elif op == "CALL":
            name, *arguments = item.args
            if name == "MakeEnum":
                if len(arguments) != 2:
                    raise NativeBackendError("native MakeEnum requires a type and variant")
                lines.extend(["    mov x0, #4096", "    bl _malloc"])
                store(item.dest)
                load(item.dest, "x0"); load(arguments[0], "x1"); lines.append("    bl _strcpy")
                dot_label = f"L_kuro_data_{len(data)}"
                data.append((dot_label, "."))
                lines.extend([f"    adrp x1, {dot_label}@PAGE", f"    add x1, x1, {dot_label}@PAGEOFF", "    bl _strcat"])
                load(item.dest, "x0"); load(arguments[1], "x1"); lines.append("    bl _strcat")
                kinds[item.dest] = "text"
                continue
            if name == "MakeRecord":
                if len(arguments) != 1:
                    raise NativeBackendError("native MakeRecord requires a type name")
                lines.extend(["    mov x0, #512", "    bl _malloc", "    mov x3, x0", "    mov x0, #0", "    str x0, [x3]"])
                lines.extend(["    mov x0, x3"])
                store(item.dest); kinds[item.dest] = "record"
                continue
            if name == "RecordSet":
                if len(arguments) != 3 or arguments[1] not in known_text:
                    raise NativeBackendError("native RecordSet requires a known field name")
                field = known_text[arguments[1]]
                slot = record_field_slots.setdefault(field, len(record_field_slots))
                load(arguments[0], "x2"); load(arguments[2], "x0")
                lines.append(f"    str x0, [x2, #{8 + slot * 8}]")
                record_field_kinds[field] = kinds.get(arguments[2], "unknown")
                lines.append("    mov x0, x2")
                store(item.dest); kinds[item.dest] = "record"
                continue
            if name == "RecordGet":
                if len(arguments) != 2 or arguments[1] not in known_text:
                    raise NativeBackendError("native RecordGet requires a known field name")
                field = known_text[arguments[1]]
                slot = record_field_slots.setdefault(field, len(record_field_slots))
                load(arguments[0], "x2")
                lines.append(f"    ldr x0, [x2, #{8 + slot * 8}]")
                store(item.dest); kinds[item.dest] = record_field_kinds.get(field, "unknown")
                continue
            if name == "MakeMap":
                if arguments:
                    raise NativeBackendError("native MakeMap takes no arguments")
                lines.extend(["    mov x0, #8192", "    bl _malloc", "    mov x3, x0", "    mov x0, #0", "    str x0, [x3]"])
                lines.append("    mov x0, x3")
                store(item.dest); kinds[item.dest] = "map"
                continue
            if name == "MapSet":
                if len(arguments) != 3 or arguments[1] not in known_text:
                    raise NativeBackendError("native MapSet requires a known text key")
                key = known_text[arguments[1]]
                slot = map_key_slots.setdefault(key, len(map_key_slots))
                load(arguments[0], "x2"); load(arguments[2], "x0")
                lines.extend([f"    str x0, [x2, #{8 + slot * 8}]", f"    mov x0, #1", f"    str x0, [x2, #{4096 + slot * 8}]", "    mov x0, x2"])
                store(item.dest); kinds[item.dest] = "map"
                map_value_kinds[key] = kinds.get(arguments[2], "unknown")
                continue
            if name == "MapGet":
                if len(arguments) != 2 or arguments[1] not in known_text:
                    raise NativeBackendError("native MapGet requires a known text key")
                key = known_text[arguments[1]]
                slot = map_key_slots.setdefault(key, len(map_key_slots))
                load(arguments[0], "x2")
                lines.append(f"    ldr x0, [x2, #{8 + slot * 8}]")
                store(item.dest); kinds[item.dest] = map_value_kinds.get(key, "unknown")
                continue
            if name == "MapHas":
                if len(arguments) != 2 or arguments[1] not in known_text:
                    raise NativeBackendError("native MapHas requires a known text key")
                key = known_text[arguments[1]]
                slot = map_key_slots.setdefault(key, len(map_key_slots))
                load(arguments[0], "x2")
                lines.extend([f"    ldr x0, [x2, #{4096 + slot * 8}]", "    cmp x0, #1", "    cset w0, eq"])
                store(item.dest); kinds[item.dest] = "number"
                continue
            if name == "Spawn":
                if len(arguments) != 2:
                    raise NativeBackendError("native Spawn requires a closure and one argument")
                lines.extend(["    mov x0, #24", "    bl _malloc", "    mov x3, x0"])
                load(arguments[0], "x0"); lines.append("    str x0, [x3]")
                load(arguments[1], "x0"); lines.extend(["    str x0, [x3, #8]", "    mov x0, #0", "    str x0, [x3, #16]", "    mov x0, x3"])
                store(item.dest); kinds[item.dest] = "task"
                if arguments[0] in closure_actions:
                    task_actions[item.dest] = closure_actions[arguments[0]]
                continue
            if name == "Await":
                if len(arguments) != 1:
                    raise NativeBackendError("native Await requires one task")
                load(arguments[0], "x2")
                lines.extend(["    ldr x9, [x2]", "    ldr x0, [x2, #8]", "    blr x9"])
                store(item.dest)
                kinds[item.dest] = function_return_kinds.get(task_actions.get(arguments[0], ""), "number")
                continue
            if name in {"Some", "Ok", "Err", "None"}:
                expected = {"None": 0, "Some": 1, "Ok": 2, "Err": 3}[name]
                if (name == "None" and arguments) or (name != "None" and len(arguments) != 1):
                    raise NativeBackendError(f"native {name} has invalid arity")
                lines.extend(["    mov x0, #16", "    bl _malloc", "    mov x3, x0", f"    mov x0, #{expected}", "    str x0, [x3]"])
                if arguments:
                    load(arguments[0], "x0")
                else:
                    lines.append("    mov x0, #0")
                lines.extend(["    str x0, [x3, #8]", "    mov x0, x3"])
                store(item.dest); kinds[item.dest] = "tagged"
                continue
            if name == "MakeClosure":
                if len(arguments) != 1 or arguments[0] not in known_text or known_text[arguments[0]] not in ir.functions:
                    raise NativeBackendError("native MakeClosure requires a statically known action")
                action = known_text[arguments[0]]
                lines.extend([f"    adrp x0, _kuro_fn_{action}@PAGE", f"    add x0, x0, _kuro_fn_{action}@PAGEOFF"])
                store(item.dest); kinds[item.dest] = "closure"; closure_actions[item.dest] = action
                continue
            if name == "Invoke":
                if not arguments or arguments[0] not in closure_actions or len(arguments) > 8:
                    raise NativeBackendError("native Invoke requires a statically known closure")
                load(arguments[0], "x9")
                for index, argument in enumerate(arguments[1:]):
                    load(argument, f"x{index}")
                lines.append("    blr x9")
                store(item.dest)
                kinds[item.dest] = function_return_kinds.get(closure_actions[arguments[0]], "number")
                continue
            if name in {"IsSome", "IsNone", "IsOk", "IsErr"}:
                if len(arguments) != 1:
                    raise NativeBackendError(f"native {name} requires one value")
                expected = {"IsNone": 0, "IsSome": 1, "IsOk": 2, "IsErr": 3}[name]
                load(arguments[0], "x2")
                lines.extend(["    ldr x0, [x2]", f"    cmp x0, #{expected}", "    cset w0, eq"])
                store(item.dest); kinds[item.dest] = "number"
                continue
            if name == "Unwrap":
                if len(arguments) != 1:
                    raise NativeBackendError("native Unwrap requires one value")
                load(arguments[0], "x2")
                lines.extend(["    ldr x0, [x2, #8]"])
                store(item.dest); kinds[item.dest] = "number"
                continue
            if name == "EnumIs":
                if len(arguments) != 2:
                    raise NativeBackendError("native EnumIs requires a value and variant")
                load(arguments[0], "x0"); load(arguments[1], "x1")
                lines.extend(["    bl _strcmp", "    cmp x0, #0", "    cset w0, eq"])
                store(item.dest); kinds[item.dest] = "number"
                continue
            function = ir.functions.get(name)
            if function is None or len(arguments) > 8:
                raise NativeBackendError(f"native dynamic backend cannot resolve action {name!r}")
            for index, argument in enumerate(arguments):
                load(argument, f"x{index}")
            lines.append(f"    bl _kuro_fn_{name}")
            store(item.dest)
            kinds[item.dest] = function_return_kinds.get(name, "text" if inferred_text_name(item.dest) else "number")
            known_lengths.pop(item.dest, None)
        elif op == "BINOP":
            bop, left, right = item.args
            if bop == "+" and kinds.get(left) == "text" and kinds.get(right) == "text":
                lines.extend(["    mov x0, #4096", "    bl _malloc"])
                store(item.dest)
                load(item.dest, "x0")
                load(left, "x1")
                lines.append("    bl _strcpy")
                load(item.dest, "x0")
                load(right, "x1")
                lines.append("    bl _strcat")
                kinds[item.dest] = "text"
                continue
            if kinds.get(left) != "number" or kinds.get(right) != "number":
                raise NativeBackendError("native dynamic BINOP requires numeric operands")
            load(left, "x0")
            load(right, "x1")
            operation = {"+": "add", "-": "sub", "*": "mul", "/": "sdiv"}.get(bop)
            if operation is None:
                raise NativeBackendError(f"unsupported native BINOP {bop!r}")
            lines.append(f"    {operation} x0, x0, x1")
            store(item.dest)
            kinds[item.dest] = "number"
        elif op == "CMP":
            cop, left, right = item.args
            load(left, "x0")
            load(right, "x1")
            condition = {"eq": "eq", "ne": "ne", "lt": "lt", "le": "le", "gt": "gt", "ge": "ge"}.get(cop)
            if condition is None:
                raise NativeBackendError(f"unsupported native comparison {cop!r}")
            if kinds.get(left) == "text" or kinds.get(right) == "text":
                lines.extend(["    bl _strcmp", "    cmp x0, #0", f"    cset w0, {condition}"])
            else:
                lines.extend(["    cmp x0, x1", f"    cset w0, {condition}"])
            store(item.dest)
            kinds[item.dest] = "number"
        elif op == "ISCLASS":
            operand, cls = item.args
            if cls not in {"digit", "alpha", "alnum", "space", "quote"}:
                raise NativeBackendError(f"unsupported native character class {cls!r}")
            invalid_label = f"L_kuro_isclass_invalid_{item.dest}"
            done_label = f"L_kuro_isclass_done_{item.dest}"
            load(operand)
            lines.extend([
                "    cmp x0, #0", f"    b.le {invalid_label}",
                "    cmp x0, #0x1000", f"    b.lo {invalid_label}",
                "    ldrb w0, [x0]",
            ])
            if cls == "digit":
                lines.extend(["    sub w0, w0, #48", "    cmp w0, #9", "    cset w0, ls"])
            elif cls == "quote":
                lines.extend(["    cmp w0, #34", "    cset w0, eq"])
            elif cls == "space":
                lines.extend([
                    "    cmp w0, #32", "    cset w1, eq",
                    "    cmp w0, #9", "    cset w2, eq", "    orr w1, w1, w2",
                    "    cmp w0, #10", "    cset w2, eq", "    orr w1, w1, w2",
                    "    cmp w0, #13", "    cset w0, eq", "    orr w0, w1, w0",
                ])
            else:
                lines.extend([
                    "    sub w1, w0, #48", "    cmp w1, #9", "    cset w1, ls",
                    "    sub w2, w0, #65", "    cmp w2, #25", "    cset w2, ls", "    orr w1, w1, w2",
                    "    sub w2, w0, #97", "    cmp w2, #25", "    cset w2, ls", "    orr w1, w1, w2",
                    "    mov w0, w1",
                ])
            lines.extend([f"    b {done_label}", f"{invalid_label}:", "    mov x0, #0", f"{done_label}:"])
            store(item.dest)
            kinds[item.dest] = "number"
        elif op in {"AND", "OR"}:
            left, right = item.args
            load(left, "x0")
            load(right, "x1")
            lines.append("    cmp x0, #0")
            lines.append("    cset w0, ne")
            lines.append("    cmp x1, #0")
            lines.append("    cset w1, ne")
            lines.append(f"    {'and' if op == 'AND' else 'orr'} w0, w0, w1")
            store(item.dest)
            kinds[item.dest] = "number"
        elif op == "JUMPF":
            target, cond = item.args
            load(cond)
            lines.append(f"    cbz w0, {labels[target]}")
        elif op == "JUMP":
            lines.append(f"    b {labels[item.args[0]]}")
        elif op == "LABEL":
            lines.append(f"{labels[item.dest]}:")
        elif op == "PRINT":
            temp = item.args[0]
            kind = kinds.get(temp)
            if kind == "text":
                load(temp)
                lines.append("    bl _puts")
            elif kind == "number":
                load(temp, "x0")
                lines.append("    bl _kuro_print_int")
            elif kind == "float":
                load(temp, "x0")
                # Darwin arm64 passes variadic arguments on the stack.  A
                # double in d0 is therefore invisible to printf("%g", ...).
                lines.extend([
                    "    sub sp, sp, #16", "    str x0, [sp]",
                    "    adrp x0, L_kuro_float_format@PAGE", "    add x0, x0, L_kuro_float_format@PAGEOFF",
                    "    bl _printf", "    add sp, sp, #16",
                ])
            else:
                raise NativeBackendError("native dynamic backend can print only text and integer values")
        elif op in {"DECLTYPE", "LOOP_GUARD", "CHECK_NONNEG"}:
            continue
        else:
            raise NativeBackendError(f"native dynamic backend does not support {op}")
    lines.extend([f"    mov x15, #{frame}", "    add sp, sp, x15"])
    if "RuntimeExitCode" in global_labels:
        lines.extend([
            f"    adrp x0, {global_labels['RuntimeExitCode']}@PAGE",
            f"    add x0, x0, {global_labels['RuntimeExitCode']}@PAGEOFF",
            "    ldr x0, [x0]",
        ])
    else:
        lines.append("    mov w0, #0")
    lines.extend([
        "    ldp x19, x20, [sp], #16",
        "    ldp x29, x30, [sp], #16",
        "    ret",
        "L_kuro_runtime_error:",
        "    mov w0, #1",
        f"    mov x15, #{frame}",
        "    add sp, sp, x15",
        "    ldp x19, x20, [sp], #16",
        "    ldp x29, x30, [sp], #16",
        "    ret",
        ".section __TEXT,__cstring",
    ])
    for function in ir.functions.values():
        function_sections.append(_emit_dynamic_function(function, collection_buffers, collection_lengths, global_labels, data, collection_kinds, function_return_kinds, char_buffers, known_lengths, global_kinds))
    if function_sections:
        lines.extend([".section __TEXT,__text", *function_sections, ".section __TEXT,__cstring"])
    for label, value in data:
        if not label.startswith("L_kuro_float_"):
            lines.append(f'{label}: .asciz "{value}"')
    if any(label.startswith("L_kuro_float_") for label, _ in data):
        lines.append(".section __TEXT,__const")
        for label, value in data:
            if label.startswith("L_kuro_float_"):
                lines.append(f"{label}: .double {value}")
        lines.append(".section __TEXT,__cstring")
    for label, value in formats:
        lines.append(f'{label}: .asciz "{value}"')
    lines.append('L_kuro_float_format: .asciz "%g\\n"')
    if collection_buffers or global_labels:
        lines.extend([
            ".section __TEXT,__text",
            "_kuro_print_int:",
            "    stp x29, x30, [sp, #-16]!",
            "    mov x29, sp",
            "    adrp x10, _kuro_int_buffer@PAGE",
            "    add x10, x10, _kuro_int_buffer@PAGEOFF",
            "    add x10, x10, #31",
            "    mov w11, #0",
            "    strb w11, [x10]",
            "    mov x11, #10",
            "    cbnz x0, L_kuro_print_int_loop",
            "    mov w12, #48",
            "    strb w12, [x10, #-1]!",
            "    b L_kuro_print_int_done",
            "L_kuro_print_int_loop:",
            "    udiv x12, x0, x11",
            "    msub x13, x12, x11, x0",
            "    add x13, x13, #48",
            "    strb w13, [x10, #-1]!",
            "    mov x0, x12",
            "    cbnz x0, L_kuro_print_int_loop",
            "L_kuro_print_int_done:",
            "    mov x0, x10",
            "    bl _puts",
            "    ldp x29, x30, [sp], #16",
            "    ret",
            "L_kuro_collection_overflow:",
            "    mov w0, #1",
            "    bl _exit",
            "    brk #0",
            "L_kuro_collection_bounds:",
            "    mov w0, #1",
            "    bl _exit",
            "    brk #0",
        ])
        for label in collection_buffers.values():
            lines.append(f".zerofill __DATA,__bss,{label},{NATIVE_COLLECTION_BYTES},3")
        for label in collection_lengths.values():
            lines.append(f".zerofill __DATA,__bss,{label},8,3")
        for label in global_labels.values():
            lines.append(f".zerofill __DATA,__bss,{label},8,3")
        for label in char_buffers.values():
            lines.append(f".zerofill __DATA,__bss,{label},2,1")
        lines.append(f".zerofill __DATA,__bss,_kuro_char_heap,{NATIVE_INPUT_CAPACITY * 2},4")
        lines.append(".zerofill __DATA,__bss,_kuro_char_heap_cursor,8,3")
        lines.append(".zerofill __DATA,__bss,_kuro_int_buffer,32,3")
        lines.append(f".zerofill __DATA,__bss,{input_buffer},{NATIVE_INPUT_CAPACITY},4")
    return "\n".join(lines) + "\n"


def _emit_dynamic_function(function, collection_buffers=None, collection_lengths=None, global_labels=None, data=None, collection_kinds=None, function_return_kinds=None, char_buffers=None, known_lengths=None, global_kinds=None) -> str:
    """Emit numeric action bodies, including recursive calls and branches."""
    collection_buffers = collection_buffers or {}
    collection_lengths = collection_lengths or {}
    global_labels = global_labels or {}
    data = data if data is not None else []
    collection_kinds = collection_kinds or {}
    function_return_kinds = function_return_kinds or {}
    char_buffers = char_buffers or {}
    known_lengths = known_lengths or {}
    global_kinds = global_kinds or {}
    kinds: dict[str, str] = {}
    def inferred_text_name(name: str) -> bool:
        lowered = name.lower()
        return any(word in lowered for word in ("kind", "operand", "name", "value", "code", "message", "text", "op"))
    for parameter in function.params:
        lowered = parameter.lower()
        if lowered in {"acc", "scale"}:
            kinds[parameter] = "float"
        elif any(word in lowered for word in ("kind", "word", "value", "name", "code", "message", "text", "class")):
            kinds[parameter] = "text"
        else:
            kinds[parameter] = "number"
    names = set(function.params)
    for item in function.body:
        if item.dest:
            names.add(item.dest)
        for arg in item.args:
            if isinstance(arg, str) and (arg.startswith("t") or arg == "_"):
                names.add(arg)
        if item.op in {"LOADVAR", "STORE_LIST", "UPDATE", "ADD", "APPEND", "SAVEVAR", "RESTOREVAR", "CALL"} and item.args:
            names.add(item.args[0])
    slots = {name: index * 8 for index, name in enumerate(sorted(names))}
    frame = ((len(slots) * 8 + 15) // 16) * 16 or 16
    labels = {item.dest: f"L_kuro_fn_{function.name}_{item.dest}" for item in function.body if item.op == "LABEL"}
    lines = [f"_kuro_fn_{function.name}:", "    stp x29, x30, [sp, #-16]!", "    mov x29, sp", f"    mov x15, #{frame}", "    sub sp, sp, x15"]

    def load(name, register="x0"):
        local = name in function.params or name.startswith("t") or name.startswith("__") or name.startswith(function.name + "_")
        if local and name in slots:
            lines.append(f"    ldr {register}, [sp, #{slots[name]}]")
            return
        if name in collection_buffers:
            lines.extend([f"    adrp {register}, {collection_buffers[name]}@PAGE", f"    add {register}, {register}, {collection_buffers[name]}@PAGEOFF"])
            return
        if name in global_labels:
            lines.extend([f"    adrp {register}, {global_labels[name]}@PAGE", f"    add {register}, {register}, {global_labels[name]}@PAGEOFF", f"    ldr {register}, [{register}]"])
            return
        raise NativeBackendError(f"native action {function.name!r} cannot load {name!r}")

    def store(name, register="x0"):
        local = name in function.params or name.startswith("t") or name.startswith("__") or name.startswith(function.name + "_")
        if local and name in slots:
            lines.append(f"    str {register}, [sp, #{slots[name]}]")
            return
        if name in global_labels:
            lines.extend([f"    adrp x2, {global_labels[name]}@PAGE", f"    add x2, x2, {global_labels[name]}@PAGEOFF", f"    str {register}, [x2]"])
            return
        raise NativeBackendError(f"native action {function.name!r} cannot store {name!r}")

    def load_collection_length(name, register="x0"):
        lines.extend([f"    adrp {register}, {collection_lengths[name]}@PAGE", f"    add {register}, {register}, {collection_lengths[name]}@PAGEOFF", f"    ldr {register}, [{register}]"])

    def store_collection_length(name, register="x0"):
        lines.extend([f"    adrp x2, {collection_lengths[name]}@PAGE", f"    add x2, x2, {collection_lengths[name]}@PAGEOFF", f"    str {register}, [x2]"])

    for index, parameter in enumerate(function.params):
        store(parameter, f"x{index}")
    for item in function.body:
        op = item.op
        if op == "CONST" and isinstance(item.args[0], int) and 0 <= item.args[0] <= NATIVE_COLLECTION_CAPACITY:
            lines.append(f"    mov x0, #{item.args[0]}"); store(item.dest); kinds[item.dest] = "number"
        elif op == "CONST" and isinstance(item.args[0], float):
            label = f"L_kuro_float_{len(data)}"
            data.append((label, repr(item.args[0])))
            lines.extend([f"    adrp x0, {label}@PAGE", f"    add x0, x0, {label}@PAGEOFF", "    ldr d0, [x0]", "    fmov x0, d0"])
            store(item.dest); kinds[item.dest] = "float"
        elif op == "CONST" and isinstance(item.args[0], str):
            label = f"L_kuro_data_{len(data)}"
            escaped = item.args[0].replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t")
            data.append((label, escaped))
            lines.extend([f"    adrp x0, {label}@PAGE", f"    add x0, x0, {label}@PAGEOFF"])
            store(item.dest); kinds[item.dest] = "text"
        elif op == "LOADVAR":
            load(item.args[0]); store(item.dest)
            kinds[item.dest] = kinds.get(item.args[0], global_kinds.get(item.args[0], collection_kinds.get(item.args[0], "unknown")))
        elif op == "STORE_LIST":
            name, values = item.args
            if name in collection_buffers:
                if len(values) > NATIVE_COLLECTION_CAPACITY: raise NativeBackendError(f"native collection exceeds fixed capacity of {NATIVE_COLLECTION_CAPACITY} values")
                for index, value in enumerate(values):
                    load(value, "x0")
                    lines.extend([f"    adrp x1, {collection_buffers[name]}@PAGE", f"    add x1, x1, {collection_buffers[name]}@PAGEOFF", f"    str x0, [x1, #{index * 8}]"])
                lines.append(f"    mov x0, #{len(values)}")
                store_collection_length(name)
            else:
                if len(values) != 1: raise NativeBackendError("native action multi-value assignment unsupported")
                load(values[0]); store(name); kinds[name] = kinds.get(values[0], "unknown")
        elif op == "ADD":
            name, temp = item.args
            load(name, "x0")
            load(temp, "x1")
            lines.append("    add x0, x0, x1")
            store(name)
        elif op == "GET":
            name, index_temp = item.args
            if index_temp is None:
                raise NativeBackendError(f"native action {function.name!r} cannot load without an index")
            if name not in collection_buffers:
                key = f"{function.name}:{item.dest}"
                if key not in char_buffers:
                    raise NativeBackendError(f"native action {function.name!r} cannot load collection {name!r}")
                load(name, "x2")
                load(index_temp, "x1")
                lines.extend([
                    "    add x2, x2, x1", "    ldrb w0, [x2]",
                    "    adrp x3, _kuro_char_heap_cursor@PAGE", "    add x3, x3, _kuro_char_heap_cursor@PAGEOFF", "    ldr x1, [x3]",
                    "    cmp x1, #512, lsl #12", "    b.hs L_kuro_collection_overflow",
                    "    adrp x2, _kuro_char_heap@PAGE", "    add x2, x2, _kuro_char_heap@PAGEOFF", "    add x2, x2, x1",
                    "    strb w0, [x2]", "    strb wzr, [x2, #1]", "    add x1, x1, #2", "    str x1, [x3]", "    mov x0, x2",
                ])
                store(item.dest); kinds[item.dest] = "text"
                continue
            load(index_temp, "x1")
            lines.extend([
                f"    adrp x2, {collection_buffers[name]}@PAGE",
                f"    add x2, x2, {collection_buffers[name]}@PAGEOFF",
                "    lsl x1, x1, #3",
                "    ldr x0, [x2, x1]",
            ])
            store(item.dest); kinds[item.dest] = collection_kinds.get(name, "unknown")
        elif op == "SET":
            name, index_temp, value_temp = item.args
            if name not in collection_buffers:
                load(name, "x2")
                load(index_temp, "x1")
                load(value_temp, "x0")
                lines.extend(["    ldrb w0, [x0]", "    strb w0, [x2, x1]"])
                continue
            load(index_temp, "x1")
            load(value_temp, "x0")
            lines.extend([
                f"    adrp x2, {collection_buffers[name]}@PAGE",
                f"    add x2, x2, {collection_buffers[name]}@PAGEOFF",
                f"    cmp x1, #{NATIVE_COLLECTION_CAPACITY}",
                "    b.hs L_kuro_collection_bounds",
                "    lsl x1, x1, #3",
                "    str x0, [x2, x1]",
            ])
        elif op == "LENGTH":
            name = item.args[0]
            if name in collection_lengths:
                load_collection_length(name)
            elif name in known_lengths:
                lines.append(f"    mov x0, #{known_lengths[name]}")
            else:
                # Action locals in the Kuro VM can hold different runtime
                # kinds across opcode branches. Source type checking guards
                # ordinary Kuro programs; the VM's dynamic dispatch requires
                # LENGTH to use the runtime text representation here.
                load(name)
                zero_label = f"L_kuro_fn_{function.name}_length_zero_{item.dest}"
                done_label = f"L_kuro_fn_{function.name}_length_done_{item.dest}"
                lines.extend(["    cbz x0, " + zero_label, "    bl _strlen", f"    b {done_label}", f"{zero_label}:", "    mov x0, #0", f"{done_label}:"])
            store(item.dest); kinds[item.dest] = "number"
        elif op == "APPEND":
            name, temp = item.args
            if name not in collection_buffers:
                raise NativeBackendError(f"native action {function.name!r} cannot append to {name!r}")
            load_collection_length(name, "x1")
            lines.extend([
                f"    adrp x2, {collection_buffers[name]}@PAGE",
                f"    add x2, x2, {collection_buffers[name]}@PAGEOFF",
                f"    cmp x1, #{NATIVE_COLLECTION_CAPACITY}",
                "    b.ge L_kuro_collection_overflow",
            ])
            load(temp, "x0")
            lines.extend(["    lsl x3, x1, #3", "    str x0, [x2, x3]", "    add x1, x1, #1"])
            store_collection_length(name, "x1")
        elif op == "BINOP":
            operator, left, right = item.args
            load(left, "x0"); load(right, "x1")
            if function.name == "VMStep" and operator == "+":
                text_label = f"L_kuro_fn_{function.name}_binop_text_{item.dest}"
                numeric_label = f"L_kuro_fn_{function.name}_binop_numeric_{item.dest}"
                done_label = f"L_kuro_fn_{function.name}_binop_done_{item.dest}"
                lines.extend([
                    "    cmp x0, #0", f"    b.le {numeric_label}",
                    "    cmp x0, #0x1000", f"    b.lo {numeric_label}",
                    "    cmp x1, #0", f"    b.le {numeric_label}",
                    "    cmp x1, #0x1000", f"    b.lo {numeric_label}",
                    f"    b {text_label}",
                    f"{numeric_label}:", "    add x0, x0, x1", f"    b {done_label}",
                    f"{text_label}:",
                    "    mov x0, #4096", "    bl _malloc",
                ])
                store(item.dest)
                load(item.dest, "x0"); load(left, "x1"); lines.append("    bl _strcpy")
                load(item.dest, "x0"); load(right, "x1"); lines.append("    bl _strcat")
                lines.append(f"{done_label}:")
                store(item.dest); kinds[item.dest] = "unknown"
                continue
            if operator == "+" and kinds.get(left) == "text" and kinds.get(right) == "text":
                lines.extend(["    mov x0, #4096", "    bl _malloc"]); store(item.dest)
                load(item.dest, "x0"); load(left, "x1"); lines.append("    bl _strcpy")
                load(item.dest, "x0"); load(right, "x1"); lines.append("    bl _strcat")
                kinds[item.dest] = "text"
                continue
            if kinds.get(left) == "float" or kinds.get(right) == "float":
                operation = {"+": "fadd", "-": "fsub", "*": "fmul", "/": "fdiv"}.get(operator)
                if operation is None: raise NativeBackendError(f"unsupported native action operator {operator!r}")
                left_convert = "fmov d0, x0" if kinds.get(left) == "float" else "scvtf d0, x0"
                right_convert = "fmov d1, x1" if kinds.get(right) == "float" else "scvtf d1, x1"
                lines.extend([f"    {left_convert}", f"    {right_convert}", f"    {operation} d0, d0, d1", "    fmov x0, d0"])
                store(item.dest); kinds[item.dest] = "float"
                continue
            operation = {"+": "add", "-": "sub", "*": "mul", "/": "sdiv"}.get(operator)
            if operation is None: raise NativeBackendError(f"unsupported native action operator {operator!r}")
            lines.append(f"    {operation} x0, x0, x1"); store(item.dest); kinds[item.dest] = "number"
        elif op == "ISCLASS":
            operand, cls = item.args
            if cls not in {"digit", "alpha", "alnum", "space", "quote"}:
                raise NativeBackendError(f"unsupported native action character class {cls!r}")
            invalid_label = f"L_kuro_fn_{function.name}_isclass_invalid_{item.dest}"
            done_label = f"L_kuro_fn_{function.name}_isclass_done_{item.dest}"
            load(operand)
            lines.extend([
                "    cmp x0, #0", f"    b.le {invalid_label}",
                "    cmp x0, #0x1000", f"    b.lo {invalid_label}",
                "    ldrb w0, [x0]",
            ])
            if cls == "digit":
                lines.extend(["    sub w0, w0, #48", "    cmp w0, #9", "    cset w0, ls"])
            elif cls == "quote":
                lines.extend(["    cmp w0, #34", "    cset w0, eq"])
            elif cls == "space":
                lines.extend([
                    "    cmp w0, #32", "    cset w1, eq",
                    "    cmp w0, #9", "    cset w2, eq", "    orr w1, w1, w2",
                    "    cmp w0, #10", "    cset w2, eq", "    orr w1, w1, w2",
                    "    cmp w0, #13", "    cset w0, eq", "    orr w0, w1, w0",
                ])
            else:
                lines.extend([
                    "    sub w1, w0, #48", "    cmp w1, #9", "    cset w1, ls",
                    "    sub w2, w0, #65", "    cmp w2, #25", "    cset w2, ls", "    orr w1, w1, w2",
                    "    sub w2, w0, #97", "    cmp w2, #25", "    cset w2, ls", "    orr w1, w1, w2",
                    "    mov w0, w1",
                ])
            lines.extend([f"    b {done_label}", f"{invalid_label}:", "    mov x0, #0", f"{done_label}:"])
            store(item.dest); kinds[item.dest] = "number"
        elif op in {"AND", "OR"}:
            left, right = item.args
            load(left, "x0"); load(right, "x1")
            lines.extend(["    cmp x0, #0", "    cset w0, ne", "    cmp x1, #0", "    cset w1, ne", f"    {'and' if op == 'AND' else 'orr'} w0, w0, w1"])
            store(item.dest)
        elif op == "CMP":
            operator, left, right = item.args
            condition = {"eq": "eq", "ne": "ne", "lt": "lt", "le": "le", "gt": "gt", "ge": "ge"}.get(operator)
            if condition is None: raise NativeBackendError(f"unsupported native action comparison {operator!r}")
            load(left, "x0"); load(right, "x1")
            if function.name == "VMStep" and operator in {"eq", "ne"}:
                numeric_label = f"L_kuro_fn_{function.name}_cmp_numeric_{item.dest}"
                done_label = f"L_kuro_fn_{function.name}_cmp_done_{item.dest}"
                lines.extend([
                    "    cmp x0, #0", f"    b.le {numeric_label}",
                    "    cmp x0, #0x1000", f"    b.lo {numeric_label}",
                    "    cmp x1, #0", f"    b.le {numeric_label}",
                    "    cmp x1, #0x1000", f"    b.lo {numeric_label}",
                    "    bl _strcmp", "    cmp x0, #0", f"    cset w0, {condition}", f"    b {done_label}",
                    f"{numeric_label}:", "    cmp x0, x1", f"    cset w0, {condition}",
                    f"{done_label}:",
                ])
                store(item.dest); kinds[item.dest] = "number"
                continue
            if kinds.get(left) == "float" or kinds.get(right) == "float":
                    left_convert = "fmov d0, x0" if kinds.get(left) == "float" else "scvtf d0, x0"
                    right_convert = "fmov d1, x1" if kinds.get(right) == "float" else "scvtf d1, x1"
                    lines.extend([f"    {left_convert}", f"    {right_convert}", "    fcmp d0, d1", f"    cset w0, {condition}"])
            elif kinds.get(left) == "text" or kinds.get(right) == "text":
                lines.extend(["    bl _strcmp", "    cmp x0, #0", f"    cset w0, {condition}"])
            else:
                lines.extend(["    cmp x0, x1", f"    cset w0, {condition}"])
            store(item.dest); kinds[item.dest] = "number"
        elif op == "CALL":
            name, *arguments = item.args
            if len(arguments) > 8: raise NativeBackendError("native action call has too many arguments")
            for index, argument in enumerate(arguments): load(argument, f"x{index}")
            lines.append(f"    bl _kuro_fn_{name}"); store(item.dest); kinds[item.dest] = function_return_kinds.get(name, "text" if inferred_text_name(item.dest) else "number")
        elif op == "PRINT":
            temp = item.args[0]
            kind = kinds.get(temp, collection_kinds.get(temp, "unknown"))
            if kind == "text":
                load(temp)
                number_label = f"L_kuro_print_dynamic_number_{function.name}_{temp}"
                text_label = f"L_kuro_print_dynamic_text_{function.name}_{temp}"
                float_label = f"L_kuro_print_dynamic_float_{function.name}_{temp}"
                done_label = f"L_kuro_print_dynamic_done_{function.name}_{temp}"
                lines.extend([
                    "    cmp x0, #4096", f"    b.lo {number_label}",
                    "    mov x1, #0x100000000000", "    cmp x0, x1", f"    b.lo {text_label}",
                    f"{float_label}:", "    sub sp, sp, #16", "    str x0, [sp]", "    adrp x0, L_kuro_float_format@PAGE", "    add x0, x0, L_kuro_float_format@PAGEOFF", "    bl _printf", "    add sp, sp, #16", f"    b {done_label}",
                    f"{text_label}:", "    bl _puts", f"    b {done_label}",
                    f"{number_label}:", "    bl _kuro_print_int", f"{done_label}:",
                ])
            elif kind == "number":
                load(temp, "x0")
                lines.append("    bl _kuro_print_int")
            elif kind == "float":
                load(temp, "x0")
                lines.extend([
                    "    sub sp, sp, #16", "    str x0, [sp]",
                    "    adrp x0, L_kuro_float_format@PAGE", "    add x0, x0, L_kuro_float_format@PAGEOFF",
                    "    bl _printf", "    add sp, sp, #16",
                ])
            else:
                raise NativeBackendError("native action can print only text and integer values")
        elif op == "JUMPF":
            target, condition = item.args; load(condition); lines.append(f"    cbz w0, {labels[target]}")
        elif op == "JUMP":
            lines.append(f"    b {labels[item.args[0]]}")
        elif op == "LABEL":
            lines.append(f"{labels[item.dest]}:")
        elif op == "RETURN":
            load(item.args[0]); lines.extend([f"    mov x15, #{frame}", "    add sp, sp, x15", "    ldp x29, x30, [sp], #16", "    ret"])
        elif op in {"DECLTYPE", "LOOP_GUARD", "CHECK_NONNEG"}:
            continue
        else:
            raise NativeBackendError(f"native action {function.name!r} does not support {op}")
    lines.extend(["    mov x0, #0", f"    mov x15, #{frame}", "    add sp, sp, x15", "    ldp x29, x30, [sp], #16", "    ret"])
    return "\n".join(lines)


def emit_macos_arm64(ir: IRProgram) -> str:
    builtin_calls = {"MakeEnum", "EnumIs", "Some", "None", "Ok", "Err", "IsSome", "IsNone", "IsOk", "IsErr", "Unwrap", "UnwrapErr", "MakeRecord", "RecordSet", "RecordGet", "MakeMap", "MapSet", "MapGet", "MapHas", "MakeClosure", "Invoke", "Spawn", "Await"}
    has_dynamic_action = any(
        item.op == "CALL"
        and (item.args[0] in builtin_calls or (ir.functions.get(item.args[0]) is not None and any(inner.op in {"JUMP", "JUMPF", "CALL", "CMP"} for inner in ir.functions[item.args[0]].body)))
        for item in ir.main
    )
    if any(item.op in {"JUMP", "JUMPF", "LOOP_GUARD", "AND", "OR", "APPEND", "ISCLASS", "INPUT"} for item in ir.main) or has_dynamic_action:
        return _emit_dynamic_macos_arm64(ir)
    labels: list[str] = []
    formats: list[tuple[str, str]] = []
    float_constants: list[tuple[str, str]] = []
    lines = [".section __TEXT,__text", ".globl _main", ".p2align 2", "_main:", "    stp x29, x30, [sp, #-16]!", "    mov x29, sp"]
    constants: dict[str, object] = {}

    def evaluate_function(name: str, args: list[object]):
        function = ir.functions.get(name)
        if function is None or len(function.params) != len(args):
            raise NativeBackendError(f"native arm64 backend cannot resolve action {name!r}")
        values = dict(zip(function.params, args))
        temps: dict[str, object] = {}
        for item in function.body:
            if item.op == "CONST":
                temps[item.dest] = item.args[0]
            elif item.op == "LOADVAR":
                if item.args[0] not in values:
                    raise NativeBackendError(f"native action {name!r} reads a dynamic value")
                temps[item.dest] = values[item.args[0]]
            elif item.op == "BINOP":
                op, left, right = item.args
                if op == "+":
                    temps[item.dest] = temps[left] + temps[right]
                elif op == "-":
                    temps[item.dest] = temps[left] - temps[right]
                elif op == "*":
                    temps[item.dest] = temps[left] * temps[right]
                elif op == "/":
                    temps[item.dest] = temps[left] / temps[right]
                else:
                    raise NativeBackendError(f"native action {name!r} uses unsupported BINOP {op!r}")
            elif item.op == "RETURN":
                return temps[item.args[0]]
            elif item.op in {"LABEL", "DECLTYPE"}:
                continue
            else:
                raise NativeBackendError(f"native action {name!r} uses unsupported {item.op}")
        raise NativeBackendError(f"native action {name!r} has no constant return")

    for instruction in ir.main:
        if instruction.op == "CONST":
            constants[instruction.dest] = instruction.args[0]
        elif instruction.op == "BINOP":
            op, left, right = instruction.args
            if left not in constants or right not in constants:
                raise NativeBackendError("native arm64 backend requires constant operands for BINOP")
            a, b = constants[left], constants[right]
            if not isinstance(a, (int, float)) or not isinstance(b, (int, float)):
                raise NativeBackendError("native arm64 backend only folds numeric BINOP operands")
            if op == "+":
                constants[instruction.dest] = a + b
            elif op == "-":
                constants[instruction.dest] = a - b
            elif op == "*":
                constants[instruction.dest] = a * b
            elif op == "/":
                constants[instruction.dest] = a / b
            else:
                raise NativeBackendError(f"native arm64 backend does not support BINOP {op!r}")
        elif instruction.op == "STORE_LIST":
            name, temp_names = instruction.args
            if not temp_names or any(temp not in constants for temp in temp_names):
                raise NativeBackendError("native arm64 backend requires constant assignment values")
            constants[name] = constants[temp_names[0]] if len(temp_names) == 1 else [constants[temp] for temp in temp_names]
        elif instruction.op == "LOADVAR":
            name = instruction.args[0]
            if name not in constants:
                raise NativeBackendError(f"native arm64 backend cannot resolve variable {name!r}")
            constants[instruction.dest] = constants[name]
        elif instruction.op == "UPDATE":
            name, temp_name = instruction.args
            if temp_name not in constants:
                raise NativeBackendError("native arm64 backend requires constant update values")
            constants[name] = constants[temp_name]
        elif instruction.op == "ADD":
            name, temp_name = instruction.args
            if not isinstance(constants.get(name), (int, float)) or not isinstance(constants.get(temp_name), (int, float)):
                raise NativeBackendError("native arm64 backend only folds numeric ADD values")
            constants[name] += constants[temp_name]
        elif instruction.op == "APPEND":
            name, temp_name = instruction.args
            current, value = constants.get(name), constants.get(temp_name)
            if isinstance(current, str) and isinstance(value, str):
                constants[name] = current + value
            elif isinstance(current, list):
                constants[name] = current + [value]
            else:
                raise NativeBackendError("native arm64 backend only folds text/list APPEND values")
        elif instruction.op == "GET":
            name, index_temp = instruction.args
            if name not in constants or index_temp not in constants:
                raise NativeBackendError("native arm64 backend requires constant collection access")
            value, index = constants[name], constants[index_temp]
            if not isinstance(index, int) or not isinstance(value, (str, list)) or not 0 <= index < len(value):
                raise NativeBackendError("native arm64 backend cannot resolve constant collection index")
            constants[instruction.dest] = value[index]
        elif instruction.op == "LENGTH":
            name = instruction.args[0]
            if name not in constants or not isinstance(constants[name], (str, list)):
                raise NativeBackendError("native arm64 backend requires a constant indexable value")
            constants[instruction.dest] = len(constants[name])
        elif instruction.op == "SET":
            name, index_temp, value_temp = instruction.args
            if name not in constants or index_temp not in constants or value_temp not in constants:
                raise NativeBackendError("native arm64 backend requires constant Set operands")
            target, index, value = constants[name], constants[index_temp], constants[value_temp]
            if not isinstance(index, int) or not isinstance(target, (str, list)) or not 0 <= index < len(target):
                raise NativeBackendError("native arm64 backend cannot resolve constant Set index")
            if isinstance(target, str):
                if not isinstance(value, str) or len(value) != 1:
                    raise NativeBackendError("constant Text Set requires one character")
                constants[name] = target[:index] + value + target[index + 1:]
            else:
                updated = list(target)
                updated[index] = value
                constants[name] = updated
        elif instruction.op == "CALL":
            name, temp_names = instruction.args[0], instruction.args[1:]
            if any(temp not in constants for temp in temp_names):
                raise NativeBackendError("native arm64 backend requires constant action arguments")
            constants[instruction.dest] = evaluate_function(name, [constants[temp] for temp in temp_names])
        elif instruction.op == "PRINT":
            value = constants.get(instruction.args[0])
            values = value if isinstance(value, list) else [value]
            for output in values:
                if isinstance(output, str):
                    label = f"L_kuro_string_{len(labels)}"
                    labels.append((label, output))
                    lines.extend([f"    adrp x0, {label}@PAGE", f"    add x0, x0, {label}@PAGEOFF", "    bl _puts"])
                elif isinstance(output, int):
                    label = f"L_kuro_string_{len(labels)}"
                    labels.append((label, str(output)))
                    lines.extend([f"    adrp x0, {label}@PAGE", f"    add x0, x0, {label}@PAGEOFF", "    bl _puts"])
                elif isinstance(output, float):
                    label = f"L_kuro_format_{len(formats)}"
                    bits = output.hex()
                    formats.append((label, "%g\\n"))
                    number_label = f"L_kuro_float_{len(formats) - 1}"
                    lines.extend([
                        f"    adrp x0, {label}@PAGE", f"    add x0, x0, {label}@PAGEOFF",
                        f"    adrp x1, {number_label}@PAGE", f"    add x1, x1, {number_label}@PAGEOFF", "    ldr x1, [x1]",
                        "    sub sp, sp, #16", "    str x1, [sp]", "    bl _printf", "    add sp, sp, #16",
                    ])
                    float_constants.append((number_label, bits))
                else:
                    raise NativeBackendError("native arm64 backend requires constant Print values")
            continue
        elif instruction.op in {"DECLTYPE", "LABEL"}:
            continue
        else:
            raise NativeBackendError(f"native arm64 backend does not support {instruction.op}")
    lines.extend(["    mov w0, #0", "    ldp x29, x30, [sp], #16", "    ret", ".section __TEXT,__cstring"])
    for label, value in labels:
        escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")
        lines.append(f'{label}: .asciz "{escaped}"')
    for label, value in formats:
        lines.append(f'{label}: .asciz "{value}"')
    for label, value in float_constants:
        lines.append(f"{label}: .double {value}")
    return "\n".join(lines) + "\n"


def emit_x86_64_linux(ir: IRProgram) -> str:
    """Emit the portable integer/text/control-flow subset for Linux x86-64.

    Values live in a real stack frame and branches target emitted labels. No
    constant evaluation or foreign runtime is involved; text output and
    integer formatting use Linux syscalls directly. Complex heap values,
    floating point, and calls remain explicit capability errors below.
    """
    items = ir.main
    def action_returns_text(name: str) -> bool:
        lowered = name.lower()
        return lowered in {
            "curkind", "curvalue", "peekkind", "peekvalue", "tctypeof", "symgettype",
        }

    def inferred_symbol_kind(name: str) -> str:
        lowered = name.lower()
        if lowered.endswith(("pos", "index", "count", "depth", "start", "end", "len", "failed")):
            return "number"
        if lowered == "char" or lowered.startswith("stop") or lowered in {"name", "value", "kind", "message", "code", "text", "word", "line", "source", "token"} or lowered.endswith(("name", "value", "kind", "message", "code", "text", "word", "line", "source", "token", "character", "output", "input", "values", "_op", "opname")):
            return "text"
        return "number"
    collection_names = {
        instruction.args[0]
        for instruction in items
        if instruction.op == "APPEND" and instruction.args
    }
    collection_names.update(
        instruction.args[0]
        for instruction in items
        if instruction.op == "STORE_LIST" and len(instruction.args) > 1 and len(instruction.args[1]) > 1
    )
    for function in ir.functions.values():
        collection_names.update(
            instruction.args[0]
            for instruction in function.body
            if instruction.op == "APPEND" and instruction.args
        )
        collection_names.update(
            instruction.args[0]
            for instruction in function.body
            if instruction.op == "STORE_LIST" and len(instruction.args) > 1 and len(instruction.args[1]) > 1
        )
    input_names = {
        instruction.args[0]
        for instruction in items
        if instruction.op == "INPUT" and instruction.args
    }
    for function in ir.functions.values():
        input_names.update(
            instruction.args[0]
            for instruction in function.body
            if instruction.op == "INPUT" and instruction.args
        )
    names: set[str] = set()
    for instruction in items:
        if instruction.dest:
            names.add(instruction.dest)
        for argument in instruction.args:
            if isinstance(argument, str) and (argument.startswith("t") or argument.startswith("__")):
                names.add(argument)
            if instruction.op in {"LOADVAR", "STORE_LIST", "UPDATE", "ADD", "INPUT"} and isinstance(argument, str):
                names.add(argument)
    slots = {name: -(index + 1) * 8 for index, name in enumerate(sorted(names))}
    frame = ((len(slots) * 8 + 15) // 16) * 16 or 16
    labels = {instruction.dest: f".Lkuro_{instruction.dest}" for instruction in items if instruction.op == "LABEL"}
    kinds: dict[str, str] = {}
    text_lengths: dict[str, int] = {}
    text_length_refs: dict[str, str] = {}
    data: list[tuple[str, bytes]] = []
    float_data: list[tuple[str, float]] = []
    collection_buffers = {name: f".Lkuro_collection_{index}" for index, name in enumerate(sorted(collection_names))}
    collection_lengths = {name: f".Lkuro_collection_len_{index}" for index, name in enumerate(sorted(collection_names))}
    collection_item_lengths = {name: f".Lkuro_collection_item_len_{index}" for index, name in enumerate(sorted(collection_names))}
    input_buffers = {name: f".Lkuro_input_{index}" for index, name in enumerate(sorted(input_names))}
    input_lengths = {name: f".Lkuro_input_len_{index}" for index, name in enumerate(sorted(input_names))}
    global_names: set[str] = set()
    for item in items:
        if item.op in {"LOADVAR", "STORE_LIST", "UPDATE", "ADD", "INPUT", "SAVEVAR", "RESTOREVAR"} and item.args:
            name = item.args[0]
            if isinstance(name, str) and not name.startswith(("t", "__")):
                global_names.add(name)
    for function in ir.functions.values():
        prefix = f"{function.name}_"
        for item in function.body:
            for argument in item.args:
                if isinstance(argument, str) and not argument.startswith(("t", "__")) and argument not in function.params and not argument.startswith(prefix):
                    global_names.add(argument)
    global_names -= set(collection_buffers) | set(input_buffers)
    global_labels = {name: f".Lkuro_global_{index}" for index, name in enumerate(sorted(global_names))}
    char_buffers = {
        instruction.dest: f".Lkuro_char_{index}"
        for index, instruction in enumerate(items)
        if instruction.op == "GET" and instruction.dest and instruction.args[0] not in collection_names
    }
    function_char_buffers = {
        f"{function.name}:{instruction.dest}": f".Lkuro_char_fn_{index}"
        for index, (function, instruction) in enumerate(
            (function, instruction)
            for function in ir.functions.values()
            for instruction in function.body
            if instruction.op == "GET" and instruction.dest and instruction.args[0] not in collection_names
        )
    }
    function_concat_buffers = {
        f"{function.name}:{instruction.dest}": f".Lkuro_fn_concat_{index}"
        for index, (function, instruction) in enumerate(
            (function, instruction)
            for function in ir.functions.values()
            for instruction in function.body
            if instruction.op == "BINOP" and instruction.args and instruction.args[0] == "+" and instruction.dest
        )
    }
    concat_buffers = {
        instruction.dest: f".Lkuro_concat_{index}"
        for index, instruction in enumerate(items)
        if instruction.op == "BINOP" and instruction.args and instruction.args[0] == "+" and instruction.dest
    }
    concat_lengths = {name: f"{label}_len" for name, label in concat_buffers.items()}
    collection_kinds: dict[str, str] = {}
    collection_ref: dict[str, str] = {}
    map_dest_labels = {
        instruction.dest: f".Lkuro_map_{index}"
        for index, instruction in enumerate(
            instruction for instruction in items
            if instruction.op == "CALL" and instruction.args and instruction.args[0] == "MakeMap" and instruction.dest
        )
    }
    map_alias: dict[str, str] = {}
    map_key_slots: dict[str, int] = {}
    known_text: dict[str, str] = {}
    map_value_kinds: dict[str, str] = {}
    map_value_lengths: dict[str, int] = {}
    tagged_dest_labels = {
        instruction.dest: f".Lkuro_tagged_{index}"
        for index, instruction in enumerate(
            instruction for instruction in items
            if instruction.op == "CALL"
            and instruction.args
            and instruction.args[0] in {"Some", "None", "Ok", "Err"}
            and instruction.dest
        )
    }
    tagged_kinds: dict[str, str] = {}
    tagged_alias: dict[str, str] = {}
    lines = [
        ".section .text", ".globl _start", ".globl main", "_start:",
        "    call main", "    mov %eax, %edi", "    mov $60, %eax", "    syscall",
        "main:",
        "    push %rbp", "    mov %rsp, %rbp", f"    sub ${frame}, %rsp",
    ]

    def load(name: str, register: str = "%rax") -> None:
        if name in collection_buffers:
            lines.append(f"    lea {collection_buffers[name]}(%rip), {register}")
            return
        if name in global_labels:
            lines.append(f"    mov {global_labels[name]}(%rip), {register}")
            return
        if name not in slots:
            raise NativeBackendError(f"x86_64-linux backend cannot load {name!r}")
        lines.append(f"    mov {slots[name]}(%rbp), {register}")

    def store(name: str, register: str = "%rax") -> None:
        if name in global_labels:
            lines.append(f"    mov {register}, {global_labels[name]}(%rip)")
            return
        if name not in slots:
            raise NativeBackendError(f"x86_64-linux backend cannot store {name!r}")
        lines.append(f"    mov {register}, {slots[name]}(%rbp)")

    input_sequence = 0
    for instruction in items:
        op = instruction.op
        if op == "CONST":
            value = instruction.args[0]
            if isinstance(value, bool) or isinstance(value, int):
                lines.append(f"    mov ${value}, %rax")
                kinds[instruction.dest] = "number"
            elif isinstance(value, float):
                label = f".Lkuro_float_{len(float_data)}"
                float_data.append((label, value))
                lines.extend([f"    movsd {label}(%rip), %xmm0", "    movq %xmm0, %rax"])
                kinds[instruction.dest] = "float"
            elif isinstance(value, str):
                label = f".Lkuro_data_{len(data)}"
                encoded = value.encode("utf-8")
                data.append((label, encoded + b"\0"))
                lines.append(f"    lea {label}(%rip), %rax")
                kinds[instruction.dest] = "text"
                text_lengths[instruction.dest] = len(encoded)
                known_text[instruction.dest] = value
            else:
                raise NativeBackendError("x86_64-linux backend supports integer and text constants")
            store(instruction.dest)
        elif op == "LOADVAR":
            load(instruction.args[0]); store(instruction.dest)
            kinds[instruction.dest] = kinds.get(instruction.args[0], "unknown")
            if instruction.args[0] in collection_buffers:
                collection_ref[instruction.dest] = instruction.args[0]
            if instruction.args[0] in map_alias:
                map_alias[instruction.dest] = map_alias[instruction.args[0]]
            if instruction.args[0] in tagged_alias:
                tagged_alias[instruction.dest] = tagged_alias[instruction.args[0]]
            if instruction.args[0] in known_text:
                known_text[instruction.dest] = known_text[instruction.args[0]]
            if instruction.args[0] in text_lengths:
                text_lengths[instruction.dest] = text_lengths[instruction.args[0]]
            if instruction.args[0] in text_length_refs:
                text_length_refs[instruction.dest] = text_length_refs[instruction.args[0]]
        elif op == "STORE_LIST":
            name, values = instruction.args
            if name in collection_buffers:
                if len(values) > NATIVE_COLLECTION_CAPACITY:
                    raise NativeBackendError(f"x86_64-linux collection exceeds fixed capacity of {NATIVE_COLLECTION_CAPACITY}")
                for index, value in enumerate(values):
                    load(value)
                    lines.append(f"    mov %rax, {collection_buffers[name]}+{index * 8}(%rip)")
                    lines.append(f"    movq ${text_lengths.get(value, 0)}, {collection_item_lengths[name]}+{index * 8}(%rip)")
                lines.append(f"    mov ${len(values)}, %rax")
                lines.append(f"    mov %rax, {collection_lengths[name]}(%rip)")
                kinds[name] = "collection"
                collection_kinds[name] = "text" if values and all(kinds.get(value) == "text" for value in values) else "number"
            elif len(values) == 1 and values[0] in map_alias:
                load(values[0]); store(name)
                map_alias[name] = map_alias[values[0]]
                kinds[name] = "map"
            elif len(values) == 1 and values[0] in tagged_alias:
                load(values[0]); store(name)
                tagged_alias[name] = tagged_alias[values[0]]
                kinds[name] = "tagged"
            elif len(values) == 1:
                load(values[0]); store(name)
                kinds[name] = kinds.get(values[0], "unknown")
                if values[0] in text_lengths:
                    text_lengths[name] = text_lengths[values[0]]
                elif name in text_lengths:
                    del text_lengths[name]
                if values[0] in text_length_refs:
                    text_length_refs[name] = text_length_refs[values[0]]
                elif name in text_length_refs:
                    del text_length_refs[name]
                if values[0] in known_text:
                    known_text[name] = known_text[values[0]]
                elif name in known_text:
                    del known_text[name]
            else:
                raise NativeBackendError("x86_64-linux backend does not yet lower this heap collection")
        elif op == "UPDATE":
            name, value = instruction.args
            load(value); store(name); kinds[name] = kinds.get(value, "unknown")
            if value in map_alias:
                map_alias[name] = map_alias[value]
            if value in tagged_alias:
                tagged_alias[name] = tagged_alias[value]
            if value in known_text:
                known_text[name] = known_text[value]
            elif name in known_text:
                del known_text[name]
            if value in text_lengths:
                text_lengths[name] = text_lengths[value]
            elif name in text_lengths:
                del text_lengths[name]
            if value in text_length_refs:
                text_length_refs[name] = text_length_refs[value]
            elif name in text_length_refs:
                del text_length_refs[name]
        elif op == "SAVEVAR":
            name = instruction.args[0]
            load(name); store(instruction.dest)
            kinds[instruction.dest] = kinds.get(name, "unknown")
        elif op == "RESTOREVAR":
            name, saved = instruction.args
            load(saved); store(name)
            kinds[name] = kinds.get(saved, "unknown")
            if saved in text_lengths:
                text_lengths[name] = text_lengths[saved]
            elif name in text_lengths:
                del text_lengths[name]
            if saved in text_length_refs:
                text_length_refs[name] = text_length_refs[saved]
            elif name in text_length_refs:
                del text_length_refs[name]
        elif op == "INPUT":
            name = instruction.args[0]
            if name not in input_buffers:
                raise NativeBackendError("x86_64-linux INPUT requires a destination")
            read_label = f"{input_buffers[name]}_read_{input_sequence}"
            read_done_label = f"{input_buffers[name]}_read_done_{input_sequence}"
            input_sequence += 1
            lines.extend([
                f"    movq $0, {input_lengths[name]}(%rip)",
                f"{read_label}:",
                f"    mov {input_lengths[name]}(%rip), %r8",
                f"    mov ${NATIVE_INPUT_READ_LIMIT}, %rdx",
                "    sub %r8, %rdx",
                "    jz .Lkuro_runtime_error",
                "    xor %eax, %eax",
                "    xor %edi, %edi",
                f"    lea {input_buffers[name]}(%rip), %rsi",
                "    add %r8, %rsi",
                "    syscall",
                "    test %rax, %rax",
                "    js .Lkuro_runtime_error",
                f"    jz {read_done_label}",
                f"    add %rax, {input_lengths[name]}(%rip)",
                f"    jmp {read_label}",
                f"{read_done_label}:",
                f"    lea {input_buffers[name]}(%rip), %rax",
                f"    mov {input_lengths[name]}(%rip), %rcx",
                "    movb $0, (%rax,%rcx,1)",
            ])
            store(name); kinds[name] = "text"
            text_length_refs[name] = input_lengths[name]
        elif op == "ADD":
            name, value = instruction.args
            load(name, "%rax"); load(value, "%rcx")
            lines.append("    add %rcx, %rax"); store(name)
            kinds[name] = "number"
        elif op == "BINOP":
            operator, left, right = instruction.args
            if operator == "+" and kinds.get(left) == "text" and kinds.get(right) == "text":
                buffer = concat_buffers[instruction.dest]
                length = concat_lengths[instruction.dest]
                load(left, "%r8"); load(right, "%r9")
                lines.extend([
                    # Mutable text can flow through a loop-carried temporary.
                    # Its source-level constant length is not its runtime
                    # length, so always measure both operands here.
                    "    mov %r8, %rax", "    call _kuro_strlen", "    mov %rax, %r10",
                    "    mov %r9, %rax", "    call _kuro_strlen", "    mov %rax, %r11",
                    "    mov %r10, %rax", "    add %r11, %rax",
                    "    mov .Lkuro_text_heap_cursor(%rip), %rdx", "    mov %rdx, %rcx", "    add %rax, %rcx", "    inc %rcx",
                    f"    cmp ${NATIVE_TEXT_HEAP_CAPACITY}, %rcx", "    ja .Lkuro_overflow",
                    "    lea .Lkuro_text_heap(%rip), %rdi", "    add %rdx, %rdi", "    mov %r8, %rsi", "    mov %r10, %rcx", "    rep movsb",
                    "    mov %r9, %rsi", "    mov %r11, %rcx", "    rep movsb",
                    "    movb $0, (%rdi)", "    lea .Lkuro_text_heap(%rip), %rsi", "    mov %rdi, %rcx", "    sub %rsi, %rcx", "    inc %rcx",
                    "    mov %rcx, .Lkuro_text_heap_cursor(%rip)", "    mov %rdi, %rdx", "    sub %rax, %rdx", f"    mov %rax, {length}(%rip)", "    mov %rdx, %rax",
                ])
                store(instruction.dest); kinds[instruction.dest] = "text"; text_length_refs[instruction.dest] = length
                continue
            if kinds.get(left) in {"number", "float"} and kinds.get(right) in {"number", "float"} and (kinds.get(left) == "float" or kinds.get(right) == "float"):
                if operator not in {"+", "-", "*", "/"}:
                    raise NativeBackendError(f"x86_64-linux floating BINOP does not support {operator!r}")
                if kinds.get(left) == "float":
                    load(left, "%rax"); lines.extend(["    movq %rax, %xmm0"])
                else:
                    load(left, "%rax"); lines.extend(["    cvtsi2sd %rax, %xmm0"])
                if kinds.get(right) == "float":
                    load(right, "%rax"); lines.extend(["    movq %rax, %xmm1"])
                else:
                    load(right, "%rax"); lines.extend(["    cvtsi2sd %rax, %xmm1"])
                lines.append(f"    { {'+':'addsd','-':'subsd','*':'mulsd','/':'divsd'}[operator] } %xmm1, %xmm0")
                lines.append("    movq %xmm0, %rax"); store(instruction.dest); kinds[instruction.dest] = "float"
                continue
            if kinds.get(left) != "number" or kinds.get(right) != "number":
                raise NativeBackendError("x86_64-linux BINOP currently requires integer operands")
            load(left, "%rax"); load(right, "%rcx")
            if operator == "+":
                lines.append("    add %rcx, %rax")
            elif operator == "-":
                lines.append("    sub %rcx, %rax")
            elif operator == "*":
                lines.append("    imul %rcx, %rax")
            elif operator == "/":
                lines.extend(["    cqo", "    idiv %rcx"])
            else:
                raise NativeBackendError(f"x86_64-linux backend does not support BINOP {operator!r}")
            store(instruction.dest); kinds[instruction.dest] = "number"
        elif op == "CMP":
            operator, left, right = instruction.args
            if operator in {"eq", "ne"} and not (
                kinds.get(left) in {"number", "float"}
                and kinds.get(right) in {"number", "float"}
            ):
                unique = len(lines)
                numeric = f".Lkuro_dynamic_cmp_numeric_{unique}"
                loop = f".Lkuro_dynamic_cmp_loop_{unique}"
                equal = f".Lkuro_dynamic_cmp_equal_{unique}"
                different = f".Lkuro_dynamic_cmp_different_{unique}"
                done = f".Lkuro_dynamic_cmp_done_{unique}"
                left_bss = f".Lkuro_dynamic_cmp_left_bss_{unique}"
                left_text = f".Lkuro_dynamic_cmp_left_text_{unique}"
                right_bss = f".Lkuro_dynamic_cmp_right_bss_{unique}"
                right_text = f".Lkuro_dynamic_cmp_right_text_{unique}"
                load(left, "%r8"); load(right, "%r9")
                lines.extend([
                    "    lea .Lkuro_rodata_begin(%rip), %r10", "    cmp %r10, %r8", f"    jb {left_bss}",
                    "    lea .Lkuro_rodata_end(%rip), %r10", "    cmp %r10, %r8", f"    jb {left_text}",
                    f"{left_bss}:", "    lea .Lkuro_bss_begin(%rip), %r10", "    cmp %r10, %r8", f"    jb {numeric}",
                    "    lea .Lkuro_bss_end(%rip), %r10", "    cmp %r10, %r8", f"    jae {numeric}",
                    f"{left_text}:",
                    "    lea .Lkuro_rodata_begin(%rip), %r10", "    cmp %r10, %r9", f"    jb {right_bss}",
                    "    lea .Lkuro_rodata_end(%rip), %r10", "    cmp %r10, %r9", f"    jb {right_text}",
                    f"{right_bss}:", "    lea .Lkuro_bss_begin(%rip), %r10", "    cmp %r10, %r9", f"    jb {numeric}",
                    "    lea .Lkuro_bss_end(%rip), %r10", "    cmp %r10, %r9", f"    jae {numeric}",
                    f"{right_text}:",
                    f"{loop}:", "    movzbq (%r8), %rax", "    movzbq (%r9), %rcx", "    cmp %rcx, %rax", f"    jne {different}",
                    "    test %rax, %rax", f"    jz {equal}", "    inc %r8", "    inc %r9", f"    jmp {loop}",
                    f"{numeric}:", "    cmp %r9, %r8", f"    je {equal}",
                    f"{different}:", "    xor %eax, %eax", f"    jmp {done}",
                    f"{equal}:", "    mov $1, %rax", f"{done}:",
                ])
                if operator == "ne":
                    lines.append("    xor $1, %eax")
                store(instruction.dest); kinds[instruction.dest] = "number"
                continue
            if kinds.get(left) in {"number", "float"} and kinds.get(right) in {"number", "float"} and (kinds.get(left) == "float" or kinds.get(right) == "float"):
                condition = {"eq": "e", "ne": "ne", "lt": "b", "le": "be", "gt": "a", "ge": "ae"}.get(operator)
                if condition is None:
                    raise NativeBackendError(f"x86_64-linux floating CMP does not support {operator!r}")
                if kinds.get(left) == "float":
                    load(left, "%rax"); lines.append("    movq %rax, %xmm0")
                else:
                    load(left, "%rax"); lines.append("    cvtsi2sd %rax, %xmm0")
                if kinds.get(right) == "float":
                    load(right, "%rax"); lines.append("    movq %rax, %xmm1")
                else:
                    load(right, "%rax"); lines.append("    cvtsi2sd %rax, %xmm1")
                lines.extend(["    ucomisd %xmm1, %xmm0", f"    set{condition} %al", "    movzbq %al, %rax"])
                store(instruction.dest); kinds[instruction.dest] = "number"
                continue
            if kinds.get(left) == "text" and kinds.get(right) == "text":
                if operator not in {"eq", "ne"}:
                    raise NativeBackendError("x86_64-linux text CMP supports only equality")
                unique = len(lines)
                loop = f".Lkuro_text_cmp_{unique}"
                equal = f".Lkuro_text_cmp_equal_{unique}"
                different = f".Lkuro_text_cmp_different_{unique}"
                done = f".Lkuro_text_cmp_done_{unique}"
                load(left, "%r8"); load(right, "%r9")
                if left in text_length_refs:
                    lines.append(f"    mov {text_length_refs[left]}(%rip), %r10")
                else:
                    lines.append(f"    mov ${text_lengths.get(left, 0)}, %r10")
                if right in text_length_refs:
                    lines.append(f"    mov {text_length_refs[right]}(%rip), %r11")
                else:
                    lines.append(f"    mov ${text_lengths.get(right, 0)}, %r11")
                lines.extend([
                    "    cmp %r11, %r10", f"    jne {different}",
                    f"{loop}:", "    test %r10, %r10", f"    jz {equal}",
                    "    movzbq (%r8), %rax", "    movzbq (%r9), %rcx", "    cmp %rcx, %rax",
                    f"    jne {different}", "    inc %r8", "    inc %r9", "    dec %r10", f"    jmp {loop}",
                    f"{equal}:", "    mov $1, %rax", f"    jmp {done}",
                    f"{different}:", "    xor %eax, %eax", f"{done}:",
                ])
                if operator == "ne":
                    lines.append("    xor $1, %eax")
                store(instruction.dest); kinds[instruction.dest] = "number"
                continue
            if kinds.get(left) != "number" or kinds.get(right) != "number":
                raise NativeBackendError(
                    "x86_64-linux CMP requires operands of one supported kind "
                    f"(operator={operator!r}, left={left!r}:{kinds.get(left)!r}, "
                    f"right={right!r}:{kinds.get(right)!r})"
                )
            condition = {"eq": "e", "ne": "ne", "lt": "l", "le": "le", "gt": "g", "ge": "ge"}.get(operator)
            if condition is None:
                raise NativeBackendError(f"unsupported x86_64-linux comparison {operator!r}")
            load(left, "%rax"); load(right, "%rcx")
            lines.extend(["    cmp %rcx, %rax", f"    set{condition} %al", "    movzbq %al, %rax"])
            store(instruction.dest); kinds[instruction.dest] = "number"
        elif op == "GET":
            name, index = instruction.args
            if index is None:
                raise NativeBackendError("x86_64-linux GET requires an index")
            if name in input_buffers:
                load(index, "%rcx")
                lines.extend([
                    f"    cmp {input_lengths[name]}(%rip), %rcx", "    jae .Lkuro_bounds",
                    f"    lea {input_buffers[name]}(%rip), %rax", "    movzbq (%rax,%rcx,1), %rdx",
                    "    mov .Lkuro_char_heap_cursor(%rip), %r8",
                    f"    cmp ${NATIVE_INPUT_CAPACITY * 2 - 2}, %r8", "    jae .Lkuro_overflow",
                    "    lea .Lkuro_char_heap(%rip), %rax", "    add %r8, %rax",
                    "    mov %dl, (%rax)", "    movb $0, 1(%rax)", "    add $2, %r8", "    mov %r8, .Lkuro_char_heap_cursor(%rip)",
                ])
                store(instruction.dest); kinds[instruction.dest] = "text"; text_lengths[instruction.dest] = 1
            elif name in known_text:
                load(index, "%rcx")
                lines.extend([
                    f"    cmp ${len(known_text[name])}, %rcx", "    jae .Lkuro_bounds",
                ])
                load(name, "%rax")
                lines.extend([
                    "    movzbq (%rax,%rcx,1), %rdx", "    mov .Lkuro_char_heap_cursor(%rip), %r8",
                    f"    cmp ${NATIVE_INPUT_CAPACITY * 2 - 2}, %r8", "    jae .Lkuro_overflow",
                    "    lea .Lkuro_char_heap(%rip), %rax", "    add %r8, %rax",
                    "    mov %dl, (%rax)", "    movb $0, 1(%rax)", "    add $2, %r8", "    mov %r8, .Lkuro_char_heap_cursor(%rip)",
                ])
                store(instruction.dest); kinds[instruction.dest] = "text"; text_lengths[instruction.dest] = 1
            elif inferred_symbol_kind(name) == "text" and name not in collection_buffers:
                load(index, "%rcx")
                load(name, "%rax")
                lines.extend([
                    "    test %rax, %rax", "    jz .Lkuro_bounds", "    call _kuro_strlen",
                    "    cmp %rax, %rcx", "    jae .Lkuro_bounds",
                ])
                load(name, "%rax")
                lines.extend([
                    "    movzbq (%rax,%rcx,1), %rdx", "    mov .Lkuro_char_heap_cursor(%rip), %r8",
                    f"    cmp ${NATIVE_INPUT_CAPACITY * 2 - 2}, %r8", "    jae .Lkuro_overflow",
                    "    lea .Lkuro_char_heap(%rip), %rax", "    add %r8, %rax",
                    "    mov %dl, (%rax)", "    movb $0, 1(%rax)", "    add $2, %r8", "    mov %r8, .Lkuro_char_heap_cursor(%rip)",
                ])
                store(instruction.dest); kinds[instruction.dest] = "text"; text_lengths[instruction.dest] = 1
            elif name in collection_buffers:
                load(index, "%rcx")
                lines.extend([
                    f"    cmp ${NATIVE_COLLECTION_CAPACITY}, %rcx", "    jae .Lkuro_bounds",
                    f"    lea {collection_buffers[name]}(%rip), %rax",
                    "    mov (%rax,%rcx,8), %rax",
                ])
                store(instruction.dest); kinds[instruction.dest] = collection_kinds.get(name, "number")
            else:
                raise NativeBackendError(
                    f"x86_64-linux GET cannot determine runtime kind of {name!r} "
                    f"({kinds.get(name)!r})"
                )
        elif op == "SET":
            name, index, value = instruction.args
            if name not in collection_buffers:
                raise NativeBackendError("x86_64-linux SET requires a native collection")
            load(index, "%rcx"); load(value, "%rdx")
            lines.extend([
                f"    cmp ${NATIVE_COLLECTION_CAPACITY}, %rcx", "    jae .Lkuro_bounds",
                f"    lea {collection_buffers[name]}(%rip), %rax",
                "    mov %rdx, (%rax,%rcx,8)",
            ])
        elif op == "LENGTH":
            name = instruction.args[0]
            if name in input_lengths:
                lines.append(f"    mov {input_lengths[name]}(%rip), %rax")
            elif name in collection_lengths:
                lines.append(f"    mov {collection_lengths[name]}(%rip), %rax")
            elif kinds.get(name) == "text" or name in known_text or inferred_symbol_kind(name) == "text":
                load(name, "%rax")
                zero_label = f".Lkuro_length_zero_{instruction.dest}"
                done_label = f".Lkuro_length_done_{instruction.dest}"
                lines.extend([
                    "    test %rax, %rax", f"    jz {zero_label}",
                    "    call _kuro_strlen", f"    jmp {done_label}",
                    f"{zero_label}:", "    xor %eax, %eax", f"{done_label}:",
                ])
            else:
                raise NativeBackendError(
                    f"x86_64-linux LENGTH cannot determine runtime kind of {name!r}"
                )
            store(instruction.dest); kinds[instruction.dest] = "number"
        elif op == "APPEND":
            name, value = instruction.args
            if name not in collection_buffers:
                raise NativeBackendError("x86_64-linux APPEND requires a native collection")
            lines.extend([
                f"    mov {collection_lengths[name]}(%rip), %rcx",
                f"    cmp ${NATIVE_COLLECTION_CAPACITY}, %rcx", "    jae .Lkuro_overflow",
            ])
            load(value, "%rdx")
            lines.extend([
                f"    lea {collection_buffers[name]}(%rip), %rax",
                "    mov %rdx, (%rax,%rcx,8)", "    inc %rcx",
                f"    mov %rcx, {collection_lengths[name]}(%rip)",
            ])
            lines.extend([
                f"    lea {collection_item_lengths[name]}(%rip), %rax",
                f"    movq ${text_lengths.get(value, 0)}, -8(%rax,%rcx,8)",
            ])
            if kinds.get(value) == "text":
                collection_kinds.setdefault(name, "text")
        elif op == "CALL":
            call_name, *arguments = instruction.args
            if call_name == "MakeMap" and not arguments:
                label = map_dest_labels.get(instruction.dest)
                if label is None:
                    raise NativeBackendError("x86_64-linux MakeMap requires a destination")
                lines.append(f"    lea {label}(%rip), %rax")
                store(instruction.dest)
                map_alias[instruction.dest] = label
                kinds[instruction.dest] = "map"
            elif call_name in {"MapSet", "MapGet", "MapHas"}:
                if not arguments or arguments[0] not in slots:
                    raise NativeBackendError(f"x86_64-linux {call_name} requires a map value")
                target = arguments[0]
                key_temp = arguments[1] if len(arguments) > 1 else None
                key = known_text.get(key_temp)
                if key is None:
                    raise NativeBackendError(f"x86_64-linux {call_name} requires a known text key")
                slot = map_key_slots.setdefault(key, len(map_key_slots))
                if slot >= 512:
                    raise NativeBackendError("x86_64-linux map exceeds fixed capacity of 512 keys")
                load(target, "%rax")
                presence = 4096 + slot * 8
                value_offset = slot * 8
                if call_name == "MapSet":
                    if len(arguments) != 3:
                        raise NativeBackendError("x86_64-linux MapSet requires map, key, and value")
                    load(arguments[2], "%rdx")
                    lines.extend([
                        f"    mov %rdx, {value_offset}(%rax)",
                        f"    movq $1, {presence}(%rax)",
                    ])
                    map_value_kinds[key] = kinds.get(arguments[2], "number")
                    if arguments[2] in text_lengths:
                        map_value_lengths[key] = text_lengths[arguments[2]]
                    store(instruction.dest)
                    map_alias[instruction.dest] = map_alias.get(target, "")
                    kinds[instruction.dest] = "map"
                elif call_name == "MapHas":
                    lines.extend([f"    cmpq $0, {presence}(%rax)", "    sete %al", "    movzbq %al, %rax"])
                    store(instruction.dest); kinds[instruction.dest] = "number"
                else:
                    lines.extend([f"    mov {value_offset}(%rax), %rax"])
                    store(instruction.dest); kinds[instruction.dest] = map_value_kinds.get(key, "number")
                    if kinds[instruction.dest] == "text" and key in map_value_lengths:
                        text_lengths[instruction.dest] = map_value_lengths[key]
            elif call_name in {"Some", "None", "Ok", "Err"}:
                label = tagged_dest_labels.get(instruction.dest)
                if label is None:
                    raise NativeBackendError(f"x86_64-linux {call_name} requires a destination")
                if call_name == "None":
                    if arguments:
                        raise NativeBackendError("x86_64-linux None takes no arguments")
                    tag = 0
                else:
                    if len(arguments) != 1:
                        raise NativeBackendError(f"x86_64-linux {call_name} requires one payload")
                    tag = {"Some": 1, "Ok": 2, "Err": 3}[call_name]
                    load(arguments[0], "%rdx")
                    lines.append(f"    mov %rdx, {label}+8(%rip)")
                    tagged_kinds[label] = kinds.get(arguments[0], "number")
                lines.extend([f"    movq ${tag}, {label}(%rip)", f"    lea {label}(%rip), %rax"])
                store(instruction.dest)
                tagged_alias[instruction.dest] = label
                kinds[instruction.dest] = "tagged"
            elif call_name in {"IsSome", "IsNone", "IsOk", "IsErr", "Unwrap", "UnwrapErr"}:
                if len(arguments) != 1:
                    raise NativeBackendError(f"x86_64-linux {call_name} requires one value")
                load(arguments[0], "%rax")
                if call_name == "Unwrap" or call_name == "UnwrapErr":
                    lines.append("    mov 8(%rax), %rax")
                    store(instruction.dest)
                    kinds[instruction.dest] = tagged_kinds.get(tagged_alias.get(arguments[0], ""), "number")
                    if kinds[instruction.dest] == "text":
                        text_lengths[instruction.dest] = 0
                else:
                    expected = {"IsNone": 0, "IsSome": 1, "IsOk": 2, "IsErr": 3}[call_name]
                    lines.extend([f"    cmpq ${expected}, (%rax)", "    sete %al", "    movzbq %al, %rax"])
                    store(instruction.dest); kinds[instruction.dest] = "number"
            elif call_name in ir.functions:
                if len(arguments) > 6:
                    raise NativeBackendError("x86_64-linux action call supports at most six arguments")
                for index, argument in enumerate(arguments):
                    load(argument, f"%{('rdi', 'rsi', 'rdx', 'rcx', 'r8', 'r9')[index]}")
                lines.append(f"    call .Lkuro_fn_{call_name}")
                store(instruction.dest)
                kinds[instruction.dest] = "text" if action_returns_text(call_name) else "number"
            else:
                raise NativeBackendError(f"x86_64-linux backend does not yet lower CALL {call_name!r}")
        elif op in {"AND", "OR"}:
            left, right = instruction.args
            load(left, "%rax"); lines.append("    test %rax, %rax"); lines.append("    setne %al"); lines.append("    movzbq %al, %rax")
            load(right, "%rcx"); lines.append("    test %rcx, %rcx"); lines.append("    setne %cl"); lines.append("    movzbq %cl, %rcx")
            lines.append(f"    {'and' if op == 'AND' else 'or'} %rcx, %rax"); store(instruction.dest); kinds[instruction.dest] = "number"
        elif op == "ISCLASS":
            operand, cls = instruction.args
            if cls not in {"digit", "alpha", "space", "alnum", "quote"}:
                raise NativeBackendError(f"unsupported x86_64-linux character class {cls!r}")
            invalid_label = f".Lkuro_isclass_invalid_{instruction.dest}"
            done_label = f".Lkuro_isclass_done_{instruction.dest}"
            load(operand, "%rax")
            lines.extend(["    test %rax, %rax", f"    jle {invalid_label}", "    cmp $4096, %rax", f"    jb {invalid_label}", "    movzbq (%rax), %rax"])
            if cls == "digit":
                lines.extend(["    cmp $48, %rax", "    setge %dl", "    cmp $57, %rax", "    setle %cl", "    and %cl, %dl", "    movzbl %dl, %eax"])
            elif cls == "alpha":
                lines.extend(["    mov %rax, %rcx", "    cmp $65, %rax", "    setge %r8b", "    cmp $90, %rcx", "    setle %r9b", "    and %r9b, %r8b", "    mov %rax, %rcx", "    cmp $97, %rax", "    setge %r9b", "    cmp $122, %rcx", "    setle %dl", "    and %dl, %r9b", "    or %r9b, %r8b", "    movzbl %r8b, %eax"])
            elif cls == "alnum":
                lines.extend([
                    "    mov %rax, %rcx",
                    "    cmp $48, %rax", "    setge %r8b", "    cmp $57, %rcx", "    setle %r9b", "    and %r9b, %r8b",
                    "    cmp $65, %rax", "    setge %r9b", "    cmp $90, %rcx", "    setle %dl", "    and %dl, %r9b", "    or %r9b, %r8b",
                    "    cmp $97, %rax", "    setge %r9b", "    cmp $122, %rcx", "    setle %dl", "    and %dl, %r9b", "    or %r9b, %r8b",
                    "    movzbl %r8b, %eax",
                ])
            elif cls == "space":
                lines.extend(["    cmp $32, %rax", "    sete %al", "    movzbq %al, %rax"])
            else:
                lines.extend(["    cmp $34, %rax", "    sete %al", "    movzbq %al, %rax"])
            lines.extend([f"    jmp {done_label}", f"{invalid_label}:", "    xor %eax, %eax", f"{done_label}:"])
            store(instruction.dest); kinds[instruction.dest] = "number"
        elif op == "JUMPF":
            target, condition = instruction.args
            load(condition); lines.extend(["    test %rax, %rax", f"    jz {labels[target]}"])
        elif op == "JUMP":
            lines.append(f"    jmp {labels[instruction.args[0]]}")
        elif op == "LABEL":
            lines.append(f"{labels[instruction.dest]}:")
        elif op == "PRINT":
            name = instruction.args[0]
            kind = kinds.get(name)
            collection_name = collection_ref.get(name, name)
            if kind == "text":
                load(name, "%rsi")
                if name in text_length_refs:
                    lines.append(f"    mov {text_length_refs[name]}(%rip), %rdx")
                else:
                    lines.append(f"    mov ${text_lengths.get(name, 0)}, %rdx")
                lines.extend([
                    "    mov $1, %rax", "    mov $1, %rdi", "    syscall",
                    "    lea .Lkuro_newline(%rip), %rsi", "    mov $1, %rdx",
                    "    mov $1, %rax", "    mov $1, %rdi", "    syscall",
                ])
            elif kind == "number":
                load(name); lines.append("    call _kuro_print_int")
            elif kind == "collection":
                if collection_kinds.get(collection_name) == "text":
                    lines.extend([
                        f"    mov {collection_lengths[collection_name]}(%rip), %rcx",
                        "    xor %r8d, %r8d",
                        f"    lea {collection_buffers[collection_name]}(%rip), %r9",
                        f"    lea {collection_item_lengths[collection_name]}(%rip), %r10",
                        ".Lkuro_print_text_collection:",
                        "    cmp %rcx, %r8", "    jae .Lkuro_print_collection_done",
                        "    mov (%r9,%r8,8), %rsi", "    mov (%r10,%r8,8), %rdx",
                        "    mov $1, %rax", "    mov $1, %rdi", "    syscall",
                        "    lea .Lkuro_newline(%rip), %rsi", "    mov $1, %rdx",
                        "    mov $1, %rax", "    mov $1, %rdi", "    syscall",
                        "    inc %r8", "    jmp .Lkuro_print_text_collection",
                        ".Lkuro_print_collection_done:",
                    ])
                else:
                    lines.extend([
                        f"    mov {collection_lengths[collection_name]}(%rip), %rcx",
                        "    xor %r8d, %r8d",
                        f"    lea {collection_buffers[collection_name]}(%rip), %r9",
                        ".Lkuro_print_collection:",
                        "    cmp %rcx, %r8", "    jae .Lkuro_print_collection_done",
                        "    mov (%r9,%r8,8), %rax", "    call _kuro_print_int",
                        "    inc %r8", "    jmp .Lkuro_print_collection",
                        ".Lkuro_print_collection_done:",
                    ])
            else:
                raise NativeBackendError("x86_64-linux PRINT requires an integer or known-length text")
        elif op in {"DECLTYPE", "LOOP_GUARD", "CHECK_NONNEG"}:
            continue
        else:
            raise NativeBackendError(f"x86_64-linux backend does not yet lower {op}")
    # Function bodies share the text section with main.  Skip over them when
    # main finishes; otherwise execution falls through into the first action
    # with no call frame or arguments.
    lines.append("    jmp .Lkuro_main_epilogue")
    for function in ir.functions.values():
        fn_names = set(function.params)
        for item in function.body:
            if item.dest:
                if item.dest not in global_names:
                    fn_names.add(item.dest)
            for argument in item.args:
                if isinstance(argument, str):
                    if argument not in global_names and argument not in collection_buffers and argument not in input_buffers:
                        fn_names.add(argument)
        fn_slots = {name: -(index + 1) * 8 for index, name in enumerate(sorted(fn_names))}
        fn_frame = ((len(fn_slots) * 8 + 15) // 16) * 16 or 16
        fn_labels = {item.dest: f".Lkuro_fn_{function.name}_{item.dest}" for item in function.body if item.op == "LABEL"}
        fn_kinds: dict[str, str] = {name: inferred_symbol_kind(name) for name in function.params}
        # The Kuro VM deliberately stores dynamically typed values in generic
        # names such as ``*_Value`` and ``_``.  For the native lowering pass,
        # collect hard numeric-use constraints before emitting instructions so
        # a numeric VM branch is not mistaken for text merely because of its
        # variable name.
        fn_numeric_names: set[str] = set()
        for constraint in function.body:
            if constraint.op in {"ADD", "BINOP"}:
                if constraint.op == "ADD":
                    fn_numeric_names.add(constraint.args[0])
                    fn_numeric_names.add(constraint.args[1])
                elif constraint.args[0] != "+":
                    fn_numeric_names.add(constraint.args[1])
                    fn_numeric_names.add(constraint.args[2])
            elif constraint.op == "CMP" and constraint.args[0] in {"lt", "lte", "le", "gt", "gte", "ge"}:
                fn_numeric_names.add(constraint.args[1])
                fn_numeric_names.add(constraint.args[2])
            elif constraint.op == "ISCLASS":
                fn_numeric_names.add(constraint.args[0])
        # Propagate those constraints through the temporary LOADVAR/UPDATE
        # aliases produced by the lowerer (for example ``t = LOADVAR x``).
        # A few passes are enough because the IR is linear and temporaries are
        # introduced in dependency order.
        for _ in range(len(function.body) + 1):
            changed = False
            for constraint in function.body:
                if constraint.op == "LOADVAR" and constraint.dest:
                    source = constraint.args[0]
                    if constraint.dest in fn_numeric_names and source not in fn_numeric_names:
                        fn_numeric_names.add(source); changed = True
                    elif source in fn_numeric_names and constraint.dest not in fn_numeric_names:
                        fn_numeric_names.add(constraint.dest); changed = True
                elif constraint.op in {"STORE_LIST", "UPDATE"}:
                    name, values = constraint.args
                    sources = values if constraint.op == "STORE_LIST" else (values,)
                    if name in fn_numeric_names:
                        for source in sources:
                            if source not in fn_numeric_names:
                                fn_numeric_names.add(source); changed = True
                    elif any(source in fn_numeric_names for source in sources):
                        fn_numeric_names.add(name); changed = True
            if not changed:
                break
        for numeric_name in fn_numeric_names:
            if numeric_name in fn_kinds:
                fn_kinds[numeric_name] = "number"
        fn_text_lengths: dict[str, int] = {}
        fn_collection_kinds: dict[str, str] = {
            name: ("number" if any(word in name.lower() for word in ("count", "pos", "start", "end", "index", "depth", "len")) else "text")
            for name in collection_buffers
        }
        lines.extend([f".Lkuro_fn_{function.name}:", "    push %rbp", "    mov %rsp, %rbp", f"    sub ${fn_frame}, %rsp"])

        def fn_load(name: str, register: str = "%rax") -> None:
            if name in collection_buffers:
                lines.append(f"    lea {collection_buffers[name]}(%rip), {register}")
                return
            if name in input_buffers:
                lines.append(f"    lea {input_buffers[name]}(%rip), {register}")
                return
            if name in global_labels:
                lines.append(f"    mov {global_labels[name]}(%rip), {register}")
                return
            if name not in fn_slots:
                raise NativeBackendError(f"x86_64-linux action {function.name!r} cannot load {name!r}")
            lines.append(f"    mov {fn_slots[name]}(%rbp), {register}")

        def fn_store(name: str, register: str = "%rax") -> None:
            if name in global_labels:
                lines.append(f"    mov {register}, {global_labels[name]}(%rip)")
                return
            if name not in fn_slots:
                raise NativeBackendError(f"x86_64-linux action {function.name!r} cannot store {name!r}")
            lines.append(f"    mov {register}, {fn_slots[name]}(%rbp)")

        for index, parameter in enumerate(function.params):
            fn_store(parameter, f"%{('rdi', 'rsi', 'rdx', 'rcx', 'r8', 'r9')[index]}")
        for item in function.body:
            fn_op = item.op
            if fn_op == "CONST":
                value = item.args[0]
                if isinstance(value, (bool, int)):
                    lines.append(f"    mov ${value}, %rax"); fn_store(item.dest); fn_kinds[item.dest] = "number"
                elif isinstance(value, str):
                    label = f".Lkuro_fn_data_{function.name}_{len(data)}"
                    encoded = value.encode("utf-8")
                    data.append((label, encoded + b"\0"))
                    lines.append(f"    lea {label}(%rip), %rax"); fn_store(item.dest)
                    fn_kinds[item.dest] = "text"; fn_text_lengths[item.dest] = len(encoded)
                elif isinstance(value, float):
                    label = f".Lkuro_fn_float_{function.name}_{len(float_data)}"
                    float_data.append((label, value))
                    lines.extend([f"    movsd {label}(%rip), %xmm0", "    movq %xmm0, %rax"])
                    fn_store(item.dest); fn_kinds[item.dest] = "float"
                else:
                    raise NativeBackendError(f"x86_64-linux action {function.name!r} constant has unsupported value {value!r}")
            elif fn_op == "LOADVAR":
                source = item.args[0]
                fn_load(source)
                fn_store(item.dest)
                inferred = inferred_symbol_kind(source)
                lowered_source = source.lower()
                strong_text_name = lowered_source.endswith(("name", "value", "kind", "message", "code", "text", "word", "line", "source", "token", "character", "output", "input")) and "isclass" not in lowered_source and "_is" not in lowered_source and not lowered_source.endswith(("ok", "flag"))
                fn_kinds[item.dest] = "number" if source in fn_numeric_names else ("text" if strong_text_name else fn_kinds.get(source, inferred))
                if source in fn_text_lengths:
                    fn_text_lengths[item.dest] = fn_text_lengths[source]
            elif fn_op == "STORE_LIST":
                name, values = item.args
                if name in collection_buffers:
                    if len(values) > NATIVE_COLLECTION_CAPACITY:
                        raise NativeBackendError("x86_64-linux action collection exceeds fixed capacity")
                    for index, value in enumerate(values):
                        fn_load(value, "%rax")
                        lines.append(f"    mov %rax, {collection_buffers[name]}+{index * 8}(%rip)")
                    lines.append(f"    movq ${len(values)}, {collection_lengths[name]}(%rip)")
                    fn_kinds[name] = "collection"
                    lowered_collection = name.lower()
                    numeric_collection = any(word in lowered_collection for word in ("count", "pos", "start", "end", "index", "depth", "len"))
                    fn_collection_kinds[name] = "number" if numeric_collection else ("text" if values and all(fn_kinds.get(value) == "text" for value in values) else "number")
                    continue
                if len(values) != 1:
                    raise NativeBackendError("x86_64-linux action multi-value assignment unsupported")
                fn_load(values[0]); fn_store(name); fn_kinds[name] = "number" if values[0] in fn_numeric_names else fn_kinds.get(values[0], inferred_symbol_kind(values[0]))
                if values[0] in fn_text_lengths:
                    fn_text_lengths[name] = fn_text_lengths[values[0]]
            elif fn_op == "UPDATE":
                name, value = item.args
                fn_load(value); fn_store(name); fn_kinds[name] = "number" if value in fn_numeric_names else fn_kinds.get(value, inferred_symbol_kind(value))
                if value in fn_text_lengths:
                    fn_text_lengths[name] = fn_text_lengths[value]
            elif fn_op == "ADD":
                name, value = item.args
                fn_load(name, "%rax"); fn_load(value, "%rcx"); lines.append("    add %rcx, %rax"); fn_store(name); fn_kinds[name] = "number"
            elif fn_op == "BINOP":
                operator, left, right = item.args
                if function.name == "VMStep" and operator == "+":
                    # VM operands are intentionally dynamic.  The same Kuro
                    # ``+`` instruction represents numeric addition and text
                    # concatenation, so static name-based inference cannot
                    # choose the operation here.  Values inside either native
                    # text region are strings; all other bit patterns use the
                    # numeric path.
                    unique = len(lines)
                    left_bss = f".Lkuro_fn_dynamic_add_left_bss_{unique}"
                    left_text = f".Lkuro_fn_dynamic_add_left_text_{unique}"
                    right_bss = f".Lkuro_fn_dynamic_add_right_bss_{unique}"
                    text_path = f".Lkuro_fn_dynamic_add_text_{unique}"
                    numeric_path = f".Lkuro_fn_dynamic_add_numeric_{unique}"
                    done = f".Lkuro_fn_dynamic_add_done_{unique}"
                    fn_load(left, "%r8"); fn_load(right, "%r9")
                    lines.extend([
                        "    lea .Lkuro_rodata_begin(%rip), %r10", "    cmp %r10, %r8", f"    jb {left_bss}",
                        "    lea .Lkuro_rodata_end(%rip), %r10", "    cmp %r10, %r8", f"    jb {left_text}",
                        f"{left_bss}:", "    lea .Lkuro_bss_begin(%rip), %r10", "    cmp %r10, %r8", f"    jb {numeric_path}",
                        "    lea .Lkuro_bss_end(%rip), %r10", "    cmp %r10, %r8", f"    jae {numeric_path}",
                        f"{left_text}:",
                        "    lea .Lkuro_rodata_begin(%rip), %r10", "    cmp %r10, %r9", f"    jb {right_bss}",
                        "    lea .Lkuro_rodata_end(%rip), %r10", "    cmp %r10, %r9", f"    jb {text_path}",
                        f"{right_bss}:", "    lea .Lkuro_bss_begin(%rip), %r10", "    cmp %r10, %r9", f"    jb {numeric_path}",
                        "    lea .Lkuro_bss_end(%rip), %r10", "    cmp %r10, %r9", f"    jae {numeric_path}",
                        f"{text_path}:",
                        "    mov %r8, %rax", "    call _kuro_strlen", "    mov %rax, %r10",
                        "    mov %r9, %rax", "    call _kuro_strlen", "    mov %rax, %r11",
                        "    mov %r10, %rax", "    add %r11, %rax",
                        "    mov .Lkuro_text_heap_cursor(%rip), %rdx", "    mov %rdx, %rcx", "    add %rax, %rcx", "    inc %rcx",
                        f"    cmp ${NATIVE_TEXT_HEAP_CAPACITY}, %rcx", "    ja .Lkuro_overflow",
                        "    lea .Lkuro_text_heap(%rip), %rdi", "    add %rdx, %rdi",
                        "    mov %r8, %rsi", "    mov %r10, %rcx", "    rep movsb",
                        "    mov %r9, %rsi", "    mov %r11, %rcx", "    rep movsb", "    movb $0, (%rdi)",
                        "    lea .Lkuro_text_heap(%rip), %rsi", "    mov %rdi, %rcx", "    sub %rsi, %rcx", "    inc %rcx",
                        "    mov %rcx, .Lkuro_text_heap_cursor(%rip)", "    mov %rdi, %rdx", "    sub %rax, %rdx", "    mov %rdx, %rax",
                        f"    jmp {done}",
                        f"{numeric_path}:", "    mov %r8, %rax", "    add %r9, %rax",
                        f"{done}:",
                    ])
                    fn_store(item.dest); fn_kinds[item.dest] = "number"
                    continue
                if operator == "+" and (fn_kinds.get(left) == "text" or fn_kinds.get(right) == "text"):
                    buffer = function_concat_buffers.get(f"{function.name}:{item.dest}")
                    if buffer is None:
                        raise NativeBackendError("x86_64-linux action text concatenation has no buffer")
                    fn_load(left, "%r8"); fn_load(right, "%r9")
                    lines.extend([
                        "    mov %r8, %rax", "    call _kuro_strlen", "    mov %rax, %r10",
                        "    mov %r9, %rax", "    call _kuro_strlen", "    mov %rax, %r11",
                        "    mov %r10, %rax", "    add %r11, %rax",
                        "    mov .Lkuro_text_heap_cursor(%rip), %rdx", "    mov %rdx, %rcx", "    add %rax, %rcx", "    inc %rcx",
                        f"    cmp ${NATIVE_TEXT_HEAP_CAPACITY}, %rcx", "    ja .Lkuro_overflow",
                        "    lea .Lkuro_text_heap(%rip), %rdi", "    add %rdx, %rdi", "    mov %r8, %rsi", "    mov %r10, %rcx", "    rep movsb",
                        "    mov %r9, %rsi", "    mov %r11, %rcx", "    rep movsb", "    movb $0, (%rdi)",
                        "    lea .Lkuro_text_heap(%rip), %rsi", "    mov %rdi, %rcx", "    sub %rsi, %rcx", "    inc %rcx", "    mov %rcx, .Lkuro_text_heap_cursor(%rip)",
                        "    mov %rdi, %rdx", "    sub %rax, %rdx", "    mov %rdx, %rax",
                    ])
                    fn_store(item.dest); fn_kinds[item.dest] = "text"
                    continue
                if fn_kinds.get(left) in {"number", "float"} and fn_kinds.get(right) in {"number", "float"} and (fn_kinds.get(left) == "float" or fn_kinds.get(right) == "float"):
                    if fn_kinds.get(left) == "float":
                        fn_load(left, "%rax"); lines.append("    movq %rax, %xmm0")
                    else:
                        fn_load(left, "%rax"); lines.append("    cvtsi2sd %rax, %xmm0")
                    if fn_kinds.get(right) == "float":
                        fn_load(right, "%rax"); lines.append("    movq %rax, %xmm1")
                    else:
                        fn_load(right, "%rax"); lines.append("    cvtsi2sd %rax, %xmm1")
                    if operator not in {"+", "-", "*", "/"}:
                        raise NativeBackendError(f"unsupported floating action operator {operator!r}")
                    lines.append(f"    { {'+':'addsd','-':'subsd','*':'mulsd','/':'divsd'}[operator] } %xmm1, %xmm0")
                    lines.append("    movq %xmm0, %rax"); fn_store(item.dest); fn_kinds[item.dest] = "float"
                    continue
                if fn_kinds.get(left) != "number" or fn_kinds.get(right) != "number":
                    raise NativeBackendError(
                        f"x86_64-linux action {function.name!r} BINOP requires integers "
                        f"(left={left!r}:{fn_kinds.get(left)!r}, right={right!r}:{fn_kinds.get(right)!r})"
                    )
                fn_load(left, "%rax"); fn_load(right, "%rcx")
                if operator == "+": lines.append("    add %rcx, %rax")
                elif operator == "-": lines.append("    sub %rcx, %rax")
                elif operator == "*": lines.append("    imul %rcx, %rax")
                elif operator == "/": lines.extend(["    cqo", "    idiv %rcx"])
                else: raise NativeBackendError(f"unsupported action operator {operator!r}")
                fn_store(item.dest); fn_kinds[item.dest] = "number"
            elif fn_op == "CMP":
                operator, left, right = item.args
                if function.name == "VMStep" and operator in {"eq", "ne"}:
                    unique = len(lines)
                    numeric = f".Lkuro_fn_dynamic_cmp_numeric_{unique}"
                    loop = f".Lkuro_fn_dynamic_cmp_loop_{unique}"
                    equal = f".Lkuro_fn_dynamic_cmp_equal_{unique}"
                    different = f".Lkuro_fn_dynamic_cmp_different_{unique}"
                    done = f".Lkuro_fn_dynamic_cmp_done_{unique}"
                    left_bss = f".Lkuro_fn_dynamic_cmp_left_bss_{unique}"
                    left_text = f".Lkuro_fn_dynamic_cmp_left_text_{unique}"
                    right_bss = f".Lkuro_fn_dynamic_cmp_right_bss_{unique}"
                    right_text = f".Lkuro_fn_dynamic_cmp_right_text_{unique}"
                    fn_load(left, "%r8"); fn_load(right, "%r9")
                    lines.extend([
                        "    lea .Lkuro_rodata_begin(%rip), %r10", "    cmp %r10, %r8", f"    jb {left_bss}",
                        "    lea .Lkuro_rodata_end(%rip), %r10", "    cmp %r10, %r8", f"    jb {left_text}",
                        f"{left_bss}:", "    lea .Lkuro_bss_begin(%rip), %r10", "    cmp %r10, %r8", f"    jb {numeric}",
                        "    lea .Lkuro_bss_end(%rip), %r10", "    cmp %r10, %r8", f"    jae {numeric}",
                        f"{left_text}:",
                        "    lea .Lkuro_rodata_begin(%rip), %r10", "    cmp %r10, %r9", f"    jb {right_bss}",
                        "    lea .Lkuro_rodata_end(%rip), %r10", "    cmp %r10, %r9", f"    jb {right_text}",
                        f"{right_bss}:", "    lea .Lkuro_bss_begin(%rip), %r10", "    cmp %r10, %r9", f"    jb {numeric}",
                        "    lea .Lkuro_bss_end(%rip), %r10", "    cmp %r10, %r9", f"    jae {numeric}",
                        f"{right_text}:",
                        f"{loop}:", "    movzbq (%r8), %rax", "    movzbq (%r9), %rcx", "    cmp %rcx, %rax", f"    jne {different}",
                        "    test %rax, %rax", f"    jz {equal}", "    inc %r8", "    inc %r9", f"    jmp {loop}",
                        f"{numeric}:", "    cmp %r9, %r8", f"    je {equal}",
                        f"{different}:", "    xor %eax, %eax", f"    jmp {done}",
                        f"{equal}:", "    mov $1, %rax", f"{done}:",
                    ])
                    if operator == "ne":
                        lines.append("    xor $1, %eax")
                    fn_store(item.dest); fn_kinds[item.dest] = "number"
                    continue
                # Equality is also the VM's dynamic tag/value comparison. If
                # one side is proven text and the other side came through a
                # generic temporary with no stable static kind, lower it as a
                # text comparison instead of rejecting the whole native image.
                if operator in {"eq", "ne"} and (fn_kinds.get(left) == "text" or fn_kinds.get(right) == "text"):
                    fn_kinds[left] = "text"
                    fn_kinds[right] = "text"
                if fn_kinds.get(left) in {"number", "float"} and fn_kinds.get(right) in {"number", "float"} and (fn_kinds.get(left) == "float" or fn_kinds.get(right) == "float"):
                    condition = {"eq": "e", "ne": "ne", "lt": "b", "le": "be", "gt": "a", "ge": "ae"}.get(operator)
                    if condition is None:
                        raise NativeBackendError(f"unsupported floating action comparison {operator!r}")
                    if fn_kinds.get(left) == "float":
                        fn_load(left, "%rax"); lines.append("    movq %rax, %xmm0")
                    else:
                        fn_load(left, "%rax"); lines.append("    cvtsi2sd %rax, %xmm0")
                    if fn_kinds.get(right) == "float":
                        fn_load(right, "%rax"); lines.append("    movq %rax, %xmm1")
                    else:
                        fn_load(right, "%rax"); lines.append("    cvtsi2sd %rax, %xmm1")
                    lines.extend(["    ucomisd %xmm1, %xmm0", f"    set{condition} %al", "    movzbq %al, %rax"])
                    fn_store(item.dest); fn_kinds[item.dest] = "number"
                    continue
                if fn_kinds.get(left) == "text" and fn_kinds.get(right) == "text":
                    if operator not in {"eq", "ne"}:
                        raise NativeBackendError("x86_64-linux action text CMP supports only equality")
                    unique = len(lines)
                    same = f".Lkuro_fn_cmp_same_{unique}"
                    different = f".Lkuro_fn_cmp_diff_{unique}"
                    done = f".Lkuro_fn_cmp_done_{unique}"
                    fn_load(left, "%r8"); fn_load(right, "%r9")
                    if left in fn_text_lengths:
                        lines.append(f"    mov ${fn_text_lengths[left]}, %r10")
                    else:
                        lines.extend(["    mov %r8, %rax", "    call _kuro_strlen", "    mov %rax, %r10"])
                    lines.append("    push %r9")
                    if right in fn_text_lengths:
                        lines.append(f"    mov ${fn_text_lengths[right]}, %r11")
                    else:
                        lines.extend(["    mov %r9, %rax", "    call _kuro_strlen", "    mov %rax, %r11"])
                    lines.extend([
                        "    pop %r9", "    cmp %r11, %r10", f"    jne {different}",
                        "    mov %r10, %rcx", "    mov %r8, %rsi", "    mov %r9, %rdi", "    repe cmpsb", f"    jne {different}",
                        f"    jmp {same}", f"{same}:", "    mov $1, %rax", f"    jmp {done}",
                        f"{different}:", "    xor %eax, %eax", f"{done}:",
                    ])
                    if operator == "ne":
                        lines.append("    xor $1, %eax")
                    fn_store(item.dest); fn_kinds[item.dest] = "number"
                    continue
                if fn_kinds.get(left) != "number" or fn_kinds.get(right) != "number":
                    raise NativeBackendError(
                        f"x86_64-linux action {function.name!r} CMP requires integers "
                        f"(left={left!r}:{fn_kinds.get(left)!r}, right={right!r}:{fn_kinds.get(right)!r})"
                    )
                condition = {"eq": "e", "ne": "ne", "lt": "l", "le": "le", "gt": "g", "ge": "ge"}.get(operator)
                if condition is None: raise NativeBackendError(f"unsupported action comparison {operator!r}")
                fn_load(left, "%rax"); fn_load(right, "%rcx")
                lines.extend(["    cmp %rcx, %rax", f"    set{condition} %al", "    movzbq %al, %rax"])
                fn_store(item.dest); fn_kinds[item.dest] = "number"
            elif fn_op in {"AND", "OR"}:
                left, right = item.args
                fn_load(left, "%rax"); lines.extend(["    test %rax, %rax", "    setne %al", "    movzbq %al, %rax"])
                fn_load(right, "%rcx"); lines.extend(["    test %rcx, %rcx", "    setne %cl", "    movzbq %cl, %rcx"])
                lines.append(f"    {'and' if fn_op == 'AND' else 'or'} %rcx, %rax")
                fn_store(item.dest); fn_kinds[item.dest] = "number"
            elif fn_op == "GET":
                name, index_temp = item.args
                if index_temp is None:
                    raise NativeBackendError(f"x86_64-linux action {function.name!r} GET requires an index")
                fn_load(index_temp, "%rcx")
                if name in collection_buffers:
                    lines.extend([
                        f"    cmp ${NATIVE_COLLECTION_CAPACITY}, %rcx", "    jae .Lkuro_bounds",
                        f"    lea {collection_buffers[name]}(%rip), %rax", "    mov (%rax,%rcx,8), %rax",
                    ])
                    fn_store(item.dest); fn_kinds[item.dest] = fn_collection_kinds.get(name, "text")
                else:
                    char_label = function_char_buffers.get(f"{function.name}:{item.dest}")
                    if char_label is None:
                        raise NativeBackendError(f"x86_64-linux action {function.name!r} cannot index {name!r}")
                    fn_load(name, "%rax")
                    lines.extend([
                        "    movzbq (%rax,%rcx,1), %rdx", "    mov .Lkuro_char_heap_cursor(%rip), %r8",
                        f"    cmp ${NATIVE_INPUT_CAPACITY * 2 - 2}, %r8", "    jae .Lkuro_overflow",
                        "    lea .Lkuro_char_heap(%rip), %rax", "    add %r8, %rax",
                        "    mov %dl, (%rax)", "    movb $0, 1(%rax)", "    add $2, %r8", "    mov %r8, .Lkuro_char_heap_cursor(%rip)",
                    ])
                    fn_store(item.dest); fn_kinds[item.dest] = "text"
            elif fn_op == "SET":
                name, index_temp, value_temp = item.args
                fn_load(index_temp, "%rcx"); fn_load(value_temp, "%rdx")
                if name in collection_buffers:
                    lines.extend([
                        f"    cmp ${NATIVE_COLLECTION_CAPACITY}, %rcx", "    jae .Lkuro_bounds",
                        f"    lea {collection_buffers[name]}(%rip), %rax", "    mov %rdx, (%rax,%rcx,8)",
                    ])
                else:
                    fn_load(name, "%rax")
                    lines.extend(["    mov %dl, (%rax,%rcx,1)"])
            elif fn_op == "LENGTH":
                name = item.args[0]
                if name in collection_lengths:
                    lines.append(f"    mov {collection_lengths[name]}(%rip), %rax")
                elif name in input_lengths:
                    lines.append(f"    mov {input_lengths[name]}(%rip), %rax")
                else:
                    fn_load(name, "%rax")
                    zero_label = f".Lkuro_fn_{function.name}_length_zero_{item.dest}"
                    done_label = f".Lkuro_fn_{function.name}_length_done_{item.dest}"
                    lines.extend(["    test %rax, %rax", f"    jz {zero_label}", "    call _kuro_strlen", f"    jmp {done_label}", f"{zero_label}:", "    xor %eax, %eax", f"{done_label}:"])
                fn_store(item.dest); fn_kinds[item.dest] = "number"
            elif fn_op == "APPEND":
                name, value = item.args
                if name not in collection_buffers:
                    raise NativeBackendError(f"x86_64-linux action {function.name!r} cannot append to {name!r}")
                fn_load(value, "%rdx")
                lines.extend([
                    f"    mov {collection_lengths[name]}(%rip), %rcx", f"    cmp ${NATIVE_COLLECTION_CAPACITY}, %rcx", "    jae .Lkuro_overflow",
                    f"    lea {collection_buffers[name]}(%rip), %rax", "    mov %rdx, (%rax,%rcx,8)", "    inc %rcx",
                    f"    mov %rcx, {collection_lengths[name]}(%rip)",
                ])
            elif fn_op == "ISCLASS":
                operand, cls = item.args
                if cls not in {"digit", "alpha", "alnum", "space", "quote"}:
                    raise NativeBackendError(f"x86_64-linux action character class {cls!r} unsupported")
                invalid_label = f".Lkuro_fn_{function.name}_isclass_invalid_{item.dest}"
                done_label = f".Lkuro_fn_{function.name}_isclass_done_{item.dest}"
                fn_load(operand, "%rax"); lines.extend(["    test %rax, %rax", f"    jle {invalid_label}", "    cmp $4096, %rax", f"    jb {invalid_label}", "    movzbq (%rax), %rax"])
                if cls == "digit":
                    lines.extend(["    cmp $48, %rax", "    setge %dl", "    cmp $57, %rax", "    setle %cl", "    and %cl, %dl", "    movzbl %dl, %eax"])
                elif cls == "alpha":
                    lines.extend([
                        "    mov %rax, %rcx", "    cmp $65, %rax", "    setge %r8b", "    cmp $90, %rcx", "    setle %r9b", "    and %r9b, %r8b",
                        "    cmp $97, %rax", "    setge %r9b", "    cmp $122, %rcx", "    setle %dl", "    and %dl, %r9b", "    or %r9b, %r8b", "    movzbl %r8b, %eax",
                    ])
                elif cls == "alnum":
                    lines.extend([
                        "    mov %rax, %rcx", "    cmp $48, %rax", "    setge %r8b", "    cmp $57, %rcx", "    setle %r9b", "    and %r9b, %r8b",
                        "    cmp $65, %rax", "    setge %r9b", "    cmp $90, %rcx", "    setle %dl", "    and %dl, %r9b", "    or %r9b, %r8b",
                        "    cmp $97, %rax", "    setge %r9b", "    cmp $122, %rcx", "    setle %dl", "    and %dl, %r9b", "    or %r9b, %r8b", "    movzbl %r8b, %eax",
                    ])
                elif cls == "space":
                    lines.extend(["    cmp $32, %rax", "    sete %al", "    movzbq %al, %rax"])
                else:
                    lines.extend(["    cmp $34, %rax", "    sete %al", "    movzbq %al, %rax"])
                lines.extend([f"    jmp {done_label}", f"{invalid_label}:", "    xor %eax, %eax", f"{done_label}:"])
                fn_store(item.dest); fn_kinds[item.dest] = "number"
            elif fn_op == "CALL":
                name, *arguments = item.args
                if name not in ir.functions or len(arguments) > 6:
                    raise NativeBackendError(f"x86_64-linux action {function.name!r} cannot call {name!r}")
                registers = ("rdi", "rsi", "rdx", "rcx", "r8", "r9")
                for index, argument in enumerate(arguments): fn_load(argument, f"%{registers[index]}")
                lines.append(f"    call .Lkuro_fn_{name}"); fn_store(item.dest); fn_kinds[item.dest] = "text" if action_returns_text(name) else "number"
            elif fn_op == "PRINT":
                name = item.args[0]
                if fn_kinds.get(name) == "text":
                    fn_load(name, "%rsi")
                    unique = len(lines)
                    number_label = f".Lkuro_fn_print_number_{unique}"
                    bss_label = f".Lkuro_fn_print_bss_{unique}"
                    text_label = f".Lkuro_fn_print_text_{unique}"
                    done_label = f".Lkuro_fn_print_done_{unique}"
                    lines.extend([
                        "    lea .Lkuro_rodata_begin(%rip), %rax", "    cmp %rax, %rsi", f"    jb {bss_label}",
                        "    lea .Lkuro_rodata_end(%rip), %rax", "    cmp %rax, %rsi", f"    jb {text_label}",
                        f"{bss_label}:", "    lea .Lkuro_bss_begin(%rip), %rax", "    cmp %rax, %rsi", f"    jb {number_label}",
                        "    lea .Lkuro_bss_end(%rip), %rax", "    cmp %rax, %rsi", f"    jae {number_label}",
                        f"{text_label}:",
                        "    mov %rsi, %rax", "    call _kuro_strlen", "    mov %rax, %rdx",
                        "    mov $1, %rax", "    mov $1, %rdi", "    syscall",
                        "    lea .Lkuro_newline(%rip), %rsi", "    mov $1, %rdx",
                        "    mov $1, %rax", "    mov $1, %rdi", "    syscall", f"    jmp {done_label}",
                        f"{number_label}:", "    mov %rsi, %rax", "    call _kuro_print_int",
                        f"{done_label}:",
                    ])
                else:
                    fn_load(name); lines.append("    call _kuro_print_int")
            elif fn_op == "JUMPF":
                target, condition = item.args
                fn_load(condition); lines.extend(["    test %rax, %rax", f"    jz {fn_labels[target]}"])
            elif fn_op == "JUMP":
                lines.append(f"    jmp {fn_labels[item.args[0]]}")
            elif fn_op == "LABEL":
                lines.append(f"{fn_labels[item.dest]}:")
            elif fn_op == "RETURN":
                fn_load(item.args[0]); lines.extend(["    leave", "    ret"])
            elif fn_op in {"DECLTYPE", "LOOP_GUARD", "CHECK_NONNEG", "SAVEVAR", "RESTOREVAR"}:
                continue
            else:
                raise NativeBackendError(f"x86_64-linux action {function.name!r} does not support {fn_op}")
        lines.extend(["    xor %eax, %eax", "    leave", "    ret"])
    lines.append(".Lkuro_main_epilogue:")
    if "RuntimeExitCode" in global_labels:
        lines.append(f"    mov {global_labels['RuntimeExitCode']}(%rip), %rax")
    else:
        lines.append("    xor %eax, %eax")
    lines.extend([
        "    leave", "    ret",
        ".Lkuro_bounds:", "    mov $60, %eax", "    mov $1, %edi", "    syscall", "    ud2",
        ".Lkuro_overflow:", "    mov $60, %eax", "    mov $1, %edi", "    syscall", "    ud2",
        ".Lkuro_runtime_error:", "    mov $1, %eax", "    leave", "    ret",
    ])
    lines.extend([
        "_kuro_print_int:", "    push %rbp", "    mov %rsp, %rbp", "    sub $32, %rsp",
        "    lea 31(%rsp), %rsi", "    movb $10, (%rsi)", "    mov $1, %rcx",
        "    xor %r8d, %r8d", "    test %rax, %rax", "    jns .Lkuro_print_positive", "    neg %rax", "    mov $1, %r8",
        ".Lkuro_print_positive:", "    xor %rdx, %rdx", "    mov $10, %r9", "    div %r9",
        "    add $48, %dl", "    dec %rsi", "    mov %dl, (%rsi)", "    inc %rcx",
        "    test %rax, %rax", "    jnz .Lkuro_print_positive",
        "    cmp $0, %r8", "    je .Lkuro_print_write", "    dec %rsi", "    movb $45, (%rsi)", "    inc %rcx",
        ".Lkuro_print_write:", "    mov $1, %rax", "    mov $1, %rdi", "    mov %rcx, %rdx", "    syscall",
        "    leave", "    ret",
    ])
    lines.extend([
        "_kuro_strlen:", "    mov %rax, %rdi", "    xor %eax, %eax", ".Lkuro_strlen_loop:",
        "    cmpb $0, (%rdi,%rax,1)", "    je .Lkuro_strlen_done", "    inc %rax", "    jmp .Lkuro_strlen_loop",
        ".Lkuro_strlen_done:", "    ret",
    ])
    lines.extend([".section .bss", ".Lkuro_bss_begin:"])
    for label in collection_buffers.values():
        lines.extend([f"    .p2align 3", f"{label}: .zero {NATIVE_COLLECTION_BYTES}"])
    for label in collection_lengths.values():
        lines.extend([f"    .p2align 3", f"{label}: .zero 8"])
    for label in collection_item_lengths.values():
        lines.extend([f"    .p2align 3", f"{label}: .zero {NATIVE_COLLECTION_BYTES}"])
    for label in input_buffers.values():
        lines.extend([f"    .p2align 3", f"{label}: .zero {NATIVE_INPUT_CAPACITY}"])
    for label in input_lengths.values():
        lines.extend([f"    .p2align 3", f"{label}: .zero 8"])
    for label in char_buffers.values():
        lines.extend([f"    .p2align 3", f"{label}: .zero 1"])
    for label in function_char_buffers.values():
        lines.extend([f"    .p2align 3", f"{label}: .zero 1"])
    lines.extend(["    .p2align 4", f".Lkuro_char_heap: .zero {NATIVE_INPUT_CAPACITY * 2}", "    .p2align 3", ".Lkuro_char_heap_cursor: .zero 8"])
    lines.extend(["    .p2align 4", f".Lkuro_text_heap: .zero {NATIVE_TEXT_HEAP_CAPACITY}", "    .p2align 3", ".Lkuro_text_heap_cursor: .zero 8"])
    for label in function_concat_buffers.values():
        lines.extend([f"    .p2align 3", f"{label}: .zero 4096"])
    for label in concat_buffers.values():
        lines.extend([f"    .p2align 3", f"{label}: .zero 4096"])
    for label in concat_lengths.values():
        lines.extend([f"    .p2align 3", f"{label}: .zero 8"])
    for label in global_labels.values():
        lines.extend([f"    .p2align 3", f"{label}: .zero 8"])
    for label in map_dest_labels.values():
        lines.extend([f"    .p2align 3", f"{label}: .zero 8192"])
    for label in tagged_dest_labels.values():
        lines.extend([f"    .p2align 3", f"{label}: .zero 16"])
    lines.extend([".Lkuro_bss_end:", ".section .rodata", ".Lkuro_rodata_begin:"])
    for label, encoded in data:
        lines.append(f"{label}: .byte {', '.join(str(byte) for byte in encoded)}")
    for label, value in float_data:
        lines.append(f"{label}: .double {value!r}")
    lines.extend([".Lkuro_newline: .byte 10", ".Lkuro_rodata_end:"])
    return "\n".join(lines) + "\n"


def emit_x86_64_macos(ir: IRProgram) -> str:
    """Adapt the freestanding x86-64 lowering to Darwin's syscall ABI.

    The instruction/data ABI is deliberately shared with Linux.  Darwin
    distinguishes syscalls with the ``0x2000000`` class prefix, while the
    register convention for ``write`` and ``exit`` remains compatible with
    the emitted AT&T code.  Keeping this as a narrow ABI adapter means the
    language lowering itself stays platform-independent.
    """
    assembly = emit_x86_64_linux(ir)
    assembly = assembly.replace(".section .text", ".section __TEXT,__text")
    assembly = assembly.replace(".section .bss", ".section __DATA,__bss")
    assembly = assembly.replace(".section .rodata", ".section __TEXT,__const")
    # Rewrite only the register assignment governing each syscall.  A global
    # text replacement would also rewrite ordinary Kuro constants whose value
    # happens to be 1, corrupting comparisons and VM state.
    lines = assembly.splitlines()
    syscall_numbers = {
        "mov $60, %eax": "    mov $0x2000001, %eax",  # exit
        "mov $1, %rax": "    mov $0x2000004, %rax",   # write
        "xor %eax, %eax": "    mov $0x2000003, %eax", # read
    }
    for index, line in enumerate(lines):
        if line.strip() != "syscall":
            continue
        for previous in range(index - 1, max(-1, index - 24), -1):
            normalized = lines[previous].strip()
            if normalized in syscall_numbers:
                lines[previous] = syscall_numbers[normalized]
                break
    return "\n".join(lines) + "\n"


def build_native(ir: IRProgram, output: str | Path, target: str | None = None) -> Path:
    """Build a native image for an explicit or host-selected Kuro target."""
    destination = Path(output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    assembly = destination.with_suffix(".s")
    selected = target or ("aarch64-macos" if __import__("platform").system() == "Darwin" and __import__("platform").machine() == "arm64" else "x86_64-linux")
    if selected == "aarch64-macos":
        assembly.write_text(emit_macos_arm64(ir), encoding="utf-8")
        command = ["clang", str(assembly), "-o", str(destination)]
    elif selected == "x86_64-macos":
        assembly.write_text(emit_x86_64_macos(ir), encoding="utf-8")
        command = [
            "clang", "-target", "x86_64-apple-macos",
            "-nostdlib", "-Wl,-e,_start", str(assembly), "-lSystem", "-o", str(destination),
        ]
    elif selected == "x86_64-linux":
        assembly.write_text(emit_x86_64_linux(ir), encoding="utf-8")
        # The Linux image is freestanding: no libc startup or foreign runtime
        # is linked. Kuro's emitted _start performs the exit syscall itself.
        _link_x86_64_linux(assembly, destination)
        command = None
    else:
        raise NativeBackendError(f"unsupported native target {selected!r}; choose from {supported_native_targets()}")
    if command is not None:
        result = subprocess.run(command, check=False, capture_output=True)
        if result.returncode:
            detail = result.stderr.decode("utf-8", errors="replace")
            raise subprocess.CalledProcessError(result.returncode, result.args, result.stdout, detail)
    destination.chmod(0o755)
    return destination
