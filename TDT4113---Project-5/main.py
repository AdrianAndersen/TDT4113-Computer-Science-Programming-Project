""" TDT4113: Project 5 - Keypad """

from fsm import FSM
from logger.Logger import Logger
from rule import Rule


class Main:
    """ Main class """
    __logger = Logger()

    def __init__(self):
        self.__logger.clear_logs()

    def main(self):
        """ Main program method """
        # $ - numbers [0-9]
        # ¤ - LED IDs [0-5]
        # @ - any character
        rules = [
            Rule("init", "read", "@", "A1"),
            Rule("read", "read", "$", "A2"),
            Rule("read", "verify", "*", "A3"),
            Rule("read", "init", "@", "A4"),
            Rule("verify", "active", "Y", "A5"),
            Rule("verify", "init", "N"),
            Rule("active", "read-2", "*"),
            Rule(
                "active", "duration-entry", "¤", "A9"
            ),  # WARNING: only 0-5 work, 6-9 crash
            Rule("active", "logout", "#"),
            Rule("read-2", "read-2", "$", "A2"),
            Rule("read-2", "read-3", "*", "A7"),
            Rule("read-2", "active", "@", "A6"),
            Rule("read-3", "read-3", "$", "A2"),
            Rule("read-3", "active", "*", "A8"),
            Rule("read-3", "active", "@", "A6"),
            Rule("duration-entry", "duration-entry", "$", "A10"),
            Rule("duration-entry", "active", "*", "A11"),
            Rule("logout", "init", "#", "A12"),
            Rule("logout", "active", "@"),
        ]
        fsm = FSM()
        fsm.set_rules(rules)
        fsm.run()


if __name__ == "__main__":
    try:
        Main().main()
    except KeyboardInterrupt:
        pass
