import sys

from InputHelper import InputHelper
from logger.Logger import Logger
from players.Historian import Historian
from players.MostCommon import MostCommon
from players.Player import Player
from players.Random import Random
from players.Sequential import Sequential
from Tournament import Tournament


class Main:
    __logger = Logger()

    def __init__(self):
        self.__logger.clear_logs()

    def __create_player(self, name, player_type):
        if player_type == "player":
            return Player(name)
        if player_type == "historian":
            return Historian(name)
        if player_type == "mostcommon":
            return MostCommon(name)
        if player_type == "random":
            return Random(name)
        if player_type == "sequential":
            return Sequential(name)

        raise ValueError("Illegal player type!")

    def main(self):
        command_helper = InputHelper(["play", "exit"])
        player_type_helper = InputHelper(
            ["player", "historian", "mostcommon", "random", "sequential"]
        )
        try:
            next_command = command_helper.get_legal_input("Please enter a command: \n")

            if next_command == "play":
                players = []
                for player_num in range(1, 3):
                    player_name = input(f"Please enter player {player_num}'s NAME: ")
                    player_type = player_type_helper.get_legal_input(
                        f"Please enter player {player_num}'s TYPE: "
                    )

                    players.append(self.__create_player(player_name, player_type))

                number_of_games = int(input("Please enter number of rounds: "))

                tournament = Tournament(players[0], players[1], number_of_games)
                tournament.arrange_tournament()
            else:
                sys.exit(0)
        except KeyboardInterrupt:
            return self.main()


if __name__ == "__main__":
    Main().main()
