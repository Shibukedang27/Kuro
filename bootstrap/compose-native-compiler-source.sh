#!/bin/sh
# Compose the self-hosted compiler source without invoking Python.
#
# This is a bootstrap source-preparation step only: it does not compile or link
# a native image. Keep its output byte-for-byte aligned with
# compiler.self_host.native_compiler_source().
set -eu

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)

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
        -v strip_debug_prints="$strip_debug_prints" \
        -v action="${6-}" -v failed="${7-}" -v condition="${8-}" '
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
            if (action != "" && $0 == "Call " action ";") {
                gate_count++
                print "If " condition ";"
                print "    Call " action ";"
                print "Else;"
                print "    " failed " = 1;"
                print "Done."
                next
            }
            print
        }
        END {
            if (skipping) exit 42
            if (begin_marker != "" && (begin_count != 1 || end_count != 1)) exit 43
            if (replace_source == "yes" && replacement_count != 1) exit 44
            if (action != "" && gate_count != 1) exit 45
        }
        ' "$file"
}

{
    filter_file "$ROOT/self_host/lexer.kuro" "" "" yes yes
    printf '\n'
    filter_file "$ROOT/self_host/parser.kuro" \
        "BEGIN_STANDALONE_TOKENS" "END_STANDALONE_TOKENS" no no
    printf '\n'
    cat "$ROOT/self_host/lengthcheck.kuro"
    printf '\n'
    filter_file "$ROOT/self_host/lower.kuro" \
        "BEGIN_STANDALONE_AST" "END_STANDALONE_AST" no no \
        LowerBlock LowerFailed \
            'ParseFailed is equal to 0 and LengthCheckFailed is equal to 0'
    printf '\n'
    filter_file "$ROOT/self_host/bytecode.kuro" \
        "BEGIN_STANDALONE_IR" "END_STANDALONE_IR" no no \
        BytecodeStep BytecodeFailed \
            'ParseFailed is equal to 0 and LengthCheckFailed is equal to 0 and LowerFailed is equal to 0'
    printf '\n'
    cat "$ROOT/self_host/compiler.kuro"
    printf '\n'
    cat "$ROOT/self_host/native_compiler_entry.kuro"
}
