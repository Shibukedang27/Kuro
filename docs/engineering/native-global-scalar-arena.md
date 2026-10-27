# A separate bounded arena for native scalar globals

The native compiler generator previously placed shared scalar globals in the same 2 KiB stack frame as operand values and reserved Repeat counters. Raising its 64-slot admission limit would therefore have allowed global values to overwrite live frame storage. This change keeps the frame size fixed and places shared globals in a separate, zero-initialized static arena instead.

## Layout and limits

Each registered global slot is one 64-bit word at byte offset `slot_index * 8` in the arena. The explicit hard limit is 266 slots: exactly 2,128 bytes, with the last permitted slot at offset 2,120. Slot 267 fails closed and clears generated assembly. A zero-global program emits neither an arena symbol nor a reference to it; nonempty programs allocate exactly `8 * slot_count` bytes.

Per-call frames remain 2,048 bytes on all supported native targets. Operand-stack words stay in `[0, 1024)`, Action parameters and locals remain in `[1024, 1536)`, Repeat counters retain their reserved `[1536, 1664)` range, and text-print scratch remains at byte 2,040. Shared global values no longer consume any of those stack-frame offsets. Action parameters and the special Action-local result slot remain frame-local; non-parameter Action variables continue to share the same persistent globals as main.

Linux x86-64 emits a RIP-relative arena base and an aligned ELF `.bss` zero-fill. macOS x86-64 uses its platform symbol spelling and Mach-O `__DATA,__bss`; macOS ARM64 materializes the base with `adrp` plus `@PAGEOFF` and uses the same zero-fill section. The main prologue and explicit global initialization use this base, while Action frames and their parameter/local/Repeat addressing are unchanged.

## Evidence at the 266-slot boundary

The audited full compiler artifact contains 9,124 instructions across 9,125 lines and requires 191 distinct Action-body store names plus 84 main names, with nine shared names: 266 unique slots overall. A deterministic synthetic fixture mirrors that census, writes and reads slot 265, crosses a recursive Action call and Repeat loop, and checks the expected Linux output `42`, `192`, and `43`. The same fixture is cross-assembled for x86-64 Linux, x86-64 macOS, and ARM64 macOS. Separate tests exercise acceptance at 64, 65, and 266 slots, rejection at 267 with empty output, Decimal-valued globals at the same boundary using one reused literal, and zero-global output on all three targets.

These tests establish the storage layout and its bounds, not full compiler generation. The full artifact is reproducible from native stage 0/1 with a restricted toolchain, but code generation still exits with status 1 and no assembly after the global-slot gate is cleared. The next observed gate is `ParseAtom`'s eight `BC_RETURN` paths; current codegen supports only the audited return-count shapes 0, 1, 2, and 4. Return lowering is intentionally not bundled with this storage change. Text equality, dynamic Text concatenation, `BC_APPEND`, and strict toolchain independence remain separate limitations.

## Verification record

Local focused results, the fresh four-image rebuild, restricted-path bytecode reproduction, independent review, and exact-head CI status are recorded with the candidate PR. Cross-assembly is not genuine Darwin execution; runtime claims are limited to native Linux execution unless macOS CI provides a real run.
