""" TDT4113: Project 5 - Keypad """


class Rule:
    """ Defines structure for a Rule used in the FSM """
    def __init__(self, state1, state2, signal, action=None):
        self.state1 = state1
        self.state2 = state2
        if signal == "¤":
            self.signal = self.signal_is_valid_led
        elif signal == "$":
            self.signal = self.signal_is_digit
        elif signal == "@":
            self.signal = self.is_any_signal
        else:
            self.signal = signal
        self.action = action

    def match(self, state, signal):
        """check whether the rule condition is fulfilled"""
        return state == self.state1 and (
            signal == self.signal or (callable(self.signal) and self.signal(signal))
        )

    @staticmethod
    def signal_is_valid_led(signal):
        """ Check if input is a valid LED ID """
        return 48 <= ord(signal) <= 53

    @staticmethod
    def signal_is_digit(signal):
        """ Check if input is a digit (0-9) """
        return 48 <= ord(signal) <= 57

    @staticmethod
    def is_any_signal(signal):
        """ Check if an input has been provided """
        return len(signal) > 0

    def __str__(self):
        return f"Rule: < state1: {self.state1}, state2: {self.state2}, signal: {self.signal}, " \
               f"action: {self.action} >"
