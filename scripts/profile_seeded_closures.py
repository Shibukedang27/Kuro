#!/usr/bin/env python3
"""Profile a source-generated, genuinely closure-returning large Action.

Run separately for timing and counters (instrumentation adds overhead):
  python scripts/profile_seeded_closures.py --output /tmp/seeded --size 200 --repeat 3
  python scripts/profile_seeded_closures.py --output /tmp/counts --size 200 --instrument
Use --root to compare unchanged checkouts; .s must match before comparing times.
No linking or execution is performed by this opt-in developer tool.
"""
from __future__ import annotations

import argparse
import ast
import cProfile
import hashlib
import inspect
import json
from pathlib import Path
import platform
import pstats
import subprocess
import sys
import time


def seeded_source(size: int) -> str:
    """Keep a real closure live across many numeric temporaries, then Invoke it."""
    return (
        'First = 0; Second = 0;\n'
        'Action MakeAdder Base;\n'
        'Action AddBase Value; Return Base + Value; Done.\n'
        'Call MakeClosure "AddBase"; Selected = @_;\n'
        + ''.join(f'Local{index} = Base + {index};\n' for index in range(size))
        + 'Return Selected; Done.\n'
        'Call MakeAdder 10; Update First to @_;\n'
        'Call MakeAdder 20; Update Second to @_;\n'
        'Call Invoke First, 7; Print @_.\n'
        'Call Invoke Second, 7; Print @_.\n'
    )


def instrumented_emitter(native, *, cfg_cache=False, count=True):
    """AST-only counters; production APIs and hot paths remain untouched.

    Match semantic assignment shapes rather than line numbers. Each copied name
    is a mapping entry; a deep target copy is a set(targets) allocation in one
    of the two whole-state clones (not the transfer/merge allocations).
    """
    metrics = dict(analyzer_calls=0, cfg_builds=0, body_visits=0,
                   copied_names=0, deep_target_copies=0, merge_attempts=0,
                   merged_names=0, merge_updates=0)
    tree = ast.parse(inspect.getsource(native.emit_x86_64_linux))

    class CacheCFG(ast.NodeTransformer):
        changed = 0

        def visit_FunctionDef(self, node):
            if node.name != 'analyze_action_closure_returns':
                return self.generic_visit(node)
            # Keep the original edge builder verbatim and in its original order.
            assert ast.unparse(node.body[1].targets[0]) == 'label_indices'
            assert isinstance(node.body[3], ast.For)
            guard = ast.parse('if function.name not in _closure_cfg_cache: pass').body[0]
            guard.body = node.body[1:4] + ast.parse(
                '_closure_cfg_cache[function.name] = tuple(successors)').body
            node.body[1:4] = [guard] + ast.parse(
                'successors = _closure_cfg_cache[function.name]').body
            self.changed += 1
            return ast.parse('_closure_cfg_cache = {}').body + [node]

    if cfg_cache:
        cache = CacheCFG()
        tree = cache.visit(tree)
        assert cache.changed == 1

    def increment(key, expression='1'):
        return ast.parse(f'_closure_metrics["{key}"] += {expression}').body[0]

    class Counters(ast.NodeTransformer):
        inside = False
        hits = set()

        def visit_FunctionDef(self, node):
            if node.name != 'analyze_action_closure_returns':
                return self.generic_visit(node)
            self.inside = True
            node = self.generic_visit(node)
            self.inside = False
            node.body.insert(0, increment('analyzer_calls'))
            return node

        def visit_Assign(self, node):
            if not self.inside:
                return node
            text = ast.unparse(node.targets[0])
            before = []
            if text == 'label_indices':
                before = [increment('cfg_builds')]
                self.hits.add('cfg')
            elif text == 'item' and ast.unparse(node.value) == 'body[index]':
                before = [increment('body_visits')]
                self.hits.add('visit')
            elif text in ('state', 'states[successor]'):
                value = node.value
                if isinstance(value, ast.DictComp):
                    source = ast.unparse(value.generators[0].iter.func.value)
                    before = [increment('copied_names', f'len({source})'),
                              increment('deep_target_copies', f'len({source})')]
                    self.hits.add(f'copy:{source}')
                elif (isinstance(value, ast.Call) and isinstance(value.func, ast.Attribute)
                      and value.func.attr == 'copy'):
                    source = ast.unparse(value.func.value)
                    before = [increment('copied_names', f'len({source})')]
                    self.hits.add(f'copy:{source}')
                elif text == 'states[successor]' and ast.unparse(value) == 'merged':
                    before = [increment('merge_updates')]
                    self.hits.add('updates')
            return before + [node]

        def visit_AnnAssign(self, node):
            if self.inside and ast.unparse(node.target) == 'merged':
                self.hits.add('merge')
                return [increment('merge_attempts'),
                        increment('merged_names', 'len(current.keys() | state.keys())'), node]
            return node

    counters = Counters()
    if count:
        tree = counters.visit(tree)
        assert counters.hits == {'cfg', 'visit', 'copy:incoming', 'copy:state', 'updates', 'merge'}, counters.hits
    namespace = vars(native).copy()
    namespace['_closure_metrics'] = metrics
    exec(compile(ast.fix_missing_locations(tree), '<counted-seeded-emitter>', 'exec'), namespace)
    return namespace['emit_x86_64_linux'], metrics


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--size', type=int, default=200)
    parser.add_argument('--repeat', type=int, default=1)
    parser.add_argument('--instrument', action='store_true')
    parser.add_argument('--profile', action='store_true')
    parser.add_argument('--cfg-cache', action='store_true', help='test-only immutable CFG-cache experiment')
    args = parser.parse_args()
    if args.size < 0 or args.repeat < 1:
        parser.error('size must be nonnegative and repeat must be positive')
    root = args.root.resolve()
    sys.path.insert(0, str(root))
    import compiler.native as native
    from compiler.pipeline import compile_source

    source = seeded_source(args.size)
    result = compile_source(source)
    if not result.ok:
        raise RuntimeError(result.diags.render_all())
    if args.instrument or args.cfg_cache:
        emit, counts = instrumented_emitter(native, cfg_cache=args.cfg_cache, count=args.instrument)
    else:
        emit, counts = native.emit_x86_64_linux, None
    metadata = dict(python=sys.version, platform=platform.platform(), size=args.size,
                    head=subprocess.check_output(['git', '-C', str(root), 'rev-parse', 'HEAD'], text=True).strip(),
                    compiler_dirty=bool(subprocess.check_output(['git', '-C', str(root), 'diff', 'HEAD', '--', 'compiler'], text=True)),
                    source_sha256=hashlib.sha256(source.encode()).hexdigest(),
                    function_instructions={name: len(fn.body) for name, fn in result.ir.functions.items()},
                    instrumented=args.instrument, profiled=args.profile,
                    cfg_cache_experiment=args.cfg_cache, emit_seconds=[])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    Path(f'{args.output}.kuro').write_text(source, encoding='utf-8')
    profiler = cProfile.Profile() if args.profile else None
    previous = None
    for run in range(args.repeat):
        started = time.perf_counter()
        if profiler:
            profiler.enable()
        try:
            assembly = emit(result.ir).encode()
        finally:
            if profiler:
                profiler.disable()
        metadata['emit_seconds'].append(time.perf_counter() - started)
        if previous is not None:
            assert assembly == previous, 'assembly changed between repetitions'
        previous = assembly
        print(json.dumps(dict(run=run + 1, seconds=metadata['emit_seconds'][-1])), flush=True)
    metadata.update(assembly_bytes=len(assembly), assembly_sha256=hashlib.sha256(assembly).hexdigest())
    if args.instrument:
        metadata['counts_total_across_repetitions'] = counts
    if profiler:
        profiler.dump_stats(f'{args.output}.prof')
        pstats.Stats(profiler).sort_stats('cumulative').print_stats(20)
    Path(f'{args.output}.s').write_bytes(assembly)
    Path(f'{args.output}.json').write_text(json.dumps(metadata, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(metadata), flush=True)


if __name__ == '__main__':
    main()
