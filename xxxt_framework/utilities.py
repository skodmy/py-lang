import subprocess
from typing import Union, Tuple, List, Dict, Any

INTERPRETERS_EXECUTABLES_NAMES = (
    'python2',
    'python3',
    'pypy',
    'pypy3',
    'jython',
)


def is_available(exec_name: str) -> bool:
    """
    Checks if an executable with a name exec_name is available. 

    :param exec_name: the name of the executable.
    :return: True if it's available, False otherwise.
    """
    if not isinstance(exec_name, str):
        raise TypeError("exec_name argument must be a string, not {}".format(exec_name.__class__.__name__))
    if exec_name == '':
        raise ValueError("exec_name value can't be an empty string")
    try:
        completed_process = subprocess.run((exec_name, '--version'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if completed_process.returncode == 0:
            return True
    except FileNotFoundError:
        pass
    return False


def list_available_interpreters_execs_names(
        interpreters_execs_names: Union[Tuple[str], List[str]]=INTERPRETERS_EXECUTABLES_NAMES
) -> List[str]:
    """
    Produces a list of available interpreters.

    :param interpreters_execs_names: list of interpreters executables names.
    :return: list
    """
    if not isinstance(interpreters_execs_names, (tuple, list)):
        raise TypeError("interpreters_execs_names argument must be a tuple of strings or a list of strings, not {}".
                        format(interpreters_execs_names.__class__.__name__))
    return [
        interpreter_exec_name for interpreter_exec_name in interpreters_execs_names
        if is_available(interpreter_exec_name)
    ]


def split2list_of_strings(src: Union[bytes, str], sep: Union[bytes, str]= '\n') -> Union[List[str], str]:
    """
    Splits bytes by using a given separator and converts results to strings. If src is a string then returns it's value.
    
    :param src: a data source which will be processed.
    :param sep: the separator which will be used for splitting, may be of bytes type or a string.
    :return: a list of strings from the given bytes.
    """
    if not isinstance(src, (bytes, str)):
        raise TypeError("src argument must be of bytes type or a string, not {}".format(src.__class__.__name__))
    if isinstance(src, str):
        return src
    if not isinstance(sep, (bytes, str)):
        raise TypeError("sep argument must be of bytes type or a string, not {}".format(sep.__class__.__name__))
    if isinstance(sep, bytes):
        return [bt.decode() for bt in src.split(sep)]
    return src.decode().split(sep)


def print_callback(xxxt_file_execution_result: Dict[str, Any]) -> None:
    """
    Prints xxxt file execution result on console.
    
    :param xxxt_file_execution_result: a dictionary with execution result of a xxxt file.
    :return: None.
    """
    keys = list(xxxt_file_execution_result.keys())
    for key in keys[:-1]:
        print("{} => {};".format(key, xxxt_file_execution_result[key]))
    print("{}: ".format(keys[-1]))
    for line in split2list_of_strings(xxxt_file_execution_result[keys[-1]]):
        print(">>> {}".format(line))
    print()


def print_xxxt_filename_callback(xxxt_filename: str) -> None:
    """
    
    :param xxxt_filename: 
    :return: 
    """
    print("file: '{}';".format(xxxt_filename))


def print_interpreter_exec_name_callback(interpreter_exec_name: str) -> None:
    """
    
    :param interpreter_exec_name: 
    :return: 
    """
    sep_line = "#" * 100
    print(sep_line, "interpreter: {}".format(interpreter_exec_name).upper(), sep_line)


def process_none_results_callback(results_list: List[Tuple[None, None]]) -> None:
    """
    Deletes reference on unnecessary list of tuples like (None, None).
    
    :param results_list: 
    :return: None.
    """
    if not isinstance(results_list, list):
        raise TypeError(" argument must be a list of tuples, not {}".format(results_list.__class__.__name__))
    del results_list
