from xxxt.utils.common import spdtutils

spdtutils.compr_timeit_difference(
    'lst[0]', 'dq[0]',
    setup_for_first='lst = [i for i in range(100)]',
    setup_for_sec='from collections import deque; dq = deque([i for i in range(100)])'
)
