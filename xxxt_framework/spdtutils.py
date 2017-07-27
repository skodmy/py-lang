import timeit


def compute_pair_difference(
        first_stmt, sec_stmt,
        stmt_executor=timeit.timeit,
        setup_for_first='pass', setup_for_sec='pass',
        times=10,
        return_full=True
):
    """
    Computes a difference between a pair of stmt_executor calls for a pair of statements.
    May return a tuple with calls results and a difference if return_full is True else return only the difference.
    See also documentation for timeit.timeit and for timeit.repeat.
    
    :param first_stmt: the first statement from the pair for the stmt_executor call.
    :param sec_stmt: the second statement from the pair for the stmt_executor call.
    :param stmt_executor: a callable object that will be used for executing the pair statements.
    :param setup_for_first: a setup for first statement.
    :param setup_for_sec: a setup for second statement.
    :param times: if stmt_executor's value is timeit.repeat then this will be passed to its repeat parameter.
    :param return_full: a boolean flag that indicates to return full result or not.
    :return: depends on ret_full argument's value. If it is True then returns a tuple else a float.
    """
    if not isinstance(first_stmt, str) or not isinstance(sec_stmt, str) or \
            not isinstance(setup_for_first, str) or not isinstance(setup_for_sec, str):
        raise TypeError("statements and setups must be strings")
    if not callable(stmt_executor):
        raise ValueError("stmt_executor value must be a callable object")
    if stmt_executor not in (timeit.timeit, timeit.repeat):
        raise ValueError("stmt_executor value must be a timeit.timeit or a timeit.repeat")
    if stmt_executor == timeit.repeat:
        result_for_first = min(stmt_executor(first_stmt, setup_for_first, repeat=times))
        result_for_second = min(stmt_executor(sec_stmt, setup_for_sec, repeat=times))
    else:
        result_for_first = stmt_executor(first_stmt, setup_for_first)
        result_for_second = stmt_executor(sec_stmt, setup_for_sec)
    difference = result_for_second - result_for_first
    return (result_for_first, result_for_second, difference) if return_full else difference


def compr_pair_difference(
        first_stmt, sec_stmt,
        stmt_executor=timeit.timeit,
        setup_for_first='pass', setup_for_sec='pass',
        times=10,
        return_full=True
):
    """
    Computes and prints a difference between a pair of stmt_executor calls for a pair of statements.
    May return a tuple with calls results and a difference if return_full is True else return only the difference.
    See also documentation for timeit.timeit and for timeit.repeat.

    :param first_stmt: the first statement from the pair for the stmt_executor call.
    :param sec_stmt: the second statement from the pair for the stmt_executor call.
    :param stmt_executor: a callable object that will be used for executing the pair statements.
    :param setup_for_first: a setup for first statement.
    :param setup_for_sec: a setup for second statement.
    :param times: if stmt_executor's value is timeit.repeat then this will be passed to its repeat parameter.
    :param return_full: a boolean flag that indicates to return full result or not.
    :return: depends on ret_full argument's value. If it is True then returns a tuple else a float.
    """
    diff_value = compute_pair_difference(
        first_stmt, sec_stmt, stmt_executor, setup_for_first, setup_for_sec, times, return_full
    )
    if isinstance(diff_value, tuple):
        format_pattern = "{}'s call with {} value: {}".format(stmt_executor.__name__, "'{}'", "{}")
        print(format_pattern.format(sec_stmt, diff_value[1]))
        print(format_pattern.format(first_stmt, diff_value[0]))
        diff_value = diff_value[2]
        print("The value of difference between {} calls with '{}' and '{}' is: {}".format(
            stmt_executor.__name__, first_stmt, sec_stmt, diff_value)
        )
    print("'" + sec_stmt + "' is potentially " +
          ('faster' if diff_value < 0 else 'slower' if diff_value > 0 else 'alternative') +
          " then '" + first_stmt + "'\n"
          )
