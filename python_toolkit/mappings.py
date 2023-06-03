from typing import Any, Union


def flatten_dict(d: "Union[dict, list[dict]]") -> dict:
    """
    Flatten a dictionary or list of dictionaries so that all keys are tuples at the top level.

    >>> flatten_dict({'a': 3, 'b': [1, 2, 3], 'c': {'d': 3}})
    {('a',): 3, ('b', 0): 1, ('b', 1): 2, ('b', 2): 3, ('c', 'd'): 3}
    """
    result = {}
    items = ()
    if isinstance(d, dict):
        items = d.items()
    if isinstance(d, list):
        items = enumerate(d)
    for k, v in items:
        if isinstance(v, (dict, list)):
            result.update({(k, *subk): subv for subk, subv in flatten_dict(v).items()})
        else:
            result[(k,)] = v
    return result


def get_key_value(vals: "Union[dict, list, tuple]", key_path: tuple) -> Any:
    """
    Get a value from a nested dictionary, list, or tuple at a certain path.

    >>> get_key_value({'a': 1, 'b': [2, 3, 4], 'c': {'d': 5}}, ('c', 'd'))
    5
    """
    if not key_path:
        return vals
    try:
        return get_key_value(vals[key_path[0]], key_path[1:])
    except (KeyError, IndexError):
        return None


# use `defaultdict` to create a dictionary with default values
from collections import defaultdict

d = defaultdict(list)
# since the default value here is a list, you can append to it without explicitly creating an empty list first
d["a"].append(1)
d["a"].append(2)
print(d)  # defaultdict(<class 'list'>, {'a': [1, 2]})
