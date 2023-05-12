# # `cProfile` is a profiling package included in the Python standard library
# import cProfile

# # demo functions that count up to some number
# def count_up_to(n):
#     for i in range(n): pass

# def foo():
#     count_up_to(100000000)

# def bar():
#     count_up_to(10000000)
#     for i in range(10000000): pass

# def baz():
#     foo()
#     bar()
#     count_up_to(1000000)

# def main():
#     baz()

# cProfile.runctx('main()', globals=globals(), locals=locals())


import cProfile

def main():
    for i in range(100000000): pass
    for i in range(10000000): pass
    for i in range(10000000): pass
    for i in range(1000000): pass

cProfile.runctx('main()', globals=globals(), locals=locals())
