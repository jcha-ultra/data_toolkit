"""
Examples of getting memory information.
"""
import sys

# get id of an object
print(id("hello"))

# get size of an object in memory in bytes
print(sys.getsizeof("hello"))
