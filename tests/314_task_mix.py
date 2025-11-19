# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "nest-asyncio2",
# ]
#
# [tool.uv.sources]
# nest-asyncio2 = { path = "../", editable = true }
# ///
import warnings
warnings.filterwarnings("default")

import asyncio
import nest_asyncio2

async def f():
    nest_asyncio2.apply()

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
