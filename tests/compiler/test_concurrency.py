from compiler.pipeline import run_source


SOURCE = (
    'Action Work Value;\n'
    '    Return Value + 1;\n'
    'Done.\n'
    'Call MakeClosure "Work";\n'
    'Call Spawn @_, 0;\n'
    'Call Await @_;\n'
    'Print @_.\n'
)


def test_spawn_and_await_are_deterministic_kuro_tasks():
    first = run_source(SOURCE)
    second = run_source(SOURCE)
    assert first.ok and second.ok
    assert first.stdout == second.stdout == "1\n"


def test_channels_provide_fifo_send_receive_and_nonblocking_probe():
    result = run_source(
        'Inbox = 0;\nCall MakeChannel;\nUpdate Inbox to @_;\n'
        'Call ChannelHas Inbox;\nPrint @_.\n'
        'Call Send Inbox, 7;\nCall Send Inbox, 9;\n'
        'Call ChannelHas Inbox;\nPrint @_.\n'
        'Call Receive Inbox;\nPrint @_.\n'
        'Call Receive Inbox;\nPrint @_.\n'
        'Call ChannelHas Inbox;\nPrint @_.\n'
    )
    assert result.ok
    assert result.stdout == "False\nTrue\n7\n9\nFalse\n"
