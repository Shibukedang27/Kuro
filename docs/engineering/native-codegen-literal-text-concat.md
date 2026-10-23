# Bounded native Text concatenation from literals

The Kuro-owned native code generator now lowers a deliberately small Text `+` case: two adjacent `BC_CONST_TEXT` operands in top-level straight-line code. The emitted native code copies their UTF-8 bytes into a distinct writable buffer and prints the resulting NUL-terminated Text. This is real runtime concatenation, not compile-time constant folding.

## Accepted boundary

Both operands must be explicit Text literals immediately before `BC_BINOP +`. The operation must be in the main program, outside Actions and `If`, `Repeat`, or `While` regions. The generator assigns a unique buffer to each accepted concat site, so one result cannot overwrite another. The shared Text-literal pool holds at most 64 entries; because each concat consumes two, at most 32 sites are possible, and ordinary Text literals can lower that ceiling. Each literal is already limited to fewer than 1,000 Kuro characters; the result buffer reserves four bytes per character plus the terminating NUL, up to 7,993 bytes for one site. That upper bound covers non-NUL UTF-8 code points without requiring the generator to infer dynamic string lengths.

Embedded-NUL operands are rejected because the current native Text representation and copy loop are NUL-terminated. Text values loaded from variables or Action parameters, shared-scalar Text loads, concatenation in Actions or control flow, and mixed-kind or non-`+` operations also remain rejected with empty assembly. The implementation does not infer Text from parameter names or unknown kinds. Each accepted site executes once in the generated straight-line main path; values are never reused through mutable aliases.

## Runtime and bootstrap limits

The emitter uses native byte-copy loops and target-specific writable storage for Linux x86-64, macOS x86-64, and macOS ARM64. Source-to-bytecode-to-assembly execution is exercised on Linux x86-64, with native macOS ARM64 execution gated to its matching runner; all three output formats are cross-assembled. These checks cover only the accepted literal case, not general Text runtime parity.

This slice does not make `RecordDiag.Message` safe to type as Text: the compiler's scratch messages still concatenate values loaded from scalars, and shared-scalar Text loads still lose their kind. The complete compiler artifact remains fail-closed in the Kuro-owned generator. Python-seeded image construction and Clang/LLVM assembly/linking remain prerequisites; no strict independence claim follows from this change.
