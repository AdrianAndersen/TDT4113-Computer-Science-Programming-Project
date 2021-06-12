from Action import Action
from players.Player import Player


class Random(Player):
    __my_actions = []
    __opponent_actions = []
    __result_list = []

    def __init__(self, name):
        super().__init__(name + " (Random)")

    def select_action(self):
        return Action.get_random_action(self)

    def recive_result(self, my_action, opponent_action, my_result):
        self.__my_actions.append(my_action)
        self.__opponent_actions.append(opponent_action)
        self.__result_list.append(my_result)

    def get_result_list(self):
        return self.__result_list
