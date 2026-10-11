#!/bin/sh
# Compose native production sources using POSIX shell and awk only.
# The output for each mode must stay byte-for-byte aligned with compiler.self_host.
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
MODE=${1:-}
TARGET=${2:-aarch64-macos}

filter_file() {
    file=$1
    begin_marker=$2
    end_marker=$3
    replace_source=$4
    strip_debug_prints=$5

    awk \
        -v begin_marker="$begin_marker" \
        -v end_marker="$end_marker" \
        -v replace_source="$replace_source" \
        -v strip_debug_prints="$strip_debug_prints" '
        BEGIN {
            skipping = 0
            begin_count = 0
            end_count = 0
            replacement_count = 0
        }
        {
            if (begin_marker != "" && index($0, begin_marker) > 0) {
                if (skipping) exit 41
                skipping = 1
                begin_count++
                next
            }
            if (skipping) {
                if (end_marker != "" && index($0, end_marker) > 0) {
                    skipping = 0
                    end_count++
                }
                next
            }
            if (replace_source == "yes" && $0 ~ /^Source = ".*";$/) {
                print "Source is Text;"
                print "Take user Source;"
                replacement_count++
                next
            }
            if (strip_debug_prints == "yes" && $0 ~ /^[[:space:]]*Print .*/) next
            print
        }
        END {
            if (skipping) exit 42
            if (begin_marker != "" && (begin_count != 1 || end_count != 1)) exit 43
            if (replace_source == "yes" && replacement_count != 1) exit 44
        }
        ' "$file"
}

case "$MODE" in
    compiler)
        exec "$ROOT/bootstrap/compose-native-compiler-source.sh"
        ;;
    runtime)
        {
            filter_file "$ROOT/self_host/lexer.kuro" "" "" yes yes
            printf '\n'
            filter_file "$ROOT/self_host/parser.kuro" \
                "BEGIN_STANDALONE_TOKENS" "END_STANDALONE_TOKENS" no no
            printf '\n'
            filter_file "$ROOT/self_host/lower.kuro" \
                "BEGIN_STANDALONE_AST" "END_STANDALONE_AST" no no
            printf '\n'
            filter_file "$ROOT/self_host/bytecode.kuro" \
                "BEGIN_STANDALONE_IR" "END_STANDALONE_IR" no no
            printf '\n'
            filter_file "$ROOT/self_host/vm.kuro" \
                "BEGIN_STANDALONE_BYTECODE" "END_STANDALONE_BYTECODE" no no
            printf '\n'
            cat "$ROOT/self_host/runtime.kuro"
        }
        ;;
    artifact-launcher)
        {
            cat "$ROOT/self_host/artifact_loader.kuro"
            printf '\n'
            filter_file "$ROOT/self_host/vm.kuro" \
                "BEGIN_STANDALONE_BYTECODE" "END_STANDALONE_BYTECODE" no no |
                filter_file /dev/stdin "BEGIN_VM_INPUT_DEFAULT" "END_VM_INPUT_DEFAULT" no no
            printf '\n'
            cat "$ROOT/self_host/runtime.kuro"
        }
        ;;
    codegen)
        case "$TARGET" in
            aarch64-macos|x86_64-macos|x86_64-linux) ;;
            *) echo "unsupported codegen output target: $TARGET" >&2; exit 2 ;;
        esac
        {
            cat "$ROOT/self_host/artifact_loader.kuro"
            printf '\n'
            awk -v target="$TARGET" '
                $0 == "NativeTarget = \"aarch64-macos\";" {
                    print "NativeTarget = \"" target "\";"
                    replacements++
                    next
                }
                { print }
                END { if (replacements != 1) exit 45 }
            ' "$ROOT/self_host/native_codegen.kuro"
        }
        ;;
    *)
        echo "usage: compose-native-source.sh <compiler|runtime|artifact-launcher|codegen> [codegen-target]" >&2
        exit 2
        ;;
esac
