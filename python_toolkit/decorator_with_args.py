"""Demonstrates a parameterized decorator."""

from functools import wraps
from typing import Callable


def decorator_with_args(arg1, arg2):
    def decorator_factory(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(f"Decorator arguments: {arg1}, {arg2}")
            print("Before function call")
            result = func(*args, **kwargs)
            print("After function call")
            return result

        return wrapper

    return decorator_factory


@decorator_with_args("arg1 value", "arg2 value")
def my_function(a, b):
    print(f"Function called with arguments: {a}, {b}")
    return a + b


result = my_function(3, 5)
print(f"Result: {result}")
