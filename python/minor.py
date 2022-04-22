from typing import Any, Tuple, Callable
import numpy as np
import pandas as pd

def is_number(n: Any) -> bool:
    """Check if value is convertible to a number."""
    try:
        int(n)
        return True
    except ValueError:
        return False

def is_ten_power(x, y) -> bool:
    """Check if one number if off by a factor of 10, 100, etc."""
    if is_number(x) and is_number(y) and float(x)!=0 and float(y)!=0:
        return np.log10(np.abs(float(x)/float(y)))%1 == 0

def is_datetime(dt: Any) -> bool:
    """Check if value is convertible to a datetime."""
    try:
        pd.to_datetime(dt)
        return True
    except ValueError:
        return False

def is_timezone_offset(dt1: pd.Timestamp, dt2: pd.Timestamp) -> 'Tuple[bool, int]':
    """Check if one datetime is separated by another by a integer number of hours, and less than a day, and returns the offset."""
    diff = dt1.replace(tzinfo=None) - dt2.replace(tzinfo=None)
    hours_diff = diff.total_seconds() / 3600
    is_offset = hours_diff % 1 == 0 and np.abs(hours_diff) < 24
    return is_offset
# test_is_timezone_offset = is_timezone_offset(pd.to_datetime('2020-01-01T00:00:00+00:00'), pd.to_datetime('2020-01-01T00:00:00+00:00'))

def is_same_up_to(x: float, y: float, n: int) -> bool:
    """Check if two numbers are the same up to a certain number of decimal places."""
    return np.round(x, n) == np.round(y, n)