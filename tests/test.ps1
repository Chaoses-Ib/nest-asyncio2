pushd tests

# uv run --python 3.5 nest_test.py
uv run --python 3.8 nest_test.py
if (!$?) {
    throw "3.10"
}
uv run --python 3.9 nest_test.py
if (!$?) {
    throw "3.9"
}
uv run --python 3.10 nest_test.py
if (!$?) {
    throw "3.10"
}
uv run --python 3.11 nest_test.py
if (!$?) {
    throw "3.11"
}
uv run --python 3.12 nest_test.py
if (!$?) {
    throw "3.12"
}
uv run --python 3.13 nest_test.py
if (!$?) {
    throw "3.13"
}
uv run --python 3.14 nest_test.py
if (!$?) {
    throw "3.14"
}

uv run --python 3.12 312_loop_factory.py
if (!$?) {
    throw "312_loop_factory"
}
uv run --python 3.14 312_loop_factory.py
if (!$?) {
    throw "314_loop_factory"
}

uv run --python 3.14 314_task.py
if (!$?) {
    throw "314_task"
}
uv run --python 3.14 314_task_mix.py
if (!$?) {
    throw "314_task_mix"
}

popd