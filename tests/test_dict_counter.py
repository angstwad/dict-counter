"""Tests for the DictCounter class."""

import pytest

from dict_counter import DictCounter


def test_initialization() -> None:
    """Verifies that DictCounter initializes correctly with and without initial data."""
    dc = DictCounter()
    assert len(dc) == 0
    assert dc.updated_count == 0

    dc2 = DictCounter({'a': 1})
    assert dc2['a'] == 1
    assert dc2.updated_count == 1


def test_update_flat() -> None:
    """Verifies that flat dictionaries are counted correctly."""
    dc = DictCounter()
    dc.update({'a': 1, 'b': 2})
    dc.update({'a': 1, 'c': 3})

    assert dc['a'] == 2
    assert dc['b'] == 1
    assert dc['c'] == 1
    assert dc.updated_count == 2


def test_update_nested() -> None:
    """Verifies that nested dictionaries are counted correctly, including the traversal key."""
    dc = DictCounter()
    docs = [
        {'foo': {'bar': 1}},
        {'foo': {'baz': 1}},
        {'foo': {'bar': 1, 'quux': 1}},
    ]
    dc.update_many(docs)

    assert dc['foo']['_self'] == 3
    assert dc['foo']['bar'] == 2
    assert dc['foo']['baz'] == 1
    assert dc['foo']['quux'] == 1
    assert dc.updated_count == 3


def test_custom_count_key() -> None:
    """Verifies that a custom nested count key is respected during updates."""
    dc = DictCounter(nested_count_key='__count__')
    dc.update({'foo': {'bar': 1}})

    assert dc['foo']['__count__'] == 1
    assert '__count__' in dc['foo']
    assert '_self' not in dc['foo']


def test_update_type_error() -> None:
    """Verifies that update raises a TypeError when provided with non-mapping input."""
    dc = DictCounter()
    with pytest.raises(TypeError, match='Expected Mapping type'):
        dc.update([('a', 1)])  # type: ignore[arg-type]


def test_clear() -> None:
    """Verifies that clearing the counter resets its internal state."""
    dc = DictCounter({'a': 1})
    dc.clear()
    assert len(dc) == 0
    assert 'a' not in dc


def test_mapping_interface() -> None:
    """Verifies that the DictCounter implements the expected Mapping methods."""
    dc = DictCounter({'a': 1, 'b': {'c': 1}})

    assert set(dc.keys()) == {'a', 'b'}
    assert len(list(dc.values())) == 2
    assert ('a', 1) in dc.items()
    assert 'a' in dc
    assert len(dc) == 2
    assert str(dc).startswith('{')


def test_setitem_not_implemented() -> None:
    """Verifies that direct assignment via __setitem__ raises NotImplementedError."""
    dc = DictCounter()
    with pytest.raises(NotImplementedError):
        dc['a'] = 1
