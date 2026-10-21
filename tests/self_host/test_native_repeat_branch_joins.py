"""All-path Decimal joins in If-only descendants of a top-level Repeat 1."""
import itertools
import json

import pytest

from compiler.pipeline import run_source
from test_native_branch_joins import (
    branch_join_rejection_cases, nested_branch_join_output, nested_branch_join_program,
)
from test_native_codegen import compile_program_to_codegen, nested_boundary_bytecode, run_codegen
from test_native_decimal_control_flow import _cross_assemble
from test_native_loop_init import _run_hosted_linux_native, requires_hosted_linux_x86_64
from test_vm_cross import run_kuro_vm


CHOICES = list(itertools.product((1, 2), repeat=3))


def repeat_branch_program(outer, middle, inner):
    return (
        "Repeat 1;\nNegativeZero = (0.0 - 1.0) * 0.0;\n"
        + nested_branch_join_program(outer, middle, inner)
        + "After = First + 0.25;\n"
        "If 1 is equal to 2; Add 0.5 to After; Done.\n"
        "Done.\nPrint First.\nPrint After.\nPrint NegativeZero.\n"
    )


def repeat_branch_output(outer, middle, inner):
    first = 1.75 + 4 * (outer - 1) + 2 * (middle - 1) + (inner - 1)
    return nested_branch_join_output(outer, middle, inner) + f"{first}\n{first + 0.25}\n-0.0\n"


def in_repeat(tokens, count="1"):
    return ["BC_CONST", count, "BC_REPEAT_BEGIN", *tokens, "BC_REPEAT_END"]


def complete_branch_tokens():
    return [
        "BC_CONST", "1", "BC_IF_BEGIN", "BC_CONST", "1.5", "BC_STORE_LIST", "Fresh",
        "BC_ELSE_BEGIN", "BC_CONST", "2.5", "BC_STORE_LIST", "Fresh", "BC_IF_END",
    ]


def repeat_branch_boundary_bytecode(depth=16, global_count=64):
    return in_repeat(nested_boundary_bytecode(depth=depth, global_count=global_count))


def repeat_branch_rejection_cases():
    # The existing unsafe branch shapes must remain unsafe under the new permission.
    cases = {f"repeat-{name}": in_repeat(tokens)
             for name, tokens in branch_join_rejection_cases().items()}
    body = complete_branch_tokens()
    cases.update({
        # Keep the formerly inherited nested-loop rejection after its top-level
        # direct-store counterpart moves to positive multitrip coverage.
        "repeat-loop-first-decimal": in_repeat([
            "BC_CONST", "2", "BC_REPEAT_BEGIN", "BC_CONST", "1.5", "BC_STORE_LIST", "Slot",
            "BC_REPEAT_END",
        ]),
        "zero-count-complete-branches": in_repeat(body, "0"),
        "two-count-complete-branches": in_repeat(body, "2"),
        "decimal-one-complete-branches": in_repeat(body, "1.0"),
        "computed-one-complete-branches": [
            "BC_CONST", "0", "BC_CONST", "1", "BC_BINOP", "+", "BC_REPEAT_BEGIN",
            *body, "BC_REPEAT_END",
        ],
        "variable-one-complete-branches": [
            "BC_CONST", "1", "BC_STORE_LIST", "N", "BC_LOADVAR", "N",
            "BC_REPEAT_BEGIN", *body, "BC_REPEAT_END",
        ],
        "repeat-under-if-complete-branches": [
            "BC_CONST", "1", "BC_IF_BEGIN", *in_repeat(body), "BC_IF_END",
        ],
        "inner-repeat-complete-branches": in_repeat(in_repeat(body)),
        "while-in-repeat-complete-branches": in_repeat([
            "BC_WHILE_BEGIN", "BC_CONST", "0", "BC_WHILE_TEST", *body, "BC_WHILE_END",
        ]),
        "repeat-in-while-complete-branches": [
            "BC_WHILE_BEGIN", "BC_CONST", "0", "BC_WHILE_TEST", *in_repeat(body),
            "BC_WHILE_END",
        ],
        "prior-read-before-branches": in_repeat(["BC_LOADVAR", "Fresh", "BC_PRINT", *body]),
        "stale-permission-after-repeat": [*in_repeat([]), *in_repeat(body, "0")],
        "stale-snapshot-in-sibling": [
            *in_repeat(body), *in_repeat([
                "BC_CONST", "0", "BC_IF_BEGIN", "BC_CONST", "1.5", "BC_STORE_LIST", "Other",
                "BC_IF_END",
            ]),
        ],
        "crossed-if-repeat-end": [
            "BC_CONST", "1", "BC_REPEAT_BEGIN", "BC_CONST", "1", "BC_IF_BEGIN",
            "BC_REPEAT_END", "BC_IF_END",
        ],
    })
    return cases


def repeat_branch_positive_cases():
    # These exact formerly rejected shapes now have positive regression coverage.
    body = complete_branch_tokens()
    return {
        "complete-branches": [*in_repeat(body), "BC_LOADVAR", "Fresh", "BC_PRINT"],
        "nested-complete-branches": in_repeat([
            "BC_CONST", "1", "BC_IF_BEGIN", *body, "BC_ELSE_BEGIN",
            "BC_CONST", "3.5", "BC_STORE_LIST", "Fresh", "BC_IF_END",
        ]),
        "permission-restored-after-inner-regions": [*in_repeat([
            *in_repeat([], "0"), "BC_WHILE_BEGIN", "BC_CONST", "0", "BC_WHILE_TEST",
            "BC_WHILE_END", *body,
        ]), "BC_LOADVAR", "Fresh", "BC_PRINT"],
        "sibling-frame-reset": [*in_repeat(body), *in_repeat([
            "BC_CONST", "0", "BC_IF_BEGIN", "BC_CONST", "3.5", "BC_STORE_LIST", "Other",
            "BC_ELSE_BEGIN", "BC_CONST", "4.5", "BC_STORE_LIST", "Other", "BC_IF_END",
        ]), "BC_LOADVAR", "Other", "BC_PRINT"],
    }


def _env(tokens, target):
    return run_codegen(", ".join(json.dumps(token) for token in tokens), target=target)


@pytest.mark.parametrize("target", ["x86_64-linux", "x86_64-macos", "aarch64-macos"])
def test_repeat_branch_joins_accept_new_shapes_and_reject_unsafe_paths(target):
    for name, tokens in repeat_branch_positive_cases().items():
        env = _env(tokens, target)
        assert env["NativeFailed"] == 0, name
        assert env["NativeOut"], name
    for name, tokens in repeat_branch_rejection_cases().items():
        env = _env(tokens, target)
        assert env["NativeFailed"] == 1, name
        assert env["NativeOut"] == "", name


@pytest.mark.parametrize("target", ["x86_64-linux", "x86_64-macos", "aarch64-macos"])
def test_repeat_branch_joins_keep_sixteen_if_frames_and_sixty_four_slots(target):
    assert _env(repeat_branch_boundary_bytecode(), target)["NativeFailed"] == 0
    for tokens in (repeat_branch_boundary_bytecode(depth=17),
                   repeat_branch_boundary_bytecode(global_count=65)):
        env = _env(tokens, target)
        assert env["NativeFailed"] == 1
        assert env["NativeOut"] == ""


@pytest.mark.parametrize("outer,middle,inner", CHOICES)
def test_repeat_branch_joins_match_interpreter_and_vm(outer, middle, inner):
    source = repeat_branch_program(outer, middle, inner)
    expected = repeat_branch_output(outer, middle, inner)
    hosted = run_source(source)
    assert hosted.ok, hosted.compile.diags.render_all() if not hosted.compile.ok else hosted.runtime_error
    assert hosted.stdout == expected
    output, failed = run_kuro_vm(source)
    assert failed in (None, 0)
    assert "".join(f"{value}\n" for value in output) == expected


@pytest.mark.parametrize("outer,middle,inner", CHOICES)
@requires_hosted_linux_x86_64
def test_repeat_branch_joins_hosted_linux_native_executes(tmp_path, outer, middle, inner):
    result = _run_hosted_linux_native(
        tmp_path, repeat_branch_program(outer, middle, inner), "repeat-branches",
    )
    assert result.stdout == repeat_branch_output(outer, middle, inner)
    assert result.stderr == ""


@pytest.mark.parametrize(
    "target,triple", [
        ("x86_64-linux", "x86_64-unknown-linux-gnu"),
        ("x86_64-macos", "x86_64-apple-macos"),
        ("aarch64-macos", "arm64-apple-macos11"),
    ],
)
@pytest.mark.parametrize("outer,middle,inner", CHOICES)
def test_repeat_branch_joins_cross_assemble(tmp_path, target, triple, outer, middle, inner):
    _, env = compile_program_to_codegen(repeat_branch_program(outer, middle, inner), target=target)
    assert env["NativeFailed"] == 0
    _cross_assemble(tmp_path, env["NativeOut"], target, triple)
