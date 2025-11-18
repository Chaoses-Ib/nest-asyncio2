# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "nest-asyncio2",
# ]
#
# [tool.uv.sources]
# nest-asyncio2 = { path = "../", editable = true }
# ///
import asyncio
import nest_asyncio2

nest_asyncio2.apply()

async def f():
    print(asyncio.get_running_loop())
    assert asyncio.get_running_loop() is not None

    print(asyncio.tasks._current_tasks)
    # assert asyncio.tasks._current_tasks == {}

    print(asyncio.tasks.current_task())
    assert asyncio.tasks.current_task() is not None

    print(asyncio.tasks._py_current_task())
    # assert asyncio.tasks._py_current_task() is None

    print(asyncio.tasks._current_tasks)
    # assert asyncio.tasks._current_tasks == {}

asyncio.run(f())
