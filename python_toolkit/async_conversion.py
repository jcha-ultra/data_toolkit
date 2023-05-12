"""
This recipe demonstrates how to convert a sync function to an async one that can be awaited via asyncio.
"""

import asyncio, functools, concurrent.futures
from typing import Callable, Union

def to_async(f: Callable, pool: 'Union[concurrent.futures.ThreadPoolExecutor, concurrent.futures.ProcessPoolExecutor]'=None):
    """
    Converts a sync function `f` to an async function. 

    If a pool is not specified, the default for the event loop will be used.
    """
    @functools.wraps(f)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(
            pool, functools.partial(f, *args, **kwargs))
        return result
    return wrapper

@to_async
def io_op(i):
    """Runs a long IO operation."""
    print(f'\nstarted `io_op({i})`')
    with open('/dev/urandom', 'rb') as f: a = f.read(100000000)
    print(f'\nfinished `io_op({i})`')

async def main():
    """
    Runs `io_op` in non-blocking threads.
    
    The result looks like the following:
        started `io_op(0)`
        started `io_op(1)`
        started `io_op(2)`
        started `io_op(3)`
        started `io_op(4)`

        finished `io_op(2)`
        finished `io_op(0)`
        finished `io_op(4)`
        finished `io_op(1)`
        finished `io_op(3)`

    Note that the individual calls of `io_op` do not block each other from starting.
    """
    await asyncio.gather(*[io_op(i) for i in range(5)])

if __name__ == '__main__':
    asyncio.run(main())
    # await main() # use this instead when running in Jupyter
