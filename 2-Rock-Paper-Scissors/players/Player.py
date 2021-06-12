from Action import Action
from InputHelper import InputHelper


class Player:
    __name = None
    __my_actions = []
    __opponent_actions = []
    __result_list = []

    __input_helper = InputHelper(Action.LEGAL_WEAPONS)

    def __init__(self, name):
        self.__name = name

    def select_action(self):
        """ selects which action to perform (play rock, scissors or paper) and return this. """
        return Action(self.__input_helper.get_legal_input("Please enter at weapon: \n"))

    def recive_result(self, my_action, opponent_action, my_result):
        self.__my_actions.append(my_action)
        self.__opponent_actions.append(opponent_action)
        self.__result_list.append(my_result)

    def get_name(self):
        return self.__name

    def get_result_list(self):
        return self.__result_list
