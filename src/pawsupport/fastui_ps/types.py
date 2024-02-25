from __future__ import annotations

from typing import TypeAlias, Union

from fastui import components as c

from . import fui

ContainerLike: TypeAlias = Union[
    type[fui.Row], type[fui.Col], type[fui.Container], type[c.Div]]
Containable: TypeAlias = fui.Row | fui.Col
