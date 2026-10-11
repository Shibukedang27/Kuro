from compiler.memory import MemoryManager


def test_kuro_heap_marks_nested_reachable_values_and_sweeps_dead_values():
    heap = MemoryManager()
    live = ["nested"]
    root = [live]
    dead = ["dead"]
    heap.track(root)
    heap.track(live)
    heap.track(dead)
    assert heap.allocated == 3
    assert heap.collect([root]) == 1
    assert heap.allocated == 2
    assert heap.stats() == {"allocated": 2, "collections": 1, "freed": 1}


def test_bytecode_vm_exposes_kuro_memory_collection_boundary():
    from compiler.bytecode import BytecodeProgram, BytecodeInstruction, BytecodeVM
    vm = BytecodeVM(BytecodeProgram((BytecodeInstruction("CONST", ("x",), "t0"),
                                    BytecodeInstruction("STORE_LIST", ("Items", ["t0"])),), {}))
    vm.run()
    assert vm.memory.stats()["collections"] == 1


def test_bytecode_vm_executes_private_artifact_suffix_instruction():
    from io import StringIO

    from compiler.bytecode import BytecodeVM, encode_ir
    from compiler.interpreter import KuroRuntimeException
    from compiler.pipeline import compile_source

    compiled = compile_source('Call __KuroArtifactSuffix "prefix-tail", 7;\nPrint @_.')
    assert compiled.ok, compiled.diags.render_all()
    output = StringIO()
    vm = BytecodeVM(encode_ir(compiled.ir), output=output)
    vm.run()
    assert vm.env["_"] == "tail"
    assert output.getvalue() == "tail\n"

    invalid = compile_source('Call __KuroArtifactSuffix "abc", -1;')
    assert invalid.ok, invalid.diags.render_all()
    try:
        BytecodeVM(encode_ir(invalid.ir), output=StringIO()).run()
    except KuroRuntimeException as error:
        assert error.code == "E6001"
    else:
        raise AssertionError("negative suffix offsets must be rejected")


def test_kuro_heap_traces_closure_tagged_and_task_ownership_edges():
    from compiler.concurrency import Task
    from compiler.values import ClosureValue, TaggedValue, TaskValue

    heap = MemoryManager()
    captured = ["captured"]
    closure = ClosureValue("Keep", {"values": captured})
    tagged = TaggedValue("Some", closure)
    task = TaskValue(Task(1, closure, [tagged]))
    heap.track(task)
    assert heap.allocated >= 5
    assert heap.collect([task]) == 0
    assert heap.allocated >= 5
    assert heap.collect([]) >= 1
    assert heap.allocated == 0


def test_kuro_heap_traces_values_queued_in_channels():
    from compiler.concurrency import Channel
    from compiler.values import ChannelValue

    heap = MemoryManager()
    queued = ["message"]
    channel = Channel()
    channel.send(queued)
    root = ChannelValue(channel)
    heap.track(root)
    assert heap.collect([root]) == 0
    assert heap.allocated >= 3
