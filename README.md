# nest-asyncio2
[![Build](https://github.com/Chaoses-Ib/nest-asyncio2/actions/workflows/test.yml/badge.svg?branche=master)](https://github.com/Chaoses-Ib/nest-asyncio2/actions)
[![status](https://img.shields.io/badge/status-stable-green.svg)]()
[![PyPi](https://img.shields.io/pypi/v/nest-asyncio2.svg)](https://pypi.python.org/pypi/nest-asyncio2)
[![License](https://img.shields.io/badge/license-BSD-blue.svg)](LICENSE)
[![Downloads](https://static.pepy.tech/badge/nest-asyncio2/month)](https://pepy.tech/project/nest-asyncio2)

## Introduction

By design asyncio [does not allow](https://github.com/python/cpython/issues/66435)
its event loop to be nested. This presents a practical problem:
When in an environment where the event loop is
already running it's impossible to run tasks and wait
for the result. Trying to do so will give the error
"`RuntimeError: This event loop is already running`".

The issue pops up in various environments, such as web servers,
GUI applications and in Jupyter notebooks.

This module patches asyncio to allow nested use of `asyncio.run` and
`loop.run_until_complete`.

## Installation

```sh
pip3 install nest-asyncio2
```

Python 3.5 or higher is required.

## Usage

```python
import nest_asyncio2
nest_asyncio2.apply()
```

Optionally the specific loop that needs patching can be given
as argument to `apply`, otherwise the current event loop is used.
An event loop can be patched whether it is already running
or not. Only event loops from asyncio can be patched;
Loops from other projects, such as uvloop or quamash,
generally can't be patched.

## Examples
### [aiohttp](https://github.com/aio-libs/aiohttp)
```py
# /// script
# requires-python = ">=3.5"
# dependencies = [
#     "aiohttp",
#     "nest-asyncio2",
# ]
# ///
import asyncio
import nest_asyncio2
import aiohttp

nest_asyncio2.apply()

async def f_async():
    # Note that ClientSession must be created and used
    # in the same event loop (under the same asyncio.run())
    async with aiohttp.ClientSession() as session:
        async with session.get('http://httpbin.org/get') as resp:
            print(resp.status)
            print(await resp.text())
            assert resp.status == 200

# async to sync
def f():
    asyncio.run(f_async())

async def main():
    f()
asyncio.run(main())
```

## Known issues
### Leaked loop
> [!TIP]
> TL;DR: Usually you don't need to worry about this.
> The biggest side effect is a `ResourceWarning: unclosed event loop` at exit on Python 3.12+ that is hidden by default.

If there is no existing event loop, patched `asyncio.run()` will create one but not close it afterwards.
It will be reused later, so there will be at most one leaked loop.

`asyncio.run()` will always create and close the loop.
But `nest_asyncio` (by accident or intentionally) missed it.
As changing this behavior will break existing projects (e.g.
[ComfyScript](https://github.com/Chaoses-Ib/ComfyScript/issues/117),
[pyvista](https://github.com/pyvista/pyvista/issues/7938)),
`nest-asyncio2` follows this behavior.

This will cause a `ResourceWarning: unclosed event loop` at exit on Python 3.12+,
although it is hidden by default.
(Note that if you call `asyncio.get_event_loop()` on the main thread without setting the loop before,
`ResourceWarning` is expected on Python 3.12~3.13, not caused by `nest-asyncio2`.)

If you want to follow `asyncio.run()`'s behavior and get rid of the `ResourceWarning`,
you can set `run_close_loop=True` for all `apply()`:
```py
nest_asyncio2.apply(run_close_loop=True)
```
Or pass `loop_factory` to `asyncio.run()` on Python 3.12+:
```py
asyncio.run(..., loop_factory=asyncio.new_event_loop)
```

`nest-asyncio2` v2 may change `run_close_loop` to be enalbed by default.

## Comparison with `nest_asyncio`
`nest-asyncio2` is a fork of the unmaintained [`nest_asyncio`](https://github.com/erdewit/nest_asyncio), with the following changes:
- Support setting `run_close_loop` to avoid [leaked loop](#leaked-loop)
- Python 3.12 support
  - `loop_factory` parameter support
<!--
  - Fix `ResourceWarning: unclosed event loop` at exit

    Note that if you call `asyncio.get_event_loop()` on the main thread without setting the loop before, `ResourceWarning` is expected on Python 3.12~3.13, not caused by `nest-asyncio2`.
-->
- Python 3.14 support
  - Fix broken `asyncio.current_task()` and others
  - Fix `DeprecationWarning: 'asyncio.get_event_loop_policy' is deprecated and slated for removal in Python 3.16`

All interfaces are kept as they are. To migrate, you just need to change the package and module name to `nest_asyncio2`.
