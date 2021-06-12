""" TDT4113: Project 5 - Keypad """

from kpc import KPC
from logger.Logger import Logger


class FSM:
    """ Class for representing a Finite State Machine """

    __logger = Logger()
    agent = KPC()
    state = "init"
    rules = []

    def add_rule(self, rule):
        """ Add new rule to the end of the FSM rule list """
        self.rules.append(rule)

    def set_rules(self, rules):
        """ Take rules and store internally """
        self.rules = rules

    def get_next_signal(self):
        """ Get the next signal from the KPC """
        return self.agent.get_next_signal()

    def run(self):
        """ Begin in initial state and repeatedly read next signal, run until final state """
        self.__logger.info(f"Starting fsm with rules:\n{self.pretty_print_rules()}")
        while self.state != "fsm-end-state":
            signal = self.agent.get_next_signal()
            for rule in self.rules:
                if rule.match(self.state, signal):
                    self.__logger.info(
                        f"Executing action: {rule.action} with signal {signal}. State moved from "
                        + f"{self.state} => {rule.state2}"
                    )
                    self.state = rule.state2
                    self.agent.do_action(rule.action, signal)
                    break

    def pretty_print_rules(self):
        """ Print rules in a pretty, human-readable format """
        result = ""
        for rule in self.rules:
            result += str(rule) + "\n"
        return result
