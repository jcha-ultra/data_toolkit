
from typing import Any, Tuple
import numpy as np
import datetime

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

def is_timezone_offset(dt1: datetime.datetime, dt2: datetime.datetime) -> 'Tuple[bool, int]':
    """Check if one datetime is separated by another by a integer number of hours, and less than a day, and returns the offset. Accurate to the second."""
    diff = dt1 - dt2
    return (diff.components.days == 0 and diff.components.minutes == 0 and diff.components.seconds == 0), diff.components.hours