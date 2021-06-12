from Action import Action
from players.Player import Player


class Sequential(Player):
    __my_actions = []
    __opponent_actions = []
    __result_list = []

    def __init__(self, name):
        super().__init__(name + " (Sequential)")

    def __get_last_weapon(self):
        if len(self.__my_actions) == 0:
            return Action("scissors")
        return self.__my_actions[len(self.__my_actions) - 1]

    def select_action(self):
        last_weapon = self.__get_last_weapon().get_weapon()
        if last_weapon == "rock":
            return Action("paper")
        if last_weapon == "paper":
            return Action("scissors")
        return Action("rock")

    def recive_result(self, my_action, opponent_action, my_result):
        self.__my_actions.append(my_action)
        self.__opponent_actions.append(opponent_action)
        self.__result_list.append(my_result)

    def get_result_list(self):
        return self.__result_list
