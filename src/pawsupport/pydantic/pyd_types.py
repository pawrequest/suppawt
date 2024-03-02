# from __future__ import annotations

import typing as _ty

import pydantic as pyd


# if _ty.TYPE_CHECKING:
#     pass


def validate_str(v):
    # return v
    if v:
        v = v.replace(r"/", "")
    return v or ""


SafeStr = _ty.Annotated[str, pyd.BeforeValidator(validate_str)]


def truncate_before(maxlength) -> pyd.BeforeValidator:
    def _truncate(v):
        if v:
            if len(v) > maxlength:
                return v[:maxlength]
        return v

    return pyd.BeforeValidator(_truncate)


def TruncatedSafeStr(max_length: int):
    return _ty.Annotated[
        SafeStr, pyd.StringConstraints(max_length=max_length), truncate_before(max_length)]


def TruncatedSafeMaybeStr(max_length: int):
    return _ty.Annotated[
        SafeStr, pyd.StringConstraints(max_length=max_length), truncate_before(
            max_length
        ), pyd.Field(
            ''
        )]
