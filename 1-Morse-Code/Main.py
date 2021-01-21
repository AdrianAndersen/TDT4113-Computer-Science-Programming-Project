from logger.Logger import Logger
from MorseCoder import MorseCoder
from Utils import Utils


class Main:
    __logger = Logger()

    def __init__(self):
        self.__logger.clear_logs()

    def __get_next_command(self):
        legal_commands = {
            "encode": ["encode", "1"],
            "decode": ["decode", "2"],
            "exit": ["exit", "3", "q"],
        }
        self.__logger.info("You are now in the main menu.")
        self.__logger.info("Legal commands: 'encode' | 'decode' | 'exit'")
        input_command = input("Please enter a command: \n").lower()

        Utils().clear_terminal()

        if input_command in legal_commands["encode"]:
            return "encode"
        elif input_command in legal_commands["decode"]:
            return "decode"
        elif input_command in legal_commands["exit"]:
            return "exit"
        else:
            self.__logger.warning("Illegal command: ", input_command)
            self.__logger.warning("Please try again...")
            return self.__get_next_command()

    def main(self):
        morse_coder = MorseCoder()
        try:
            command = self.__get_next_command()

            if command == "encode":
                morse_coder.start_encode_mode()
            elif command == "decode":
                morse_coder.start_decode_mode()
            else:
                quit()
        except KeyboardInterrupt:
            return self.main()


if __name__ == "__main__":
    Main().main()
