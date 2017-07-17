import xxxt_framework.core


class App:
    """
    Class that represents a xxxt app.

    directory - app's directory.
    settings_filename - a name of a file with settings for the app.
    __settings - a dictionary with settings for the app.
    """
    directory = __file__
    settings_filename = 'settings.py'
    __settings = dict()

    def __init__(self, directory: str = None, settings_filename: str = None):
        if directory is not None:
            self.directory = directory
        if settings_filename is not None:
            self.settings_filename = settings_filename
        xxxt_framework.core.populate_settings_with_file(self.settings_filename, self.directory)
        self.__settings = xxxt_framework.core.settings()
        self.__settings['XXXT_FILES'] = xxxt_framework.core.explore_for_files(self.directory)

    def run(self) -> None:
        """
        Run the app.

        :return: None.
        """
        results = xxxt_framework.core.execute_all_for_all(self.__settings['XXXT_FILES'])
        if self.__settings['DISPLAY_RESULT']:
            for result in results:
                print(result)
