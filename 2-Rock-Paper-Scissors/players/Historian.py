from Action import Action
from players.Player import Player


class Historian(Player):
    __my_actions = []
    __opponent_actions = []
    __result_list = []

    __remember = 3

    def __init__(self, name):
        super().__init__(name + " (Historian)")

    def __most_frequent(self, actions):
        frequency_dict = {"rock": 0, "paper": 0, "scissors": 0}
        for action in actions:
            weapon = action.get_weapon()
            frequency_dict[weapon] = frequency_dict[weapon] + 1
        return max(frequency_dict, key=frequency_dict.get)

    def select_action(self):
        if len(self.__opponent_actions) <= self.__remember:
            return Action.get_random_action(self)

        last_opponent_actions = self.__opponent_actions.copy()[-1 * self.__remember :]
        historical_next_actions = []

        for i in range(0, len(self.__opponent_actions) - 1):
            if i < self.__remember - 1:
                continue
            sub_sequence = []
            next_action = self.__opponent_actions[i + 1]
            for j in range(0, self.__remember):
                sub_sequence.append(self.__opponent_actions[i - j].get_weapon())
            sub_sequence.reverse()

            matches = True
            for k in range(0, self.__remember):
                if last_opponent_actions[k].get_weapon() != sub_sequence[k]:
                    matches = False
            if matches:
                historical_next_actions.append(next_action)

        if len(historical_next_actions) == 0:
            return Action.get_random_action(self)

        most_probable_action = Action(self.__most_frequent(historical_next_actions))

        return Action.get_counter_action(self, most_probable_action)

    def recive_result(self, my_action, opponent_action, my_result):
        self.__my_actions.append(my_action)
        self.__opponent_actions.append(opponent_action)
        self.__result_list.append(my_result)

    def get_result_list(self):
        return self.__result_list
