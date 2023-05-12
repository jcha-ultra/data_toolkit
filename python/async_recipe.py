





# https://stackoverflow.com/questions/34377319/combine-awaitables-like-promise-all
# https://stackoverflow.com/questions/43241221/how-can-i-wrap-a-synchronous-function-in-an-async-coroutine
# https://docs.python.org/3/library/asyncio-eventloop.html#asyncio.loop.run_in_executor

# %%




# ....


import asyncio
import functools

def read_io(i):
    print(f'started {i}\n')
    with open('/dev/urandom', 'rb') as f: a = f.read(100000000)
    print(f'finished {i}\n')
    return len(a)

async def read_io_async(i):
    loop = asyncio.get_running_loop()
    result = await loop.run_in_executor(
        None, functools.partial(read_io, i))
    # print(result)

async def main():
    await asyncio.gather(*[read_io_async(i) for i in range(5)])

# await main()
asyncio.run(main())


# > convert this into recipe
# ....

# %%
async def wait_for_count(i): 
    for j in range((i + 1) * 10000000): pass

async def bar(i):
    print('started', i)
    # await asyncio.sleep(1)
    await wait_for_count(i)
    print('finished', i)

async def main():
    await asyncio.gather(*[bar(i) for i in range(2)])


# %%

import asyncio


# async def factorial(name, number):
#     f = 1
#     for i in range(2, number + 1):
#         print(f"Task {name}: Compute factorial({number}), currently i={i}...")
#         await asyncio.sleep(1)
#         f *= i
#     print(f"Task {name}: factorial({number}) = {f}")
#     return f

# async def main():
#     # Schedule three calls *concurrently*:
#     L = await asyncio.gather(
#         factorial("A", 2),
#         factorial("B", 3),
#         factorial("C", 4),
#     )
#     print(L)

# # asyncio.run(main())
# await main()

# Expected output:
#
#     Task A: Compute factorial(2), currently i=2...
#     Task B: Compute factorial(3), currently i=2...
#     Task C: Compute factorial(4), currently i=2...
#     Task A: factorial(2) = 2
#     Task B: Compute factorial(3), currently i=3...
#     Task C: Compute factorial(4), currently i=3...
#     Task B: factorial(3) = 6
#     Task C: Compute factorial(4), currently i=4...
#     Task C: factorial(4) = 24
#     [2, 6, 24]


async def wait_for_count(i): 
    for j in range((i + 1) * 10000000): pass

async def bar(i):
    print('started', i)
    # await asyncio.sleep(1)
    await wait_for_count(i)
    print('finished', i)

async def main():
    await asyncio.gather(*[bar(i) for i in range(2)])

await main()
# asyncio.run(main())

# loop = asyncio.get_event_loop()
# loop.run_until_complete(main())
# loop.close()


# %%

import asyncio
import concurrent.futures

def blocking_io():
    # File operations (such as logging) can block the
    # event loop: run them in a thread pool.
    with open('/dev/urandom', 'rb') as f:
        return f.read(100)

def cpu_bound():
    # CPU-bound operations will block the event loop:
    # in general it is preferable to run them in a
    # process pool.
    return sum(i * i for i in range(10 ** 7))

async def main():
    loop = asyncio.get_running_loop()

    ## Options:

    # 1. Run in the default loop's executor:
    result = await loop.run_in_executor(
        None, blocking_io)
    print('default thread pool', result)

    # # 2. Run in a custom thread pool:
    # with concurrent.futures.ThreadPoolExecutor() as pool:
    #     result = await loop.run_in_executor(
    #         pool, blocking_io)
    #     print('custom thread pool', result)

    # # 3. Run in a custom process pool:
    # with concurrent.futures.ProcessPoolExecutor() as pool:
    #     result = await loop.run_in_executor(
    #         pool, cpu_bound)
    #     print('custom process pool', result)

await main()
# asyncio.run(main())

# %%
