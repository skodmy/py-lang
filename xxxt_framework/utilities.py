from subprocess import run, PIPE

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
        completed_process = run((exec_name, '--version'), stdout=PIPE, stderr=PIPE)
    except FileNotFoundError:
        return False
    if completed_process.returncode == 0:
        return True
    return False