# Kuro bytecode format — Stage 8

This document defines the first Kuro-owned bytecode encoding. It is a flat
list of values so it can be represented by Kuro's current collection model
while the self-hosted compiler is being bootstrapped.

Every instruction begins with a `BC_` opcode. Operands follow immediately and
are consumed according to the table below.

| Opcode | Operands |
| --- | --- |
| `BC_CONST` | value |
| `BC_LOADVAR` | variable name |
| `BC_STORE_LIST` | variable name |
| `BC_BINOP` | operator |
| `BC_CMP` | comparison operator |
| `BC_BOOL` | `AND` or `OR` |
| `BC_UPDATE`, `BC_ADD`, `BC_APPEND` | variable name |
| `BC_GET` | variable name, indexed flag (`0`/`1`) |
| `BC_LENGTH`, `BC_SET`, `BC_INPUT` | variable name |
| `BC_DECLTYPE` | variable name, type |
| `BC_PRINT` | none |
| `BC_IF_BEGIN`, `BC_ELSE_BEGIN`, `BC_IF_END` | none |
| `BC_REPEAT_BEGIN`, `BC_REPEAT_END` | none |
| `BC_WHILE_BEGIN`, `BC_WHILE_END` | none |
| `BC_FUNC_BEGIN` | function name |
| `BC_PARAM` | parameter name, type |
| `BC_FUNC_END`, `BC_RETURN` | none |
| `BC_CALL_BEGIN` | function name |
| `BC_CALL_END` | none |

The encoding is intentionally stack-oriented: value-producing operations push
onto the VM stack, mutation and output operations consume stack values, and
structured control markers delimit nested blocks. A later encoder revision
may replace markers with jump offsets after the Kuro VM has a verified
instruction-pointer model.

The JSON/binary development artifacts are executable through hosted `kuro
exec`. The native line-stream artifact is executable through `kuro-native
exec`; its instruction loop is the Kuro-authored `self_host/vm.kuro`, compiled
into `dist/kuro-bytecode`. The Kuro-authored `self_host/bytecode.kuro` encoder
remains the reference encoder. General native image construction still uses
the temporary bootstrap backend and system assembler/linker.

## Native stream format

The native compiler and standalone launcher use `kuro.bytecode/1`, a strict
UTF-8 line stream. The first line is exactly `kuro.bytecode/1`; every
subsequent non-empty physical line is one escaped flat bytecode value. A
missing header, raw empty lines, malformed escapes, CRLF framing, and a
header-only stream are rejected. Values use `\\e` for empty text, `\\n` for
LF, `\\r` for CR, `\\t` for tab, and `\\\\` for a literal backslash.

An optional physical line containing `kuro.input/1` terminates the bytecode
values. Every byte after that line's LF is application input. `BC_INPUT`
stores this payload on its first execution and stores empty text on later
executions, matching the native runtime's consume-to-EOF input behavior. An
ordinary bytecode value equal to the reserved marker is encoded as `\\i`, so
program data cannot be mistaken for framing.

The compiler escapes empty and control-character literals before publishing
an artifact. The loader reverses that encoding and checks opcode names, operand counts, and
balanced `If`, `Repeat`, `While`, function, and call structures before
execution. It limits the stream to 65,536 values, matching the native
collection ABI. Stack effects across branches and calls are still
validated dynamically by the VM.

The parser for this envelope is implemented in
`self_host/artifact_loader.kuro`, and the resulting `BytecodeOut` collection
is executed by `self_host/vm.kuro`. The built `dist/kuro-bytecode` image has
no Python runtime dependency and reports validation/runtime failure through
its real process exit status.

The same loader feeds `self_host/native_codegen.kuro` in the built
`dist/kuro-codegen` image. That Kuro-owned backend currently emits macOS arm64
assembly for literal output and straight-line or structured integer programs.
The integer subset includes variables, arithmetic (`+`, `-`, `*`, guarded
`/`), comparisons, `If`/`Else`, `Repeat`, `While`, assignment, `Add`, and
printing. It converts decimal assembly operands in Kuro, escapes quotes,
backslashes, and control characters, and includes its own integer-print
routine. The generator validates stack balance and structured-control nesting
and rejects unsupported bytecode, invalid integer spellings, oversized
immediates, malformed loops/branches, and runtime division by zero with a
nonzero process status.
