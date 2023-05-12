from typing import Any, Union, Callable

def search_for_value(data: Union[dict, list], is_value: 'Callable[[Any], bool]') -> 'list[list[str]]':
    """Recursively finds paths to values that match the given value.

    Parameters
    ----------
    data : Union[dict, list]
        The data to search through.
    is_value : 'Callable[[Any], bool]'
        A filter function that determines whether a particular value's path will be returned.
    
    Returns
    -------
    list[list[str]]
        A list of paths to values that match the given value.
    """
    if isinstance(data, dict):
        return [[key] + path for key, val in data.items() for path in search_for_value(val, is_value)]
    elif isinstance(data, list):
        return [[str(i)] + path for i, val in enumerate(data) for path in search_for_value(val, is_value)]
    else:
        return [[]] if is_value(data) else []
# test_search_for_value = search_for_value([{'a': 1, 'b': {'c': 2, 'd': {'e': 3, 'f': {'g': 4, 'h': {'i': 5, 'j': 6}}}}}, {'c': 3}], lambda x: x == 3)

def get_result_paths(paths: 'list[list[str]]', sep: str='.') -> 'list[str]':
    """Converts search result paths from the `search_for_value` function to a list of strings.

    Parameters
    ----------
    paths : list[list[str]]
        The paths to convert.
    sep : str
        The separator to use between path elements.

    Returns
    -------
    list[str]
        The converted paths.
    """
    return [sep.join(path) for path in paths]
# test_get_result_paths = get_result_paths(test_search_for_value)