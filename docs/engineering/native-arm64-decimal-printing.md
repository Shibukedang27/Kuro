# Freestanding ARM64 Decimal printing

The Kuro-authored native generator now lowers computed Decimal `BC_PRINT` for Apple ARM64, including printing inside an Action and printing a returned Decimal. Generated programs use a repository-owned formatter and Darwin write syscalls, not `printf`, libc allocation, or a Python formatter.

## What changed and why

The print instruction passes the binary64 bits in `x0` to one shared `_kuro_print_float` helper. An 80-byte, 16-byte-aligned wrapper saves its return address, supplies a bounded output buffer, calls `_kuro_decimal_format`, writes the returned bytes directly, and restores the stack. Integer and Text paths are unchanged.

There was no existing freestanding ARM64 formatter to copy: the hosted ARM64 backend calls libc `%g`, which defaults to six significant digits. Reusing it would both introduce a forbidden dependency and lose information. The new formatter instead follows the Python/Kuro display contract used by the Decimal regression cases: shortest round-tripping binary64 digits, fixed notation for decimal exponents -4 through 15, `.0` for fixed-form integral Decimals, signed zero, scientific exponents with a sign and at least two digits, and `inf`, `-inf`, `nan`.

`self_host/decimal_formatter.c` is the readable implementation of a Dragon4-style exact rounding-interval algorithm. Five fixed 40-limb base-2^32 integers cover the full binary64 range, including asymmetric rounding intervals at powers of two and subnormal boundaries. Digit generation uses small multiplication, comparison, and subtraction; it needs no floating-point environment, heap, table generation, or big-integer division library. The 1280-bit capacity exceeds the largest intermediate (under 1152 bits), and the wrapper's 64-byte output area exceeds the maximum 25-byte line.

`scripts/freeze_decimal_formatter.py` is a development-only Clang 18 regeneration tool. The ARM64 instructions are checked into bounded Kuro Text chunks with the C source digest. Building or executing the Kuro generator does not read the C file, invoke a C compiler, or run this script. Regeneration is explicit, not a new bootstrap build step. The frozen helper has no undefined imports; a macOS regression also checks that the linked Decimal program has none.

The Darwin executable test uses the repository's existing `-nostdlib -lSystem` link convention: macOS loader metadata may still name the platform library, but Decimal formatting imports and calls no libc functions. This is not a claim to replace Darwin's executable loader or platform runtime.

## Verification

Local Linux x86-64 results (Python 3.12):

- Native codegen plus VM conformance: **181 passed, 18 skipped in 2602.80 seconds (43m22s)**. This comprises **159 native-codegen passes** and **22 VM passes**. The fresh compiled Linux Kuro-generator fixture took **2558.83 seconds**; it exercises existing x86 Decimal output as a regression, while source-level tests cross-assemble the new Apple ARM64 output.
- Formatter regressions: **4 passed in 2.67 seconds**. The checked-in differential corpus has **10,086 bit patterns**: 8,038 boundary/special patterns (all normal powers of two and neighbors, decimal powers and formatting cutoffs) plus 2,048 seeded random patterns. Exact output, returned lengths, and bitwise finite/infinity round-trips match Python. A separate development probe matched 100,000 random patterns; this is additional evidence, not a replacement for the checked-in corpus.
- ARM64 emulation executes the **frozen instructions** on all 8,038 boundary/special patterns, then executes a complete Kuro-emitted program covering Action parameter/return printing, computed fractions, `0.1 + 0.2`, scientific notation, negative values, signed zero, infinities, and NaN. Both linked ELF images have no undefined symbols. Only section/relocation syntax, entry spelling, and Darwin-to-Linux syscall wrappers are adapted; formatter instructions are unchanged.
- Portable language/toolchain baseline: **554 passed in 29.06 seconds**, excluding the separately run formatter and native-codegen modules.
- Linux backend/CLI subset: **12 passed, 69 deselected in 0.38 seconds**.
- `python3 scripts/freeze_decimal_formatter.py --check` and `git diff --check`: passed. Independent static review found no arithmetic, ABI, or dependency blocker.

The macOS compiled-generator regression feeds the same Decimal bytecode to a freshly built Kuro generator, links its emitted Darwin assembly with `-nostdlib`, checks exact stdout and empty stderr, and checks zero undefined imports. Actual Darwin execution is required from the final-head GitHub macOS checks, not inferred from local cross-assembly or emulation. GitHub verification is recorded on the stacked PR and must cover all eight checks on the documentation-updated head.

## Limits and next path

This changes the self-hosted native generator, not the hosted ARM64 `%g` implementation. The latter remains a known display-oracle discrepancy; this slice does not silently redefine it or claim all backends now agree. The x86 formatter is unchanged and retains its previously documented high-precision fallback limits. Literal-only direct output can still preserve source spelling instead of using runtime formatting. The random and boundary differential corpus is strong regression evidence, not an exhaustive proof over all binary64 values.

The C source and frozen assembly are repository-owned runtime implementation code, but regeneration still needs a host C compiler. Native generator construction still uses the Python-hosted bootstrap, and emitted programs still require a host assembler/linker. No clean-checkout C-free/Python-free/toolchain-free bootstrap claim is made. Generator build performance remains an engineering cost.

Next broaden hosted-versus-self-hosted Decimal conformance, especially the hosted ARM64 `%g` discrepancy and x86 fallback, then add non-parameter Decimal storage/mutation and broader compiler/runtime lowering. Python-free production-image rebuilding and a repository-owned image-construction path remain unfinished. This PR is a bounded parity improvement, not completion of Kuro independence.
