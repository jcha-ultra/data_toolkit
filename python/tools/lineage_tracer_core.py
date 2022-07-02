"""
This module provides a lightweight set of hooks for tracing data that exists in one structure (e.g. a pandas DataFrame) to data that exists in another structure (e.g. a JSON file). The former is called the `target` and the latter is called the `lookup`.

The main function is `trace`, which takes two datasets, functions that help to relate data from one dataset to the other, and returns a dataframe of location pairs and indices for matching values at those locations.
It does not work out of the box, and requires some helper functions to be set up to traverse the data in each of the respective structures. 

Helper functions are either set up as cases for generic functions, or as arguments to the `trace` function:
- `make_idx_iter`: a generic function that iterates through the indices of a dataset. This must be defined for the `target` dataset.
- `get_entry`: a generic function that returns the entry at a given index in a dataset. This must be defined for the `target` dataset.
- `make_loc_iter`: a generic function that returns an iterator for the locations within an entry of a dataset. This must be defined for both the `target` dataset and the `lookup` dataset.
- `get_value`: a generic function that returns the value at a given location within an entry of a dataset. This must be defined for both the `target` dataset and the `lookup` dataset.
- `identify`: a function argument for `trace` that returns the index and entry of an entry in the `lookup` dataset that matches the entry in the `target` dataset at a given index.
- `is_match`: a function argument for `trace` that returns whether two values are considered equal.

See ``data_tracer_demo.py`` for examples of how to define these functions.
"""

from functools import singledispatch
from itertools import product
import sys
from typing import Any, Callable, Iterator, Tuple
import pandas as pd

@singledispatch
def make_idx_iter(dataset: Any) -> Iterator:
    """Given a dataset, return an iterator that can be used to iterate over all desired indices in the dataset.
    - This will be used by the `trace` function to navigate across all entries represented by the indices in the dataset.
    - An index is commonly an integer (e.g. a row number in a dataframe), but can be any value that uniquely identifies an entry in the dataset in question, such as a URL.

    Parameters
    ----------
    dataset : Any
        The dataset to be iterated over.

    Returns
    -------
    Iterator
        An iterator that can be used to iterate over all indices in the dataset.
    """
    raise NotImplementedError('make_entry_iterator is not implemented for the given type: {}'.format(type(dataset)))

@singledispatch
def make_loc_iter(entry: Any) -> Iterator:
    """Given an entry, return an iterator that can be used to iterate over all locations in the entry.
    - This will be used by the `trace` function to identify individual values in entries to compare across the datasets.
    - A location should uniquely identify a value in an entry. i.e. given a location and an entry, it must be possible to retrieve the value at that location in the entry.
    - Examples: column names in a dataframe, key paths to values in a dictionary, etc.

    Parameters
    ----------
    entry : Any
        The entry to be iterated over.

    Returns
    -------
    Iterator
        An iterator that can be used to iterate over all locations in the entry.
    """
    raise NotImplementedError('make_location_iterator is not implemented for the given type: {}'.format(type(entry)))

@singledispatch
def get_entry(dataset: Any, idx: Any) -> Any:
    """Given a dataset and an index, return the entry at that index.

    Parameters
    ----------
    dataset : Any
        The dataset to be queried.
    idx : Any
        The index of the entry to be returned.

    Returns
    -------
    Any
        The entry at the given index.
    """
    raise NotImplementedError('`get_entry` is not implemented for the given type: {}'.format(type(dataset)))

@singledispatch
def get_value(entry: Any, location: Any) -> Any:
    """Given an entry and a location, return the value stored at that location.

    Parameters
    ----------
    entry : Any
        The entry to be searched.
    location : Any
        The location where the value is at.

    Returns
    -------
    Any
        The value at the location.
    """
    raise NotImplementedError('`get_value` is not implemented for the given type: {}'.format(type(entry)))

def trace(target: Any, lookup: Any, identify: 'Callable[[Any, Any, Any], Any]', is_match: 'Callable[[Any, Any, Any, Any], Tuple[bool, str]]', analytics: 'list[Callable[[Any, Any, Any, Any], Any]]' ) -> pd.DataFrame:
    """Given two datasets, return a dataframe of location pairs and matching entry numbers for each pair.

    Parameters
    ----------
    target : Any
        The dataset to be traced. All traversible entries in this dataset (defined via the `traverse` function) will be traced.
    lookup : Any
        The dataset where the information in `target` will be looked up.
    identify : Callable[[Any, Any, Any], Any]
        A function that can be used to identify entries from the target dataset with entries in the lookup dataset.
    is_match : Callable[[Any, Any, Any, Any], Tuple[bool, str]]
        A function that can be used to check if the values at two locations are considered equal.
    analytics : list[Callable[[Any, Any, Any, Any], Any]]
        A list of functions that can be used to perform additional analysis on the entries.

    Returns
    -------
    DataFrame
        A dataframe of location pairs and matching entry numbers for each pair.
    """
    matches = pd.DataFrame(columns=['target_location', 'target_idx', 'target_value', 'lookup_location', 'lookup_idx', 'lookup_value', 'note'])
    indices = make_idx_iter(target)
    for target_idx in indices:
        try:
            target_entry = get_entry(target, target_idx)
            lookup_idx, lookup_entry = identify(lookup, target_idx, target_entry)
            target_locations = make_loc_iter(target_entry)
            lookup_locations = make_loc_iter(lookup_entry)
            for target_location, lookup_location in product(target_locations, lookup_locations):
                try:
                    target_value = get_value(target_entry, target_location)
                    lookup_value = get_value(lookup_entry, lookup_location)
                    for analyze in analytics:
                        analyze(target_idx, target_entry, target_location, target_value)
                    has_matched, match_note = is_match(target_value, lookup_value, target_location, lookup_location)
                    if has_matched:
                        matches.loc[len(matches)] = [target_location, target_idx, target_value, lookup_location, lookup_idx, lookup_value, match_note]
                except:
                    print(f"Error: {sys.exc_info()[0]}. {sys.exc_info()[1]}, line: {sys.exc_info()[2].tb_lineno}")
                    print(f"Error tracing lookup location {lookup_location} while on target location {target_location} and index {target_idx}")
        except KeyboardInterrupt:
            print('Data trace interrupted by user. Returning partial results.')
            return matches
        except:
            print(f"Error: {sys.exc_info()[0]}. {sys.exc_info()[1]}, line: {sys.exc_info()[2].tb_lineno}")
            print(f"Error tracing targe entry {target_idx} due to unhandled exception. Skipping.")
    print(f"Successfully found {len(matches)} potential matching values across {len(indices)} entries in the target dataset.")
    return matches

