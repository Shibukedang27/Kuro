#!/bin/sh
# Audit the remaining native image rebuild gap without Python or a toolchain.
# This is a bounded diagnostic, not a production image builder: it proves that
# the stage-0 compiler emits a substantial artifact for the complete composed
# compiler source, that the stage-0 codegen accepts a small control, and that
# it rejects the full-source artifact with the observed normal failure shape.
# It writes only to a temporary directory.
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"
SEED_COMPILER=${KURO_NATIVE_SEED_COMPILER:-"$ROOT/dist/kuro-compiler"}
SEED_CODEGEN=${KURO_NATIVE_SEED_CODEGEN:-"$ROOT/dist/kuro-codegen"}

# Current-source guardrails, intentionally below the observed 9,119 / 73 / 294
# values. Review these bounds deliberately when compiler source changes.
MIN_FULL_BYTECODE_LINES=9000
MIN_FUNCTION_MARKERS=70
MIN_CALL_MARKERS=290

[ -x "$SEED_COMPILER" ] || {
    echo "native bootstrap audit: executable stage-0 compiler required: $SEED_COMPILER" >&2
    exit 2
}
[ -x "$SEED_CODEGEN" ] || {
    echo "native bootstrap audit: executable stage-0 codegen required: $SEED_CODEGEN" >&2
    exit 2
}

# Retain only the shell utilities used by this audit and its source composer.
# The native images are explicit paths, so no compiler/interpreter/toolchain is
# discoverable while any candidate input is compiled or generated.
TOOL_PATH=$(mktemp -d "${TMPDIR:-/tmp}/kuro-bootstrap-audit-path.XXXXXX")
BUILD=
cleanup() {
    if [ -n "$BUILD" ]; then rm -rf "$BUILD"; fi
    rm -rf "$TOOL_PATH"
}
trap cleanup EXIT
trap 'exit 129' HUP
trap 'exit 130' INT
trap 'exit 143' TERM
for tool in dirname mktemp rm ln awk cat cmp grep head tr wc; do
    resolved=$(command -v "$tool") || {
        echo "native bootstrap audit: required shell utility missing: $tool" >&2
        exit 2
    }
    ln -s "$resolved" "$TOOL_PATH/$tool"
done
PATH=$TOOL_PATH
export PATH
for forbidden in python python3 clang gcc cc as ld ld.lld lld; do
    if command -v "$forbidden" >/dev/null 2>&1; then
        echo "native bootstrap audit: forbidden tool visible on restricted PATH: $forbidden" >&2
        exit 2
    fi
done

BUILD=$(mktemp -d "${TMPDIR:-/tmp}/kuro-bootstrap-audit.XXXXXX")
SOURCE=$BUILD/compiler.source.kuro
FULL_BYTECODE=$BUILD/compiler.kurobc
FULL_ASSEMBLY=$BUILD/compiler.s
FULL_CODEGEN_STDERR=$BUILD/compiler-codegen.stderr
CONTROL_SOURCE=$BUILD/control.kuro
CONTROL_BYTECODE=$BUILD/control.kurobc
CONTROL_ASSEMBLY=$BUILD/control.s

if ! "$ROOT/bootstrap/compose-native-compiler-source.sh" > "$SOURCE"; then
    echo "native bootstrap audit: shell compiler-source composition failed" >&2
    exit 1
fi
if ! "$SEED_COMPILER" < "$SOURCE" > "$FULL_BYTECODE"; then
    echo "native bootstrap audit: stage-0 compiler rejected the composed full compiler source" >&2
    exit 1
fi
IFS= read -r marker < "$FULL_BYTECODE" || {
    echo "native bootstrap audit: stage-0 compiler emitted no artifact" >&2
    exit 1
}
[ "$marker" = "kuro.bytecode/1" ] || {
    echo "native bootstrap audit: stage-0 compiler emitted an invalid artifact marker" >&2
    exit 1
}
line_count=$(wc -l < "$FULL_BYTECODE" | tr -d '[:space:]')
function_markers=$(grep -c -x 'BC_FUNC_BEGIN' "$FULL_BYTECODE" || true)
call_markers=$(grep -c -x 'BC_CALL_BEGIN' "$FULL_BYTECODE" || true)
indexed_markers=$(grep -Ec -x 'BC_MULTI_BEGIN|BC_STORE_MULTI' "$FULL_BYTECODE" || true)
if [ "$line_count" -lt "$MIN_FULL_BYTECODE_LINES" ] || \
   [ "$function_markers" -lt "$MIN_FUNCTION_MARKERS" ] || \
   [ "$call_markers" -lt "$MIN_CALL_MARKERS" ]; then
    echo "native bootstrap audit: compiler artifact is below the documented full-source guardrails (lines=$line_count functions=$function_markers calls=$call_markers)" >&2
    exit 1
fi

printf 'Print 2 + 3.\n' > "$CONTROL_SOURCE"
if ! "$SEED_COMPILER" < "$CONTROL_SOURCE" > "$CONTROL_BYTECODE"; then
    echo "native bootstrap audit: stage-0 compiler failed the arithmetic control" >&2
    exit 1
fi
if ! "$SEED_CODEGEN" < "$CONTROL_BYTECODE" > "$CONTROL_ASSEMBLY"; then
    echo "native bootstrap audit: stage-0 codegen rejected the arithmetic control" >&2
    exit 1
fi
if ! grep -Eq '\.globl[[:space:]]+(_main|_start)' "$CONTROL_ASSEMBLY"; then
    echo "native bootstrap audit: arithmetic control produced no native entry point" >&2
    exit 1
fi

# This failure is the result under audit. Accept only the observed normal reject
# (status 1, no stdout/stderr, hence no partial assembly). A crash, changed error
# path, or successful codegen needs a real temporary image-build proof instead.
if "$SEED_CODEGEN" < "$FULL_BYTECODE" > "$FULL_ASSEMBLY" 2> "$FULL_CODEGEN_STDERR"; then
    echo "native bootstrap audit: full compiler codegen now exits successfully; replace this blocker audit with a native-image reproduction gate" >&2
    exit 1
else
    full_codegen_status=$?
fi
if [ "$full_codegen_status" -ne 1 ]; then
    echo "native bootstrap audit: expected normal codegen rejection status 1, got $full_codegen_status" >&2
    exit 1
fi
assembly_bytes=$(wc -c < "$FULL_ASSEMBLY" | tr -d '[:space:]')
stderr_bytes=$(wc -c < "$FULL_CODEGEN_STDERR" | tr -d '[:space:]')
if [ "$assembly_bytes" -ne 0 ] || [ "$stderr_bytes" -ne 0 ]; then
    echo "native bootstrap audit: expected empty output on normal rejection (stdout=$assembly_bytes bytes stderr=$stderr_bytes bytes); refusing partial or diagnostic output" >&2
    exit 1
fi

printf 'Python/toolchain visibility: blocked during audit\n'
printf 'Shell composition and stage-0 compiler: passed\n'
printf 'Arithmetic stage-0 codegen control: passed\n'
printf 'Full-source compiler artifact: %s lines; BC_FUNC_BEGIN markers=%s; BC_CALL_BEGIN markers=%s; indexed-collection markers=%s (minimum guards: %s/%s/%s)\n' \
    "$line_count" "$function_markers" "$call_markers" "$indexed_markers" \
    "$MIN_FULL_BYTECODE_LINES" "$MIN_FUNCTION_MARKERS" "$MIN_CALL_MARKERS"
printf 'Full compiler stage-0 codegen: normal rejection (status %s, stdout/stderr empty; no partial assembly)\n' \
    "$full_codegen_status"
printf 'Result: Python-free native image reconstruction remains blocked at general compiler-codegen capability; no dist files changed.\n'
