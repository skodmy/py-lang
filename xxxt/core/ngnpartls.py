from functools import partial
from xxxt.core.engine import explore_dir_for_files, execute_all_for_all


explore_dir_py3impls = partial(explore_dir_for_files, only_for_third_python_implementations=True)


execute_all_for_py3impls = partial(execute_all_for_all, only_for_third_python_implementations=True)
