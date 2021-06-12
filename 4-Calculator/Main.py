import sys

from Calculator import Calculator
from InputHelper import InputHelper
from logger.Logger import Logger
from TestHandler import TestHandler


class Main:
    __logger = Logger()

    def __init__(self):
        self.__logger.clear_logs()

    def main(self):
        command_helper = InputHelper(["calc", "test", "exit"])
        try:
            next_command = command_helper.get_legal_input("Please enter a command: \n")
            if next_command == "test":
                test_handler = TestHandler()
                test_handler.run()
                pass
            if next_command == "calc":
                calc = Calculator()
                calc.calculate_expression(
                    input("Enter an expression to be calculated: ")
                )
            if next_command == "exit":
                sys.exit(0)

        except KeyboardInterrupt:
            return self.main()


if __name__ == "__main__":
    Main().main()
