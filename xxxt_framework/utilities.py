import subprocess
from typing import List

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
    if exec_name == '' or exec_name is None:
        raise ValueError('exec_name can not be None or empty string!')
    try:
        completed_process = subprocess.run((exec_name, '--version'), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except FileNotFoundError:
        return False
    if completed_process.returncode == 0:
        return True
    return False


def list_available_interpreters(interpreters_exec_names: List[str] = INTERPRETERS_EXECUTABLES_NAMES) -> List[str]:
    """
    Produces a list of available interpreters.

    :param interpreters_exec_names: list of interpreters executables names.
    :return: 
    """
    if interpreters_exec_names is None:
        raise ValueError("interpreters_exec_names can't be None!")
    return [
        interpreter_exec_name for interpreter_exec_name in interpreters_exec_names
        if is_available(interpreter_exec_name)
    ]
