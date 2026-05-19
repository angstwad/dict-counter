"""Lightweight dictionary-based counter for tracking hierarchical data."""

import pprint
from collections.abc import ItemsView
from collections.abc import Iterator
from collections.abc import KeysView
from collections.abc import Mapping
from collections.abc import ValuesView
from typing import Any
from typing import Hashable
from typing import Iterable
from typing import Self

type StackItem = tuple[Hashable, Any, dict[Hashable, Any]]


class DictCounter:
    """Manages a nested dictionary-based counter for tracking hierarchical data counts.

    Attributes:
        updated_count: The number of successful update operations performed.
    """

    def __init__(self, dct: Mapping[Any, Any] | None = None, nested_count_key: str = '_self'):
        """Initializes the counter with an optional mapping and a custom nested count key.

        Args:
            dct: Initial data for the counter.
            nested_count_key: Key used to track traversal counts at each level.
        """
        self._counter_dict: dict[Hashable, Any] = {}
        self._key_name = nested_count_key
        self.updated_count = 0
        if dct is not None:
            self.update(dct)

    def update(self, dct: Mapping[Any, Any]) -> Self:
        """Recursively updates the counter with keys from the provided mapping.

        Args:
            dct: Mapping containing data to accumulate.

        Raises:
            TypeError: If the input is not a Mapping.
        """
        if not isinstance(dct, Mapping):
            raise TypeError(f"Expected Mapping type, got '{type(dct)}'")

        stack: list[StackItem] = [(*item, self._counter_dict) for item in dct.items()]
        while stack:
            k, v, ptr = stack.pop()
            if isinstance(v, Mapping):
                if k not in ptr:
                    ptr[k] = {self._key_name: 1}
                else:
                    ptr[k][self._key_name] += 1
                for item in v.items():
                    stack.append((*item, ptr[k]))
            elif k in ptr:
                ptr[k] += 1
            else:
                ptr[k] = 1
        self.updated_count += 1
        return self

    def update_many(self, dcts: Iterable[Mapping[Any, Any]]) -> Self:
        """Iteratively updates the counter with multiple mappings.

        Args:
            dcts: Iterable of mappings to process.
        """
        for d in dcts:
            self.update(d)
        return self

    def clear(self) -> None:
        """Resets the internal counter state."""
        self._counter_dict.clear()

    def items(self) -> ItemsView[Hashable, Any]:
        """Returns a view of the counter's items."""
        return self._counter_dict.items()

    def keys(self) -> KeysView[Hashable]:
        """Returns a view of the counter's keys."""
        return self._counter_dict.keys()

    def values(self) -> ValuesView[Any]:
        """Returns a view of the counter's values."""
        return self._counter_dict.values()

    def get(self, key, default=None):
        """Return the value for key if key is in the DictCounter, else default; default is None."""
        return self._counter_dict.get(key, default)

    def __getitem__(self, item: Hashable) -> Any:
        """Accesses a count or sub-counter by key."""
        return self._counter_dict[item]

    def __setitem__(self, key: Hashable, value: Any) -> None:
        """Assignment is not supported."""
        raise NotImplementedError('DictCounter does not support direct assignment.')

    def __contains__(self, item: object) -> bool:
        """Checks if a key exists in the counter."""
        return item in self._counter_dict

    def __len__(self) -> int:
        """Returns the number of top-level keys."""
        return len(self._counter_dict)

    def __iter__(self) -> Iterator[Hashable]:
        """Returns an iterator over the counter's keys."""
        return iter(self._counter_dict)

    def __str__(self) -> str:
        """Returns a formatted string representation of the counter."""
        return pprint.pformat(self._counter_dict)
