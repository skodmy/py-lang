import timeit


def compute_timeit_difference(
        first_stmt, sec_stmt,
        setup_for_sec='pass', setup_for_first='pass',
        stmts_executor=timeit.timeit,
        times_to_repeat=10,
        return_full=True
):
    """
    Computes a difference between a pair of stmt_executor calls for a pair of statements.
    May return a tuple with calls results and a difference if return_full is True else return only the difference.
    See also documentation for timeit.timeit and for timeit.repeat.
    
    :param first_stmt: the first statement from the pair for the stmt_executor call.
    :param sec_stmt: the second statement from the pair for the stmt_executor call.
    :param setup_for_sec: a setup for second statement.
    :param setup_for_first: a setup for first statement.
    :param stmts_executor: a callable object that will be used for executing the pair statements.
    :param times_to_repeat: if stmt_executor's value is timeit.repeat then this will be passed to its repeat parameter.
    :param return_full: a boolean flag that indicates to return full result or not.
    :return: depends on ret_full argument's value. If it is True then returns a tuple else a float.
    """
    if not isinstance(first_stmt, str) or not isinstance(sec_stmt, str) or \
            not isinstance(setup_for_first, str) or not isinstance(setup_for_sec, str):
        raise TypeError("statements and setups must be strings")
    if not callable(stmts_executor):
        raise ValueError("stmts_executor value must be a callable object")
    if stmts_executor not in (timeit.timeit, timeit.repeat):
        raise ValueError("stmts_executor value must be a timeit.timeit or a timeit.repeat")
    if not isinstance(times_to_repeat, int):
        raise TypeError("times_to_repeat must be an integer, not {}".format(times_to_repeat.__class__.__name__))
    if times_to_repeat < 0:
        raise ValueError("times_to_repeat's value must be greater then 0")
    if stmts_executor == timeit.repeat:
        result_for_first = min(stmts_executor(first_stmt, setup_for_first, repeat=times_to_repeat))
        result_for_second = min(stmts_executor(sec_stmt, setup_for_sec, repeat=times_to_repeat))
    else:
        result_for_first = stmts_executor(first_stmt, setup_for_first)
        result_for_second = stmts_executor(sec_stmt, setup_for_sec)
    difference = result_for_second - result_for_first
    return (result_for_first, result_for_second, difference) if return_full else difference


def compr_timeit_difference(
        first_stmt, sec_stmt,
        setup_for_sec='pass', setup_for_first='pass',
        stmts_executor=timeit.timeit,
        times_to_repeat=10,
        return_full=True
):
    """
    Computes and prints a difference between a pair of stmt_executor calls for a pair of statements.
    May return a tuple with calls results and a difference if return_full is True else return only the difference.
    See also documentation for timeit.timeit and for timeit.repeat.

    :param first_stmt: the first statement from the pair for the stmt_executor call.
    :param sec_stmt: the second statement from the pair for the stmt_executor call.
    :param setup_for_sec: a setup for second statement.
    :param setup_for_first: a setup for first statement.
    :param stmts_executor: a callable object that will be used for executing the pair statements.
    :param times_to_repeat: if stmt_executor's value is timeit.repeat then this will be passed to its repeat parameter.
    :param return_full: a boolean flag that indicates to return full result or not.
    :return: depends on ret_full argument's value. If it is True then returns a tuple else a float.
    """
    diff_value = compute_timeit_difference(
        first_stmt, sec_stmt, setup_for_sec, setup_for_first, stmts_executor, times_to_repeat, return_full
    )
    if isinstance(diff_value, tuple):
        format_pattern = "{}'s call with {} value: {}".format(stmts_executor.__name__, "'{}'", "{}")
        print(format_pattern.format(first_stmt, diff_value[0]))
        print(format_pattern.format(sec_stmt, diff_value[1]))
        diff_value = diff_value[2]
        print("The value of difference between {} calls with '{}' and '{}' is: {}".format(
            stmts_executor.__name__, first_stmt, sec_stmt, diff_value)
        )
    print("'" + sec_stmt + "' is potentially " +
          ('faster' if diff_value < 0 else 'slower' if diff_value > 0 else 'alternative') +
          " then '" + first_stmt + "'\n"
          )


class TimeitDifferenceComputationModel(object):
    first_statement = 'pass'
    second_statement = 'pass'
    setup4second = 'pass'
    setup4first = 'pass'
    statements_executor = 'timeit'
    times_to_repeat = 10
    return_full_computation_result = True

    def __prepare_and_pack_args(self, first_statement, second_statement):
        return (
            first_statement if first_statement is not None else self.first_statement,
            second_statement if second_statement is not None else self.second_statement,
            self.setup4second,
            self.setup4first,
            timeit.repeat if self.statements_executor == 'repeat' else timeit.timeit,
            self.times_to_repeat,
            self.return_full_computation_result
        )

    def compute(self, first_statement=None, second_statement=None):
        return compute_timeit_difference(*self.__prepare_and_pack_args(first_statement, second_statement))

    def comprint(self, first_statement=None, second_statement=None):
        compr_timeit_difference(*self.__prepare_and_pack_args(first_statement, second_statement))
