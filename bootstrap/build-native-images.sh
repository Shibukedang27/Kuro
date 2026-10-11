#!/bin/sh
# Rebuild the native production images from Kuro sources using the checked-in
# native Kuro compiler/codegen seeds. Clang remains the current assembler/linker.
set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
ROOT=$(CDPATH= cd -- "$SCRIPT_DIR/.." && pwd)
TARGET=${NATIVE_TARGET:-aarch64-macos}
CLANG=${CLANG:-clang}
SEED_COMPILER=${KURO_NATIVE_SEED_COMPILER:-"$ROOT/dist/kuro-compiler"}
SEED_CODEGEN=${KURO_NATIVE_SEED_CODEGEN:-"$ROOT/dist/kuro-codegen"}

case "$TARGET" in
    aarch64-macos) ;;
    *)
        echo "Python-free seeded rebuild currently supports aarch64-macos only (requested: $TARGET). Use 'make native-hosted-bootstrap' for an unseeded/cross target." >&2
        exit 2
        ;;
esac
[ "$(uname -s)" = Darwin ] || {
    echo "the aarch64-macos seed can only run on macOS" >&2
    exit 2
}
[ "$(uname -m)" = arm64 ] || {
    echo "the checked-in seed currently requires a macOS ARM64 host" >&2
    exit 2
}
[ -x "$SEED_COMPILER" ] || { echo "native compiler seed missing or not executable: $SEED_COMPILER" >&2; exit 1; }
[ -x "$SEED_CODEGEN" ] || { echo "native codegen seed missing or not executable: $SEED_CODEGEN" >&2; exit 1; }
command -v "$CLANG" >/dev/null 2>&1 || { echo "assembler/linker driver not found: $CLANG" >&2; exit 1; }

BUILD=$(mktemp -d "$ROOT/dist/.native-build.XXXXXX")
cleanup() {
    rm -rf "$BUILD"
}
trap cleanup EXIT HUP INT TERM

build_one() {
    name=$1
    mode=$2
    source_target=$3
    source="$BUILD/$name.source.kuro"
    artifact="$BUILD/$name.kurobc"
    assembly="$BUILD/$name.s"
    image="$BUILD/$name"

    "$ROOT/bootstrap/compose-native-source.sh" "$mode" "$source_target" > "$source"
    "$SEED_COMPILER" < "$source" > "$artifact"
    IFS= read -r marker < "$artifact" || {
        echo "seed compiler produced no bytecode for $name" >&2
        exit 1
    }
    [ "$marker" = "kuro.bytecode/1" ] || {
        echo "seed compiler produced an invalid bytecode stream for $name" >&2
        exit 1
    }
    "$SEED_CODEGEN" < "$artifact" > "$assembly"
    grep -Fq '.globl _main' "$assembly" || {
        echo "seed codegen produced no native entry point for $name" >&2
        exit 1
    }
    "$CLANG" "$assembly" -o "$image"
    chmod 755 "$image"
    test -s "$image"
}

# Every image is built against the original seeds in the staging directory;
# none replaces a seed until all four new images have linked successfully.
build_one compiler compiler "$TARGET"
build_one runtime runtime "$TARGET"
build_one bytecode artifact-launcher "$TARGET"
build_one codegen codegen "$TARGET"

# Prove the new compiler reproduces its own complete input before promotion.
"$BUILD/kuro-compiler" < "$BUILD/kuro-compiler.source.kuro" > "$BUILD/kuro-compiler-self.kurobc"
cmp "$BUILD/kuro-compiler.kurobc" "$BUILD/kuro-compiler-self.kurobc"

for name in compiler runtime bytecode codegen; do
    mv "$BUILD/$name" "$ROOT/dist/kuro-$name"
    cp "$BUILD/$name.s" "$ROOT/dist/kuro-$name.s"
done
cp "$BUILD/kuro-compiler.source.kuro" "$ROOT/dist/kuro-compiler.source.kuro"

"$ROOT/bin/kuro-native" doctor
echo "Kuro native production images rebuilt from Kuro source without Python (target: $TARGET)"
