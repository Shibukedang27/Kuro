#!/bin/sh
# Exercise already-built native production images with Python and compiler
# toolchains removed from PATH. Image construction is a separate bootstrap step.
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
COMPILER_SOURCE=${KURO_NATIVE_COMPILER_SOURCE:-"$ROOT/dist/kuro-compiler.source.kuro"}
TOOL_PATH=$(mktemp -d "${TMPDIR:-/tmp}/kuro-no-python-path.XXXXXX")
PROBE=
ARTIFACT=
ASSEMBLY=
COMPOSED_SOURCE=
STAGE1_COMPILER=
STAGE0_PROBE_ARTIFACT=
STAGE1_PROBE_ARTIFACT=
BOOTSTRAP_ARTIFACT=
STAGE2_COMPILER=
STAGE2_INPUT=

cleanup() {
    if [ -n "$PROBE" ]; then
        rm -f "$PROBE" "$ARTIFACT" "$ASSEMBLY" "$COMPOSED_SOURCE" \
            "$STAGE1_COMPILER" "$STAGE0_PROBE_ARTIFACT" \
            "$STAGE1_PROBE_ARTIFACT" "$BOOTSTRAP_ARTIFACT" \
            "$STAGE2_COMPILER" "$STAGE2_INPUT"
    fi
    rm -rf "$TOOL_PATH"
}
trap cleanup EXIT HUP INT TERM

# Keep only shell utilities required by the wrapper and its doctor checks.
for tool in dirname mktemp rm grep head wc awk cat cmp; do
    resolved=$(command -v "$tool")
    ln -s "$resolved" "$TOOL_PATH/$tool"
done
PATH=$TOOL_PATH
export PATH

for forbidden in python python3 clang gcc as ld ld.lld; do
    if command -v "$forbidden" >/dev/null 2>&1; then
        echo "unexpected tool on restricted PATH: $forbidden" >&2
        exit 1
    fi
done

PROBE=$(mktemp "${TMPDIR:-/tmp}/kuro-no-python.XXXXXX.kuro")
ARTIFACT=$PROBE.kurobc
ASSEMBLY=$PROBE.s
COMPOSED_SOURCE=$PROBE.composed-source.kuro
STAGE1_COMPILER=$PROBE.stage1.kurobc
STAGE0_PROBE_ARTIFACT=$PROBE.stage0-probe.kurobc
STAGE1_PROBE_ARTIFACT=$PROBE.stage1-probe.kurobc
BOOTSTRAP_ARTIFACT=$PROBE.stage1-input.kurobc
STAGE2_COMPILER=$PROBE.stage2.kurobc
STAGE2_INPUT=$PROBE.stage1-self-rebuild-input.kurobc
"$ROOT/bootstrap/compose-native-compiler-source.sh" > "$COMPOSED_SOURCE"
cmp "$COMPOSED_SOURCE" "$COMPILER_SOURCE"
printf 'Print 2 + 3.\n' > "$PROBE"

run_output=$("$ROOT/bin/kuro-native" run "$PROBE")
[ "$run_output" = "5" ] || { echo "native runtime smoke failed: $run_output" >&2; exit 1; }
"$ROOT/bin/kuro-native" compile "$PROBE" > "$ARTIFACT"
exec_output=$("$ROOT/bin/kuro-native" exec "$ARTIFACT")
[ "$exec_output" = "5" ] || { echo "native bytecode smoke failed: $exec_output" >&2; exit 1; }
"$ROOT/bin/kuro-native" codegen "$ARTIFACT" > "$ASSEMBLY"
grep -Fq '.globl _main' "$ASSEMBLY" || { echo "native codegen smoke failed" >&2; exit 1; }
"$ROOT/bin/kuro-native" doctor

# Bootstrap the compiler as bytecode, then execute that stage-1 compiler to
# compile a small program. Its output must match the native stage-0 compiler.
"$ROOT/bin/kuro-native" compile "$COMPILER_SOURCE" > "$STAGE1_COMPILER"
"$ROOT/bin/kuro-native" compile "$PROBE" > "$STAGE0_PROBE_ARTIFACT"
{
    cat "$STAGE1_COMPILER"
    printf 'kuro.input/1\n'
    cat "$PROBE"
} > "$BOOTSTRAP_ARTIFACT"
"$ROOT/bin/kuro-native" exec "$BOOTSTRAP_ARTIFACT" > "$STAGE1_PROBE_ARTIFACT"
cmp "$STAGE0_PROBE_ARTIFACT" "$STAGE1_PROBE_ARTIFACT"
printf 'Python-free native runtime, compiler, bytecode launcher, and codegen verified\n'
printf 'Self-hosted stage-1 compiler matches native stage 0 on a probe\n'

# Recompile the complete compiler source with the bytecode stage-1 compiler.
# The native launcher, not the hosted compiler, must execute this build.
{
    cat "$STAGE1_COMPILER"
    printf 'kuro.input/1\n'
    cat "$COMPILER_SOURCE"
} > "$STAGE2_INPUT"
"$ROOT/bin/kuro-native" exec "$STAGE2_INPUT" > "$STAGE2_COMPILER"
cmp "$STAGE1_COMPILER" "$STAGE2_COMPILER"
printf 'Self-hosted stage-1 compiler reproduces its full compiler bytecode\n'
