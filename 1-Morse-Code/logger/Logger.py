import os
from datetime import datetime


class Logger:
    __logs_folder = "logs"
    __log_levels = ["critical", "error", "warning", "info", "debug"]

    # The log levels to be displayed to the console
    __console_log_levels = ["info"]

    def __init__(self):
        if not os.path.exists(self.__logs_folder):
            os.makedirs(self.__logs_folder)

    def __write(self, message, path):
        f = open(path, "a")
        f.write(message)
        f.close()

    def __create_log_entry(self, message, log_level):
        now = datetime.now()
        log_prefix = f'[{now.strftime("%d/%m/%Y %H:%M:%S")}] {log_level.upper()}: '
        log_suffix = "\n"
        return log_prefix + message + log_suffix

    def __log(self, message, log_level):
        log_entry = self.__create_log_entry(message, log_level)
        if log_level in self.__console_log_levels:
            print(log_entry)

        return self.__write(log_entry, self.__logs_folder + f"/{log_level}.txt")

    def clear_logs(self):
        for log_level in self.__log_levels:
            open(self.__logs_folder + f"/{log_level}.txt", "w").close()

    def critical(self, message):
        return self.__log(message, "critical")

    def error(self, message):
        return self.__log(message, "error")

    def warning(self, message):
        return self.__log(message, "warning")

    def info(self, message):
        return self.__log(message, "info")

    def debug(self, message):
        return self.__log(message, "debug")
