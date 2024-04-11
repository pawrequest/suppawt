from __future__ import annotations

import importlib.util


def can_import(module_name):
    spec = importlib.util.find_spec(module_name)
    return spec is not None
