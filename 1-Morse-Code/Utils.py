class Utils:
    def clear_terminal(self):
        import os

        return os.system("cls" if os.name == "nt" else "clear")
