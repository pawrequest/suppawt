# # Define a custom type with a maximum length constraint that truncates the input
# from typing import Annotated
#
# from pydantic import Field, BaseModel
#
#
# def truncating_str(max_length: int):
#     class TruncatingStr(str):
#         @classmethod
#         def __get_validators__(cls):
#             yield cls.validate
#
#         @classmethod
#         def validate(cls, v):
#             if isinstance(v, str) and len(v) > max_length:
#                 return v[:max_length]
#             return v
#
#     return Annotated[TruncatingStr, Field(max_length=max_length)]
#
# class YourModel(BaseModel):
#     # Use the custom truncating_str type for fields that should truncate instead of failing
#     name: truncating_str(10)  # Truncates to 10 characters
#     description: truncating_str(20)  # Truncates to 20 characters
from __future__ import annotations

from typing import Annotated

from pydantic import BeforeValidator, Field, StringConstraints


def validate_str(v):
    if v:
        v = v.replace(r"/", "")
    return v or ""


SafeStr = Annotated[str, BeforeValidator(validate_str)]


def truncate_before(maxlength) -> BeforeValidator:
    def _truncate(v):
        if v:
            if len(v) <= maxlength:
                return v[:maxlength]
        return v

    return BeforeValidator(_truncate)


def TruncatedSafeStr(max_length: int):
    return Annotated[SafeStr, truncate_before(max_length), StringConstraints(max_length=max_length)]


def TruncatedSafeMaybeStr(max_length: int):
    return Annotated[
        SafeStr, truncate_before(max_length), StringConstraints(max_length=max_length), Field(
            default=""
        )]
