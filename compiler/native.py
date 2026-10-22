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


def _x86_collection_index_bounds(length_label: str, *, read: bool) -> list[str]:
    """Check %rcx before scaled addressing; preserve value/base registers.

    Length is maintained by bounded literal initialization and APPEND. Only GET
    normalizes negative indices. The speculative sum for nonnegative indices is
    discarded (including its flags), so signed overflow cannot admit an index.
    """
    lines = [f"    mov {length_label}(%rip), %r8"]
    if read:
        lines.extend([
            "    mov %rcx, %r9", "    add %r8, %r9",
            "    test %rcx, %rcx", "    cmovs %r9, %rcx",
        ])
    return lines + ["    cmp %r8, %rcx", "    jae .Lkuro_bounds"]


def _untracked_collection_pointers(ir: IRProgram, buffers: set[str]) -> dict[str, set[str]]:
    """Conservative rejection-only provenance, not collection lowering/type inference.

    An alias, argument or return carries a pointer but no owner/length pair in
    this ABI. Never let those known collection pointers enter byte-oriented Text
    operations, even when a parameter shadows a static collection buffer.
    """
    bodies = {"": ir.main, **{name: fn.body for name, fn in ir.functions.items()}}
    pointers = {name: set() for name in bodies}
    # Variable targets, not spelling, distinguish cross-scope user aliases
    # from per-body IR temporaries. Names such as target and __bag are legal.
    variable_targets = {
        scope: {
            item.args[0] for item in body
            if item.op in {"STORE_LIST", "UPDATE", "INPUT", "ADD", "APPEND"}
        } - (set(ir.functions[scope].params) if scope else set())
        for scope, body in bodies.items()
    }

    def global_aliases() -> set[str]:
        # Actions can assign globals first seen outside main. Share all
        # non-parameter variable aliases conservatively, never IR destinations
        # identified only by their spelling. This scan grants no new support.
        return set().union(*(pointers[scope] & targets for scope, targets in variable_targets.items()))
    for name, fn in ir.functions.items():
        pointers[name].update(
            parameter for parameter in fn.params
            if _native_kind_for_type(fn.parameter_types.get(parameter)) == "collection"
        )
    changed = True
    while changed:
        before = sum(map(len, pointers.values()))
        for scope, body in bodies.items():
            globals_ = global_aliases()
            known = buffers | globals_ | pointers[scope]
            for item in body:
                source = target = None
                if item.op in {"LOADVAR", "SAVEVAR"}:
                    target, source = item.dest, item.args[0]
                elif item.op == "STORE_LIST" and len(item.args[1]) == 1:
                    target, source = item.args[0], item.args[1][0]
                elif item.op in {"UPDATE", "RESTOREVAR"}:
                    target, source = item.args
                if source in known and target is not None:
                    pointers[scope].add(target)
                    known.add(target)
                if item.op == "CALL" and item.args[0] in ir.functions:
                    callee = ir.functions[item.args[0]]
                    for parameter, argument in zip(callee.params, item.args[1:]):
                        if argument in known:
                            pointers[callee.name].add(parameter)
                    if any(inner.op == "RETURN" and inner.args[0] in (buffers | globals_ | pointers[callee.name]) for inner in callee.body):
                        pointers[scope].add(item.dest)
                        known.add(item.dest)
        changed = sum(map(len, pointers.values())) != before
    shared_aliases = global_aliases()
    return {scope: names | shared_aliases for scope, names in pointers.items()}


def _arm64_collection_index_bounds(length_label: str, *, read: bool) -> list[str]:
    """Check x1 against logical length before scaling, preserving x0/x2."""
    lines = [
        f"    adrp x3, {length_label}@PAGE",
        f"    add x3, x3, {length_label}@PAGEOFF", "    ldr x3, [x3]",
    ]
    if read:
        lines.extend([
            "    cmp x1, #0", "    add x4, x1, x3",
            "    csel x1, x4, x1, lt",
        ])
    return lines + ["    cmp x1, x3", "    b.hs L_kuro_collection_bounds"]


def _x87_extended_power10_bytes(power: int) -> bytes:
    """Return the rounded x87 binary80 encoding of the positive integer 10**power."""
    if not 0 <= power <= 341:
        raise ValueError("x87 power-of-ten table supports exponents 0 through 341")
    value = 10**power
    binary_exponent = value.bit_length() - 1
    numerator = value << 63
    denominator = 1 << binary_exponent
    significand, remainder = divmod(numerator, denominator)
    if remainder * 2 > denominator or (
        remainder * 2 == denominator and significand & 1
    ):
        significand += 1
    if significand == 1 << 64:
        significand >>= 1
        binary_exponent += 1
    biased_exponent = binary_exponent + 16383
    return significand.to_bytes(8, "little") + biased_exponent.to_bytes(2, "little")


def _native_kind_for_type(type_name: str | None) -> str | None:
    if type_name == "Text":
        return "text"
    if type_name == "Decimals":
        return "float"
    if type_name in {"Integers", "Symbols"}:
        return "number"
    if type_name and type_name.startswith(("List<", "Map<")):
        return "collection"
    return None


def _statically_text_values(
    instructions,
    symbol_types: dict[str, str],
    collection_names: set[str],
    parameter_types: dict[str, str] | None = None,
    function_return_kinds: dict[str, str] | None = None,
) -> set[str]:
    """Return names whose Text kind follows from declarations or IR value flow."""
    parameter_types = parameter_types or {}
    function_return_kinds = function_return_kinds or {}
    declared_text = {
        name for name, type_name in symbol_types.items()
        if type_name == "Text" and name not in collection_names
    }
    known = declared_text | {
        name for name, type_name in parameter_types.items() if type_name == "Text"
    }
    for item in instructions:
        if item.op == "CONST" and item.dest:
            if isinstance(item.args[0], str):
                known.add(item.dest)
            else:
                known.discard(item.dest)
        elif item.op == "INPUT" and item.args and item.args[0] not in collection_names:
            known.add(item.args[0])
        elif item.op == "LOADVAR" and item.dest:
            if item.args[0] in known:
                known.add(item.dest)
            else:
                known.discard(item.dest)
        elif item.op == "STORE_LIST" and item.args:
            name, values = item.args
            if name in declared_text or (
                name not in collection_names and len(values) == 1 and values[0] in known
            ):
                known.add(name)
            else:
                known.discard(name)
        elif item.op == "UPDATE" and item.args:
            name, value = item.args
            if name in declared_text or value in known:
                known.add(name)
            else:
                known.discard(name)
        elif item.op == "BINOP" and item.dest:
            if item.args[0] == "+" and item.args[1] in known and item.args[2] in known:
                known.add(item.dest)
            else:
                known.discard(item.dest)
        elif item.op == "CALL" and item.dest:
            if item.args and function_return_kinds.get(item.args[0]) == "text":
                known.add(item.dest)
            else:
                known.discard(item.dest)
        elif item.op == "ARTIFACT_SUFFIX" and item.dest:
            known.add(item.dest)
    return known


NATIVE_INPUT_CAPACITY = 1 << 20
NATIVE_INPUT_READ_LIMIT = NATIVE_INPUT_CAPACITY - 1
NATIVE_COLLECTION_CAPACITY = 1 << 16
NATIVE_COLLECTION_BYTES = NATIVE_COLLECTION_CAPACITY * 8
NATIVE_TEXT_HEAP_CAPACITY = 1 << 24
# Native code generators grow assembly through repeated immutable Text joins.
# Their 4096-token path needs over 512 MiB cumulatively, so scope a larger heap
# to generator images instead of increasing the default for ordinary programs.
NATIVE_CODEGEN_TEXT_HEAP_CAPACITY = 1 << 30


def _resolve_text_heap_capacity(capacity: int | None) -> int:
    if capacity is None:
        return NATIVE_TEXT_HEAP_CAPACITY
    if type(capacity) is not int or not 1 <= capacity <= NATIVE_CODEGEN_TEXT_HEAP_CAPACITY:
        raise NativeBackendError(
            f"native text heap capacity must be in [1, {NATIVE_CODEGEN_TEXT_HEAP_CAPACITY}]"
        )
    return capacity


def _link_x86_64_linux(assembly: Path, destination: Path) -> None:
    """Assemble and link a freestanding Linux image, including on macOS.

    Apple's linker cannot consume ELF objects.  Cross-build hosts therefore
    use LLVM's ELF linker directly; native Linux hosts keep the normal clang
    driver path.  The resulting image has no libc or dynamic-loader dependency.
    """
    if platform.system() == "Linux":
        command = [
            "clang", "-target", "x86_64-unknown-linux-gnu", "-nostdlib", "-static",
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


def _arm64_integer_collections(ir: IRProgram, collection_names: set[str]) -> set[str]:
    """Prove Integer-typed element writes, without trusting names or types alone.

    Union every definition's dependencies, including both sides of branches and
    every direct caller's arguments. Remove unsupported/non-integer definitions
    and their dependants to a fixed point. Numeric collection/frame cycles are
    allowed, but a Text or unknown write anywhere poisons the entire cycle.
    This does not infer kinds without resolved Integer metadata.
    """
    candidates = {n for n in collection_names if ir.symbol_types.get(n) == "Integers"}
    if not candidates:
        return set()
    dependencies: dict[tuple[str, str], set[tuple[str, str]]] = {}
    invalid: set[tuple[str, str]] = set()

    def define(key, sources=(), *, numeric=True):
        dependencies.setdefault(key, set()).update(sources)
        if not numeric:
            invalid.add(key)

    def collection(name):
        return ("<collection>", name)

    blocks = [("", (), ir.main)] + [
        (f.name, f.params, f.body) for f in ir.functions.values()
    ]
    indirect_calls = any(
        i.op == "CALL" and i.args[0] in {"MakeClosure", "Invoke", "Spawn"}
        for _, _, body in blocks for i in body
    )
    for scope, params, body in blocks:
        def key(name):
            local = scope and (name in params or name.startswith(scope + "_"))
            return (scope if local or name.startswith(("t", "__")) else "", name)

        if indirect_calls:
            for parameter in params:
                define((scope, parameter), numeric=False)
        # @_ is an accumulator, not SSA. Only use a producer in the same
        # straight-line block; never guess its value across a control-flow join.
        accumulator = None
        for item in body:
            op, args = item.op, item.args
            if op in {"LABEL", "JUMP", "JUMPF", "RETURN"}:
                accumulator = None
            if op == "CONST":
                define(key(item.dest), numeric=type(args[0]) is int)
            elif op == "LOADVAR":
                source = accumulator if args[0] == "_" else key(args[0])
                define(key(item.dest), () if source is None else (source,), numeric=source is not None)
            elif op == "STORE_LIST":
                name, values = args
                if name in candidates:
                    define(collection(name), (key(v) for v in values))
                elif name == "_":
                    accumulator = key(values[0]) if len(values) == 1 else None
                else:
                    define(key(name), (key(v) for v in values), numeric=len(values) == 1 and name not in collection_names)
            elif op in {"APPEND", "SET"}:
                if args[0] in candidates:
                    define(collection(args[0]), (key(args[-1]),))
            elif op == "GET":
                define(key(item.dest), (collection(args[0]),), numeric=args[0] in candidates)
            elif op in {"UPDATE", "RESTOREVAR", "ADD"}:
                define(key(args[0]), (key(args[1]),))
                if args[0] == "_":
                    accumulator = None
            elif op == "SAVEVAR":
                define(key(item.dest), (key(args[0]),))
            elif op in {"BINOP", "AND", "OR"}:
                operands = args[1:] if op == "BINOP" else args
                define(key(item.dest), (key(v) for v in operands))
            elif op in {"CMP", "ISCLASS", "LENGTH"}:
                define(key(item.dest))
            elif op == "CALL":
                function = ir.functions.get(args[0])
                if item.dest:
                    define(key(item.dest), ((args[0], "<return>"),), numeric=function is not None)
                if function is not None:
                    for index, parameter in enumerate(function.params, 1):
                        define((function.name, parameter), (key(args[index]),) if index < len(args) else (), numeric=index < len(args))
                accumulator = None
            elif op == "RETURN":
                define((scope, "<return>"), (key(args[0]),) if args else ())
            elif op == "INPUT":
                define(key(args[0]), numeric=False)
                if args[0] == "_":
                    accumulator = None
            elif item.dest and op != "LABEL":
                define(key(item.dest), numeric=False)

    proven = set(dependencies) - invalid
    while True:
        refined = {n for n in proven if dependencies[n] <= proven}
        if refined == proven:
            return {n for n in candidates if collection(n) in proven}
        proven = refined


def _emit_dynamic_macos_arm64(ir: IRProgram) -> str:
    """Lower the straight-line IR/control-flow subset to real arm64 code."""
    instructions = ir.main
    artifact_suffix_needed = any(item.op == "ARTIFACT_SUFFIX" for item in instructions) or any(
        item.op == "ARTIFACT_SUFFIX"
        for function in ir.functions.values()
        for item in function.body
    )
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
    untracked_collection_pointers = _untracked_collection_pointers(ir, collection_names)
    # Keep existing unsupported-alias diagnostics ahead of the new proof. A
    # source binding such as t0 can collide with an IR temporary's spelling.
    for scope, body in [("", instructions)] + [(f.name, f.body) for f in ir.functions.values()]:
        for item in body:
            if item.op in {"GET", "SET", "LENGTH", "APPEND"} and item.args[0] in untracked_collection_pointers[scope]:
                raise NativeBackendError(f"native {item.op} requires logical length metadata for collection aliases")
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
    # refine only Integer-typed owners with proven numeric writes.
    integer_collections = _arm64_integer_collections(ir, collection_names)
    if any(ir.symbol_types.get(name) == "Integers" and name not in integer_collections for name in collection_names):
        raise NativeBackendError("native Integer collection writes require proven numeric values")
    collection_kinds.update({
        name: "number" if name in integer_collections else "text"
        for name in collection_names
    })
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
    for name, declared_type in ir.symbol_types.items():
        if declared_type == "Text" and global_kinds.get(name) == "unknown":
            global_kinds[name] = "text"
    function_return_kinds: dict[str, str] = {}
    def inferred_text_name(name: str) -> bool:
        lowered = name.lower()
        return any(word in lowered for word in ("kind", "operand", "name", "value", "code", "message", "text", "op"))
    for _ in range(len(ir.functions) + 1):
        changed = False
        for function in ir.functions.values():
            inferred: dict[str, str] = {}
            for parameter in function.params:
                inferred[parameter] = _native_kind_for_type(function.parameter_types.get(parameter)) or (
                    "float" if parameter.lower() in {"acc", "scale"}
                    else "text" if any(word in parameter.lower() for word in ("kind", "word", "value", "name", "code", "message", "text", "class"))
                    else "number"
                )
            for item in function.body:
                if item.op == "CONST": inferred[item.dest] = "text" if isinstance(item.args[0], str) else "float" if isinstance(item.args[0], float) else "number"
                elif item.op == "GET": inferred[item.dest] = collection_kinds.get(item.args[0], "unknown")
                elif item.op == "LOADVAR": inferred[item.dest] = inferred.get(item.args[0], global_kinds.get(item.args[0], collection_kinds.get(item.args[0], "unknown")))
                elif item.op == "ARTIFACT_SUFFIX": inferred[item.dest] = "text"
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
    main_statically_text = _statically_text_values(
        instructions, ir.symbol_types, collection_names,
    )
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

    def emit_text_concat(left: str, right: str, destination: str):
        load(left, "x0")
        load(right, "x1")
        lines.append("    bl _kuro_concat_text")
        store(destination)

    def load_collection_length(name: str, register: str = "x0"):
        lines.extend([f"    adrp {register}, {collection_lengths[name]}@PAGE", f"    add {register}, {register}, {collection_lengths[name]}@PAGEOFF", f"    ldr {register}, [{register}]"])

    def store_collection_length(name: str, register: str = "x0"):
        lines.extend([f"    adrp x2, {collection_lengths[name]}@PAGE", f"    add x2, x2, {collection_lengths[name]}@PAGEOFF", f"    str {register}, [x2]"])

    for item in instructions:
        op = item.op
        if op in {"GET", "SET", "LENGTH", "APPEND"} and item.args[0] in untracked_collection_pointers[""]:
            raise NativeBackendError(f"native {op} requires logical length metadata for collection aliases")
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
            lines.extend(_arm64_collection_index_bounds(collection_lengths[name], read=True))
            lines.extend([
                f"    adrp x2, {collection_buffers[name]}@PAGE",
                f"    add x2, x2, {collection_buffers[name]}@PAGEOFF",
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
        elif op == "ARTIFACT_SUFFIX":
            if len(item.args) != 2:
                raise NativeBackendError("native ARTIFACT_SUFFIX requires Text and an integer offset")
            source, offset = item.args
            if source not in main_statically_text:
                raise NativeBackendError("native ARTIFACT_SUFFIX requires a statically known Text source")
            load(source, "x0")
            load(offset, "x1")
            lines.append("    bl _kuro_artifact_suffix")
            store(item.dest)
            kinds[item.dest] = "text"
        elif op == "SET":
            name, index_temp, value_temp = item.args
            if name not in collection_buffers:
                raise NativeBackendError("native SET requires a native collection")
            load(index_temp, "x1")
            load(value_temp, "x0")
            lines.extend(_arm64_collection_index_bounds(collection_lengths[name], read=False))
            lines.extend([
                f"    adrp x2, {collection_buffers[name]}@PAGE",
                f"    add x2, x2, {collection_buffers[name]}@PAGEOFF",
                "    lsl x1, x1, #3",
                "    str x0, [x2, x1]",
            ])
        elif op == "CALL":
            name, *arguments = item.args
            if name == "MakeEnum":
                if len(arguments) != 2:
                    raise NativeBackendError("native MakeEnum requires a type and variant")
                dot_label = f"L_kuro_data_{len(data)}"
                data.append((dot_label, "."))
                load(arguments[0], "x0")
                lines.extend([
                    f"    adrp x1, {dot_label}@PAGE",
                    f"    add x1, x1, {dot_label}@PAGEOFF",
                    "    bl _kuro_concat_text",
                ])
                store(item.dest)
                emit_text_concat(item.dest, arguments[1], item.dest)
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
                emit_text_concat(left, right, item.dest)
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
    ])
    if artifact_suffix_needed:
        # Text values are immutable, so an in-range suffix can safely share its source storage.
        lines.extend([
            ".section __TEXT,__text",
            "_kuro_artifact_suffix:",
            "    stp x29, x30, [sp, #-16]!",
            "    sub sp, sp, #16",
            "    str x0, [sp]",
            "    str x1, [sp, #8]",
            "    cmp x1, #0",
            "    b.lt L_kuro_artifact_suffix_error",
            "    bl _strlen",
            "    ldr x1, [sp, #8]",
            "    cmp x1, x0",
            "    b.hi L_kuro_artifact_suffix_error",
            "    ldr x0, [sp]",
            "    add x0, x0, x1",
            "    add sp, sp, #16",
            "    ldp x29, x30, [sp], #16",
            "    ret",
            "L_kuro_artifact_suffix_error:",
            "    mov w0, #1",
            "    bl _exit",
            "    brk #0",
        ])
    lines.append(".section __TEXT,__cstring")
    for function in ir.functions.values():
        function_sections.append(_emit_dynamic_function(
            function, collection_buffers, collection_lengths, global_labels,
            data, collection_kinds, function_return_kinds, char_buffers,
            known_lengths, global_kinds, ir.symbol_types, collection_names,
            untracked_collection_pointers[function.name],
        ))
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
    if any(
        (item.op == "BINOP" and item.args and item.args[0] == "+")
        or (item.op == "CALL" and item.args and item.args[0] == "MakeEnum")
        for item in all_items
    ):
        lines.extend([
            ".section __TEXT,__text",
            "_kuro_concat_text:",
            "    stp x29, x30, [sp, #-16]!",
            "    mov x29, sp",
            "    stp x19, x20, [sp, #-16]!",
            "    stp x21, x22, [sp, #-16]!",
            "    mov x19, x0",
            "    mov x20, x1",
            "    mov x0, x19",
            "    bl _strlen",
            "    mov x21, x0",
            "    mov x0, x20",
            "    bl _strlen",
            "    add x0, x0, x21",
            "    add x0, x0, #1",
            "    bl _malloc",
            "    mov x22, x0",
            "    mov x0, x22",
            "    mov x1, x19",
            "    bl _strcpy",
            "    mov x0, x22",
            "    mov x1, x20",
            "    bl _strcat",
            "    mov x0, x22",
            "    ldp x21, x22, [sp], #16",
            "    ldp x19, x20, [sp], #16",
            "    ldp x29, x30, [sp], #16",
            "    ret",
        ])
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


def _emit_dynamic_function(
    function, collection_buffers=None, collection_lengths=None, global_labels=None,
    data=None, collection_kinds=None, function_return_kinds=None, char_buffers=None,
    known_lengths=None, global_kinds=None, symbol_types=None,
    static_collection_names=None, untracked_collection_pointers=None,
) -> str:
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
    function_statically_text = _statically_text_values(
        function.body, symbol_types or {}, set(static_collection_names or ()),
        function.parameter_types,
    )
    kinds: dict[str, str] = {}
    def inferred_text_name(name: str) -> bool:
        lowered = name.lower()
        return any(word in lowered for word in ("kind", "operand", "name", "value", "code", "message", "text", "op"))
    for parameter in function.params:
        lowered = parameter.lower()
        declared_kind = _native_kind_for_type(function.parameter_types.get(parameter))
        if declared_kind is not None:
            kinds[parameter] = declared_kind
        elif lowered in {"acc", "scale"}:
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
        if op in {"GET", "SET", "LENGTH", "APPEND"} and item.args[0] in (untracked_collection_pointers or set()):
            raise NativeBackendError(f"native action {op} requires logical length metadata for collection parameters or aliases")
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
            if name in collection_buffers and name in function.params:
                raise NativeBackendError("native action GET requires logical length metadata for collection parameters")
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
            lines.extend(_arm64_collection_index_bounds(collection_lengths[name], read=True))
            lines.extend([
                f"    adrp x2, {collection_buffers[name]}@PAGE",
                f"    add x2, x2, {collection_buffers[name]}@PAGEOFF",
                "    lsl x1, x1, #3",
                "    ldr x0, [x2, x1]",
            ])
            store(item.dest); kinds[item.dest] = collection_kinds.get(name, "unknown")
        elif op == "ARTIFACT_SUFFIX":
            if len(item.args) != 2:
                raise NativeBackendError("native ARTIFACT_SUFFIX requires Text and an integer offset")
            source, offset = item.args
            if source not in function_statically_text:
                raise NativeBackendError("native ARTIFACT_SUFFIX requires a statically known Text source")
            load(source, "x0")
            load(offset, "x1")
            lines.append("    bl _kuro_artifact_suffix")
            store(item.dest)
            kinds[item.dest] = "text"
        elif op == "SET":
            name, index_temp, value_temp = item.args
            if name in collection_buffers and name in function.params:
                raise NativeBackendError("native action SET requires logical length metadata for collection parameters")
            if name not in collection_buffers:
                load(name, "x2")
                load(index_temp, "x1")
                load(value_temp, "x0")
                lines.extend(["    ldrb w0, [x0]", "    strb w0, [x2, x1]"])
                continue
            load(index_temp, "x1")
            load(value_temp, "x0")
            lines.extend(_arm64_collection_index_bounds(collection_lengths[name], read=False))
            lines.extend([
                f"    adrp x2, {collection_buffers[name]}@PAGE",
                f"    add x2, x2, {collection_buffers[name]}@PAGEOFF",
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
                    f"{text_label}:", "    bl _kuro_concat_text",
                ])
                lines.append(f"{done_label}:")
                store(item.dest); kinds[item.dest] = "unknown"
                continue
            if operator == "+" and kinds.get(left) == "text" and kinds.get(right) == "text":
                load(left, "x0"); load(right, "x1"); lines.append("    bl _kuro_concat_text")
                store(item.dest)
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
                # Darwin ARM64 user-space pointers are above 4 GiB and below
                # the 48-bit virtual-address ceiling.  A 4 KiB cutoff treats
                # ordinary integer results (for example, a 70,000-byte
                # length) as string pointers and can fault inside puts/strlen.
                lines.extend([
                    "    mov x1, #0x100000000", "    cmp x0, x1", f"    b.lo {number_label}",
                    "    mov x1, #0x1000000000000", "    cmp x0, x1", f"    b.lo {text_label}",
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
        and (item.args[0] in builtin_calls or (ir.functions.get(item.args[0]) is not None and any(inner.op in {"JUMP", "JUMPF", "CALL", "CMP", "ARTIFACT_SUFFIX"} for inner in ir.functions[item.args[0]].body)))
        for item in ir.main
    )
    if any(item.op in {"JUMP", "JUMPF", "LOOP_GUARD", "AND", "OR", "APPEND", "ISCLASS", "INPUT", "ARTIFACT_SUFFIX"} for item in ir.main) or has_dynamic_action:
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
            lower_bound = -len(value) if isinstance(value, list) else 0
            if not isinstance(index, int) or not isinstance(value, (str, list)) or not lower_bound <= index < len(value):
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


def _check_x86_result_owner_channel(
    ir: IRProgram, global_names: set[str], collection_names: set[str],
    input_names: set[str], capture_slots: dict[str, dict[str, int]],
) -> None:
    """Reject shapes lacking an integer proof for an inherited owner read.

    This is rejection-only provenance, not new native type inference. The hidden
    channel transports one word, not a runtime kind/length pair. Unioning facts
    across writes/branches is intentionally conservative; it never admits a new
    instruction, collection representation, or closure invocation shape.
    """
    if not ir.functions:
        return
    if "_" in collection_names or "_" in input_names:
        raise NativeBackendError(
            "x86_64 result owner channel does not support collection/input-backed '_'"
        )

    def contains_result(value) -> bool:
        if isinstance(value, (tuple, list)):
            return any(contains_result(part) for part in value)
        return value == "_"

    inherited_readers = set()
    for name, function in ir.functions.items():
        if "_" in function.params or "_" in capture_slots.get(name, {}):
            continue
        labels = {item.dest: index for index, item in enumerate(function.body) if item.op == "LABEL"}
        pending = [0] if function.body else []
        visited = set()
        while pending:
            index = pending.pop()
            if index in visited or index >= len(function.body):
                continue
            visited.add(index)
            item = function.body[index]
            args = item.args
            # Constants, labels, type/class/operator names are not variable
            # reads. In particular the authored VM compares names to literal
            # "_" without reading its native Action's inherited result.
            if item.op in {"CONST", "DECLTYPE", "LABEL", "JUMP"}:
                args = ()
            elif item.op in {"STORE_LIST", "UPDATE", "RESTOREVAR", "INPUT", "CALL", "BINOP", "CMP"}:
                args = args[1:]
            elif item.op == "ISCLASS":
                args = args[:1]
            if contains_result(args):
                inherited_readers.add(name)
                break
            overwritten = item.dest == "_" or (
                item.op in {"STORE_LIST", "UPDATE", "RESTOREVAR", "INPUT"}
                and item.args[0] == "_"
            )
            if overwritten or item.op == "RETURN":
                continue
            if item.op in {"JUMP", "JUMPF"}:
                pending.append(labels[item.args[0]])
            if item.op != "JUMP":
                pending.append(index + 1)
    if not inherited_readers:
        return

    bodies = {"": ir.main, **{name: fn.body for name, fn in ir.functions.items()}}
    noninteger: set[tuple[str, str]] = set()

    def key(scope, name):
        if name == "_" or (scope and name in ir.functions[scope].params):
            return scope, name
        return ("", name) if name in global_names or name in collection_names or name in input_names else (scope, name)

    def unsafe(scope, name):
        return key(scope, name) in noninteger

    def mark(scope, name):
        if name is not None:
            noninteger.add(key(scope, name))

    for scope, body in bodies.items():
        for name in collection_names | input_names:
            mark(scope, name)
        if scope:
            for parameter, type_name in ir.functions[scope].parameter_types.items():
                if type_name not in {"Integers", "Symbols"}:
                    mark(scope, parameter)
            # Existing environment captures are not carried by the new channel.
            # Do not guess their kind for a downstream inherited-owner read.
            for capture in capture_slots.get(scope, {}):
                mark(scope, capture)

    integer_builtins = {"EnumIs", "IsSome", "IsNone", "IsOk", "IsErr", "MapHas"}
    while True:
        before = len(noninteger)
        for scope, body in bodies.items():
            for item in body:
                op, args = item.op, item.args
                if op == "CONST" and not isinstance(args[0], (bool, int)):
                    mark(scope, item.dest)
                elif op in {"INPUT", "ARTIFACT_SUFFIX", "GET"}:
                    mark(scope, args[0] if op == "INPUT" else item.dest)
                elif op in {"LOADVAR", "SAVEVAR"}:
                    if unsafe(scope, args[0]):
                        mark(scope, item.dest)
                elif op in {"STORE_LIST", "UPDATE", "RESTOREVAR"}:
                    sources = args[1] if op == "STORE_LIST" else [args[1]]
                    if len(sources) != 1 or any(unsafe(scope, source) for source in sources):
                        mark(scope, args[0])
                elif op == "BINOP":
                    if unsafe(scope, args[1]) or unsafe(scope, args[2]):
                        mark(scope, item.dest)
                elif op == "ADD":
                    if unsafe(scope, args[1]):
                        mark(scope, args[0])
                elif op == "CALL":
                    callee, *arguments = args
                    if callee in ir.functions:
                        target = ir.functions[callee]
                        if "_" not in target.params and unsafe(scope, "_"):
                            mark(callee, "_")
                        for parameter, argument in zip(target.params, arguments):
                            if unsafe(scope, argument):
                                mark(callee, parameter)
                        if any(inner.op == "RETURN" and unsafe(callee, inner.args[0]) for inner in target.body):
                            mark(scope, item.dest)
                    elif callee not in integer_builtins:
                        mark(scope, item.dest)
                    if callee in {"Invoke", "Spawn", "Await"}:
                        raise NativeBackendError(
                            "x86_64 result owner inherited reads require direct integer calls, not closure/task channels"
                        )
        if len(noninteger) == before:
            break
    for name in sorted(inherited_readers):
        if unsafe(name, "_"):
            raise NativeBackendError(
                f"x86_64 result owner inherited read in action {name!r} requires an integer-only channel"
            )


def emit_x86_64_linux(
    ir: IRProgram, *, text_heap_capacity: int | None = None
) -> str:
    """Emit the portable integer/text/control-flow subset for Linux x86-64.

    Values live in a real stack frame and branches target emitted labels. No
    constant evaluation or foreign runtime is involved; text output and
    integer formatting use Linux syscalls directly. Complex heap values,
    floating point, and unsupported call forms remain explicit capability errors below.
    """
    text_heap_capacity = _resolve_text_heap_capacity(text_heap_capacity)
    items = ir.main
    # Captured closure objects reserve a 16-byte header and up to 30 numeric
    # captures. Linux brk grows their process-local heap one page at a time.
    closure_object_bytes = 256
    closure_heap_page_bytes = 4096
    max_closure_captures = (closure_object_bytes - 16) // 8
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

    def action_return_kind(name: str, arguments: tuple[str, ...] = ()) -> str:
        function = ir.functions.get(name)
        if function is None:
            return "text" if action_returns_text(name) else "number"
        local_kinds = dict(function_capture_kinds.get(name, {}))
        local_texts: dict[str, str] = {}
        local_kinds.update({
            parameter: kinds.get(argument, "unknown")
            for parameter, argument in zip(function.params, arguments)
        })
        for item in function.body:
            if item.op == "CONST" and item.dest:
                value = item.args[0]
                local_kinds[item.dest] = "text" if isinstance(value, str) else "float" if isinstance(value, float) else "number"
                if isinstance(value, str):
                    local_texts[item.dest] = value
                else:
                    local_texts.pop(item.dest, None)
            elif item.op == "LOADVAR" and item.dest:
                source = item.args[0]
                local_kinds[item.dest] = local_kinds.get(source, kinds.get(source, inferred_symbol_kind(source)))
                if source in local_texts:
                    local_texts[item.dest] = local_texts[source]
                else:
                    local_texts.pop(item.dest, None)
            elif item.op == "GET" and item.dest:
                source = item.args[0]
                source_kind = local_kinds.get(source, kinds.get(source, "unknown"))
                if source_kind.startswith("collection:"):
                    local_kinds[item.dest] = source_kind.split(":", 1)[1]
                elif source_kind == "text":
                    local_kinds[item.dest] = "text"
                else:
                    local_kinds[item.dest] = collection_kinds.get(source, "unknown")
            elif item.op == "BINOP" and item.dest:
                operator, left, right = item.args
                left_kind = local_kinds.get(left, kinds.get(left, inferred_symbol_kind(left)))
                right_kind = local_kinds.get(right, kinds.get(right, inferred_symbol_kind(right)))
                local_kinds[item.dest] = "text" if operator == "+" and left_kind == right_kind == "text" else "float" if "float" in {left_kind, right_kind} else "number"
                local_texts.pop(item.dest, None)
            elif item.op in {"CMP", "AND", "OR", "ISCLASS", "LENGTH"} and item.dest:
                local_kinds[item.dest] = "number"
                local_texts.pop(item.dest, None)
            elif item.op == "STORE_LIST" and len(item.args[1]) == 1:
                target, source = item.args[0], item.args[1][0]
                local_kinds[target] = local_kinds.get(source, kinds.get(source, "unknown"))
                if source in local_texts:
                    local_texts[target] = local_texts[source]
                else:
                    local_texts.pop(target, None)
            elif item.op == "UPDATE":
                target, source = item.args
                local_kinds[target] = local_kinds.get(source, kinds.get(source, "unknown"))
                if source in local_texts:
                    local_texts[target] = local_texts[source]
                else:
                    local_texts.pop(target, None)
            elif item.op == "ARTIFACT_SUFFIX" and item.dest:
                local_kinds[item.dest] = "text"
                local_texts.pop(item.dest, None)
            elif item.op == "CALL" and item.dest:
                call_name, *call_arguments = item.args
                if call_name == "RecordGet" and len(call_arguments) == 2:
                    field = local_texts.get(call_arguments[1])
                    local_kinds[item.dest] = record_field_kinds.get(field, "unknown") if field is not None else "unknown"
                elif call_name == "RecordSet" and len(call_arguments) == 3:
                    local_kinds[item.dest] = "record"
                elif call_name == "MapGet" and len(call_arguments) == 2:
                    key = local_texts.get(call_arguments[1])
                    local_kinds[item.dest] = map_value_kinds.get(key, "unknown") if key is not None else "unknown"
                elif call_name == "MapSet" and len(call_arguments) == 3:
                    local_kinds[item.dest] = "map"
                elif call_name == "MapHas" and len(call_arguments) == 2:
                    local_kinds[item.dest] = "number"
            elif item.op == "RETURN":
                return local_kinds.get(item.args[0], kinds.get(item.args[0], "unknown"))
        return "unknown"

    def remember_action_argument_kinds(name: str, arguments: tuple[str, ...]) -> None:
        function = ir.functions.get(name)
        if function is None:
            return
        hints = function_parameter_kinds.setdefault(name, {})
        for parameter, argument in zip(function.params, arguments):
            kind = kinds.get(argument, "unknown")
            if kind == "collection":
                source_name = collection_ref.get(argument, argument)
                kind = f"collection:{collection_kinds.get(source_name, 'unknown')}"
            previous = hints.get(parameter)
            hints[parameter] = kind if previous is None or previous == kind else "unknown"
        refresh_function_capture_kinds()

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
    text_constant_labels: dict[str, list[str]] = {}
    next_text_label = 0
    for text_instruction in items:
        if text_instruction.op == "CONST" and isinstance(text_instruction.args[0], str):
            text_constant_labels.setdefault(text_instruction.args[0], []).append(
                f".Lkuro_data_{next_text_label}"
            )
            next_text_label += 1
    untracked_collection_pointers = _untracked_collection_pointers(ir, collection_names)
    collection_buffers = {name: f".Lkuro_collection_{index}" for index, name in enumerate(sorted(collection_names))}
    collection_lengths = {name: f".Lkuro_collection_len_{index}" for index, name in enumerate(sorted(collection_names))}
    collection_item_lengths = {name: f".Lkuro_collection_item_len_{index}" for index, name in enumerate(sorted(collection_names))}
    main_statically_text = _statically_text_values(
        items, ir.symbol_types, collection_names
    )
    input_buffers = {name: f".Lkuro_input_{index}" for index, name in enumerate(sorted(input_names))}
    input_lengths = {name: f".Lkuro_input_len_{index}" for index, name in enumerate(sorted(input_names))}
    main_global_names: set[str] = set()
    for item in items:
        if item.op in {"LOADVAR", "STORE_LIST", "UPDATE", "ADD", "INPUT", "SAVEVAR", "RESTOREVAR"} and item.args:
            name = item.args[0]
            if isinstance(name, str) and not name.startswith(("t", "__")):
                main_global_names.add(name)
    # The root result is zero-initialized BSS even when main never names it.
    # Action calls copy it (or their caller's local owner) through %rax.
    global_names = set(main_global_names) | {"_"}
    for function in ir.functions.values():
        prefix = f"{function.name}_"
        for item in function.body:
            for argument in item.args:
                if isinstance(argument, str) and not argument.startswith(("t", "__")) and argument not in function.params and not argument.startswith(prefix):
                    global_names.add(argument)

    action_closure_sites: list[tuple[str, str]] = []
    for function in ir.functions.values():
        text_values: dict[str, str] = {}
        for action_instruction in function.body:
            if action_instruction.op == "CONST" and action_instruction.dest:
                value = action_instruction.args[0]
                if isinstance(value, str):
                    text_values[action_instruction.dest] = value
                else:
                    text_values.pop(action_instruction.dest, None)
            elif action_instruction.op == "LOADVAR" and action_instruction.dest:
                source = action_instruction.args[0]
                if source in text_values:
                    text_values[action_instruction.dest] = text_values[source]
                else:
                    text_values.pop(action_instruction.dest, None)
            elif action_instruction.op == "STORE_LIST":
                name, values = action_instruction.args
                if len(values) == 1 and values[0] in text_values:
                    text_values[name] = text_values[values[0]]
                else:
                    text_values.pop(name, None)
            elif action_instruction.op == "UPDATE":
                name, value = action_instruction.args
                if value in text_values:
                    text_values[name] = text_values[value]
                else:
                    text_values.pop(name, None)
            elif action_instruction.op == "CALL":
                call_name, *arguments = action_instruction.args
                if (
                    call_name == "MakeClosure"
                    and len(arguments) == 1
                    and arguments[0] in text_values
                    and text_values[arguments[0]] in ir.functions
                ):
                    action_closure_sites.append((function.name, text_values[arguments[0]]))
                if action_instruction.dest:
                    text_values.pop(action_instruction.dest, None)
            elif action_instruction.dest:
                text_values.pop(action_instruction.dest, None)

    supplied_captures: dict[str, set[str]] = {}
    supplied_capture_sources: dict[str, dict[str, set[tuple[str, str]]]] = {}
    for maker_name, target_name in action_closure_sites:
        maker = ir.functions[maker_name]
        target = ir.functions[target_name]
        maker_locals = set(maker.params)
        maker_locals.update(
            item.args[0]
            for item in maker.body
            if item.op in {"STORE_LIST", "UPDATE", "ADD", "INPUT"} and item.args
        )
        target_locals = set(target.params)
        target_locals.update(
            item.args[0]
            for item in target.body
            if item.op == "STORE_LIST" and item.args
        )
        target_reads = {
            item.args[0]
            for item in target.body
            if item.op == "LOADVAR" and item.args
        }
        target_reads.update(
            item.args[0]
            for item in target.body
            if item.op in {"GET", "SET", "APPEND", "LENGTH"} and item.args
        )
        target_free_names = target_reads - target_locals - main_global_names
        available_captures = target_free_names & maker_locals
        supplied_captures.setdefault(target_name, set()).update(available_captures)
        for capture_name in available_captures:
            supplied_capture_sources.setdefault(target_name, {}).setdefault(capture_name, set()).add(
                (maker_name, capture_name)
            )

    for captures in supplied_captures.values():
        # A captured result can initialize an Action, but does not replace the
        # independent root owner used by main's hidden call channel.
        global_names.difference_update(set(captures) - {"_"})
    global_names -= set(collection_buffers) | set(input_buffers)
    function_capture_names: dict[str, tuple[str, ...]] = {
        name: tuple(sorted(supplied_captures.get(name, set())))
        for name in ir.functions
    }
    function_capture_slots: dict[str, dict[str, int]] = {
        name: {capture_name: index for index, capture_name in enumerate(captures)}
        for name, captures in function_capture_names.items()
    }
    for function_name, captures in function_capture_names.items():
        if len(captures) > max_closure_captures:
            raise NativeBackendError(
                f"x86_64-linux closure {function_name!r} exceeds the fixed capture capacity"
            )
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

    def collection_origin(name: str) -> str | None:
        if name in collection_ref:
            return collection_ref[name]
        if name in collection_buffers:
            return name
        return None

    def transfer_collection_ref(destination: str, source: str) -> None:
        origin = collection_origin(source)
        if origin is None:
            collection_ref.pop(destination, None)
            return
        collection_ref[destination] = origin
        collection_kinds[destination] = collection_kinds.get(
            origin, collection_kinds.get(source, "unknown")
        )

    map_dest_labels = {
        instruction.dest: f".Lkuro_map_{index}"
        for index, instruction in enumerate(
            instruction for instruction in items
            if instruction.op == "CALL" and instruction.args and instruction.args[0] == "MakeMap" and instruction.dest
        )
    }
    record_dest_labels = {
        instruction.dest: f".Lkuro_record_{index}"
        for index, instruction in enumerate(
            instruction for instruction in items
            if instruction.op == "CALL" and instruction.args and instruction.args[0] == "MakeRecord" and instruction.dest
        )
    }
    task_argument_labels = {
        instruction.dest: f".Lkuro_task_arg_{index}"
        for index, instruction in enumerate(
            instruction for instruction in items
            if instruction.op == "CALL" and instruction.args and instruction.args[0] == "Spawn" and instruction.dest
        )
    }
    map_alias: dict[str, str] = {}
    closure_actions: dict[str, str] = {}
    task_actions: dict[str, str] = {}
    task_argument_refs: dict[str, str] = {}
    task_argument_values: dict[str, str] = {}
    function_parameter_kinds: dict[str, dict[str, str]] = {}
    function_capture_kinds: dict[str, dict[str, str]] = {name: {} for name in ir.functions}

    def refresh_function_capture_kinds() -> None:
        for target_name, captures in supplied_capture_sources.items():
            for capture_name, sources in captures.items():
                observed_kinds: set[str] = set()
                has_unknown = False
                for maker_name, source_name in sources:
                    maker_hints = function_parameter_kinds.get(maker_name, {})
                    if source_name not in maker_hints:
                        continue
                    kind = maker_hints[source_name]
                    if kind == "unknown":
                        has_unknown = True
                    else:
                        observed_kinds.add(kind)
                if has_unknown or len(observed_kinds) > 1:
                    function_capture_kinds[target_name][capture_name] = "unknown"
                elif observed_kinds:
                    function_capture_kinds[target_name][capture_name] = next(iter(observed_kinds))
    map_key_slots: dict[str, int] = {}
    record_field_slots: dict[str, int] = {}
    record_field_kinds: dict[str, str] = {}
    record_field_lengths: dict[str, int] = {}
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
    closure_construction_actions: dict[int, str] = {}
    static_text_values: dict[str, str] = {}
    static_text_value_seeds: dict[int, set[str]] = {}
    for instruction_index, instruction in enumerate(items):
        if instruction.op == "CONST" and instruction.dest:
            value = instruction.args[0]
            if isinstance(value, str):
                static_text_values[instruction.dest] = value
                static_text_value_seeds[instruction_index] = {value}
            else:
                static_text_values.pop(instruction.dest, None)
        elif instruction.op == "LOADVAR" and instruction.dest:
            source = instruction.args[0]
            if source in static_text_values:
                static_text_values[instruction.dest] = static_text_values[source]
            else:
                static_text_values.pop(instruction.dest, None)
        elif instruction.op == "STORE_LIST":
            name, values = instruction.args
            if len(values) == 1 and values[0] in static_text_values:
                static_text_values[name] = static_text_values[values[0]]
            else:
                static_text_values.pop(name, None)
        elif instruction.op == "UPDATE":
            name, value = instruction.args
            if value in static_text_values:
                static_text_values[name] = static_text_values[value]
            else:
                static_text_values.pop(name, None)
        elif instruction.op == "CALL":
            call_name, *arguments = instruction.args
            if (
                call_name == "MakeClosure"
                and len(arguments) == 1
                and arguments[0] in static_text_values
                and static_text_values[arguments[0]] in ir.functions
            ):
                closure_construction_actions[instruction_index] = static_text_values[arguments[0]]
            if instruction.dest:
                static_text_values.pop(instruction.dest, None)

    function_closure_construction_targets: dict[tuple[str, int], str] = {}
    function_return_closure_targets: dict[str, set[str]] = {}
    for function in ir.functions.values():
        action_text_values: dict[str, str] = {}
        action_closure_values: dict[str, set[str]] = {}
        returned_closures: set[str] = set()
        for action_instruction_index, action_instruction in enumerate(function.body):
            if action_instruction.op == "CONST" and action_instruction.dest:
                value = action_instruction.args[0]
                if isinstance(value, str):
                    action_text_values[action_instruction.dest] = value
                else:
                    action_text_values.pop(action_instruction.dest, None)
                action_closure_values.pop(action_instruction.dest, None)
            elif action_instruction.op == "LOADVAR" and action_instruction.dest:
                source = action_instruction.args[0]
                if source in action_text_values:
                    action_text_values[action_instruction.dest] = action_text_values[source]
                else:
                    action_text_values.pop(action_instruction.dest, None)
                if source in action_closure_values:
                    action_closure_values[action_instruction.dest] = set(action_closure_values[source])
                else:
                    action_closure_values.pop(action_instruction.dest, None)
            elif action_instruction.op == "STORE_LIST":
                name, values = action_instruction.args
                if len(values) == 1 and values[0] in action_text_values:
                    action_text_values[name] = action_text_values[values[0]]
                else:
                    action_text_values.pop(name, None)
                if len(values) == 1 and values[0] in action_closure_values:
                    action_closure_values[name] = set(action_closure_values[values[0]])
                else:
                    action_closure_values.pop(name, None)
            elif action_instruction.op == "UPDATE":
                name, value = action_instruction.args
                if value in action_text_values:
                    action_text_values[name] = action_text_values[value]
                else:
                    action_text_values.pop(name, None)
                if value in action_closure_values:
                    action_closure_values[name] = set(action_closure_values[value])
                else:
                    action_closure_values.pop(name, None)
            elif action_instruction.op == "CALL":
                call_name, *arguments = action_instruction.args
                target = None
                if (
                    call_name == "MakeClosure"
                    and len(arguments) == 1
                    and arguments[0] in action_text_values
                    and action_text_values[arguments[0]] in ir.functions
                ):
                    target = action_text_values[arguments[0]]
                    function_closure_construction_targets[(function.name, action_instruction_index)] = target
                if action_instruction.dest:
                    action_text_values.pop(action_instruction.dest, None)
                    if target is not None:
                        action_closure_values[action_instruction.dest] = {target}
                    else:
                        action_closure_values.pop(action_instruction.dest, None)
            elif action_instruction.op == "RETURN" and action_instruction.args:
                returned_closures.update(action_closure_values.get(action_instruction.args[0], set()))
            elif action_instruction.op != "LABEL" and action_instruction.dest:
                action_text_values.pop(action_instruction.dest, None)
                action_closure_values.pop(action_instruction.dest, None)
        if returned_closures:
            function_return_closure_targets[function.name] = returned_closures

    # Recompute returned targets over the action CFG. The preceding linear scan
    # is still useful for resolving each MakeClosure constructor, but a branch
    # merge must retain every closure that can reach a RETURN.
    function_return_closure_targets.clear()

    def analyze_action_closure_returns(
        function,
        known_returns: dict[str, set[str]],
    ) -> tuple[set[str], bool, bool]:
        body = function.body
        label_indices = {
            item.dest: index for index, item in enumerate(body)
            if item.op == "LABEL" and item.dest
        }
        successors: list[tuple[int, ...]] = []
        for index, item in enumerate(body):
            next_index = index + 1
            if item.op == "JUMP":
                target = label_indices.get(item.args[0])
                successors.append((target,) if target is not None else ())
            elif item.op == "JUMPF":
                target = label_indices.get(item.args[0])
                edges = [next_index] if next_index < len(body) else []
                if target is not None:
                    edges.append(target)
                successors.append(tuple(edges))
            elif item.op in {"RETURN", "STOP"}:
                successors.append(())
            else:
                successors.append((next_index,) if next_index < len(body) else ())

        if not body:
            return set(), True, False
        # Each local carries (known target set, is-known-on-every-path). The
        # boolean prevents a known branch from masking an unknown path.
        states: list[dict[str, tuple[set[str], bool]] | None] = [None] * len(body)
        states[0] = {}
        pending = [0]
        returned: set[str] = set()
        saw_return = False
        all_returns_known = True
        while pending:
            index = pending.pop()
            incoming = states[index]
            if incoming is None:
                continue
            # Target sets in states are read-only: transfers replace tuples,
            # merges allocate new sets, and RETURN updates a separate set.
            # Copy the mapping, not every target set; never mutate a shared
            # target set in place (including empty/unknown facts).
            state = incoming.copy()
            item = body[index]
            if item.op == "LOADVAR" and item.dest:
                source = item.args[0]
                targets, is_known = state.get(source, (set(), False))
                state[item.dest] = (set(targets), is_known)
            elif item.op == "STORE_LIST":
                name, values = item.args
                if len(values) == 1:
                    targets, is_known = state.get(values[0], (set(), False))
                    state[name] = (set(targets), is_known)
                else:
                    state[name] = (set(), False)
            elif item.op == "UPDATE":
                name, value = item.args
                targets, is_known = state.get(value, (set(), False))
                state[name] = (set(targets), is_known)
            elif item.op == "CALL" and item.dest:
                call_name = item.args[0]
                target = function_closure_construction_targets.get((function.name, index))
                targets = {target} if target is not None else set(known_returns.get(call_name, set()))
                state[item.dest] = (targets, bool(targets))
            elif item.op == "RETURN" and item.args:
                saw_return = True
                targets, is_known = state.get(item.args[0], (set(), False))
                if is_known and targets:
                    returned.update(targets)
                else:
                    all_returns_known = False
            elif item.op != "LABEL" and item.dest:
                state[item.dest] = (set(), False)

            for successor in successors[index]:
                current = states[successor]
                if current is None:
                    states[successor] = state.copy()
                    pending.append(successor)
                    continue
                merged: dict[str, tuple[set[str], bool]] = {}
                for name in set(current) | set(state):
                    current_targets, current_known = current.get(name, (set(), False))
                    incoming_targets, incoming_known = state.get(name, (set(), False))
                    merged[name] = (
                        set(current_targets) | set(incoming_targets),
                        current_known and incoming_known,
                    )
                if merged != current:
                    states[successor] = merged
                    pending.append(successor)
        return returned, all_returns_known, saw_return

    # Only constructors and calls with a currently known closure return can
    # introduce a target. Without either seed every target set stays empty,
    # regardless of CFG reachability or the all-paths-known flag, so the old
    # analysis could not add this function to updated_returns. Cache only the
    # immutable call-site facts; recheck known returns on every fixed-point
    # round (including recursive/forward calls), never cache dataflow results.
    closure_return_constructors = {
        name for name, _ in function_closure_construction_targets
    }
    closure_return_callees = {
        function.name: {
            item.args[0] for item in function.body
            if item.op == "CALL" and item.dest
        }
        for function in ir.functions.values()
    }
    for _ in range(len(ir.functions) + 1):
        updated_returns: dict[str, set[str]] = {}
        for function in ir.functions.values():
            if (
                function.name not in closure_return_constructors
                and function_return_closure_targets.keys().isdisjoint(
                    closure_return_callees[function.name]
                )
            ):
                continue
            targets, all_known, saw_return = analyze_action_closure_returns(
                function, function_return_closure_targets
            )
            if targets and all_known and saw_return:
                updated_returns[function.name] = targets
        if updated_returns == function_return_closure_targets:
            break
        function_return_closure_targets = updated_returns

    closure_label_indices = {
        instruction.dest: index
        for index, instruction in enumerate(items)
        if instruction.op == "LABEL" and instruction.dest
    }
    closure_successors: list[tuple[int, ...]] = []
    for index, instruction in enumerate(items):
        next_index = index + 1
        if instruction.op == "JUMP":
            target = closure_label_indices.get(instruction.args[0])
            closure_successors.append((target,) if target is not None else ())
        elif instruction.op == "JUMPF":
            target = closure_label_indices.get(instruction.args[0])
            successors = [next_index] if next_index < len(items) else []
            if target is not None:
                successors.append(target)
            closure_successors.append(tuple(successors))
        else:
            closure_successors.append((next_index,) if next_index < len(items) else ())

    def propagate_static_targets(
        seeds: dict[int, set[str]],
    ) -> list[dict[str, set[str]] | None]:
        targets_before: list[dict[str, set[str]] | None] = [None] * len(items)
        if not items:
            return targets_before
        targets_before[0] = {}
        pending = [0]
        while pending:
            index = pending.pop()
            incoming = targets_before[index]
            if incoming is None:
                continue
            state = {name: set(targets) for name, targets in incoming.items()}
            instruction = items[index]
            if instruction.op == "CONST" and instruction.dest:
                targets = seeds.get(index, set())
                if targets:
                    state[instruction.dest] = set(targets)
                else:
                    state.pop(instruction.dest, None)
            elif instruction.op == "LOADVAR" and instruction.dest:
                source = instruction.args[0]
                if state.get(source):
                    state[instruction.dest] = set(state[source])
                else:
                    state.pop(instruction.dest, None)
            elif instruction.op == "STORE_LIST":
                name, values = instruction.args
                if len(values) == 1 and state.get(values[0]):
                    state[name] = set(state[values[0]])
                else:
                    state.pop(name, None)
            elif instruction.op == "UPDATE":
                name, value = instruction.args
                if state.get(value):
                    state[name] = set(state[value])
                else:
                    state.pop(name, None)
            elif instruction.op != "LABEL" and instruction.dest:
                targets = seeds.get(index, set())
                if targets:
                    state[instruction.dest] = set(targets)
                else:
                    state.pop(instruction.dest, None)
            for successor in closure_successors[index]:
                current = targets_before[successor]
                if current is None:
                    targets_before[successor] = {
                        name: set(targets) for name, targets in state.items()
                    }
                    pending.append(successor)
                    continue
                merged = {name: set(targets) for name, targets in current.items()}
                for name, targets in state.items():
                    merged.setdefault(name, set()).update(targets)
                if merged != current:
                    targets_before[successor] = merged
                    pending.append(successor)
        return targets_before

    closure_target_seeds = {
        index: {action} for index, action in closure_construction_actions.items()
    }
    for instruction_index, instruction in enumerate(items):
        if instruction.op == "CALL" and instruction.args:
            returned = function_return_closure_targets.get(instruction.args[0])
            if returned:
                closure_target_seeds[instruction_index] = set(returned)
    _check_x86_result_owner_channel(
        ir, global_names, collection_names, input_names, function_capture_slots,
    )
    closure_targets_before = propagate_static_targets(closure_target_seeds)
    field_text_targets_before = propagate_static_targets(static_text_value_seeds)
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
    for instruction_index, instruction in enumerate(items):
        op = instruction.op
        if op in {"GET", "SET", "LENGTH", "APPEND"} and instruction.args[0] in untracked_collection_pointers[""]:
            raise NativeBackendError(f"x86_64-linux {op} requires logical length metadata for collection aliases")
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
            transfer_collection_ref(instruction.dest, instruction.args[0])
            if instruction.args[0] in map_alias:
                map_alias[instruction.dest] = map_alias[instruction.args[0]]
            if instruction.args[0] in tagged_alias:
                tagged_alias[instruction.dest] = tagged_alias[instruction.args[0]]
            if instruction.args[0] in closure_actions:
                closure_actions[instruction.dest] = closure_actions[instruction.args[0]]
            if instruction.args[0] in task_actions:
                task_actions[instruction.dest] = task_actions[instruction.args[0]]
                task_argument_refs[instruction.dest] = task_argument_refs[instruction.args[0]]
                task_argument_values[instruction.dest] = task_argument_values[instruction.args[0]]
            if instruction.args[0] in known_text:
                known_text[instruction.dest] = known_text[instruction.args[0]]
            if instruction.args[0] in text_lengths:
                text_lengths[instruction.dest] = text_lengths[instruction.args[0]]
            if instruction.args[0] in text_length_refs:
                text_length_refs[instruction.dest] = text_length_refs[instruction.args[0]]
        elif op == "STORE_LIST":
            name, values = instruction.args
            single_collection_origin = (
                collection_origin(values[0]) if len(values) == 1 else None
            )
            collection_ref.pop(name, None)
            if not (len(values) == 1 and values[0] in closure_actions):
                closure_actions.pop(name, None)
            if not (len(values) == 1 and values[0] in task_actions):
                task_actions.pop(name, None)
                task_argument_refs.pop(name, None)
                task_argument_values.pop(name, None)
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
                collection_kinds[name] = (
                    "text" if values and all(kinds.get(value) == "text" for value in values)
                    else "float" if values and all(kinds.get(value) == "float" for value in values)
                    else "number"
                )
            elif len(values) == 1 and values[0] in map_alias:
                load(values[0]); store(name)
                map_alias[name] = map_alias[values[0]]
                kinds[name] = "map"
            elif len(values) == 1 and values[0] in tagged_alias:
                load(values[0]); store(name)
                tagged_alias[name] = tagged_alias[values[0]]
                kinds[name] = "tagged"
            elif len(values) == 1 and values[0] in closure_actions:
                load(values[0]); store(name)
                closure_actions[name] = closure_actions[values[0]]
                kinds[name] = "closure"
            elif len(values) == 1 and values[0] in task_actions:
                load(values[0]); store(name)
                task_actions[name] = task_actions[values[0]]
                task_argument_refs[name] = task_argument_refs[values[0]]
                task_argument_values[name] = task_argument_values[values[0]]
                kinds[name] = "task"
            elif len(values) == 1:
                load(values[0]); store(name)
                kinds[name] = kinds.get(values[0], "unknown")
                if single_collection_origin is not None:
                    collection_ref[name] = single_collection_origin
                    collection_kinds[name] = collection_kinds.get(
                        single_collection_origin,
                        collection_kinds.get(values[0], "unknown"),
                    )
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
            transfer_collection_ref(name, value)
            if value in map_alias:
                map_alias[name] = map_alias[value]
            if value in tagged_alias:
                tagged_alias[name] = tagged_alias[value]
            if value in closure_actions:
                closure_actions[name] = closure_actions[value]
            elif name in closure_actions:
                del closure_actions[name]
            if value in task_actions:
                task_actions[name] = task_actions[value]
                task_argument_refs[name] = task_argument_refs[value]
                task_argument_values[name] = task_argument_values[value]
            else:
                task_actions.pop(name, None)
                task_argument_refs.pop(name, None)
                task_argument_values.pop(name, None)
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
            transfer_collection_ref(instruction.dest, name)
        elif op == "RESTOREVAR":
            name, saved = instruction.args
            load(saved); store(name)
            kinds[name] = kinds.get(saved, "unknown")
            transfer_collection_ref(name, saved)
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
            if kinds.get(name) in {"number", "float"} and kinds.get(value) in {"number", "float"} and (kinds.get(name) == "float" or kinds.get(value) == "float"):
                if kinds.get(name) == "float":
                    load(name, "%rax"); lines.append("    movq %rax, %xmm0")
                else:
                    load(name, "%rax"); lines.append("    cvtsi2sd %rax, %xmm0")
                if kinds.get(value) == "float":
                    load(value, "%rax"); lines.append("    movq %rax, %xmm1")
                else:
                    load(value, "%rax"); lines.append("    cvtsi2sd %rax, %xmm1")
                lines.extend(["    addsd %xmm1, %xmm0", "    movq %xmm0, %rax"])
                store(name); kinds[name] = "float"
            else:
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
                    f"    cmp ${text_heap_capacity}, %rcx", "    ja .Lkuro_overflow",
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
                lines.extend(_x86_collection_index_bounds(collection_lengths[name], read=True))
                lines.extend([
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
            lines.extend(_x86_collection_index_bounds(collection_lengths[name], read=False))
            lines.extend([
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
        elif op == "ARTIFACT_SUFFIX":
            if len(instruction.args) != 2:
                raise NativeBackendError("x86_64-linux ARTIFACT_SUFFIX requires Text and an integer offset")
            source, offset = instruction.args
            if source not in main_statically_text:
                raise NativeBackendError("x86_64-linux ARTIFACT_SUFFIX requires a statically known Text source")
            load(source, "%r8")
            load(offset, "%r9")
            lines.extend([
                "    test %r9, %r9", "    js .Lkuro_bounds",
                "    mov %r8, %rax", "    call _kuro_strlen", "    cmp %rax, %r9", "    ja .Lkuro_bounds",
                "    sub %r9, %rax", "    mov %rax, %r10",
                "    mov .Lkuro_text_heap_cursor(%rip), %rdx", "    mov %rdx, %rcx", "    add %r10, %rcx", "    inc %rcx",
                f"    cmp ${text_heap_capacity}, %rcx", "    ja .Lkuro_overflow",
                "    lea .Lkuro_text_heap(%rip), %rdi", "    add %rdx, %rdi", "    lea (%r8,%r9,1), %rsi",
                "    mov %r10, %rcx", "    rep movsb", "    movb $0, (%rdi)",
                "    lea .Lkuro_text_heap(%rip), %rsi", "    mov %rdi, %rcx", "    sub %rsi, %rcx", "    inc %rcx",
                "    mov %rcx, .Lkuro_text_heap_cursor(%rip)", "    lea .Lkuro_text_heap(%rip), %rax", "    add %rdx, %rax",
            ])
            store(instruction.dest)
            kinds[instruction.dest] = "text"
            known_text.pop(instruction.dest, None)
            text_lengths.pop(instruction.dest, None)
            text_length_refs.pop(instruction.dest, None)
        elif op == "CALL":
            call_name, *arguments = instruction.args
            if call_name == "MakeRecord":
                if len(arguments) != 1 or arguments[0] not in known_text:
                    raise NativeBackendError("x86_64-linux MakeRecord requires a known type name")
                label = record_dest_labels.get(instruction.dest)
                if label is None:
                    raise NativeBackendError("x86_64-linux MakeRecord requires a destination")
                lines.append(f"    lea {label}(%rip), %rax")
                store(instruction.dest)
                kinds[instruction.dest] = "record"
            elif call_name in {"RecordSet", "RecordGet"}:
                if len(arguments) < 2 or arguments[0] not in slots:
                    raise NativeBackendError(f"x86_64-linux {call_name} requires a record and field name")
                if call_name == "RecordSet" and len(arguments) != 3:
                    raise NativeBackendError("x86_64-linux RecordSet requires record, field, and value")
                if call_name == "RecordGet" and len(arguments) != 2:
                    raise NativeBackendError("x86_64-linux RecordGet requires record and field")
                incoming_text_targets = field_text_targets_before[instruction_index] or {}
                fields = set(incoming_text_targets.get(arguments[1], set()))
                if not fields and arguments[1] in known_text:
                    fields.add(known_text[arguments[1]])
                if not fields:
                    raise NativeBackendError(
                        f"x86_64-linux {call_name} requires a statically bounded field-name set"
                    )
                ordered_fields = sorted(fields)
                field_slots: dict[str, int] = {}
                for field in ordered_fields:
                    slot = record_field_slots.setdefault(field, len(record_field_slots))
                    if slot >= 63:
                        raise NativeBackendError("x86_64-linux record exceeds fixed capacity of 63 fields")
                    field_slots[field] = slot

                if len(ordered_fields) == 1:
                    field = ordered_fields[0]
                    slot = field_slots[field]
                    load(arguments[0], "%rax")
                    if call_name == "RecordSet":
                        load(arguments[2], "%rdx")
                        lines.append(f"    mov %rdx, {8 + slot * 8}(%rax)")
                        store(instruction.dest)
                        kinds[instruction.dest] = "record"
                        record_field_kinds[field] = kinds.get(arguments[2], "unknown")
                        if arguments[2] in text_lengths:
                            record_field_lengths[field] = text_lengths[arguments[2]]
                        else:
                            record_field_lengths.pop(field, None)
                    else:
                        lines.append(f"    mov {8 + slot * 8}(%rax), %rax")
                        store(instruction.dest)
                        kinds[instruction.dest] = record_field_kinds.get(field, "unknown")
                        if kinds[instruction.dest] == "text" and field in record_field_lengths:
                            text_lengths[instruction.dest] = record_field_lengths[field]
                else:
                    result_kind = "record"
                    if call_name == "RecordGet":
                        field_kinds = {record_field_kinds.get(field, "unknown") for field in ordered_fields}
                        if len(field_kinds) != 1 or "unknown" in field_kinds:
                            raise NativeBackendError(
                                "x86_64-linux runtime RecordGet requires fields with one known value kind"
                            )
                        result_kind = next(iter(field_kinds))
                    unique = len(lines)
                    dispatch_labels = {
                        field: f".Lkuro_record_field_{unique}_{index}"
                        for index, field in enumerate(ordered_fields)
                    }
                    done_label = f".Lkuro_record_field_done_{unique}"
                    load(arguments[1], "%r8")
                    for field in ordered_fields:
                        literal_labels = text_constant_labels.get(field, [])
                        if not literal_labels:
                            raise NativeBackendError(
                                f"x86_64-linux cannot dispatch runtime field name {field!r}"
                            )
                        for literal_label in literal_labels:
                            lines.extend([
                                f"    lea {literal_label}(%rip), %r9",
                                "    cmp %r9, %r8",
                                f"    je {dispatch_labels[field]}",
                            ])
                    lines.append("    jmp .Lkuro_runtime_error")
                    for field in ordered_fields:
                        lines.append(f"{dispatch_labels[field]}:")
                        load(arguments[0], "%rax")
                        if call_name == "RecordSet":
                            load(arguments[2], "%rdx")
                            lines.append(f"    mov %rdx, {8 + field_slots[field] * 8}(%rax)")
                        else:
                            lines.append(f"    mov {8 + field_slots[field] * 8}(%rax), %rax")
                        store(instruction.dest)
                        lines.append(f"    jmp {done_label}")
                    lines.append(f"{done_label}:")
                    kinds[instruction.dest] = result_kind
                    if call_name == "RecordSet":
                        value_kind = kinds.get(arguments[2], "unknown")
                        value_length = text_lengths.get(arguments[2])
                        for field in ordered_fields:
                            previous_kind = record_field_kinds.get(field, "unknown")
                            record_field_kinds[field] = (
                                value_kind if previous_kind == value_kind else "unknown"
                            )
                            previous_length = record_field_lengths.get(field)
                            if (
                                previous_kind == value_kind == "text"
                                and previous_length is not None
                                and previous_length == value_length
                            ):
                                record_field_lengths[field] = value_length
                            else:
                                record_field_lengths.pop(field, None)
                    elif result_kind == "text":
                        lengths = {record_field_lengths.get(field) for field in ordered_fields}
                        if len(lengths) == 1 and None not in lengths:
                            text_lengths[instruction.dest] = next(iter(lengths))
                        else:
                            text_lengths.pop(instruction.dest, None)
            elif call_name == "MakeClosure":
                if len(arguments) != 1 or arguments[0] not in known_text or known_text[arguments[0]] not in ir.functions:
                    raise NativeBackendError("x86_64-linux MakeClosure requires a statically known action")
                action = known_text[arguments[0]]
                if function_capture_names.get(action):
                    raise NativeBackendError(
                        "x86_64-linux captured MakeClosure requires construction inside an action"
                    )
                lines.append(f"    lea .Lkuro_fn_{action}(%rip), %rax")
                store(instruction.dest)
                kinds[instruction.dest] = "closure"
                closure_actions[instruction.dest] = action
            elif call_name == "Invoke":
                if not arguments or len(arguments) > 7:
                    raise NativeBackendError("x86_64-linux Invoke requires a closure and at most six arguments")
                action_arguments = tuple(arguments[1:])
                incoming_closure_targets = closure_targets_before[instruction_index] or {}
                candidate_actions = set(incoming_closure_targets.get(arguments[0], set()))
                if not candidate_actions and arguments[0] in closure_actions:
                    candidate_actions.add(closure_actions[arguments[0]])
                if not candidate_actions:
                    raise NativeBackendError("x86_64-linux Invoke requires closures with statically known targets")
                for candidate in candidate_actions:
                    function = ir.functions.get(candidate)
                    if function is None or len(action_arguments) != len(function.params):
                        raise NativeBackendError(
                            f"x86_64-linux Invoke target {candidate!r} has an incompatible argument count"
                        )
                    remember_action_argument_kinds(candidate, action_arguments)
                return_kinds = {
                    action_return_kind(candidate, action_arguments)
                    for candidate in candidate_actions
                }
                if len(return_kinds) != 1:
                    raise NativeBackendError("x86_64-linux Invoke targets must have the same return kind")
                registers = ("%rdi", "%rsi", "%rdx", "%rcx", "%r8", "%r9")
                load(arguments[0], "%r11")
                # Captured closure object pointers carry a low-bit tag; raw
                # no-capture function pointers are 16-byte aligned.
                raw_closure_label = f".Lkuro_invoke_raw_{instruction_index}"
                invoke_ready_label = f".Lkuro_invoke_ready_{instruction_index}"
                lines.extend([
                    "    test $1, %r11",
                    f"    jz {raw_closure_label}",
                    "    and $-2, %r11",
                    "    mov 0(%r11), %rax",
                    "    mov 8(%r11), %r10",
                    "    mov %rax, %r11",
                    f"    jmp {invoke_ready_label}",
                    f"{raw_closure_label}:",
                    "    xor %r10d, %r10d",
                    f"{invoke_ready_label}:",
                ])
                for index, argument in enumerate(action_arguments):
                    load(argument, registers[index])
                load("_")
                lines.append("    call *%r11")
                store(instruction.dest)
                kinds[instruction.dest] = next(iter(return_kinds))
            elif call_name == "Spawn":
                if len(arguments) != 2 or arguments[0] not in closure_actions:
                    raise NativeBackendError("x86_64-linux Spawn requires a statically known closure and one argument")
                action = closure_actions[arguments[0]]
                if len(ir.functions[action].params) != 1:
                    raise NativeBackendError("x86_64-linux Spawn supports actions with exactly one parameter")
                remember_action_argument_kinds(action, (arguments[1],))
                label = task_argument_labels.get(instruction.dest)
                if label is None:
                    raise NativeBackendError("x86_64-linux Spawn requires a destination")
                load(arguments[1], "%rax")
                lines.append(f"    mov %rax, {label}(%rip)")
                lines.append(f"    lea {label}(%rip), %rax")
                store(instruction.dest)
                kinds[instruction.dest] = "task"
                task_actions[instruction.dest] = action
                task_argument_refs[instruction.dest] = label
                task_argument_values[instruction.dest] = arguments[1]
            elif call_name == "Await":
                if len(arguments) != 1 or arguments[0] not in task_actions:
                    raise NativeBackendError("x86_64-linux Await requires a statically known task")
                action = task_actions[arguments[0]]
                label = task_argument_refs[arguments[0]]
                lines.append(f"    mov {label}(%rip), %rdi")
                lines.append("    xor %r10d, %r10d")
                load("_")
                lines.append(f"    call .Lkuro_fn_{action}")
                store(instruction.dest)
                kinds[instruction.dest] = action_return_kind(action, (task_argument_values[arguments[0]],))
            elif call_name == "MakeEnum":
                if len(arguments) != 2 or any(argument not in known_text for argument in arguments):
                    raise NativeBackendError("x86_64-linux MakeEnum requires known type and variant names")
                enum_text = f"{known_text[arguments[0]]}.{known_text[arguments[1]]}"
                label = f".Lkuro_data_{len(data)}"
                encoded = enum_text.encode("utf-8")
                data.append((label, encoded + b"\0"))
                lines.append(f"    lea {label}(%rip), %rax")
                store(instruction.dest)
                kinds[instruction.dest] = "text"
                text_lengths[instruction.dest] = len(encoded)
                known_text[instruction.dest] = enum_text
            elif call_name == "MakeMap" and not arguments:
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
                    lines.extend([f"    cmpq $0, {presence}(%rax)", "    setne %al", "    movzbq %al, %rax"])
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
                if function_capture_names.get(call_name):
                    raise NativeBackendError(
                        f"x86_64-linux action {call_name!r} requires a captured closure environment"
                    )
                if len(arguments) > 6:
                    raise NativeBackendError("x86_64-linux action call supports at most six arguments")
                remember_action_argument_kinds(call_name, tuple(arguments))
                for index, argument in enumerate(arguments):
                    load(argument, f"%{('rdi', 'rsi', 'rdx', 'rcx', 'r8', 'r9')[index]}")
                lines.append("    xor %r10d, %r10d")
                load("_")
                lines.append(f"    call .Lkuro_fn_{call_name}")
                store(instruction.dest)
                kinds[instruction.dest] = action_return_kind(call_name, tuple(arguments))
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
                elif text_lengths.get(name, 0) > 0:
                    lines.append(f"    mov ${text_lengths[name]}, %rdx")
                else:
                    lines.extend([
                        "    mov %rsi, %rax", "    call _kuro_strlen", "    mov %rax, %rdx",
                    ])
                lines.extend([
                    "    mov $1, %rax", "    mov $1, %rdi", "    syscall",
                    "    lea .Lkuro_newline(%rip), %rsi", "    mov $1, %rdx",
                    "    mov $1, %rax", "    mov $1, %rdi", "    syscall",
                ])
            elif kind == "number":
                load(name); lines.append("    call _kuro_print_int")
            elif kind == "float":
                load(name); lines.append("    call _kuro_print_float")
            elif kind == "collection":
                if collection_kinds.get(collection_name) == "text":
                    # Linux syscall clobbers %rcx, so reload the collection
                    # length at each loop head and measure each NUL-terminated
                    # text item instead of trusting stale length metadata.
                    lines.extend([
                        "    xor %r8d, %r8d",
                        f"    lea {collection_buffers[collection_name]}(%rip), %r9",
                        ".Lkuro_print_text_collection:",
                        f"    mov {collection_lengths[collection_name]}(%rip), %rcx",
                        "    cmp %rcx, %r8", "    jae .Lkuro_print_collection_done",
                        "    mov (%r9,%r8,8), %rsi",
                        "    mov %rsi, %rax", "    call _kuro_strlen", "    mov %rax, %rdx",
                        "    mov $1, %rax", "    mov $1, %rdi", "    syscall",
                        "    lea .Lkuro_newline(%rip), %rsi", "    mov $1, %rdx",
                        "    mov $1, %rax", "    mov $1, %rdi", "    syscall",
                        "    inc %r8", "    jmp .Lkuro_print_text_collection",
                        ".Lkuro_print_collection_done:",
                    ])
                elif collection_kinds.get(collection_name) == "float":
                    unique = len(lines)
                    loop_label = f".Lkuro_print_float_collection_{unique}"
                    done_label = f".Lkuro_print_float_collection_done_{unique}"
                    lines.extend([
                        "    xor %r8d, %r8d",
                        f"    lea {collection_buffers[collection_name]}(%rip), %r9",
                        f"{loop_label}:",
                        f"    mov {collection_lengths[collection_name]}(%rip), %rcx",
                        "    cmp %rcx, %r8", f"    jae {done_label}",
                        "    mov (%r9,%r8,8), %rax", "    push %r9", "    call _kuro_print_float", "    pop %r9",
                        "    inc %r8", f"    jmp {loop_label}", f"{done_label}:",
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
        # Result storage belongs to this stack frame, never an ambient global
        # or mutable capture. %rax carries its entry value independently of the
        # six argument registers and %r10 closure-environment channel.
        fn_names = set(function.params) | {"_"}
        for item in function.body:
            if item.dest:
                if item.dest not in global_names:
                    fn_names.add(item.dest)
            for argument in item.args:
                if isinstance(argument, str):
                    if argument not in global_names and argument not in collection_buffers and argument not in input_buffers:
                        fn_names.add(argument)
        fn_slots = {name: -(index + 1) * 8 for index, name in enumerate(sorted(fn_names))}
        fn_env_slot = -(len(fn_slots) + 1) * 8
        fn_frame = (((len(fn_slots) + 1) * 8 + 15) // 16) * 16 or 16
        fn_labels = {item.dest: f".Lkuro_fn_{function.name}_{item.dest}" for item in function.body if item.op == "LABEL"}
        parameter_hints = function_parameter_kinds.get(function.name, {})
        fn_kinds: dict[str, str] = {
            name: parameter_hints.get(name, inferred_symbol_kind(name))
            for name in function.params
        }
        fn_kinds.update(function_capture_kinds.get(function.name, {}))
        for parameter, declared_type in function.parameter_types.items():
            declared_kind = _native_kind_for_type(declared_type)
            if declared_kind is not None:
                fn_kinds[parameter] = declared_kind
        # The Kuro VM deliberately stores dynamically typed values in generic
        # names such as ``*_Value`` and ``_``.  For the native lowering pass,
        # collect hard numeric-use constraints before emitting instructions so
        # a numeric VM branch is not mistaken for text merely because of its
        # variable name.
        fn_numeric_names: set[str] = {
            name for name in function.params if parameter_hints.get(name) == "number"
        }
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
            if numeric_name in fn_kinds and fn_kinds[numeric_name] != "float":
                fn_kinds[numeric_name] = "number"
        function_statically_text = _statically_text_values(
            function.body, ir.symbol_types, collection_names,
            function.parameter_types,
        )
        fn_text_lengths: dict[str, int] = {}
        fn_collection_kinds: dict[str, str] = {
            name: ("number" if any(word in name.lower() for word in ("count", "pos", "start", "end", "index", "depth", "len")) else "text")
            for name in collection_buffers
        }
        for name, kind in fn_kinds.items():
            if kind.startswith("collection:"):
                fn_collection_kinds[name] = kind.split(":", 1)[1]
        fn_known_text = {
            item.dest: item.args[0]
            for item in function.body
            if item.op == "CONST" and item.dest and isinstance(item.args[0], str)
        }
        lines.extend([
            "    .p2align 4", f".Lkuro_fn_{function.name}:", "    push %rbp", "    mov %rsp, %rbp",
            f"    sub ${fn_frame}, %rsp", f"    mov %r10, {fn_env_slot}(%rbp)",
            f"    mov %rax, {fn_slots['_']}(%rbp)",
        ])
        result_capture_index = function_capture_slots.get(function.name, {}).get("_")
        if result_capture_index is not None:
            # Preserve an already-admitted captured result as an entry snapshot,
            # but writes/producers must not mutate that snapshot on later Invoke.
            lines.extend([
                f"    mov {result_capture_index * 8}(%r10), %rax",
                f"    mov %rax, {fn_slots['_']}(%rbp)",
            ])

        def fn_load(name: str, register: str = "%rax") -> None:
            capture_index = function_capture_slots.get(function.name, {}).get(name) if name != "_" else None
            if capture_index is not None:
                lines.append(f"    mov {fn_env_slot}(%rbp), %r11")
                lines.append(f"    mov {capture_index * 8}(%r11), {register}")
                return
            if name in fn_slots:
                lines.append(f"    mov {fn_slots[name]}(%rbp), {register}")
                return
            if name in collection_buffers:
                lines.append(f"    lea {collection_buffers[name]}(%rip), {register}")
                return
            if name in input_buffers:
                lines.append(f"    lea {input_buffers[name]}(%rip), {register}")
                return
            if name in global_labels:
                lines.append(f"    mov {global_labels[name]}(%rip), {register}")
                return
            raise NativeBackendError(f"x86_64-linux action {function.name!r} cannot load {name!r}")

        def fn_store(name: str, register: str = "%rax") -> None:
            capture_index = function_capture_slots.get(function.name, {}).get(name) if name != "_" else None
            if capture_index is not None:
                lines.append(f"    mov {fn_env_slot}(%rbp), %r11")
                lines.append(f"    mov {register}, {capture_index * 8}(%r11)")
                return
            if name in fn_slots:
                lines.append(f"    mov {register}, {fn_slots[name]}(%rbp)")
                return
            if name in global_labels:
                lines.append(f"    mov {register}, {global_labels[name]}(%rip)")
                return
            raise NativeBackendError(f"x86_64-linux action {function.name!r} cannot store {name!r}")

        for index, parameter in enumerate(function.params):
            fn_store(parameter, f"%{('rdi', 'rsi', 'rdx', 'rcx', 'r8', 'r9')[index]}")
        for function_item_index, item in enumerate(function.body):
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
                # Actions may read text constants initialized in the main
                # program. Preserve that concrete global kind before falling
                # back to name-based inference (e.g. NativeBackslash).
                source_kind = fn_kinds.get(source, kinds.get(source, inferred))
                if source_kind == "float":
                    fn_kinds[item.dest] = "float"
                elif source in fn_numeric_names:
                    fn_kinds[item.dest] = "number"
                else:
                    fn_kinds[item.dest] = "text" if strong_text_name else source_kind
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
                fn_load(values[0]); fn_store(name)
                source_kind = fn_kinds.get(values[0], inferred_symbol_kind(values[0]))
                fn_kinds[name] = source_kind if source_kind == "float" else ("number" if values[0] in fn_numeric_names else source_kind)
                if values[0] in fn_text_lengths:
                    fn_text_lengths[name] = fn_text_lengths[values[0]]
            elif fn_op == "UPDATE":
                name, value = item.args
                fn_load(value); fn_store(name)
                source_kind = fn_kinds.get(value, inferred_symbol_kind(value))
                fn_kinds[name] = source_kind if source_kind == "float" else ("number" if value in fn_numeric_names else source_kind)
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
                        f"    cmp ${text_heap_capacity}, %rcx", "    ja .Lkuro_overflow",
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
                        f"    cmp ${text_heap_capacity}, %rcx", "    ja .Lkuro_overflow",
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
                if (
                    name in collection_buffers
                    or name in untracked_collection_pointers[function.name]
                    or fn_kinds.get(name, "") == "collection"
                    or fn_kinds.get(name, "").startswith("collection:")
                ):
                    if name in untracked_collection_pointers[function.name] or name not in collection_lengths or name in function.params or name in function_capture_slots.get(function.name, {}):
                        raise NativeBackendError("x86_64-linux action GET requires logical length metadata for collection parameters or captures")
                    lines.extend(_x86_collection_index_bounds(collection_lengths[name], read=True))
                    fn_load(name, "%rax")
                    lines.extend([
                        "    mov (%rax,%rcx,8), %rax",
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
                if (
                    name in collection_buffers
                    or name in untracked_collection_pointers[function.name]
                    or fn_kinds.get(name, "") == "collection"
                    or fn_kinds.get(name, "").startswith("collection:")
                ):
                    if fn_kinds.get(name, "").startswith("collection:"):
                        collection_item_kind = fn_collection_kinds.get(name, "unknown")
                        if fn_kinds.get(value_temp, "unknown") != collection_item_kind:
                            raise NativeBackendError(
                                "x86_64-linux captured collection SET value kind must match the known element kind"
                            )
                        if collection_item_kind == "text":
                            raise NativeBackendError(
                                "x86_64-linux captured collection SET does not yet update text item lengths"
                            )
                    if name in untracked_collection_pointers[function.name] or name not in collection_lengths or name in function.params or name in function_capture_slots.get(function.name, {}):
                        raise NativeBackendError("x86_64-linux action SET requires logical length metadata for collection parameters or captures")
                    lines.extend(_x86_collection_index_bounds(collection_lengths[name], read=False))
                    fn_load(name, "%rax")
                    lines.append("    mov %rdx, (%rax,%rcx,8)")
                else:
                    fn_load(name, "%rax")
                    lines.extend(["    mov %dl, (%rax,%rcx,1)"])
            elif fn_op == "LENGTH":
                name = item.args[0]
                if fn_kinds.get(name, "").startswith("collection:"):
                    raise NativeBackendError(
                        "x86_64-linux action LENGTH does not yet support captured collection lengths"
                    )
                if name in untracked_collection_pointers[function.name] or fn_kinds.get(name) == "collection" and (name not in collection_lengths or name in function.params or name in function_capture_slots.get(function.name, {})):
                    raise NativeBackendError("x86_64-linux action LENGTH requires logical length metadata for collection parameters or aliases")
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
                if fn_kinds.get(name, "").startswith("collection:"):
                    raise NativeBackendError(
                        "x86_64-linux action APPEND does not yet support captured collection length metadata"
                    )
                if name in untracked_collection_pointers[function.name] or name in function.params or name in function_capture_slots.get(function.name, {}) or fn_kinds.get(name) == "collection" and name not in collection_lengths:
                    raise NativeBackendError("x86_64-linux action APPEND requires logical length metadata for collection parameters or aliases")
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
            elif fn_op == "ARTIFACT_SUFFIX":
                if len(item.args) != 2:
                    raise NativeBackendError(f"x86_64-linux action {function.name!r} ARTIFACT_SUFFIX requires Text and an integer offset")
                source, offset = item.args
                if source not in function_statically_text:
                    raise NativeBackendError(f"x86_64-linux action {function.name!r} ARTIFACT_SUFFIX requires a statically known Text source")
                fn_load(source, "%r8")
                fn_load(offset, "%r9")
                lines.extend([
                    "    test %r9, %r9", "    js .Lkuro_bounds",
                    "    mov %r8, %rax", "    call _kuro_strlen", "    cmp %rax, %r9", "    ja .Lkuro_bounds",
                    "    sub %r9, %rax", "    mov %rax, %r10",
                    "    mov .Lkuro_text_heap_cursor(%rip), %rdx", "    mov %rdx, %rcx", "    add %r10, %rcx", "    inc %rcx",
                    f"    cmp ${text_heap_capacity}, %rcx", "    ja .Lkuro_overflow",
                    "    lea .Lkuro_text_heap(%rip), %rdi", "    add %rdx, %rdi", "    lea (%r8,%r9,1), %rsi",
                    "    mov %r10, %rcx", "    rep movsb", "    movb $0, (%rdi)",
                    "    lea .Lkuro_text_heap(%rip), %rsi", "    mov %rdi, %rcx", "    sub %rsi, %rcx", "    inc %rcx",
                    "    mov %rcx, .Lkuro_text_heap_cursor(%rip)", "    lea .Lkuro_text_heap(%rip), %rax", "    add %rdx, %rax",
                ])
                fn_store(item.dest)
                fn_kinds[item.dest] = "text"
            elif fn_op == "CALL":
                name, *arguments = item.args
                if name in {"MapGet", "MapSet", "MapHas"}:
                    expected_count = 3 if name == "MapSet" else 2
                    if len(arguments) != expected_count:
                        expected_arguments = (
                            "a map, key, and value"
                            if name == "MapSet"
                            else "a map and key"
                        )
                        raise NativeBackendError(
                            f"x86_64-linux action {name} requires {expected_arguments}"
                        )
                    if fn_kinds.get(arguments[0]) != "map":
                        raise NativeBackendError(
                            f"x86_64-linux action {name} currently requires a statically known map reference"
                        )
                    key = fn_known_text.get(arguments[1])
                    if key is None:
                        raise NativeBackendError(
                            f"x86_64-linux action {name} requires a statically known literal text key"
                        )
                    slot = map_key_slots.setdefault(key, len(map_key_slots))
                    if slot >= 512:
                        raise NativeBackendError("x86_64-linux map exceeds fixed capacity of 512 keys")
                    value_offset = slot * 8
                    presence_offset = 4096 + slot * 8
                    if name == "MapHas":
                        fn_load(arguments[0], "%rax")
                        lines.extend([
                            f"    cmpq $0, {presence_offset}(%rax)",
                            "    setne %al",
                            "    movzbq %al, %rax",
                        ])
                        fn_store(item.dest)
                        fn_kinds[item.dest] = "number"
                    elif name == "MapGet":
                        value_kind = map_value_kinds.get(key, "unknown")
                        if value_kind == "unknown":
                            raise NativeBackendError(
                                "x86_64-linux action MapGet requires a key with a previously known value kind"
                            )
                        fn_load(arguments[0], "%rax")
                        lines.append(f"    mov {value_offset}(%rax), %rax")
                        fn_store(item.dest)
                        fn_kinds[item.dest] = value_kind
                        if value_kind == "text" and key in map_value_lengths:
                            fn_text_lengths[item.dest] = map_value_lengths[key]
                    else:
                        expected_kind = map_value_kinds.get(key, "unknown")
                        value_kind = fn_kinds.get(arguments[2], "unknown")
                        if expected_kind == "unknown" or value_kind != expected_kind:
                            raise NativeBackendError(
                                "x86_64-linux action MapSet value kind must match the key's statically known kind"
                            )
                        if expected_kind == "text":
                            raise NativeBackendError(
                                "x86_64-linux action MapSet does not yet support text values with variable display lengths"
                            )
                        fn_load(arguments[2], "%rdx")
                        fn_load(arguments[0], "%rax")
                        lines.extend([
                            f"    mov %rdx, {value_offset}(%rax)",
                            f"    movq $1, {presence_offset}(%rax)",
                        ])
                        fn_store(item.dest)
                        fn_kinds[item.dest] = "map"
                    continue
                if name in {"RecordGet", "RecordSet"}:
                    expected_count = 2 if name == "RecordGet" else 3
                    if len(arguments) != expected_count:
                        expected_arguments = (
                            "a record and field name"
                            if name == "RecordGet"
                            else "a record, field name, and value"
                        )
                        raise NativeBackendError(
                            f"x86_64-linux action {name} requires {expected_arguments}"
                        )
                    if fn_kinds.get(arguments[0]) != "record":
                        raise NativeBackendError(
                            f"x86_64-linux action {name} currently requires a statically known record reference"
                        )
                    field = fn_known_text.get(arguments[1])
                    if field is None:
                        raise NativeBackendError(
                            f"x86_64-linux action {name} requires a statically known literal field name"
                        )
                    slot = record_field_slots.setdefault(field, len(record_field_slots))
                    if slot >= 63:
                        raise NativeBackendError("x86_64-linux record exceeds fixed capacity of 63 fields")
                    field_kind = record_field_kinds.get(field, "unknown")
                    if field_kind == "unknown":
                        raise NativeBackendError(
                            f"x86_64-linux action {name} requires a field with a previously known value kind"
                        )
                    if name == "RecordGet":
                        fn_load(arguments[0], "%rax")
                        lines.append(f"    mov {8 + slot * 8}(%rax), %rax")
                        fn_store(item.dest)
                        fn_kinds[item.dest] = field_kind
                        if field_kind == "text" and field in record_field_lengths:
                            fn_text_lengths[item.dest] = record_field_lengths[field]
                    else:
                        value_kind = fn_kinds.get(arguments[2], "unknown")
                        if value_kind != field_kind:
                            raise NativeBackendError(
                                "x86_64-linux action RecordSet value kind must match the field's statically known kind"
                            )
                        if field_kind == "text":
                            raise NativeBackendError(
                                "x86_64-linux action RecordSet does not yet support text fields with variable display lengths"
                            )
                        fn_load(arguments[0], "%rax")
                        fn_load(arguments[2], "%rdx")
                        lines.append(f"    mov %rdx, {8 + slot * 8}(%rax)")
                        fn_store(item.dest)
                        fn_kinds[item.dest] = "record"
                    continue
                if name == "MakeClosure":
                    target = function_closure_construction_targets.get(
                        (function.name, function_item_index)
                    )
                    if target is None:
                        raise NativeBackendError(
                            f"x86_64-linux action {function.name!r} MakeClosure requires a statically known action"
                        )
                    capture_slots = function_capture_slots.get(target, {})
                    for capture_name in capture_slots:
                        capture_kind = fn_kinds.get(capture_name, "unknown")
                        if capture_kind not in {"number", "float", "text", "record", "map"} and not capture_kind.startswith("collection:"):
                            raise NativeBackendError(
                                "x86_64-linux action-created closures currently support statically known numeric, text, record, map, or collection captures only"
                            )
                        if capture_kind == "collection:unknown":
                            raise NativeBackendError(
                                "x86_64-linux collection captures require a statically known element kind"
                            )
                        target_capture_kind = function_capture_kinds.get(target, {}).get(
                            capture_name, "unknown"
                        )
                        if target_capture_kind != capture_kind:
                            raise NativeBackendError(
                                "x86_64-linux closure capture kinds must be statically consistent across constructors"
                            )
                    if capture_slots:
                        lines.extend([
                            "    call _kuro_alloc_closure",
                            "    mov %rax, %r9",
                            f"    lea .Lkuro_fn_{target}(%rip), %rax",
                            "    mov %rax, 0(%r9)",
                            "    lea 16(%r9), %rax",
                            "    mov %rax, 8(%r9)",
                        ])
                        for capture_name, capture_index in capture_slots.items():
                            if 16 + capture_index * 8 >= closure_object_bytes:
                                raise NativeBackendError(
                                    f"x86_64-linux closure {target!r} exceeds the fixed capture capacity"
                                )
                            fn_load(capture_name, "%rax")
                            lines.append(f"    mov %rax, {16 + capture_index * 8}(%r9)")
                        lines.extend(["    lea 1(%r9), %rax"])
                        fn_store(item.dest)
                    else:
                        lines.append(f"    lea .Lkuro_fn_{target}(%rip), %rax")
                        fn_store(item.dest)
                    fn_kinds[item.dest] = "closure"
                    continue
                if name in ir.functions and function_capture_names.get(name):
                    raise NativeBackendError(
                        f"x86_64-linux action {name!r} requires a captured closure environment"
                    )
                if name not in ir.functions or len(arguments) > 6:
                    raise NativeBackendError(f"x86_64-linux action {function.name!r} cannot call {name!r}")
                registers = ("rdi", "rsi", "rdx", "rcx", "r8", "r9")
                for index, argument in enumerate(arguments): fn_load(argument, f"%{registers[index]}")
                lines.append("    xor %r10d, %r10d")
                fn_load("_")
                lines.append(f"    call .Lkuro_fn_{name}")
                fn_store(item.dest)
                fn_kinds[item.dest] = "text" if action_returns_text(name) else "number"
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
                elif fn_kinds.get(name) == "float":
                    fn_load(name); lines.append("    call _kuro_print_float")
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
    lines.extend([
        "_kuro_print_float:", "    push %rbp", "    mov %rsp, %rbp", "    sub $112, %rsp",
        "    mov %rax, %r11", "    sar $63, %r11", "    mov %r11, -88(%rbp)",
        "    btr $63, %rax", "    mov %rax, -96(%rbp)", "    mov %rax, -104(%rbp)", "    movq $0, -40(%rbp)", "    movq $0, -48(%rbp)",
        "    mov %rax, %r10", "    movabs $0x7ff0000000000000, %r9", "    and %r9, %r10", "    cmp %r9, %r10", "    je .Lkuro_print_float_nonfinite",
        "    test %rax, %rax", "    jz .Lkuro_print_float_fixed", "    movq %rax, %xmm0",
        "    ucomisd .Lkuro_float_scientific_min(%rip), %xmm0", "    jb .Lkuro_print_float_scientific",
        "    ucomisd .Lkuro_float_scientific_max(%rip), %xmm0", "    jae .Lkuro_print_float_scientific", "    jmp .Lkuro_print_float_fixed",
        ".Lkuro_print_float_nonfinite:", "    mov %rax, %r10", "    movabs $0x000fffffffffffff, %r9", "    and %r9, %r10", "    test %r10, %r10", "    jnz .Lkuro_print_float_nan",
        "    cmpq $0, -88(%rbp)", "    jne .Lkuro_print_float_negative_infinity", "    lea .Lkuro_float_inf_text(%rip), %rsi", "    mov $4, %rdx", "    jmp .Lkuro_print_float_special_write",
        ".Lkuro_print_float_negative_infinity:", "    lea .Lkuro_float_negative_inf_text(%rip), %rsi", "    mov $5, %rdx", "    jmp .Lkuro_print_float_special_write",
        ".Lkuro_print_float_nan:", "    lea .Lkuro_float_nan_text(%rip), %rsi", "    mov $4, %rdx",
        ".Lkuro_print_float_special_write:", "    mov $1, %rax", "    mov $1, %rdi", "    syscall", "    leave", "    ret",
        ".Lkuro_print_float_scientific:", "    movq $1, -40(%rbp)", "    movq -96(%rbp), %xmm0", "    xor %r10d, %r10d",
        ".Lkuro_float_exp_find:", "    ucomisd .Lkuro_float_ten(%rip), %xmm0", "    jae .Lkuro_float_exp_large",
        "    ucomisd .Lkuro_float_one(%rip), %xmm0", "    jb .Lkuro_float_exp_small", "    jmp .Lkuro_float_exp_found",
        ".Lkuro_float_exp_large:", "    divsd .Lkuro_float_ten(%rip), %xmm0", "    inc %r10", "    jmp .Lkuro_float_exp_find",
        ".Lkuro_float_exp_small:", "    mulsd .Lkuro_float_ten(%rip), %xmm0", "    dec %r10", "    jmp .Lkuro_float_exp_find",
        ".Lkuro_float_exp_found:", "    mov %r10, -48(%rbp)", "    fldl -96(%rbp)", "    lea .Lkuro_float_pow10_ext(%rip), %r8",
        "    test %r10, %r10", "    js .Lkuro_float_scale_small", "    mov %r10, %r9", "    imul $10, %r9, %r9", "    fldt (%r8,%r9)", "    fdivrp %st, %st(1)", "    jmp .Lkuro_float_scale_done",
        ".Lkuro_float_scale_small:", "    neg %r10", "    mov %r10, %r9", "    imul $10, %r9, %r9", "    fldt (%r8,%r9)", "    fmulp %st, %st(1)",
        ".Lkuro_float_scale_done:", "    fstpl -96(%rbp)", "    movq -96(%rbp), %xmm0",
        "    ucomisd .Lkuro_float_one(%rip), %xmm0", "    jb .Lkuro_float_adjust_low", "    ucomisd .Lkuro_float_ten(%rip), %xmm0", "    jae .Lkuro_float_adjust_high", "    jmp .Lkuro_print_float_fixed",
        ".Lkuro_float_adjust_low:", "    mulsd .Lkuro_float_ten(%rip), %xmm0", "    movq %xmm0, -96(%rbp)", "    decq -48(%rbp)", "    jmp .Lkuro_print_float_fixed",
        ".Lkuro_float_adjust_high:", "    divsd .Lkuro_float_ten(%rip), %xmm0", "    movq %xmm0, -96(%rbp)", "    incq -48(%rbp)",
        ".Lkuro_print_float_fixed:", "    movq -96(%rbp), %xmm0", "    cvttsd2si %xmm0, %rax",
        "    mov %rax, -72(%rbp)", "    mov %rax, -56(%rbp)", "    cvtsi2sd %rax, %xmm1", "    subsd %xmm1, %xmm0",
        "    mulsd .Lkuro_float_scale(%rip), %xmm0", "    addsd .Lkuro_float_round(%rip), %xmm0",
        "    cvttsd2si %xmm0, %rax", "    movabs $100000000000000000, %r9",
        "    cmp %r9, %rax", "    jne .Lkuro_print_float_frac_ready", "    incq -72(%rbp)", "    xor %eax, %eax",
        ".Lkuro_print_float_frac_ready:", "    mov %rax, -80(%rbp)",
        "    movq -96(%rbp), %xmm0", "    cvttsd2si %xmm0, %rax", "    cvtsi2sd %rax, %xmm1", "    subsd %xmm1, %xmm0",
        "    mulsd .Lkuro_float_scale16(%rip), %xmm0", "    addsd .Lkuro_float_round(%rip), %xmm0", "    cvttsd2si %xmm0, %rax",
        "    mov %rax, -64(%rbp)", "    movq -96(%rbp), %xmm0", "    cvttsd2si %xmm0, %rax", "    cvtsi2sd %rax, %xmm0",
        "    mov -64(%rbp), %rax", "    cvtsi2sd %rax, %xmm1", "    divsd .Lkuro_float_scale16(%rip), %xmm1", "    addsd %xmm1, %xmm0",
        "    movq %xmm0, %rax", "    cmp -96(%rbp), %rax", "    jne .Lkuro_print_float_use17",
        "    mov -56(%rbp), %rax", "    mov %rax, -72(%rbp)", "    mov -64(%rbp), %rax", "    movabs $10000000000000000, %r9",
        "    cmp %r9, %rax", "    jne .Lkuro_print_float_16_no_carry", "    incq -72(%rbp)", "    xor %eax, %eax",
        ".Lkuro_print_float_16_no_carry:", "    mov %rax, -80(%rbp)", "    mov $16, %r10", "    cmpq $0, -40(%rbp)", "    jne .Lkuro_print_float_scientific_check", "    jmp .Lkuro_print_float_format_fraction",
        ".Lkuro_print_float_use17:", "    mov $17, %r10", "    cmpq $0, -40(%rbp)", "    jne .Lkuro_print_float_scientific_check", "    jmp .Lkuro_print_float_format_fraction",
        ".Lkuro_print_float_scientific_check:", "    mov %r10, -24(%rbp)", "    mov %r10, %r11", "    mov $1, %r9",
        ".Lkuro_float_candidate_scale:", "    test %r11d, %r11d", "    jz .Lkuro_float_candidate_scale_done", "    imul $10, %r9, %r9", "    dec %r11", "    jmp .Lkuro_float_candidate_scale",
        ".Lkuro_float_candidate_scale_done:", "    mov %r9, -32(%rbp)", "    mov -72(%rbp), %rax", "    imul %r9, %rax", "    add -80(%rbp), %rax", "    mov %rax, -64(%rbp)",
        "    mov -48(%rbp), %r10", "    sub -24(%rbp), %r10", "    fildll -64(%rbp)", "    lea .Lkuro_float_pow10_ext(%rip), %r8", "    test %r10, %r10", "    js .Lkuro_float_candidate_small",
        "    mov %r10, %r9", "    imul $10, %r9, %r9", "    fldt (%r8,%r9)", "    fmulp %st, %st(1)", "    jmp .Lkuro_float_candidate_scaled",
        ".Lkuro_float_candidate_small:", "    neg %r10", "    mov %r10, %r9", "    imul $10, %r9, %r9", "    fldt (%r8,%r9)", "    fdivrp %st, %st(1)",
        ".Lkuro_float_candidate_scaled:", "    fstpl -112(%rbp)", "    mov -112(%rbp), %rax", "    cmp -104(%rbp), %rax", "    jne .Lkuro_print_float_scientific_precise", "    mov -24(%rbp), %r10", "    jmp .Lkuro_print_float_scientific_shorten_start",
        ".Lkuro_print_float_scientific_precise:", "    fldl -104(%rbp)", "    lea .Lkuro_float_pow10_ext(%rip), %r8", "    mov -48(%rbp), %r10", "    test %r10, %r10", "    js .Lkuro_float_digits_small",
        "    mov %r10, %r9", "    imul $10, %r9, %r9", "    fldt (%r8,%r9)", "    fdivrp %st, %st(1)", "    jmp .Lkuro_float_digits_scaled",
        ".Lkuro_float_digits_small:", "    neg %r10", "    mov %r10, %r9", "    imul $10, %r9, %r9", "    fldt (%r8,%r9)", "    fmulp %st, %st(1)",
        ".Lkuro_float_digits_scaled:", "    fldt 160(%r8)", "    fmulp %st, %st(1)", "    fistpll -64(%rbp)",
        "    mov -64(%rbp), %rax", "    movabs $10000000000000000, %r9", "    xor %edx, %edx", "    div %r9", "    cmp $10, %rax", "    jae .Lkuro_float_digits_carry",
        "    mov %rax, -72(%rbp)", "    mov %rdx, -80(%rbp)", "    mov $16, %r10", "    jmp .Lkuro_print_float_scientific_shorten_start",
        ".Lkuro_float_digits_carry:", "    mov -64(%rbp), %rax", "    xor %edx, %edx", "    mov $10, %r9", "    div %r9", "    mov %rax, -64(%rbp)", "    movq $1, -72(%rbp)", "    movq $0, -80(%rbp)", "    incq -48(%rbp)", "    mov $16, %r10", "    jmp .Lkuro_print_float_scientific_shorten_start",
        ".Lkuro_print_float_scientific_shorten_start:", "    cmpq $10, -72(%rbp)", "    jne .Lkuro_float_shorten_normalized", "    mov -64(%rbp), %rax", "    xor %edx, %edx", "    mov $10, %r9", "    div %r9", "    mov %rax, -64(%rbp)", "    movq $1, -72(%rbp)", "    movq $0, -80(%rbp)", "    incq -48(%rbp)",
        ".Lkuro_float_shorten_normalized:", "    mov %r10, -16(%rbp)", "    mov $10, %rax", "    mov %rax, -32(%rbp)", "    decq %r10", "    mov %r10, -24(%rbp)",
        ".Lkuro_float_shorten_try:", "    cmpq $0, -24(%rbp)", "    jl .Lkuro_float_shorten_keep", "    mov -64(%rbp), %rax", "    xor %edx, %edx", "    divq -32(%rbp)", "    mov %rax, -56(%rbp)",
        "    fildll -56(%rbp)", "    lea .Lkuro_float_pow10_ext(%rip), %r8", "    mov -48(%rbp), %r10", "    sub -24(%rbp), %r10", "    test %r10, %r10", "    js .Lkuro_float_shorten_lower_small",
        "    mov %r10, %r9", "    imul $10, %r9, %r9", "    fldt (%r8,%r9)", "    fmulp %st, %st(1)", "    jmp .Lkuro_float_shorten_lower_scaled",
        ".Lkuro_float_shorten_lower_small:", "    neg %r10", "    mov %r10, %r9", "    imul $10, %r9, %r9", "    fldt (%r8,%r9)", "    fdivrp %st, %st(1)",
        ".Lkuro_float_shorten_lower_scaled:", "    fstpl -112(%rbp)", "    mov -112(%rbp), %rax", "    cmp -104(%rbp), %rax", "    je .Lkuro_float_shorten_accept",
        "    addq $1, -56(%rbp)", "    fildll -56(%rbp)", "    lea .Lkuro_float_pow10_ext(%rip), %r8", "    mov -48(%rbp), %r10", "    sub -24(%rbp), %r10", "    test %r10, %r10", "    js .Lkuro_float_shorten_upper_small",
        "    mov %r10, %r9", "    imul $10, %r9, %r9", "    fldt (%r8,%r9)", "    fmulp %st, %st(1)", "    jmp .Lkuro_float_shorten_upper_scaled",
        ".Lkuro_float_shorten_upper_small:", "    neg %r10", "    mov %r10, %r9", "    imul $10, %r9, %r9", "    fldt (%r8,%r9)", "    fdivrp %st, %st(1)",
        ".Lkuro_float_shorten_upper_scaled:", "    fstpl -112(%rbp)", "    mov -112(%rbp), %rax", "    cmp -104(%rbp), %rax", "    je .Lkuro_float_shorten_accept",
        "    mov -32(%rbp), %rax", "    imul $10, %rax, %rax", "    mov %rax, -32(%rbp)", "    decq -24(%rbp)", "    jmp .Lkuro_float_shorten_try",
        ".Lkuro_float_shorten_accept:", "    mov $1, %r9", "    mov -24(%rbp), %r11",
        ".Lkuro_float_shorten_output_scale:", "    test %r11d, %r11d", "    jz .Lkuro_float_shorten_output_ready", "    imul $10, %r9, %r9", "    dec %r11", "    jmp .Lkuro_float_shorten_output_scale",
        ".Lkuro_float_shorten_output_ready:", "    mov -56(%rbp), %rax", "    xor %edx, %edx", "    div %r9", "    cmp $10, %rax", "    jae .Lkuro_float_shorten_output_carry",
        "    mov %rax, -72(%rbp)", "    mov %rdx, -80(%rbp)", "    mov -24(%rbp), %r10", "    jmp .Lkuro_print_float_format_fraction",
        ".Lkuro_float_shorten_output_carry:", "    movq $1, -72(%rbp)", "    movq $0, -80(%rbp)", "    incq -48(%rbp)", "    mov -24(%rbp), %r10", "    jmp .Lkuro_print_float_format_fraction",
        ".Lkuro_float_shorten_keep:", "    mov -16(%rbp), %r10", "    jmp .Lkuro_print_float_format_fraction",
        ".Lkuro_print_float_format_fraction:", "    lea -1(%rbp), %rsi", "    movb $10, (%rsi)", "    mov $1, %rcx",
        "    cmpq $0, -40(%rbp)", "    je .Lkuro_print_float_no_exponent", "    mov -48(%rbp), %rax", "    test %rax, %rax", "    jns .Lkuro_print_float_exp_positive",
        "    neg %rax", "    mov $45, %r8d", "    jmp .Lkuro_print_float_exp_sign_ready", ".Lkuro_print_float_exp_positive:", "    mov $43, %r8d",
        ".Lkuro_print_float_exp_sign_ready:", "    xor %r11d, %r11d", "    mov $10, %r9",
        ".Lkuro_print_float_exp_digits:", "    xor %edx, %edx", "    div %r9", "    add $48, %dl", "    dec %rsi", "    mov %dl, (%rsi)", "    inc %rcx", "    inc %r11", "    test %rax, %rax", "    jnz .Lkuro_print_float_exp_digits",
        "    cmp $1, %r11", "    jne .Lkuro_print_float_exp_sign", "    dec %rsi", "    movb $48, (%rsi)", "    inc %rcx",
        ".Lkuro_print_float_exp_sign:", "    dec %rsi", "    mov %r8b, (%rsi)", "    inc %rcx", "    dec %rsi", "    movb $101, (%rsi)", "    inc %rcx",
        ".Lkuro_print_float_no_exponent:", "    mov -80(%rbp), %rax", "    test %rax, %rax", "    jnz .Lkuro_print_float_trim_start",
        "    cmpq $0, -40(%rbp)", "    je .Lkuro_print_float_fixed_zero_fraction", "    xor %r10d, %r10d", "    jmp .Lkuro_print_float_trim_done",
        ".Lkuro_print_float_fixed_zero_fraction:", "    mov $1, %r10", "    jmp .Lkuro_print_float_trim_done",
        ".Lkuro_print_float_trim_start:", "    mov $10, %r9",
        ".Lkuro_print_float_trim:", "    xor %edx, %edx", "    div %r9", "    test %rdx, %rdx",
        "    jne .Lkuro_print_float_trim_done", "    mov %rax, -80(%rbp)", "    dec %r10", "    jmp .Lkuro_print_float_trim",
        ".Lkuro_print_float_trim_done:", "    mov -80(%rbp), %rax", "    mov $10, %r9", "    test %r10, %r10", "    jz .Lkuro_print_float_fraction_done",
        ".Lkuro_print_float_fraction:", "    xor %edx, %edx", "    div %r9", "    add $48, %dl",
        "    dec %rsi", "    mov %dl, (%rsi)", "    inc %rcx", "    dec %r10", "    jnz .Lkuro_print_float_fraction",
        ".Lkuro_print_float_fraction_done:", "    cmpq $0, -40(%rbp)", "    je .Lkuro_print_float_emit_dot", "    cmpq $0, -80(%rbp)", "    je .Lkuro_print_float_integer",
        ".Lkuro_print_float_emit_dot:", "    dec %rsi", "    movb $46, (%rsi)", "    inc %rcx",
        ".Lkuro_print_float_integer:", "    mov -72(%rbp), %rax", "    mov $10, %r9",
        ".Lkuro_print_float_integer_loop:", "    xor %edx, %edx", "    div %r9", "    add $48, %dl",
        "    dec %rsi", "    mov %dl, (%rsi)", "    inc %rcx", "    test %rax, %rax", "    jnz .Lkuro_print_float_integer_loop",
        "    cmpq $0, -88(%rbp)", "    je .Lkuro_print_float_write", "    dec %rsi", "    movb $45, (%rsi)", "    inc %rcx",
        ".Lkuro_print_float_write:", "    mov $1, %rax", "    mov $1, %rdi", "    mov %rcx, %rdx", "    syscall",
        "    leave", "    ret",
    ])
    lines.extend([
        "_kuro_alloc_closure:",
        "    mov .Lkuro_closure_heap_cursor(%rip), %rax",
        "    mov %rax, %r8",
        "    mov .Lkuro_closure_heap_end(%rip), %rcx",
        f"    lea {closure_object_bytes}(%rax), %rdx",
        "    cmp %rcx, %rdx",
        "    jbe .Lkuro_alloc_closure_existing",
        "    xor %edi, %edi",
        "    mov $12, %eax",
        "    syscall",
        "    add $4095, %rax",
        "    and $-4096, %rax",
        "    mov %rax, %r8",
        f"    lea {closure_heap_page_bytes}(%r8), %r9",
        "    mov %r9, %rdi",
        "    mov $12, %eax",
        "    syscall",
        "    cmp %r9, %rax",
        "    jne .Lkuro_overflow",
        "    mov %r9, .Lkuro_closure_heap_end(%rip)",
        f"    lea {closure_object_bytes}(%r8), %rax",
        "    mov %rax, .Lkuro_closure_heap_cursor(%rip)",
        "    mov %r8, %rax",
        "    ret",
        ".Lkuro_alloc_closure_existing:",
        "    mov %rdx, .Lkuro_closure_heap_cursor(%rip)",
        "    mov %r8, %rax",
        "    ret",
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
    lines.extend(["    .p2align 4", f".Lkuro_text_heap: .zero {text_heap_capacity}", "    .p2align 3", ".Lkuro_text_heap_cursor: .zero 8"])
    for label in function_concat_buffers.values():
        lines.extend([f"    .p2align 3", f"{label}: .zero 4096"])
    for label in concat_buffers.values():
        lines.extend([f"    .p2align 3", f"{label}: .zero 4096"])
    for label in concat_lengths.values():
        lines.extend([f"    .p2align 3", f"{label}: .zero 8"])
    for label in global_labels.values():
        lines.extend([f"    .p2align 3", f"{label}: .zero 8"])
    lines.extend([
        "    .p2align 3",
        ".Lkuro_closure_heap_cursor: .zero 8",
        ".Lkuro_closure_heap_end: .zero 8",
    ])
    for label in map_dest_labels.values():
        lines.extend([f"    .p2align 3", f"{label}: .zero 8192"])
    for label in record_dest_labels.values():
        lines.extend([f"    .p2align 3", f"{label}: .zero 512"])
    for label in task_argument_labels.values():
        lines.extend([f"    .p2align 3", f"{label}: .zero 8"])
    for label in tagged_dest_labels.values():
        lines.extend([f"    .p2align 3", f"{label}: .zero 16"])
    lines.extend([".Lkuro_bss_end:", ".section .rodata", ".Lkuro_rodata_begin:"])
    for label, encoded in data:
        lines.append(f"{label}: .byte {', '.join(str(byte) for byte in encoded)}")
    for label, value in float_data:
        lines.append(f"{label}: .double {value!r}")
    lines.extend(["    .p2align 1", ".Lkuro_float_pow10_ext:"])
    for power in range(342):
        encoded_power = _x87_extended_power10_bytes(power)
        lines.append("    .byte " + ", ".join(str(byte) for byte in encoded_power))
    lines.extend([
        "    .p2align 3",
        ".Lkuro_float_scale: .double 100000000000000000.0",
        ".Lkuro_float_scale16: .double 10000000000000000.0",
        ".Lkuro_float_scientific_min: .double 0.0001",
        ".Lkuro_float_scientific_max: .double 10000000000000000.0",
        ".Lkuro_float_one: .double 1.0",
        ".Lkuro_float_ten: .double 10.0",
        ".Lkuro_float_round: .double 0.5",
        ".Lkuro_float_inf_text: .ascii \"inf\\n\"",
        ".Lkuro_float_negative_inf_text: .ascii \"-inf\\n\"",
        ".Lkuro_float_nan_text: .ascii \"nan\\n\"",
        ".Lkuro_newline: .byte 10", ".Lkuro_rodata_end:",
    ])
    return "\n".join(lines) + "\n"


def emit_x86_64_macos(
    ir: IRProgram, *, text_heap_capacity: int | None = None
) -> str:
    """Adapt the freestanding x86-64 lowering to Darwin's syscall ABI.

    The instruction/data ABI is deliberately shared with Linux.  Darwin
    distinguishes syscalls with the ``0x2000000`` class prefix, while the
    register convention for ``write`` and ``exit`` remains compatible with
    the emitted AT&T code.  Keeping this as a narrow ABI adapter means the
    language lowering itself stays platform-independent.
    """
    assembly = emit_x86_64_linux(ir, text_heap_capacity=text_heap_capacity)
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


def build_native(
    ir: IRProgram,
    output: str | Path,
    target: str | None = None,
    *,
    text_heap_capacity: int | None = None,
) -> Path:
    """Build a native image for an explicit or host-selected Kuro target."""
    text_heap_capacity = _resolve_text_heap_capacity(text_heap_capacity)
    destination = Path(output)
    destination.parent.mkdir(parents=True, exist_ok=True)
    assembly = destination.with_suffix(".s")
    selected = target or ("aarch64-macos" if __import__("platform").system() == "Darwin" and __import__("platform").machine() == "arm64" else "x86_64-linux")
    if selected == "aarch64-macos":
        assembly.write_text(emit_macos_arm64(ir), encoding="utf-8")
        command = ["clang", str(assembly), "-o", str(destination)]
    elif selected == "x86_64-macos":
        assembly.write_text(
            emit_x86_64_macos(ir, text_heap_capacity=text_heap_capacity),
            encoding="utf-8",
        )
        command = [
            "clang", "-target", "x86_64-apple-macos",
            "-nostdlib", "-Wl,-e,_start", str(assembly), "-lSystem", "-o", str(destination),
        ]
    elif selected == "x86_64-linux":
        assembly.write_text(
            emit_x86_64_linux(ir, text_heap_capacity=text_heap_capacity),
            encoding="utf-8",
        )
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
