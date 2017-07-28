from typing import Any

import xxxt.core.engine
import xxxt.core.ngnpartls
import xxxt.core.utilities


class App:
    """
    Class that represents a xxxt app.
    
    """
    def __init__(self, include_py3only=False):
        """
        Initializes App instances.
        
        :param include_py3only: a boolean flag that indicates to include or not python3 only executions.
        """
        xxxt.core.engine.populate_settings_with_file()
        self._settings = xxxt.core.engine.settings()
        self._settings['XXXT_FILES'] = xxxt.core.engine.explore_dir_for_files()
        self._include_py3only = include_py3only
        if self._include_py3only:
            self._settings['XXXT_FILES_FOR_PY3IMPLS'] = xxxt.core.ngnpartls.execute_all_for_py3impls()

    def apply_setting(self, name: str, value: Any) -> bool:
        """
        Applies setting for an app.
        
        :param name: setting's name, must be of type str.
        :param value: setting's value, can be of any type.
        :return: True if setting was applied, False otherwise.
        """
        return xxxt.core.engine.set_setting(name, value, self._settings)

    def run(self) -> None:
        """
        Run the app by calling execute_all_for_all function from xxxt.core 
        and 
        if PRINT_EXECUTION_RESULT_ON_CONSOLE setting is True outputs execution result on console.

        :return: None.
        """
        executions_results = xxxt.core.engine.execute_all_for_all(self._settings['XXXT_FILES'])
        executions_results_for_py3impls = None
        if self._include_py3only:
            executions_results_for_py3impls = xxxt.core.ngnpartls.execute_all_for_py3impls(
                self._settings['XXXT_FILES_FOR_PY3IMPLS']
            )
        if self._settings['PRINT_EXECUTION_RESULT_ON_CONSOLE']:
            xxxt.core.engine.process_all_for_all(
                executions_results,
                xxxt.core.utilities.print_interpreter_exec_name_callback,
                xxxt.core.utilities.print_xxxt_filename_callback,
                xxxt.core.utilities.print_callback,
                xxxt.core.utilities.process_none_results_callback,
                xxxt.core.utilities.process_none_results_callback
            )
            if executions_results_for_py3impls is not None:
                xxxt.core.engine.process_all_for_all(
                    executions_results,
                    xxxt.core.utilities.print_interpreter_exec_name_callback,
                    xxxt.core.utilities.print_xxxt_filename_callback,
                    xxxt.core.utilities.print_callback,
                    xxxt.core.utilities.process_none_results_callback,
                    xxxt.core.utilities.process_none_results_callback
                )
