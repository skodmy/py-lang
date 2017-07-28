from xxxt.core.engine import populate_settings_with_file, execute_all_for_all, explore_dir_for_files, \
    settings, process_all_for_all
from xxxt.core.ngnpartls import execute_all_for_py3impls, explore_dir_py3impls
from xxxt.core.utilities import print_interpreter_exec_name_callback, print_xxxt_filename_callback, \
    print_callback, process_none_results_callback


def main():
    populate_settings_with_file('demo_settings.py')
    executions_results_for_each_interpreter = execute_all_for_all(explore_dir_for_files())
    executions_results_for_third_interpreter = execute_all_for_py3impls(explore_dir_py3impls())
    if settings()['PRINT_EXECUTION_RESULT_ON_CONSOLE']:
        process_all_for_all(
            executions_results_for_each_interpreter,
            print_interpreter_exec_name_callback,
            print_xxxt_filename_callback,
            print_callback,
            process_none_results_callback,
            process_none_results_callback
        )
        process_all_for_all(
            executions_results_for_third_interpreter,
            print_interpreter_exec_name_callback,
            print_xxxt_filename_callback,
            print_callback,
            process_none_results_callback,
            process_none_results_callback
        )


if __name__ == '__main__':
    main()
