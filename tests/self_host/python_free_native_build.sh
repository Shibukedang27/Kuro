#!/bin/sh
# Rebuild native images from Kuro source with Python removed from PATH, then
# exercise the promoted compiler/runtime/bytecode images.
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/../.." && pwd)
TOOL_PATH=$(mktemp -d "${TMPDIR:-/tmp}/kuro-native-build-path.XXXXXX")
PROBE=
ARTIFACT=

cleanup() {
    if [ -n "$PROBE" ]; then
        rm -f "$PROBE" "$ARTIFACT"
    fi
    rm -rf "$TOOL_PATH"
}
trap cleanup EXIT HUP INT TERM

# Retain only the shell utilities needed for a native-host rebuild and smoke
# check. In particular, neither python nor python3 can be discovered here.
for tool in dirname uname mktemp rm mv cp chmod cat awk grep head wc cmp ln make clang; do
    resolved=$(command -v "$tool")
    ln -s "$resolved" "$TOOL_PATH/$tool"
done
PATH=$TOOL_PATH
export PATH
for forbidden in python python3; do
    if command -v "$forbidden" >/dev/null 2>&1; then
        echo "unexpected tool on restricted PATH: $forbidden" >&2
        exit 1
    fi
done

make -C "$ROOT" native NATIVE_TARGET=aarch64-macos

PROBE=$(mktemp "${TMPDIR:-/tmp}/kuro-native-build.XXXXXX.kuro")
ARTIFACT=$PROBE.kurobc
printf 'Print 2 + 3.\n' > "$PROBE"
run_output=$("$ROOT/bin/kuro-native" run "$PROBE")
[ "$run_output" = "5" ] || { echo "rebuilt runtime smoke failed: $run_output" >&2; exit 1; }
"$ROOT/bin/kuro-native" compile "$PROBE" > "$ARTIFACT"
exec_output=$("$ROOT/bin/kuro-native" exec "$ARTIFACT")
[ "$exec_output" = "5" ] || { echo "rebuilt compiler/bytecode smoke failed: $exec_output" >&2; exit 1; }
echo "Python-free native image rebuild and runtime/compiler smoke tests passed"
