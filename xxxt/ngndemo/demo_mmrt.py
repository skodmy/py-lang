from operator import add

from xxxt.utils.forpy3only.mmrtutils import compr_tracemalloc_snapshots, prepare_for_passing, \
    prepare_for_passing_without_kwargs


def create_ints(n: int) -> list:
    return [i for i in range(n)]


def create_tuple_of_ints(n: int) -> tuple:
    return tuple(i for i in range(n))


def create_1000_ints():
    return create_ints(1000)


compr_tracemalloc_snapshots(prepare_for_passing(create_ints, 10, **dict()))

compr_tracemalloc_snapshots(prepare_for_passing_without_kwargs(create_ints, 10))

compr_tracemalloc_snapshots(prepare_for_passing_without_kwargs(create_tuple_of_ints, 10))

compr_tracemalloc_snapshots(create_1000_ints)

compr_tracemalloc_snapshots(prepare_for_passing_without_kwargs(add, 100, 205))
