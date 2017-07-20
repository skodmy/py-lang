import subprocess
from typing import Union, Tuple, List

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


def split2list_of_strings(bts: bytes, sep: Union[bytes, str]= '\n') -> List[str]:
    """
    Splits bytes with a given separator and converts results to stings.
    
    :param bts: the bytes which will be processed.
    :param sep: the separator which will be used for splitting, may be of bytes type or a string.
    :return: a list of strings from the given bytes.
    """
    if not isinstance(bts, bytes):
        raise TypeError("bts argument must be of bytes type, not {}".format(bts.__class__.__name__))
    if not isinstance(sep, (bytes, str)):
        raise TypeError("sep argument must be of bytes type or a string, not {}".format(sep.__class__.__name__))
    if isinstance(sep, bytes):
        return [bt.decode() for bt in bts.split(sep)]
    return bts.decode().split(sep)
