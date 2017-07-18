import os
import subprocess
from typing import List, Any

__SETTINGS = {
    'ENVIRONMENT': os.name,
    'AVAILABLE_INTERPRETERS_EXECUTABLES_NAMES': ['python3'],
    'XXXT_FILES_NAMES_SUFFIXES': ['spd', 'mmr'],
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
    if filename in os.listdir(directory):
        from importlib import import_module
        settings_module = import_module(filename.replace('.py', ''), directory)
        for setting_name in __SETTINGS:
            if hasattr(settings_module, setting_name):
                set_setting(setting_name, getattr(settings_module, setting_name))


def list_files_names(interpreters_execs_names: List[str]) -> List[str]:
    """
    Produces a list of files names for results.
    
    :param interpreters_execs_names: 
    :return: 
    """
    if interpreters_execs_names is None or len(interpreters_execs_names) == 0:
        raise ValueError
    return [interpreter_name + '.txt' for interpreter_name in interpreters_execs_names]


def explore_for_files(directory: str='.', files_names_suffixes: List[str]=None) -> List[str]:
    """
    Explores a directory for files that match filter's condition.
    
    :param directory: the directory which will be explored for files.
    :param files_names_suffixes: a list of suffixes with which should end files in the directory.
    :return: a list of found files.
    """
    if files_names_suffixes is None:
        files_names_suffixes = __SETTINGS['XXXT_FILES_NAMES_SUFFIXES']
    return [
        entry for entry in os.listdir(directory)
        if any([
            entry.endswith('_' + file_name_suffix + 't.py') for file_name_suffix in files_names_suffixes
        ])
    ]


def execute_xxxt_file(filename: str, interpreter_exec_name: str, files_names_suffixes: List[str]=None) -> dict:
    """
    Executes a xxxt file with a given interpreter's executable name.
    
    :param filename: a name of the xxxt file.
    :param interpreter_exec_name: interpreter's executable name.
    :param files_names_suffixes: a list of suffixes with which should end file.
    :return: a dictionary with a result of execution.
    """
    if filename is None or filename == '':
        raise ValueError
    if files_names_suffixes is None:
        files_names_suffixes = __SETTINGS['XXXT_FILES_NAMES_SUFFIXES']
    for suffix in files_names_suffixes:
        if filename.endswith('_' + suffix + 't.py'):
            break
    else:
        raise ValueError("Not a xxxt file!")
    completed_process = subprocess.run((interpreter_exec_name, filename), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return {
        'status': 'SUCCESS' if not completed_process.returncode else 'FAILURE',
        'interpreter': interpreter_exec_name,
        'output': completed_process.stdout if not completed_process.returncode else completed_process.stderr
    }


def execute_all(xxxt_files: List[str], interpreter_exec_name: str) -> dict:
    """
    Executes all xxxt files with names from a given list for a given interpreter.
    
    :param xxxt_files: a list with xxxt files names.
    :param interpreter_exec_name: name of interpreter's executable.
    :return: a dictionary which describes a status of execution for each xxxt file.
    """
    if xxxt_files is None:
        raise ValueError("xxxt_files can't be None!")
    if interpreter_exec_name is None:
        raise ValueError("interpreter_exec_name can't be None!")
    return {xxxt_file: execute_xxxt_file(xxxt_file, interpreter_exec_name) for xxxt_file in xxxt_files}


def execute_all_for_all(xxxt_files: List[str], interpreters_execs_names: List[str]=None) -> list:
    """
    Executes all xxxt files with names from a given list for all available interpreters.
    
    :param xxxt_files: a list with xxxt files names.
    :param interpreters_execs_names: a list with interpreters executables names.
    :return: a list of dictionaries which describes a status of execution xxxt files for each available interpreter.
    """
    if interpreters_execs_names is None:
        interpreters_execs_names = __SETTINGS['AVAILABLE_INTERPRETERS_EXECUTABLES_NAMES']
    return [
        execute_all(xxxt_files, interpreter_exec_name) for interpreter_exec_name in interpreters_execs_names
    ]
