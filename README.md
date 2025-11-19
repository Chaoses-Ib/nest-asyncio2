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

## Comparison with `nest_asyncio`
`nest-asyncio2` is a fork of the unmaintained [`nest_asyncio`](https://github.com/erdewit/nest_asyncio), with the following changes:
- Python 3.12 support
  - `loop_factory` parameter support
  - Fix `ResourceWarning: unclosed event loop` at exit

    Note that if you call `asyncio.get_event_loop()` on the main thread without setting the loop before, `ResourceWarning` is expected on Python 3.12~3.13, not caused by `nest-asyncio2`.
- Python 3.14 support
  - Fix broken `asyncio.current_task()` and others
  - Fix `DeprecationWarning: 'asyncio.get_event_loop_policy' is deprecated and slated for removal in Python 3.16`

All interfaces are kept as they are. To migrate, you just need to change the package and module name to `nest_asyncio2`.
