"""
This module provides a framework for automatic debugging of functions. It includes a decorator `auto_debugging` that wraps a function in an `AutodebuggingFunction` class. The `AutodebuggingFunction` class has methods to call the function, automatically debug it, and retrieve the latest debugged version of the function. The module also includes a demo function to illustrate the usage of the auto_debug decorator.

Example usage:
    @auto_debugging
    def add_failed(a: int, b: int) -> int:
        return a + b + 1

    add_failed.autodebug((1, 2), {}, 3)
    print(add_failed.latest_debugged_func)
"""

import inspect
from typing import Callable, Any, List, Tuple, Dict


def generate_debugged_func(func_def: str, error: Exception) -> str:
    """
    Method to debug a function. This is currently unimplemented.

    Parameters
    ----------
    func_to_debug : Callable
        The function to be debugged.

    Returns
    -------
    Callable
        The debugged version of the function.
    """
    raise NotImplementedError("This function needs to be implemented.")


class AutodebuggingFunction:
    """A class representing a function that can be automatically debugged."""

    def __init__(self, func: Callable[..., Any]) -> None:
        """Initializes a new instance of AutodebuggingFunction."""
        self.func = func
        self.debugged_funcs: List[str] = [
            inspect.cleandoc(inspect.getsource(func)).replace("@auto_debugging\n", "")
        ]

    def __call__(self, *args: Tuple[Any, ...], **kwargs: Dict[str, Any]) -> Any:
        """Calls the function with the specified arguments and keyword arguments."""
        return self.func(*args, **kwargs)

    @property
    def latest_debugged_func(self) -> str:
        """Returns the latest debugged version of the function."""
        return self.debugged_funcs[-1]

    def autodebug(
        self, args: Tuple[Any, ...], kwargs: Dict[str, Any], expected_output: Any
    ) -> None:
        """
        Method to automatically debug the function. It repeatedly runs the latest debugged version of
        the function on the provided arguments and keyword arguments, and asserts that the output matches
        the expected output. If the function throws an error or produces an incorrect output, it debugs the
        function and adds the debugged version to the list of debugged functions.

        Parameters
        ----------
        args : Tuple[Any]
            The positional arguments to pass to the function.
        kwargs : Dict[str, Any]
            The keyword arguments to pass to the function.
        expected_output : Any
            The expected output of the function.

        Returns
        -------
        None
        """
        while True:
            try:
                # Try to run the latest version of the debugged function and check the output.
                # exec(self.latest_debugged_func.replace(self.func.__name__, "func"))
                exec(self.latest_debugged_func)
                output = locals()[self.func.__name__](*args, **kwargs)
                # try:
                #     func(*args, **kwargs)
                # except NameError:
                #     breakpoint()
                # output = func(*args, **kwargs) # pylint: disable=undefined-variable # type: ignore
                assert (
                    output == expected_output
                ), f"The function's output does not match the expected output.\n- Input:`args`: {args}, `kwargs`: {kwargs}\n- Expected Output: {expected_output}\n- Actual Output: {output}"
                # If the function ran successfully and produced the correct output, we can break the loop.
                break
            except Exception as error:
                # If the function threw an error or produced an incorrect output, debug it and add the debugged
                # version to the list.
                print(f"Error occurred: {str(error)}. Debugging function...")
                debugged_func = generate_debugged_func(self.latest_debugged_func, error)
                self.debugged_funcs.append(debugged_func)
                print("Debugged function added to the list.")
                # Print an error message.


def auto_debugging(func: Callable[..., Any]) -> AutodebuggingFunction:
    """
    A decorator for automatic debugging of functions.

    Parameters
    ----------
    func : Callable
        A pure python function to be debugged.

    Returns
    -------
    AutodebuggingFunction
        An AutodebuggingFunction object that runs the function and provides methods for debugging.
    """
    return AutodebuggingFunction(func)


@auto_debugging
def add_passed(a: int, b: int) -> int:
    """Adds two numbers without needing debugging."""
    return a + b


@auto_debugging
def add_failed(a: int, b: int) -> int:
    """Adds two numbers with a bug that needs debugging."""
    return a + b + 1


def demo() -> None:
    """A demo function to show the usage of the auto_debug decorator."""
    add_passed.autodebug((1, 2), {}, 3)
    print(add_passed.latest_debugged_func)

    add_failed.autodebug((1, 2), {}, 3)
    print(add_failed.latest_debugged_func)


if __name__ == "__main__":
    demo()
