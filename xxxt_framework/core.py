import os
import subprocess
from typing import Union, Tuple, List, Any, Callable, Dict

__SETTINGS = {
    'ENVIRONMENT': os.name,
    'CURRENT_WORKING_DIRECTORY': os.getcwd(),
    'AVAILABLE_INTERPRETERS_EXECUTABLES_NAMES': ['python3'],
    'XXXT_FILES_NAMES_SUFFIXES': ['spd', ],
    'XXXT_FILES_NAMES_SUFFIXES_ONLY_FOR_THIRD_PYTHON_IMPLEMENTATIONS': ['mmr', ],
    'PRINT_EXECUTION_RESULT_ON_CONSOLE': True,
}


def settings() -> dict:
    """
    Makes and returns a deep copy of a settings dictionary.
    
    :return: the deep copy of the settings dictionary.
    """
    from copy import deepcopy
    return deepcopy(__SETTINGS)


def set_setting(name: str, value: Any, target: dict = None) -> bool:
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


def populate_settings_with_file(filename: str = 'settings.py', directory: str = None) -> None:
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
        raise ValueError("filename's value can't be an empty string!")
    if directory == '':
        raise ValueError("directory's value can't be an empty string!")
    if not filename.endswith('.py'):
        raise ValueError("file with name 'filename' is not a python module!")
    if filename in os.listdir(directory):
        from importlib import import_module
        settings_module = import_module(filename.replace('.py', ''), directory)
        for setting_name in __SETTINGS:
            if hasattr(settings_module, setting_name):
                set_setting(setting_name, getattr(settings_module, setting_name))
    else:
        raise FileNotFoundError("File with a name 'filename' was not found in directory 'directory'")


def explore_dir_for_files(
        directory: str = None,
        only_for_third_python_implementations=False,
        files_names_suffixes: Union[Tuple[str], List[str]] = None
) -> List[str]:
    """
    Explores a directory for files that match filter's condition.
    
    :param directory: the directory which will be explored for files.
    :param only_for_third_python_implementations: a boolean flag which indicates that 
    __SETTINGS['XXXT_FILES_NAMES_SUFFIXES_ONLY_FOR_THIRD_PYTHON_IMPLEMENTATIONS'] value will be used as
    files_names_suffixes value.
    :param files_names_suffixes: a list of suffixes with which should end files in the directory.
    :return: a list of found files.
    """
    if directory is None:
        directory = __SETTINGS['CURRENT_WORKING_DIRECTORY']
    if files_names_suffixes is None:
        if only_for_third_python_implementations:
            files_names_suffixes = __SETTINGS['XXXT_FILES_NAMES_SUFFIXES_ONLY_FOR_THIRD_PYTHON_IMPLEMENTATIONS']
        else:
            files_names_suffixes = __SETTINGS['XXXT_FILES_NAMES_SUFFIXES']
    if not isinstance(directory, str):
        raise TypeError("directory argument must be a string, not {}".format(directory.__class__.__name__))
    if not isinstance(files_names_suffixes, (tuple, list)):
        raise TypeError("files_names_suffixes argument must be a tuple of strings or a list of strings, not {}".format(
            files_names_suffixes.__class__.__name__
        ))
    if directory == '':
        raise ValueError("directory's value can't be an empty string")
    return [
        entry for entry in os.listdir(directory)
        if any([
            entry.endswith('_' + file_name_suffix + 't.py') for file_name_suffix in files_names_suffixes
        ])
    ]


def execute(xxxt_filename: str, interpreter_exec_name: str,
            files_names_suffixes: Union[Tuple[str], List[str]] = None) -> Dict[str, Any]:
    """
    Executes a xxxt file with a given interpreter's executable name.
    
    :param xxxt_filename: a name of the xxxt file.
    :param interpreter_exec_name: interpreter's executable name.
    :param files_names_suffixes: a list of suffixes with which should end each file.
    :return: a dictionary with a result of execution.
    """
    if files_names_suffixes is None:
        files_names_suffixes = __SETTINGS['XXXT_FILES_NAMES_SUFFIXES']
    if not isinstance(xxxt_filename, str):
        raise TypeError("filename argument must be a string, not {}".format(xxxt_filename.__class__.__name__))
    if not isinstance(interpreter_exec_name, str):
        raise TypeError("interpreter_exec_name argument must be a string, not {}".format(
            interpreter_exec_name.__class__.__name__
        ))
    if not isinstance(files_names_suffixes, (tuple, list)):
        raise TypeError("files_names_suffixes argument must be a tuple of strings, a list of strings, not {}".format(
            files_names_suffixes.__class__.__name__
        ))
    if xxxt_filename == '':
        raise ValueError("filename's value can't be an empty string")
    if interpreter_exec_name == '':
        raise ValueError("interpreter_exec_name's value can't be an empty string")
    for suffix in files_names_suffixes:
        if xxxt_filename.endswith('_' + suffix + 't.py'):
            break
    else:
        raise ValueError("Not a xxxt file!")
    execution_result = {
        'status': "FAILURE",
        'output': b"Interpreter's executable not found!"
    }
    try:
        completed_process = subprocess.run(
            (interpreter_exec_name, xxxt_filename), stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        execution_result.update({
            'status': 'SUCCESS' if not completed_process.returncode else 'FAILURE',
            'output': completed_process.stdout if not completed_process.returncode else completed_process.stderr
        })
    except FileNotFoundError:
        pass
    return execution_result


def execute_all(xxxt_filenames: Union[Tuple[str], List[str]], interpreter_exec_name: str,
                files_names_suffixes: Union[Tuple[str], List[str]] = None) -> Dict[str, Dict[str, Any]]:
    """
    Executes all xxxt files with names from a given list for a given interpreter.
    
    :param xxxt_filenames: a list with xxxt filenames.
    :param interpreter_exec_name: name of interpreter's executable.
    :param files_names_suffixes: a list of suffixes with which should end each file.
    :return: a dictionary which describes a status of execution for each xxxt file.
    """
    if not isinstance(xxxt_filenames, (tuple, list)):
        raise TypeError("xxxt_files argument must be a tuple of strings or a list of strings, not {}".format(
            xxxt_filenames.__class__.__name__
        ))
    return {xxxt_filename: execute(xxxt_filename, interpreter_exec_name, files_names_suffixes)
            for xxxt_filename in xxxt_filenames}


def execute_all_for_all(
        xxxt_filenames: List[str],
        interpreters_execs_names: Union[Tuple[str], List[str]] = None,
        only_for_third_python_implementations = False,
        files_names_suffixes: Union[Tuple[str], List[str]] = None
) -> Dict[str, Dict[str, Dict[str, Any]]]:
    """
    Executes all xxxt files with names from a given list for all available interpreters.
    
    :param xxxt_filenames: a list with xxxt filenames.
    :param interpreters_execs_names: a list with interpreters executables names.
    :param files_names_suffixes: a list of suffixes with which should end each file.
    :return: a list of dictionaries which describes a status of execution xxxt files for each available interpreter.
    """
    if interpreters_execs_names is None:
        interpreters_execs_names = __SETTINGS['AVAILABLE_INTERPRETERS_EXECUTABLES_NAMES']
    if not isinstance(interpreters_execs_names, (tuple, list)):
        raise TypeError("interpreters_execs_names argument must be a tuple of strings or list of strings, not {}".
                        format(interpreters_execs_names.__class__.__name__))
    if only_for_third_python_implementations:
        interpreters_execs_names = filter(
            lambda interpreter_exec_name: interpreter_exec_name.find('3') != -1,
            interpreters_execs_names
        )
    return {
        interpreter_exec_name: execute_all(xxxt_filenames, interpreter_exec_name, files_names_suffixes)
        for interpreter_exec_name in interpreters_execs_names
    }


def process(xxxt_file_execution_result: Dict[str, Any], callback: Callable[[Dict[str, Any]], Any]) -> Any:
    """
    Applies callback to a xxxt_file_execution_result and returns it's call result.
    
    :param xxxt_file_execution_result: a dictionary which contains result's data of execution.
    :param callback: a callable like (dict) -> any that will be used to process xxxt file execution result.
    :return: callback's call result.
    """
    if not isinstance(xxxt_file_execution_result, dict):
        raise TypeError("file_execution_result argument must be a dictionary, not {}".format(
            xxxt_file_execution_result.__class__.__name__
        ))
    if not callable(callback):
        raise ValueError("callback's value must be a callable object like (dict) -> any")
    return callback(xxxt_file_execution_result)


def process_all(
        xxxt_files_executions_results: Dict[str, Dict[str, Any]],
        xxxt_filename_callback: Callable[[str], Any],
        process_callback: Callable[[Dict[str, Dict[str, Any]]], Any],
        process_results_callback: Callable[[List[Tuple[Any, Any]]], Any]
) -> Any:
    """
    Applies a callback to each xxxt file execution result in a given dictionary and produces a list of calls results.
    Applies to the list of calls results all_callback and returns it's return value.
    
    :param xxxt_files_executions_results: the dictionary with data of xxxt files executions results.
    :param xxxt_filename_callback: a callable object which will be applied to each xxxt file's name.
    :param process_callback: a callable object which will be applied to each xxxt file execution result.
    :param process_results_callback: a callable object which will be applied to the list of process_callback's calls 
    results.
    :return: process_results_callback's call result.
    """
    if not isinstance(xxxt_files_executions_results, dict):
        raise TypeError("xxxt_files_executions_results argument must be a dictionary, not {}".format(
            xxxt_files_executions_results.__class__.__name__
        ))
    if not callable(xxxt_filename_callback):
        raise ValueError("xxxt_filename_callback's value must be a callable object like (str) -> any")
    if not callable(process_results_callback):
        raise ValueError("process_results_callback's value must be a callable object like (list) -> any")
    return process_results_callback([
        (xxxt_filename_callback(xxxt_filename), process(xxxt_files_executions_results[xxxt_filename], process_callback))
        for xxxt_filename in xxxt_files_executions_results
    ])


def process_all_for_all(
        executions_results_for_each_interpreter: Dict[str, Dict[str, Dict[str, Any]]],
        interpreter_exec_name_callback: Callable[[str], Any],
        xxxt_filename_callback: Callable[[str], Any],
        process_callback: Callable[[Dict[str, Any]], Any],
        process_results_callback: Callable[[List[Tuple[Any, Any]]], Any],
        process_all_results_callback: Callable[[List[Tuple[Any, Any]]], Any]
) -> Any:
    """
    Applies a callback to each xxxt file execution result in a given dictionary and produces a list of calls results.
    Produces a list by applying to the each list of calls results all_callback.
    Then applies to that list for_all_callback and returns it's return value.
    
    :param executions_results_for_each_interpreter: a dictionary with data of executions results for each interpreter.
    :param interpreter_exec_name_callback: a callable object which will be applied to each interpreter's exe name.
    :param xxxt_filename_callback: a callable object which will be applied to each xxxt file's name.
    :param process_callback: a callable object which will be applied to each xxxt file execution result.
    :param process_results_callback: a callable object which will be applied to the list of process_callback's calls 
    results.
    :param process_all_results_callback: a callable object which will be applied to the list produced by a list 
    comprehension and process_results_callback's calls.
    :return: process_all_results_callback's call result.
    """
    if not isinstance(executions_results_for_each_interpreter, dict):
        raise TypeError("executions_results_for_each_interpreter argument must be a dictionary, not {}".format(
            executions_results_for_each_interpreter.__class__.__name__
        ))
    if not callable(interpreter_exec_name_callback):
        raise ValueError("interpreter_exec_name_callback's value must be a callable object like (str) -> any")
    if not callable(process_all_results_callback):
        raise ValueError("process_all_results_callback's value must be a callable object like (any) -> any")
    return process_all_results_callback([
        (
            interpreter_exec_name_callback(interpreter_exec_name),
            process_all(
                executions_results_for_each_interpreter[interpreter_exec_name],
                xxxt_filename_callback,
                process_callback,
                process_results_callback
            )
        )
        for interpreter_exec_name in executions_results_for_each_interpreter
    ])
