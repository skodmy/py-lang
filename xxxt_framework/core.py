import os
import subprocess
from typing import Union, Tuple, List, Any

__SETTINGS = {
    'ENVIRONMENT': os.name,
    'CURRENT_WORKING_DIRECTORY': os.getcwd(),
    'AVAILABLE_INTERPRETERS_EXECUTABLES_NAMES': ['python3'],
    'XXXT_FILES_NAMES_SUFFIXES': ['spd', 'mmr'],
    'PRINT_EXECUTION_RESULT_ON_CONSOLE': True,
}


def settings() -> dict:
    """
    Makes and returns a deep copy of a settings dictionary.
    
    :return: the deep copy of the settings dictionary.
    """
    from copy import deepcopy
    return deepcopy(__SETTINGS)


def set_setting(name: str, value: Any, target: dict=None) -> bool:
    """
    Apply a setting to the __SETTINGS dictionary.
    
    :param name: setting's name, must be of type str.
    :param value: setting's value, can be of any type.
    :param target: a dictionary which contains settings.
    :return: True if setting was set, False otherwise.
    """
    if target is None:
        target = __SETTINGS
    if not isinstance(target, dict):
        raise TypeError("target must be a dictionary, not {}".format(target.__class__.__name__))
    if name in target and value is not None and value != '':
        target[name] = value
        return True
    return False


def populate_settings_with_file(filename: str= 'settings.py', directory: str=None) -> None:
    """
    Populates __SETTINGS dictionary with pairs defined in a file with a name filename within a directory.
    
    :param filename: the name of the file with settings.
    :param directory: the directory in which the file is located.
    :return: None.
    """
    if directory is None:
        directory = __SETTINGS['CURRENT_WORKING_DIRECTORY']
    if not isinstance(filename, str):
        raise TypeError("filename argument must be a string, not {}".format(filename.__class__.__name__))
    if not isinstance(directory, str):
        raise TypeError("directory argument must be a string, not {}".format(directory.__class__.__name__))
    if filename == '':
        raise ValueError("filename can't be an empty string!")
    if directory == '':
        raise ValueError("directory can't be an empty string!")
    if not filename.endswith('.py'):
        raise ValueError("file is not a python module!")
    if filename in os.listdir(directory):
        from importlib import import_module
        settings_module = import_module(filename.replace('.py', ''), directory)
        for setting_name in __SETTINGS:
            if hasattr(settings_module, setting_name):
                set_setting(setting_name, getattr(settings_module, setting_name))
    else:
        raise FileNotFoundError("File with a name 'filename' was not found in directory 'directory'")


def explore_dir_for_files(directory: str=None, files_names_suffixes: Union[Tuple[str], List[str]]=None) -> List[str]:
    """
    Explores a directory for files that match filter's condition.
    
    :param directory: the directory which will be explored for files.
    :param files_names_suffixes: a list of suffixes with which should end files in the directory.
    :return: a list of found files.
    """
    if directory is None:
        directory = __SETTINGS['CURRENT_WORKING_DIRECTORY']
    if files_names_suffixes is None:
        files_names_suffixes = __SETTINGS['XXXT_FILES_NAMES_SUFFIXES']
    if not isinstance(directory, str):
        raise TypeError("directory argument must be a string, not {}".format(directory.__class__.__name__))
    if not isinstance(files_names_suffixes, (tuple, list)):
        raise TypeError("files_names_suffixes argument must be a tuple of strings or a list of strings, not {}".format(
            files_names_suffixes.__class__.__name__
        ))
    if directory == '':
        raise ValueError("directory value can't be an empty string")
    return [
        entry for entry in os.listdir(directory)
        if any([
            entry.endswith('_' + file_name_suffix + 't.py') for file_name_suffix in files_names_suffixes
        ])
    ]


def execute_xxxt_file(filename: str, interpreter_exec_name: str, files_names_suffixes: Union[Tuple[str],
                                                                                             List[str]]=None) -> dict:
    """
    Executes a xxxt file with a given interpreter's executable name.
    
    :param filename: a name of the xxxt file.
    :param interpreter_exec_name: interpreter's executable name.
    :param files_names_suffixes: a list of suffixes with which should end each file.
    :return: a dictionary with a result of execution.
    """
    if files_names_suffixes is None:
        files_names_suffixes = __SETTINGS['XXXT_FILES_NAMES_SUFFIXES']
    if not isinstance(filename, str):
        raise TypeError("filename argument must be a string, not {}".format(filename.__class__.__name__))
    if not isinstance(interpreter_exec_name, str):
        raise TypeError("interpreter_exec_name argument must be a string, not {}".format(
            interpreter_exec_name.__class__.__name__
        ))
    if not isinstance(files_names_suffixes, (tuple, list)):
        raise TypeError("files_names_suffixes argument must be a tuple of strings, a list of strings, not {}".format(
            files_names_suffixes.__class__.__name__
        ))
    if filename == '':
        raise ValueError("filename value can't be an empty string")
    if interpreter_exec_name == '':
        raise ValueError("interpreter_exec_name value can't be an empty string")
    for suffix in files_names_suffixes:
        if filename.endswith('_' + suffix + 't.py'):
            break
    else:
        raise ValueError("Not a xxxt file!")
    execution_result = {
        'status': "FAILURE",
        'interpreter': interpreter_exec_name,
        'output': b"Interpreter's executable not found!"
    }
    try:
        completed_process = subprocess.run(
            (interpreter_exec_name, filename), stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        execution_result.update({
            'status': 'SUCCESS' if not completed_process.returncode else 'FAILURE',
            'output': completed_process.stdout if not completed_process.returncode else completed_process.stderr
        })
    except FileNotFoundError:
        pass
    return execution_result


def execute_all(xxxt_files: Union[Tuple[str], List[str]], interpreter_exec_name: str,
                files_names_suffixes: Union[Tuple[str], List[str]]=None) -> dict:
    """
    Executes all xxxt files with names from a given list for a given interpreter.
    
    :param xxxt_files: a list with xxxt files names.
    :param interpreter_exec_name: name of interpreter's executable.
    :param files_names_suffixes: a list of suffixes with which should end each file.
    :return: a dictionary which describes a status of execution for each xxxt file.
    """
    if not isinstance(xxxt_files, (tuple, list)):
        raise TypeError("xxxt_files argument must be a tuple of strings or a list of strings, not {}".format(
            xxxt_files.__class__.__name__
        ))
    return {xxxt_file: execute_xxxt_file(xxxt_file, interpreter_exec_name, files_names_suffixes)
            for xxxt_file in xxxt_files}


def execute_all_for_all(xxxt_files: List[str], interpreters_execs_names: Union[Tuple[str], List[str]]=None,
                        files_names_suffixes: Union[Tuple[str], List[str]] = None) -> list:
    """
    Executes all xxxt files with names from a given list for all available interpreters.
    
    :param xxxt_files: a list with xxxt files names.
    :param interpreters_execs_names: a list with interpreters executables names.
    :param files_names_suffixes: a list of suffixes with which should end each file.
    :return: a list of dictionaries which describes a status of execution xxxt files for each available interpreter.
    """
    if interpreters_execs_names is None:
        interpreters_execs_names = __SETTINGS['AVAILABLE_INTERPRETERS_EXECUTABLES_NAMES']
    if not isinstance(interpreters_execs_names, (tuple, list)):
        raise TypeError("interpreters_execs_names argument must be a tuple of strings or list of strings, not {}".
                        format(interpreters_execs_names.__class__.__name__))
    return [
        execute_all(xxxt_files, interpreter_exec_name, files_names_suffixes)
        for interpreter_exec_name in interpreters_execs_names
    ]
