import random


class Action:
    LEGAL_WEAPONS = ["rock", "paper", "scissors"]
    __weapon = None

    def __init__(self, weapon):
        weapon = weapon.lower()
        if weapon not in self.LEGAL_WEAPONS:
            raise ValueError("Illegal Weapon!")
        self.__weapon = weapon

    def get_weapon(self):
        return self.__weapon

    def __eq__(self, other):
        return self.get_weapon() == other.get_weapon()

    def __gt__(self, other):
        if self.get_weapon() == "rock":
            if other.get_weapon() == "paper":
                return False
            if other.get_weapon() == "scissors":
                return True
        elif self.get_weapon() == "paper":
            if other.get_weapon() == "rock":
                return True
            if other.get_weapon() == "scissors":
                return False
        elif self.get_weapon() == "scissors":
            if other.get_weapon() == "paper":
                return True
            if other.get_weapon() == "rock":
                return False
        return False

    def __str__(self):
        return self.get_weapon()

    def get_counter_action(self, action):
        if action.get_weapon() == "rock":
            return Action("paper")
        if action.get_weapon() == "paper":
            return Action("scissors")
        return Action("rock")

    def get_random_action(self):
        return Action(Action.LEGAL_WEAPONS[random.randint(0, 2)])
