# https://github.com/Chaoses-Ib/nest-asyncio2/issues/5
# /// script
# requires-python = ">=3.6"
# dependencies = [
#     "nest-asyncio2",
# ]
#
# [tool.uv.sources]
# nest-asyncio2 = { path = "../", editable = true }
# ///
import asyncio
import gc
import sys

import nest_asyncio2


async def agen():
    try:
        yield 1
        yield 2
    finally:
        # Cleanup that awaits, as httpx/httpcore stream generators do.
        await asyncio.sleep(0)
        print("  cleanup finished")


async def main():
    print("  finalizer hook set:", sys.get_asyncgen_hooks().finalizer is not None)
    g = agen()
    await g.__anext__()  # leave the generator suspended, never closed
    del g
    gc.collect()
    await asyncio.sleep(0.01)


print("stock asyncio.run:")
asyncio.run(main())

loop = asyncio.new_event_loop()
nest_asyncio2.apply(loop)  # patches the loop class
loop.close()

print("asyncio.run after nest_asyncio2.apply on another loop:")
asyncio.run(main())
