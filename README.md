# dict-counter

This is lightweight Python library for counting occurrences of keys within nested dictionaries. It traverses Mapping types to provide a consolidated count of how many times each key and each branch appears across a dataset.  I created this with a single purpose: to evaluate documents represented as Python dicts, to find the number of keys (and nested key paths) across a dataset, and determine when the keys are always present sometimes present.

It may have other uses, but I'm not clever or creative enough to think of any.

## Usage

The primary interface is the `DictCounter` class. It behaves similarly to a standard mapping but includes specialized methods for accumulating counts from nested data.

### Initializing the Counter

Create an instance with an optional initial dictionary. You can also specify a `nested_count_key` which defaults to `_self`. This key is used at each level of the nested structure to track how many times that specific branch was traversed.

Use `update` to process a single dictionary or `update_many` for an iterable of dictionaries. The library uses a stack-based depth-first search to traverse the input, which avoids recursion depth limits and ensures performance even with deeply nested data.

```python
from dict_counter import DictCounter

counter = DictCounter()

d1 = {"foo": {"bar": None}}
counter.update(d1)

d2 = {"foo": {"baz": None}}
counter.update(d2)

d3 = {"foo": {"bar": None, "quux": None}}
counter.update(d3)
```

#### Accumulation Example

Updating the counter with multiple documents shows how counts are aggregated:

```python
docs = [
    {"foo": {"bar": None}},
    {"foo": {"baz": None}},
    {"foo": {"bar": None, "quux": None}}
]

counter.update_many(docs)
print(counter)
```

**Output:**

```python
{
    'foo': {
        '_self': 3,
        'bar': 2,
        'baz': 1,
        'quux': 1
    }
}
```

As the counter processes data, it increments values for leaf nodes and updates the `_self` count for dictionary nodes. If you pass a second dictionary with the same structure, the counts will accumulate accordingly.

### Accessing Data

`DictCounter` implements the mapping interface, allowing you to use standard dictionary methods like `items()`, `keys()`, and `values()`, as well as bracket notation for access.

```python
print(counter["user"]["_self"])  # Returns the traversal count for the 'user' key
print(len(counter))             # Returns the number of top-level keys
```

## Testing

The project uses `pytest` for verification. If you have the source code locally, you can run the suite through your preferred Python test runner.

```bash
pytest
```

## License

This project is licensed under the Apache License, Version 2.0.
