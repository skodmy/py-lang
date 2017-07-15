from timeit import timeit

print(timeit('op.add(2, 3)', setup='import operator as op'))

print(timeit('2 + 3'))
