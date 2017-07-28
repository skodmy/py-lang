import tracemalloc
import functools
from typing import Callable, Any, Union, Tuple, List, Dict


def wrap(callable_from_stdlib: Callable[[Any], Any]) -> Callable[[Any], Any]:
    """
    Creates a dummy wrapper for a callable object from the standard library.
    
    :param callable_from_stdlib: the callable object from the standard library.
    :return: the created wrapper.
    """
    def wrapper(*args, **kwargs):
        return callable_from_stdlib(*args, **kwargs)
    return wrapper

# TODO finish the doc string.
def compare_tracemalloc_snapshots(
        func_leak_mem: Union[Callable[[Any], Any], Tuple[Callable[[Any], Any], Any, Any]],
        cmp_to_key_type='lineno', cmp_to_cumulative=False
) -> List[tracemalloc.StatisticDiff]:
    """
    Calls a given function and takes two tracemalloc snapshots, a one before and a one after a call, 
    then compares them and returns a comparison result object.
    If func_leak_mem is a callable object from the standard library then wraps it by using wrap from this module
    and uses stats_limit value to slice a comparison result list.
    
    :param func_leak_mem: the given function which is leaking memory or 
    a tuple with the function and positional plus keyword arguments for its call.
    :param cmp_to_key_type: a key to group comparison statistics.
    :param cmp_to_cumulative: a comparison cumulative flag.
    :return: the comparison result list of tracemalloc.StatisticDiff objects.
    """
    func_leak_mem_args = tuple()
    func_leak_mem_kwargs = dict()
    if isinstance(func_leak_mem, tuple):
        if not callable(func_leak_mem[0]):
            raise ValueError("first element's value in a func_leak_mem tuple must be a callable object")
        if func_leak_mem[1] is not None:
            if not isinstance(func_leak_mem[1], tuple):
                raise TypeError("func_leak_mem second element must be a tuple")
            func_leak_mem_args = func_leak_mem[1]
        if func_leak_mem[2] is not None:
            if not isinstance(func_leak_mem[2], dict):
                raise TypeError("func_leak_mem third element must be a dictionary")
            func_leak_mem_kwargs = func_leak_mem[2]
        func_leak_mem = func_leak_mem[0]
    elif not callable(func_leak_mem):
        raise ValueError("func_leak_mem's value must be a callable object")
    from inspect import getsourcefile
    try:
        srcfile = getsourcefile(func_leak_mem)
        stats_limit = 0
    except TypeError:
        func_leak_mem = wrap(func_leak_mem)
        srcfile = getsourcefile(func_leak_mem)
        stats_limit = 1
    tracemalloc.start()
    traces_filters = [tracemalloc.Filter(True, srcfile)]
    before_call_snapshot = tracemalloc.take_snapshot().filter_traces(traces_filters)
    func_leak_mem_call_result = func_leak_mem(*func_leak_mem_args, **func_leak_mem_kwargs)
    after_call_snapshot = tracemalloc.take_snapshot().filter_traces(traces_filters)
    tracemalloc.stop()
    del func_leak_mem_call_result
    comparison_result = after_call_snapshot.compare_to(before_call_snapshot, cmp_to_key_type, cmp_to_cumulative)
    return comparison_result[:stats_limit] if stats_limit else comparison_result


def compr_tracemalloc_snapshots(
        func_leak_mem: Union[Callable[[Any], Any], Tuple[Callable[[Any], Any], Any, Any]],
        cmp_to_key_type='lineno', cmp_to_cumulative=False,
        stats_limit=10
) -> None:
    """
    Calls a given function and takes two tracemalloc snapshots, a one before and a one after a call, 
    then compares them and prints comparison statistics limited to stats_limit.
    
    :param func_leak_mem: the given function which is leaking memory or 
    a tuple with the function and positional plus keyword arguments for its call.
    :param cmp_to_key_type: key to group comparison statistics.
    :param cmp_to_cumulative: comparison cumulative flag.
    :param stats_limit: a value to which comparison statistics lines count is limited.
    :return: tracemalloc.StatisticDiff object.
    """
    for stat in compare_tracemalloc_snapshots(func_leak_mem, cmp_to_key_type, cmp_to_cumulative)[:stats_limit]:
        print(stat)


def prepare_for_passing(func: Callable[[Any], Any], *func_args, **func_kwargs) -> Tuple[
    Callable[[Any], Any], Tuple[Any, ...], Dict[str, Any]
]:
    """
    Prepares a given function and its arguments values for passing it 
    as a value of a first argument in compare_tracemalloc_snapshots call.
    
    :param func: the function to be prepared.
    :param func_args: arguments which will be passed to the function call within compare_tracemalloc_snapshots.
    :param func_kwargs: keyword arguments which will be passed to function call within compare_tracemalloc_snapshots.
    :return: a tuple with prepared function and its arguments.
    """
    if not callable(func):
        raise ValueError("func value must be a callable object like (any) -> any")
    return func, func_args, func_kwargs


prepare_for_passing_without_kwargs = functools.partial(prepare_for_passing, **dict())
