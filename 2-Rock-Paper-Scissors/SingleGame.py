from logger.Logger import Logger


class SingleGame:
    __logger = Logger()

    __player1 = None
    __player2 = None

    def __init__(self, player1, player2):
        self.__player1 = player1
        self.__player2 = player2

    def perform_game(self):
        player1_action = self.__player1.select_action()
        player2_action = self.__player2.select_action()

        if player1_action == player2_action:
            self.__player1.recive_result(player1_action, player2_action, "d")
            self.__player2.recive_result(player2_action, player1_action, "d")
            self.__logger.info(
                f"{self.__player1.get_name()}: {player1_action.get_weapon()} | {self.__player2.get_name()}: {player2_action.get_weapon()} => Draw!"
            )
        elif player1_action > player2_action:
            self.__player1.recive_result(player1_action, player2_action, "w")
            self.__player2.recive_result(player2_action, player1_action, "l")
            self.__logger.info(
                f"{self.__player1.get_name()}: {player1_action.get_weapon()} | {self.__player2.get_name()}: {player2_action.get_weapon()} => {self.__player1.get_name()} wins!"
            )

        elif player2_action > player1_action:
            self.__player1.recive_result(player1_action, player2_action, "l")
            self.__player2.recive_result(player2_action, player1_action, "w")
            self.__logger.info(
                f"{self.__player1.get_name()}: {player1_action.get_weapon()} | {self.__player2.get_name()}: {player2_action.get_weapon()} => {self.__player2.get_name()} wins!"
            )

        else:
            self.__logger.error("Illegal weapon in game!")
