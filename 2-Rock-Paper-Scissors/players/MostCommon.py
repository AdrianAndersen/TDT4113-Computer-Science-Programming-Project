from Action import Action
from players.Player import Player


class MostCommon(Player):
    __my_actions = []
    __opponent_actions = []
    __result_list = []

    def __init__(self, name):
        super().__init__(name + " (MostCommon)")

    def __get_most_frequent_opponent_weapon(self):
        frequency_dict = {"rock": 0, "paper": 0, "scissors": 0}
        for action in self.__opponent_actions:
            weapon = action.get_weapon()
            frequency_dict[weapon] = frequency_dict[weapon] + 1
        return max(frequency_dict, key=frequency_dict.get)

    def select_action(self):
        if len(self.__opponent_actions) == 0:
            return Action.get_random_action(self)

        most_common_opponent_weapon = self.__get_most_frequent_opponent_weapon()

        return Action.get_counter_action(self, Action(most_common_opponent_weapon))

    def recive_result(self, my_action, opponent_action, my_result):
        self.__my_actions.append(my_action)
        self.__opponent_actions.append(opponent_action)
        self.__result_list.append(my_result)

    def get_result_list(self):
        return self.__result_list
