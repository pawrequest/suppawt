import typing as _t
from collections.abc import Collection

import pytest

type NestedStrings = str | Collection[NestedStrings]
type Nested2[T] = T | Collection[Nested2[T]]


def any_in_any(*strings: NestedStrings, match_self=False) -> set[str]:
    strings = list(strings)
    wrapper = list if match_self else set
    # flattened_strings = wrapper(flatten(strings))
    flattened_strings = wrapper(flatten_generic(strings))
    if len(flattened_strings) < 2:
        raise ValueError(f'Must provide more than one {'' if match_self else 'unique'} string')
    return {
        f"'{s1}' matched with '{s2}'"
        for i1, s1 in enumerate(flattened_strings)
        for i2, s2 in enumerate(flattened_strings)
        if i1 != i2 and s1.lower() in s2.lower()
    }


def flatten(strings: NestedStrings) -> _t.Generator[str, None, None]:
    for string in strings:
        if isinstance(string, str):
            yield string
        elif isinstance(string, _t.Sequence):
            yield from flatten(string)
        else:
            raise TypeError(f'Expected str or Sequence, got {type(string)}')


def flatten_generic[T](invals: Nested2[T]):
    for inval in invals:
        if isinstance(inval, str):
            yield inval
        else:
            yield from flatten_generic(inval)


def test_different_kinds_of_sequences():
    # Testing with a list and a tuple
    mixed_sequences = (['abc', 'def'], ('ghi', 'defg'))
    expected_results = [
        "'def' matched with 'defg'",

    ]
    results = any_in_any(*mixed_sequences)
    assert all(
        item in results for item in expected_results
    ), 'Test for different_kinds_of_sequences failed.'


def test_empty_strings():
    strings_with_empty = ['abc', '', 'a', '']
    expected_results = [
        "'' matched with 'abc'",
        "'' matched with 'a'",
    ]
    results = any_in_any(*strings_with_empty)
    assert all(item in results for item in expected_results), 'Test for empty_strings failed.'


def test_strings_with_whitespace():
    strings_with_whitespace = [' ', ' leading space', 'trailing space ']
    expected_results = [
        "' ' matched with ' leading space'",
        "' ' matched with 'trailing space '",
    ]
    results = any_in_any(*strings_with_whitespace)
    assert all(
        item in results for item in expected_results
    ), 'Test for strings_with_whitespace failed.'


def test_numerical_strings():
    numerical_strings = ['123', '1234', '234']
    expected_results = [
        "'123' matched with '1234'",
        "'234' matched with '1234'",
    ]
    results = any_in_any(*numerical_strings)
    assert all(item in results for item in expected_results), 'Test for numerical_strings failed.'


def test_identical_strings():
    identical_strings = ['repeat', 'repeat']
    res = any_in_any(*identical_strings, match_self=True)
    ...
    with pytest.raises(ValueError):
        any_in_any(*identical_strings)


def test_nested_empty_sequences_raises():
    nested_empty = ([[], []], [])
    # Expect a ValueError due to the lack of actual strings
    with pytest.raises(ValueError):
        any_in_any(*nested_empty, match_self=True)
