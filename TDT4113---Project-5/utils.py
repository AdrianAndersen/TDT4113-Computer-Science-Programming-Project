""" TDT4113: Project 5 - Keypad """

import os


class Utils:
    """ Utility class, providing generally useful functions """

    @staticmethod
    def clear_terminal():
        """ Clear the terminal, using platform-specific command """

        return os.system("cls" if os.name == "nt" else "clear")
