import matplotlib.pyplot as plt

from logger.Logger import Logger
from SingleGame import SingleGame


class Tournament:
    __logger = Logger()
    __player1 = None
    __player2 = None
    __number_of_games = None

    def __init__(self, player1, player2, number_of_games):
        self.__player1 = player1
        self.__player2 = player2
        self.__number_of_games = number_of_games

    def __arrange_singlegame(self):
        single_game = SingleGame(self.__player1, self.__player2)
        single_game.perform_game()

    def __plot_statistics(self):
        self.__logger.info("Ploting statistics...")
        player1_game_stats = self.__player1.get_result_list()
        win_probablities = []
        for i in range(0, self.__number_of_games):
            stats_till_now = player1_game_stats.copy()[: i + 1]
            win_count = 0
            for stat in stats_till_now:
                if stat == "w":
                    win_count += 1
            prob = win_count / len(stats_till_now)
            win_probablities.append(prob)
        plt.ion()
        plt.plot(win_probablities)
        plt.show()
        input("Press any enter to continue...")

    def arrange_tournament(self):
        for i in range(1, self.__number_of_games + 1):
            self.__logger.info(
                f"Starting round number {i} of {self.__number_of_games}: "
            )
            self.__arrange_singlegame()
        self.__logger.info("Tournament ended")
        self.__plot_statistics()
