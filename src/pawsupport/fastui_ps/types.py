from __future__ import annotations

from typing import Union

from fastui import components as c

from pawsupport.fastui_ps import Col, Container, Row

WrapIn = Union[type[Row], type[Col], type[Container], type[c.Div]]
