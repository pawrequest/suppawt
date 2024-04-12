from collections.abc import Collection

import pytest

from suppawt.compare import flatten_generic, handle_match, handle_match_bools, any_in_any



def test_different_kinds_of_sequences():
    # Testing with a list and a tuple
    mixed_sequences = (['abc', 'def'], ('ghi', 'defg'))
    expected_results = [
        "'def' matched with 'defg'",

    ]
    results = any_in_any(*mixed_sequences, handler=handle_match)
    assert all(
        item in results for item in expected_results
    ), 'Test for different_kinds_of_sequences failed.'


def test_empty_strings():
    strings_with_empty = ['abc', '', 'a', '']
    expected_results = [
        "'' matched with 'abc'",
        "'' matched with 'a'",
    ]
    results = any_in_any(*strings_with_empty, handler=handle_match)
    assert all(item in results for item in expected_results), 'Test for empty_strings failed.'


def test_strings_with_whitespace():
    strings_with_whitespace = [' ', ' leading space', 'trailing space ']
    expected_results = [
        "' ' matched with ' leading space'",
        "' ' matched with 'trailing space '",
    ]
    results = any_in_any(*strings_with_whitespace, handler=handle_match)
    assert all(
        item in results for item in expected_results
    ), 'Test for strings_with_whitespace failed.'


def test_numerical_strings():
    numerical_strings = ['123', '1234', '234']
    expected_results = [
        "'123' matched with '1234'",
        "'234' matched with '1234'",
    ]
    results = any_in_any(*numerical_strings, handler=handle_match)
    assert all(item in results for item in expected_results), 'Test for numerical_strings failed.'


def test_identical_strings():
    identical_strings = ['repeat', 'repeat']
    res = any_in_any(*identical_strings, match_self=True)
    ...
    with pytest.raises(ValueError):
        any_in_any(*identical_strings)


def test_nested_empty_sequences_raises():
    nested_empty = ([[], []], [])
    # Expect a ValueError due to the lack of actual invals
    with pytest.raises(ValueError):
        any_in_any(*nested_empty, match_self=True)


def test_flatten_with_integers():
    nested_ints: Nested2[int] = [1, [2, 3], {4, 5, 6}, (7,)]
    expected_output = [1, 2, 3, 4, 5, 6, 7]
    assert list(flatten_generic(nested_ints)) == expected_output


def test_flatten_with_custom_objects():
    class CustomObject:
        def __init__(self, value):
            self.value = value

        def __eq__(self, other):
            return self.value == other.value

        def __repr__(self):
            return f'CustomObject({self.value})'

    nested_objects: Nested2[CustomObject] = [CustomObject(1), [CustomObject(2), CustomObject(3)]]
    expected_output = [CustomObject(1), CustomObject(2), CustomObject(3)]
    res = list(flatten_generic(nested_objects))
    assert [item in res for item in expected_output]


def test_flatten_with_mixed_types():
    nested_mixed: Nested2 = [1, 'two', [3, 'four'], {'five', 6}]
    expected_output = [1, 'two', 3, 'four', 'five', 6]
    flattened_result = list(flatten_generic(nested_mixed))
    assert all(item in flattened_result for item in expected_output)
    assert len(flattened_result) == len(expected_output)


def test_flatten_with_empty_sequences():
    empty_nested: Nested2[int] = [[], [], [()]]
    assert list(flatten_generic(empty_nested)) == []


def test_flatten_with_dicts():
    # Note: Only keys are collected since values are not part of the collection
    nested_dicts: Nested2 = [{'key1': 1}, [{'key2': 2}, {'key3': 3}]]
    expected_keys = ['key1', 'key2', 'key3']
    assert sorted(list(flatten_generic(nested_dicts))) == sorted(expected_keys)


# Additional tests to check handling of very deep nesting
def test_flatten_with_deep_nesting():
    deep_nested = [1, [2, [3, [4, [5]]]]]
    expected_output = [1, 2, 3, 4, 5]
    assert list(flatten_generic(deep_nested)) == expected_output


def test_match_identification():
    inputs = ['hello', 'Hello', 'world', 'World']
    # Test default handler
    results = any_in_any(*inputs, handler=handle_match)
    assert "'hello' matched with 'Hello'" in results
    assert "'world' matched with 'World'" in results

    # Test boolean match handler
    bool_results = any_in_any(*inputs, handler=handle_match_bools)
    assert True in bool_results  # Expect True if any match found


def test_no_match_condition():
    inputs = ['apple', 'banana', 'cherry']
    results = any_in_any(*inputs, handler=handle_match_bools)
    assert not results  # Expect empty set if no matches


def test_handle_match_functionality():
    inputs = ['test', 'testing', 'tester', 'Test']
    # Using a custom handler that checks for substring presence
    results = any_in_any(*inputs, handler=lambda s1, s2: s1.lower() in s2.lower())
    assert True in results  # Expect True if any substrings match


@pytest.mark.parametrize('handler_function', [handle_match, handle_match_bools])
def test_dynamic_handler_usage(handler_function):
    inputs = ['part', 'partial', 'article', 'particle']
    results = any_in_any(*inputs, handler=handler_function)
    # Check based on what handler_function we use
    if handler_function == handle_match_bools:
        assert True in results
    else:
        expected_matches = {
            "'part' matched with 'partial'",
            "'article' matched with 'particle'",
            "'part' matched with 'particle'"  # Acknowledge this valid match given the logic
        }
        assert results == expected_matches
