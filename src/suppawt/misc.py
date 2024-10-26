from __future__ import annotations

import importlib.util
from pathlib import Path


def can_import(module_name):
    spec = importlib.util.find_spec(module_name)
    return spec is not None


def unused_path(filepath: Path):
    def numbered_filepath(number: int):
        return filepath if not number else filepath.with_stem(f"{filepath.stem}_{number}")

    incremented = 0
    lpath = numbered_filepath(incremented)
    while lpath.exists():
        incremented += 1
        lpath = numbered_filepath(incremented)
    return lpath
