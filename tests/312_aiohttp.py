# /// script
# requires-python = ">=3.5"
# dependencies = [
#     "aiohttp",
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
import aiohttp

with warnings.catch_warnings(record=True) as w:
    nest_asyncio2.apply()
    assert len(w) == 0, w

async def f_async():
    async with aiohttp.ClientSession() as session:
        async with session.get('http://httpbin.org/get') as resp:
            print(resp.status)
            print(await resp.text())
            assert resp.status == 200

def f():
    asyncio.run(f_async())

async def main():
    f()

with warnings.catch_warnings(record=True) as w:
    asyncio.run(main())
    assert len(w) == 0, w
