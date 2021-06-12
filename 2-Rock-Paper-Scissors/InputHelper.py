from logger.Logger import Logger
from Utils import Utils


class InputHelper:
    __logger = Logger()
    __legal_inputs = []
    __alias_dict = None
    __error_message = None
    __error_limit = None
    __error_count = 0

    def __init__(
        self,
        legal_inputs,
        error_message="Illegal input, please try again",
        error_limit=5,
    ):
        self.__legal_inputs = legal_inputs.copy()
        self.__alias_dict = self.__create_legal_aliases(legal_inputs)
        self.__error_message = error_message
        self.__error_limit = error_limit

    def __pretty_print_legal_inputs(self):
        result = "Legal inputs: \n"

        for key in self.__alias_dict:
            result += f"{key} (aliases: {self.__alias_dict[key]})\n"

        self.__logger.debug(result)

    def __create_short_alias(self, original_input, used_aliases):
        for char in original_input:
            if char not in used_aliases:
                return char
        return original_input

    def __create_legal_aliases(self, legal_inputs):
        alias_dict = {}

        used_aliases = []
        index = 0
        for input_value in legal_inputs:
            input_aliases = []

            short_alias = self.__create_short_alias(input_value, used_aliases)
            if short_alias != input_value:
                input_aliases += short_alias
                used_aliases += short_alias

            input_aliases += str(index + 1)
            index += 1

            self.__legal_inputs += input_aliases
            alias_dict[input_value] = input_aliases
        self.__logger.debug(f"Created input alias dict: {alias_dict}")
        return alias_dict

    def get_legal_input(self, message):
        if self.__error_count > self.__error_limit:
            Utils.clear_terminal(self)
            self.__logger.warning(
                "Wrong command entered to many times. Returning to main menu..."
            )
            raise KeyboardInterrupt()

        self.__pretty_print_legal_inputs()
        input_value = input(message)
        # Utils.clear_terminal(self)

        if input_value not in self.__legal_inputs:
            self.__logger.warning(self.__error_message)
            self.__pretty_print_legal_inputs()
            self.__error_count += 1
            return self.get_legal_input(message)

        for key in self.__alias_dict:
            if input_value == key or input_value in self.__alias_dict[key]:
                return key

        raise ValueError("Illegal input!")
