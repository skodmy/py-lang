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


class TimeitDifferenceComputer:
    _setup4second = 'pass'
    _setup4first = 'pass'
    _statements_executor = timeit.timeit
    _times_to_repeat = 10
    _return_full_computation_result = True

    def __init__(
            self,
            setup4second=None, setup4first=None,
            statements_executor=None, times_to_repeat=None, return_full_computation_result=None
    ):
        self.setup4second = setup4second
        self.setup4first = setup4first
        self.statements_executor = statements_executor
        self.times_to_repeat = times_to_repeat
        self.return_full_computation_result = return_full_computation_result

    @property
    def setup4second(self):
        return self._setup4second

    @property
    def setup4first(self):
        return self._setup4first

    @property
    def statements_executor(self):
        return self._statements_executor

    @property
    def times_to_repeat(self):
        return self._times_to_repeat

    @property
    def return_full_computation_result(self):
        return self._return_full_computation_result

    @staticmethod
    def _validate_value4setup(name, value):
        if value is not None:
            if not isinstance(value, str):
                raise TypeError("value for {} must be of a string type, not {}".format(name, value.__class__.__name__))
            return value
        return 'pass'

    @setup4second.setter
    def setup4second(self, value):
        self._setup4second = TimeitDifferenceComputer._validate_value4setup('setup4second', value)

    @setup4first.setter
    def setup4first(self, value):
        self._setup4first = TimeitDifferenceComputer._validate_value4setup('setup4first', value)

    @statements_executor.setter
    def statements_executor(self, value):
        if value is not None:
            if not callable(value):
                raise ValueError("value for statements_executor must be a callable object")
            if value not in (timeit.timeit, timeit.repeat):
                raise ValueError("value for statements_executor must be a timeit.timeit or a timeit.repeat")
            self._statements_executor = value

    @times_to_repeat.setter
    def times_to_repeat(self, value):
        if value is not None:
            if not isinstance(value, int):
                raise TypeError("value for times_to_repeat must be of an integer type")
            if value < 0:
                raise ValueError("value for times_to_repeat must be greater then 0")
        self._times_to_repeat = value

    @return_full_computation_result.setter
    def return_full_computation_result(self, value):
        self._return_full_computation_result = bool(value)

    def compute(self, first_statement, second_statement):
        return compute_timeit_difference(
            first_statement,
            second_statement,
            self.setup4second,
            self.setup4first,
            self.statements_executor,
            self.times_to_repeat,
            self.return_full_computation_result
        )

    def comprint(self, first_statement, second_statement):
        self.compute(first_statement, second_statement)
