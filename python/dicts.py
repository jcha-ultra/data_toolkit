from typing import Union


def flatten_dict(d: 'Union[dict, list[dict]]') -> dict:
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
