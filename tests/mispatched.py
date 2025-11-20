# /// script
# requires-python = ">=3.5"
# dependencies = [
#     "nest-asyncio",
#     "nest-asyncio2",
# ]
#
# [tool.uv.sources]
# nest-asyncio2 = { path = "../", editable = true }
# ///
import warnings
import sys

import nest_asyncio
nest_asyncio.apply()

import nest_asyncio2

with warnings.catch_warnings(record=True) as w:
    nest_asyncio2.apply()
    if sys.version_info < (3, 12, 0):
        assert len(w) == 0, w
    else:
        assert len(w) == 1, w

error = False
try:
    nest_asyncio2.apply(error_on_mispatched=True)
except RuntimeError:
    error = True
assert error
