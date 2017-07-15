from os import name as __os_name, listdir as __ls_dir
from subprocess import run as __run, PIPE as __PIPE
from typing import List, Any

__SETTINGS = {
    'ENVIRONMENT': __os_name,
    'INTERPRETERS_EXECUTABLES_NAMES': [
        'python2',
        'python3',
        'pypy',
        'pypy3',
        'jython',
    ],
    'AVAILABLE_INTERPRETERS': [],
    'XXXT_FILES_SUFFIXES': ['spd', 'mmr'],
    'DISPLAY_RESULT': True,
    'WRITE_RESULT_TO_FILE': False,
    'RESULT_FILE_EXTENSION': 'txt',
    'RESULTS_FILES_MAP': dict(),
}


def settings() -> dict:
    """
    Makes and returns a deep copy of a settings dictionary.
    
    :return: the deep copy of the settings dictionary.
    """
    from copy import deepcopy
    return deepcopy(__SETTINGS)


def set_setting(name: str, value: Any) -> bool:
    """
    Apply a setting to the __SETTINGS dictionary.
    
    :param name: setting's name, must be of str type.
    :param value: setting's value, can be of any type.
    :return: True if applied successfully, False otherwise.
    """
    if name in __SETTINGS:
        __SETTINGS[name] = value
        return True
    return False


def populate_settings_with_file(filename: str= 'settings.py', directory: str= '.') -> None:
    """
    Populates __SETTINGS dictionary with pairs defined in a file with a name filename within a directory.
    
    :param filename: the name of the file with settings.
    :param directory: the directory in which the file is located.
    :return: None.
    """
    if filename is None:
        raise ValueError("filename can't be None!")
    if directory is None:
        raise ValueError("directory can't be None!")
    if filename == '':
        raise ValueError
    if not filename.endswith('.py'):
        raise ValueError
    if directory == '':
        raise ValueError
    if filename in __ls_dir(directory):
        from importlib import import_module
        settings_module = import_module(filename)
        for setting_name in __SETTINGS:
            if hasattr(settings_module, setting_name):
                set_setting(setting_name, getattr(settings_module, setting_name))


def is_available(exec_name: str) -> bool:
    """
    Checks if an executable with a name exec_name is available. 
    
    :param exec_name: the name of the executable.
    :return: True if it's available, False otherwise.
    """
    if exec_name == '' or exec_name is None:
        raise ValueError('exec_name can not be None or empty string!')
    try:
        completed_process = __run((exec_name, '--version'), stdout=__PIPE, stderr=__PIPE)
    except FileNotFoundError:
        return False
    if completed_process.returncode == 0:
        return True
    return False


def list_available_interpreters(interpreters_exec_names: List[str] = None) -> List[str]:
    """
    Produces a list of available interpreters.
    
    :param interpreters_exec_names: list of interpreters executables names.
    :return: 
    """
    if interpreters_exec_names is None:
        interpreters_exec_names = __SETTINGS['INTERPRETERS_EXECUTABLES_NAMES']
    return [
        interpreter_exec_name for interpreter_exec_name in interpreters_exec_names
        if is_available(interpreter_exec_name)
    ]


def list_files_names(interpret_names: List[str]) -> List[str]:
    """
    Produces a list of files names for results.
    
    :param interpret_names: 
    :return: 
    """
    if interpret_names is None or len(interpret_names) == 0:
        raise ValueError
    return [name + '.txt' for name in interpret_names]


def explore_for_files(directory: str='.') -> List[str]:
    """
    Explores a directory for files that match filter's condition.
    
    :param directory: the directory which will be explored for files.
    :return: a list of found files.
    """
    return [
        entry for entry in __ls_dir(directory)
        if any([
            entry.endswith(suffix) for suffix in __SETTINGS['XXXT_FILES_SUFFIXES']
        ])
    ]


def execute_xxxt_file(filename: str, interpreter_exec_name: str) -> int:
    """
    Executes a xxxt file with a given interpreter's executable name.
    
    :param filename: name of the xxxt file.
    :param interpreter_exec_name: 
    :return: 
    """
    if filename is None or filename == '':
        raise ValueError
    if not filename.endswith('_test.py'):
        raise ValueError
    return __run((interpreter_exec_name, filename), stdout=__PIPE, stderr=__PIPE).returncode


def execute_all(xxxt_files: List[str], interpreter_exec_name: str) -> dict:
    """
    Executes all xxxt files with names from a given list.
    
    :param xxxt_files: a list with xxxt files names.
    :param interpreter_exec_name: name of interpreter's executable.
    :return: a dictionary which describes a status of execution for each xxxt file.
    """
    if xxxt_files is None:
        raise ValueError("xxxt_files can't be None!")
    if interpreter_exec_name is None:
        raise ValueError("interpreter_exec_name can't be None!")
    return {xxxt_file: execute_xxxt_file(xxxt_file, interpreter_exec_name) for xxxt_file in xxxt_files}