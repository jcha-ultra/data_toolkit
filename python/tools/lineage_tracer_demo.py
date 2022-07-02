"""This module demonstrates how to set up the helper functions for the `trace` function in ``data_tracer.py``."""
# %%

import json
from typing import Any, Iterator, Tuple, Union
import pandas as pd
from data_tracer import get_entry, get_value, make_idx_iter, make_loc_iter, trace

@make_idx_iter.register
def _(dataset: pd.DataFrame) -> Iterator:
    """Iterates over all indices for rows in a dataframe."""
    return iter(range(len(dataset)))
# test_make_idx_iter_df = make_idx_iter(pd.DataFrame({'c1': [10, 11, 12], 'c2': [100, 110, 120]}))

@make_loc_iter.register
def _(entry: pd.Series) -> Iterator:
    """Iterates over the names of a pandas Series."""
    return iter(entry.index)
# test_make_loc_iter_series = make_loc_iter(pd.DataFrame({'c1': [10, 11, 12], 'c2': [100, 110, 500]}).iloc[0])

@make_loc_iter.register
def _(entry: dict) -> Iterator:
    """Recursively iterates over a dict and returns the next path where the value is not a dict or list."""
    def _recurse(entry: Union[dict, list], path: list) -> Iterator:
        if isinstance(entry, dict):
            for key, value in entry.items():
                yield from _recurse(value, path + [key])
        elif isinstance(entry, list):
            for idx, value in enumerate(entry):
                yield from _recurse(value, path + [idx])
        else:
            yield path
    return _recurse(entry, [])
# test_make_loc_iter_dict = make_loc_iter({'c1': 10, 'c2': 100, 'c3': {'c3_1': [3, 4, 500]}})

@get_entry.register
def _(dataset: pd.DataFrame, idx: int) -> pd.Series:
    """Returns the row at the given index in a dataframe."""
    return dataset.iloc[idx]
# test_get_entry_df = get_entry(pd.DataFrame({'c1': [10, 11, 12], 'c2': [100, 110, 120]}), 1)

@get_value.register
def _(entry: dict, location: list) -> Any:
    """Returns the value of a dict at the given path by sequentially going down the key list."""
    def _recurse(entry: dict, path: list) -> Any:
        if len(path) == 0:
            return entry
        else:
            return _recurse(entry[path[0]], path[1:])
    return _recurse(entry, location)
# test_get_value_dict = get_value({'c1': 10, 'c2': 100, 'c3': {'c3_1': [3, 4, 500]}}, ['c3', 'c3_1', 0])

@get_value.register
def _(entry: pd.Series, location: str) -> Any:
    """Returns the value of a pandas Series at the given column name."""
    return entry[location]
# test_get_value_series = get_value(pd.DataFrame({'c1': [10, 11, 12], 'c2': [100, 110, 500]}).iloc[0], 'c2')

def identify(lookup_json: 'list[dict]', target_idx: int, target_entry_df: pd.Series) -> 'Tuple[int, dict]':
    """Dummy identification function that just returns the same row in the lookup dataset (a list of dicts) as the index of the target entry.

    Parameters
    ----------
    lookup_json : list[dict]
        The lookup list of dicts.
    target_idx : int
        The index of the target entry in the target dataset.
    target_entry : pd.Series
        The target row.

    Returns
    -------
    Tuple[int, pd.Series]
        The index and the corresponding entry in the lookup list.
    """
    return [(idx, entry) for idx, entry in enumerate(lookup_json) if idx == target_idx][0]
# test_identify = dummy_identify(lookup, 1, target.iloc[1])

target = pd.DataFrame({'c1': [10, 11, 12], 'c2': [100, 110, 500]})
lookup = [{'c1': 10, 'c2': 100}, {'c1': 11, 'c2': 110}, {'c1': 12, 'c2': 120, 'c3': {'c3_1': 500}}]
is_match = lambda x, y, *args: (x == y, 'Placeholder note!')

def main():
    test_trace = trace(target, lookup, identify, is_match)
    print('\ntarget:')
    print(target)
    print('\nlookup:')
    print(json.dumps(lookup, indent=4))
    print('\ntest_trace:')
    print(test_trace)

if __name__ == '__main__':
    main()
# %%
