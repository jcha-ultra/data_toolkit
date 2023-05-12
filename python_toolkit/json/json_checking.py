from typing import Mapping, Sequence


def is_flat(json_dict: dict):
    """Check whether a dictionary represents a flat JSON object."""
    for key, value in json_dict.items():
        if isinstance(value, Mapping, Sequence):
            return False
    return True

