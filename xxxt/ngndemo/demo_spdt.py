import timeit

from xxxt.utils.common.spdtutils import compr_timeit_difference

compr_timeit_difference(
    "25 + 352", "op.add(25, 352)",
    stmt_executor=timeit.repeat,
    setup_for_sec="import operator as op"
)

compr_timeit_difference('258 ** 2', '258 * 258')

compr_timeit_difference('258 ** 3', '258 * 258 * 258')
