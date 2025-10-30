# Convenience re-export of the game scripting API.

import importlib

_api = importlib.import_module("global")

__all__ = []
_names = getattr(_api, "__all__", [])
index = 0
while index < len(_names):
    name = _names[index]
    globals()[name] = getattr(_api, name)
    __all__.append(name)
    index = index + 1
