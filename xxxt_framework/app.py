import xxxt_framework.core
import xxxt_framework.utilities
from typing import Any


class App:
    """
    Class that represents a xxxt app.
    
    """
    def __init__(self):
        xxxt_framework.core.populate_settings_with_file()
        self._settings = xxxt_framework.core.settings()
        self._settings['XXXT_FILES'] = xxxt_framework.core.explore_dir_for_files()
        print(self._settings)

    def apply_setting(self, name: str, value: Any) -> bool:
        """
        Applies setting for an app.
        
        :param name: setting's name, must be of type str.
        :param value: setting's value, can be of any type.
        :return: True if setting was applied, False otherwise.
        """
        return xxxt_framework.core.set_setting(name, value, self._settings)

    def run(self) -> None:
        """
        Run the app by calling execute_all_for_all function from xxxt_framework.core 
        and 
        if PRINT_EXECUTION_RESULT_ON_CONSOLE setting is True outputs execution result on console.

        :return: None.
        """
        results = xxxt_framework.core.execute_all_for_all(self._settings['XXXT_FILES'])
        if self._settings['PRINT_EXECUTION_RESULT_ON_CONSOLE']:
            xxxt_framework.core.process_all_for_all(
                results,
                xxxt_framework.utilities.print_interpreter_exec_name_callback,
                xxxt_framework.utilities.print_xxxt_filename_callback,
                xxxt_framework.utilities.print_callback,
                xxxt_framework.utilities.process_none_results_callback,
                xxxt_framework.utilities.process_none_results_callback
            )
