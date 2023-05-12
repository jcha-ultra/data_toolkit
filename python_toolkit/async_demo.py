

#%% Synchronous function example

import time

def sync_return_after_5(val): 
    time.sleep(5)
    print('waited for 5 seconds')
    return val

def main():
    x = sync_return_after_5('foo') # waits for 5 seconds before assigning `x` to the return value
    print('x:', x) # prints out "foo", which is the value of `x`

main()

#%% Asynchronous function example

import time, asyncio

async def async_return_after_5(val):
    time.sleep(5)
    print('waited for 5 seconds')
    return val

async def main():
    y = async_return_after_5('bar') # does NOT wait for 5 seconds before assigning `y`
    print('y before await:', y) # prints out an Awaitable object
    y = await y # now waits until the `Awaitable` has resolved
    print('y after await:', y)

asyncio.run(main())

# %%

import time
import random

random.seed(0)

def send_request(req_num):
    """Simulates sending a request and waiting for a response."""
    print('Sent request number:', req_num)
    time.sleep(random.random())
    res = f"response_{req_num}"
    print('Received response for request number:', req_num)
    return res

def process_response(res, req_num):
    """Simulates processing a response by concatenating a string to it."""
    result = f"processed_{res}"
    print('Processed result for request number:', req_num)
    return result

def get_result(num):
    """Requests data for and then processes a result."""
    response = send_request(num)
    result = process_response(response, num)
    return result

def main():
    """Synchronously sends 20 requests, processes the responses, and saves the responses"""
    time_start = time.perf_counter()
    results = []
    for i in range(20):
        result = get_result(i)
        results.append(result)
    print('\nResults:')
    print(results)
    total_time = time.perf_counter() - time_start
    print('\nTotal Time:', total_time)
main()

# %%


import time, random
import asyncio, functools
from typing import Callable

random.seed(0)

def to_async(f: Callable):
    """
    Converts a sync function `f` to an async function. 

    If a pool is not specified, the default for the event loop will be used.
    """
    @functools.wraps(f)
    async def wrapper(*args, **kwargs):
        loop = asyncio.get_running_loop()
        result = await loop.run_in_executor(
            None, functools.partial(f, *args, **kwargs))
        return result
    return wrapper

@to_async
def send_request(req_num):
    """Simulates sending a request and waiting for a response."""
    print('Sent request number:', req_num)
    time.sleep(random.random())
    response = f"response_{req_num}"
    print('Received response for request number:', req_num)
    return response

def process_response(response, req_num):
    """Simulates processing a response by concatenating a string to it."""
    result = f"processed_{response}"
    print('Processed result for request number:', req_num)
    return result

async def get_result(num):
    """Requests data for and then processes a result."""
    response = await send_request(num)
    result = process_response(response, num)
    return result

async def main():
    """Sends 20 requests, processes the responses, and saves the responses"""
    time_start = time.perf_counter()
    results = []
    for i in range(20):
        result = get_result(i)
        results.append(result)
    results = await asyncio.gather(*results) # `gather` waits for all of its arguments to resolve
    print('\nResults:')
    print(results)
    total_time = time.perf_counter() - time_start
    print('Total Time:', total_time)
await main()
