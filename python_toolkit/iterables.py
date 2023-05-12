# basic comprehensions
[i * 2 for i in range(10)] # list
{i * 2 for i in range(10)} # set
(i * 2 for i in range(10)) # generator
{i: i * 2 for i in range(10)} # dictionary

# remove duplicates from iterable
numbers = [1, 2, 3, 3, 4]
list(set(numbers))

# flattening nested iterables
xss = [[1, 2], [3, 4], [5, 6]]
[x for xs in xss for x in xs]
