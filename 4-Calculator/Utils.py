import os


class Utils:
    def clear_terminal(self):

        return os.system("cls" if os.name == "nt" else "clear")
