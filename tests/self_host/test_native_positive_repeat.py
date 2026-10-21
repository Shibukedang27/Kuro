"""Positive and negative witnesses for top-level multitrip Decimal initialization."""
import json

import pytest

from compiler.pipeline import run_source
from loop_flow_facts import analyze
from test_native_codegen import compile_program_to_codegen, run_codegen
from test_native_decimal_control_flow import _cross_assemble
from test_native_loop_init import _run_hosted_linux_native, requires_hosted_linux_x86_64
from test_vm_cross import run_kuro_vm


TARGETS = ("x86_64-linux", "x86_64-macos", "aarch64-macos")


def _repeat(count, body):
    """Raw bytecode for a Repeat whose count tokens immediately precede its header."""
    return [*count, "BC_REPEAT_BEGIN", *body, "BC_REPEAT_END"]


def _fresh_decimal(name="Fresh", value="1.5"):
    return ["BC_CONST", value, "BC_STORE_LIST", name]


def _read_print(name):
    return ["BC_LOADVAR", name, "BC_PRINT"]


def positive_repeat_cases():
    """Return accepted raw bytecode witnesses and their expected printed output."""
    cases = {
        f"count-{count}": (
            _repeat(("BC_CONST", str(count)), [*_fresh_decimal(f"Fresh{count}"),
                                                *_read_print(f"Fresh{count}")])
            + _read_print(f"Fresh{count}"),
            "1.5\n" * (count + 1),
        )
        for count in range(2, 10)
    }
    # Preserve the legacy exact-once shape alongside the newly permitted counts.
    cases["count-one-unchanged"] = (
        _repeat(("BC_CONST", "1"), [*_fresh_decimal("Once")]) + _read_print("Once"),
        "1.5\n",
    )
    cases.update({
        "legacy-loop-first-decimal": (
            ["BC_CONST", "2", "BC_REPEAT_BEGIN", "BC_CONST", "1.5", "BC_STORE_LIST", "Slot",
             "BC_REPEAT_END"], "",
        ),
        "legacy-repeat-two-direct": (
            ["BC_CONST", "2", "BC_REPEAT_BEGIN", "BC_CONST", "1.5", "BC_STORE_LIST", "D",
             "BC_REPEAT_END"], "",
        ),
        "multiple-fresh-slots-with-dependency": (
            _repeat(("BC_CONST", "3"), [
                *_fresh_decimal("Base"), "BC_LOADVAR", "Base", "BC_CONST", "0.5",
                "BC_BINOP", "+", "BC_STORE_LIST", "Dependent",
            ]) + _read_print("Base") + _read_print("Dependent"),
            "1.5\n2.0\n",
        ),
        "reset-and-reassign": (
            _repeat(("BC_CONST", "2"), [
                *_fresh_decimal("Reset", "2.0"), "BC_LOADVAR", "Reset", "BC_CONST", "0.5",
                "BC_BINOP", "+", "BC_STORE_LIST", "Reset",
            ]) + _read_print("Reset"),
            "2.5\n",
        ),
        "negative-zero": (
            _repeat(("BC_CONST", "2"), [
                "BC_CONST", "0.0", "BC_CONST", "1.0", "BC_BINOP", "-", "BC_CONST", "0.0",
                "BC_BINOP", "*", "BC_STORE_LIST", "NegativeZero",
            ]) + _read_print("NegativeZero"),
            "-0.0\n",
        ),
        "postloop-read": (
            _repeat(("BC_CONST", "4"), _fresh_decimal("PostLoop", "7.25"))
            + _read_print("PostLoop"),
            "7.25\n",
        ),
        "established-decimal-modification": (
            ["BC_CONST", "1.0", "BC_STORE_LIST", "Established"]
            + _repeat(("BC_CONST", "3"), [
                "BC_LOADVAR", "Established", "BC_CONST", "0.5", "BC_BINOP", "+",
                "BC_STORE_LIST", "Established",
            ]) + _read_print("Established"),
            "2.5\n",
        ),
        "sibling-repeat-reset": (
            _repeat(("BC_CONST", "2"), _fresh_decimal("FirstSibling", "3.0"))
            + _repeat(("BC_CONST", "2"), _fresh_decimal("SecondSibling", "4.0"))
            + _read_print("FirstSibling") + _read_print("SecondSibling"),
            "3.0\n4.0\n",
        ),
    })
    cases["outside-store-after-unrelated-loop"] = (
        _repeat(("BC_CONST", "2"), _fresh_decimal("First"))
        + ["BC_CONST", "0", "BC_REPEAT_BEGIN", "BC_REPEAT_END"]
        + _fresh_decimal("Outside") + _read_print("Outside"), "1.5\n",
    )
    return cases


def positive_repeat_rejection_cases():
    """Return raw bytecode witnesses outside the narrow Repeat initialization rule."""
    c2 = ("BC_CONST", "2")
    cases = {
        "read-before-loop": _read_print("Fresh") + _repeat(c2, _fresh_decimal()),
        "read-before-in-loop-initialization": _repeat(c2, [
            *_read_print("Fresh"), *_fresh_decimal(),
        ]),
        "read-before-branch-initialization": _repeat(c2, [
            *_read_print("Fresh"), "BC_CONST", "1", "BC_IF_BEGIN",
            *_fresh_decimal(), "BC_IF_END",
        ]),
        "read-inside-branch-before-initialization": _repeat(c2, [
            "BC_CONST", "1", "BC_IF_BEGIN", *_read_print("Fresh"), *_fresh_decimal(),
            "BC_IF_END",
        ]),
        "nested-loop-read-before-outer-initialization": _repeat(c2, [
            *_repeat(("BC_CONST", "2"), _read_print("Fresh")), *_fresh_decimal(),
        ]),
        "backedge-integer-decimal-conflict": (
            ["BC_CONST", "1", "BC_STORE_LIST", "Conflict"]
            + _repeat(c2, [*_read_print("Conflict"), *_fresh_decimal("Conflict")])
            + _read_print("Conflict")
        ),
        "mutation-before-initialization": _repeat(c2, [
            "BC_CONST", "1", "BC_STORE_LIST", "Fresh", *_fresh_decimal("Fresh"),
        ]),
        "text-to-decimal-kind-conflict": [
            "BC_CONST_TEXT", "old", "BC_STORE_LIST", "Fresh",
            *_repeat(c2, _fresh_decimal("Fresh")),
        ],
        "mixed-store-after-init-integer": _repeat(c2, [
            *_fresh_decimal(), "BC_CONST", "1", "BC_STORE_LIST", "Fresh",
        ]),
        "mixed-store-after-init-text": _repeat(c2, [
            *_fresh_decimal(), "BC_CONST_TEXT", "x", "BC_STORE_LIST", "Fresh",
        ]),
        "mixed-store-after-init-nested": _repeat(c2, [
            *_fresh_decimal(), *_repeat(("BC_CONST", "2"), [
                "BC_CONST", "1", "BC_STORE_LIST", "Fresh",
            ]),
        ]),
        "count-zero": _repeat(("BC_CONST", "0"), _fresh_decimal()),
        "count-negative": _repeat(("BC_CONST", "-2"), _fresh_decimal()),
        "count-dynamic": ["BC_CONST", "2", "BC_STORE_LIST", "N", "BC_LOADVAR", "N",
                          "BC_REPEAT_BEGIN", *_fresh_decimal(), "BC_REPEAT_END"],
        "count-computed": ["BC_CONST", "1", "BC_CONST", "1", "BC_BINOP", "+",
                           "BC_REPEAT_BEGIN", *_fresh_decimal(), "BC_REPEAT_END"],
        "count-decimal": _repeat(("BC_CONST", "2.0"), _fresh_decimal()),
        "count-text": _repeat(("BC_CONST_TEXT", "2"), _fresh_decimal()),
        "count-large": _repeat(("BC_CONST", "10"), _fresh_decimal()),
        "count-noncanonical-leading-zero": _repeat(("BC_CONST", "02"), _fresh_decimal()),
        "count-noncanonical-plus-sign": _repeat(("BC_CONST", "+2"), _fresh_decimal()),
        "branch-initialization": _repeat(c2, [
            "BC_CONST", "1", "BC_IF_BEGIN", *_fresh_decimal(), "BC_IF_END",
        ]),
        "nested-repeat-initialization": _repeat(c2, [
            *_repeat(("BC_CONST", "2"), _fresh_decimal()),
        ]),
        "nested-while-initialization": _repeat(c2, [
            "BC_WHILE_BEGIN", "BC_CONST", "0", "BC_WHILE_TEST", *_fresh_decimal(),
            "BC_WHILE_END",
        ]),
        "repeat-under-branch-initialization": [
            "BC_CONST", "1", "BC_IF_BEGIN", *_repeat(c2, _fresh_decimal()), "BC_IF_END",
        ],
        "underscore-target": _repeat(c2, [*_fresh_decimal("_")]),
        "action-present": [
            "BC_FUNC_BEGIN", "Action", "BC_CONST", "1", "BC_RETURN", "BC_FUNC_END",
            *_repeat(c2, _fresh_decimal()),
        ],
        "crossed-repeat-if-delimiters": [
            "BC_CONST", "2", "BC_REPEAT_BEGIN", "BC_CONST", "1", "BC_IF_BEGIN",
            "BC_REPEAT_END", "BC_IF_END",
        ],
        "residual-stack": _repeat(c2, ["BC_CONST", "9", *_fresh_decimal()]),
        "stale-literal-provenance": [
            "BC_CONST", "0", "BC_CONST", "2", "BC_PRINT", "BC_REPEAT_BEGIN",
            *_fresh_decimal(), "BC_REPEAT_END",
        ],
        "stale-permission-across-sibling": (
            _repeat(("BC_CONST", "2"), [])
            + _repeat(("BC_CONST", "0"), _fresh_decimal("Stale"))
        ),
        "branch-read-before-direct-store-no-snapshot-reset": _repeat(c2, [
            "BC_CONST", "1", "BC_IF_BEGIN", *_read_print("Fresh"),
            "BC_ELSE_BEGIN", "BC_CONST", "0", "BC_PRINT", "BC_IF_END",
            *_fresh_decimal(), *_read_print("Fresh"),
        ]),
        "add-before-direct-store": _repeat(c2, [
            "BC_CONST", "1", "BC_ADD", "Fresh", *_fresh_decimal(),
        ]),
        "update-before-direct-store": _repeat(c2, [
            "BC_CONST", "1", "BC_UPDATE", "Fresh", *_fresh_decimal(),
        ]),
        "fresh-decimal-add-not-a-store": _repeat(c2, ["BC_CONST", "1.5", "BC_ADD", "Fresh"]),
        "fresh-decimal-update-not-a-store": _repeat(c2, ["BC_CONST", "1.5", "BC_UPDATE", "Fresh"]),
        "backedge-earlier-slot-read": _repeat(c2, [
            "BC_LOADVAR", "Later", "BC_CONST", "0.5", "BC_BINOP", "+",
            "BC_STORE_LIST", "Earlier", *_fresh_decimal("Later"),
        ]),
    }
    for count in ("2", "9"):
        for name, abrupt in (
            ("return", ["BC_CONST", "0", "BC_RETURN"]),
            ("break", ["BC_BREAK"]),
            ("continue", ["BC_CONTINUE"]),
        ):
            cases[f"count-{count}-{name}-after-initialization"] = _repeat(
                ("BC_CONST", count), [*_fresh_decimal(), *abrupt],
            )
    return cases


# Exported for fresh-compiled gate integration: this source exercises all supported
# counts plus dependencies, repeated assignment, negative zero, and sibling frames.
POSITIVE_REPEAT_SOURCE = (
    "Repeat 2; Two = 2.0; Done.\n"
    "Repeat 3; Three = 3.0; Done.\n"
    "Repeat 4; Four = 4.0; Done.\n"
    "Repeat 5; Five = 5.0; Done.\n"
    "Repeat 6; Six = 6.0; Done.\n"
    "Repeat 7; Seven = 7.0; Done.\n"
    "Repeat 8; Eight = 8.0; Done.\n"
    "Repeat 9; Nine = 9.0; Done.\n"
    "Repeat 3; Base = 0.5; Dependent = Base + 1.0; Base = Base + 0.25; Done.\n"
    "Repeat 2; Reset = 1.0; Reset = Reset + 1.0; Done.\n"
    "Repeat 2; NegativeZero = (0.0 - 1.0) * 0.0; Done.\n"
    "Established = 1.0; Repeat 3; Add 0.5 to Established; Done.\n"
    "Repeat 2; FirstSibling = 3.0; Done.\n"
    "Repeat 2; SecondSibling = 4.0; Done.\n"
    "Print Two.\nPrint Three.\nPrint Four.\nPrint Five.\nPrint Six.\n"
    "Print Seven.\nPrint Eight.\nPrint Nine.\nPrint Base.\nPrint Dependent.\n"
    "Print Reset.\nPrint NegativeZero.\nPrint Established.\n"
    "Print FirstSibling.\nPrint SecondSibling.\n"
)
POSITIVE_REPEAT_OUTPUT = (
    "2.0\n3.0\n4.0\n5.0\n6.0\n7.0\n8.0\n9.0\n"
    "0.75\n1.5\n2.0\n-0.0\n2.5\n3.0\n4.0\n"
)


def _raw(tokens, target):
    return run_codegen(", ".join(json.dumps(token) for token in tokens), target=target)


def test_native_positive_repeat_raw_acceptance_and_rejection_grouped_by_target():
    """Check the full raw-token matrix once per target, with named diagnostics."""
    for target in TARGETS:
        for name, (tokens, _expected_stdout) in positive_repeat_cases().items():
            env = _raw(tokens, target)
            assert env["NativeFailed"] == 0, f"{name} unexpectedly rejected for {target}"
            assert env["NativeOut"], f"{name} emitted no assembly for {target}"
        for name, tokens in positive_repeat_rejection_cases().items():
            env = _raw(tokens, target)
            assert env["NativeFailed"] == 1, f"{name} unexpectedly accepted for {target}"
            assert env["NativeOut"] == "", f"{name} emitted assembly for {target}"


def test_loop_flow_oracle_records_positive_repeat_entry_backedge_and_exit_facts():
    tokens, _ = positive_repeat_cases()["count-2"]
    result = analyze(tokens)
    loop = result["loops"][0]
    assert loop["count"] == "positive"
    assert loop["entry_facts"]["slots"]["Fresh2"] == {"?"}
    assert loop["backedge_facts"]["slots"]["Fresh2"] == {"D"}
    assert loop["exit_facts"]["Fresh2"] == {"D"}
    assert [load["kinds"] for load in result["loads"]] == [{"D"}, {"D"}]


def test_positive_repeat_source_matches_interpreter_and_vm():
    hosted = run_source(POSITIVE_REPEAT_SOURCE)
    assert hosted.ok, hosted.compile.diags.render_all() if not hosted.compile.ok else hosted.runtime_error
    assert hosted.stdout == POSITIVE_REPEAT_OUTPUT
    vm_output, failed = run_kuro_vm(POSITIVE_REPEAT_SOURCE)
    assert failed in (None, 0)
    assert "".join(f"{value}\n" for value in vm_output) == POSITIVE_REPEAT_OUTPUT


@requires_hosted_linux_x86_64
def test_positive_repeat_source_executes_as_hosted_linux_native(tmp_path):
    result = _run_hosted_linux_native(tmp_path, POSITIVE_REPEAT_SOURCE, "positive-repeat")
    assert result.stdout == POSITIVE_REPEAT_OUTPUT
    assert result.stderr == ""


@pytest.mark.parametrize(
    ("target", "triple"),
    [
        ("x86_64-linux", "x86_64-unknown-linux-gnu"),
        ("x86_64-macos", "x86_64-apple-macos"),
        ("aarch64-macos", "arm64-apple-macos11"),
    ],
)
def test_positive_repeat_source_cross_assembles_all_native_targets(tmp_path, target, triple):
    _, env = compile_program_to_codegen(POSITIVE_REPEAT_SOURCE, target=target)
    assert env["NativeFailed"] == 0
    _cross_assemble(tmp_path, env["NativeOut"], target, triple)
