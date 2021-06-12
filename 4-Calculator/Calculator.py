import numbers
import re

import numpy

from Function import Function
from logger.Logger import Logger
from Operator import Operator
from Queue import Queue
from Stack import Stack


class Calculator:
    _logger = Logger()

    def __init__(self, input_queue=Queue()):
        self.functions = {
            "EXP": Function(numpy.exp),
            "LOG": Function(numpy.log),
            "SIN": Function(numpy.sin),
            "COS": Function(numpy.cos),
            "SQRT": Function(numpy.sqrt),
        }

        self.operators = {
            "ADD": Operator(numpy.add, 0),
            "MULTIPLY": Operator(numpy.multiply, 1),
            "DIVIDE": Operator(numpy.divide, 1),
            "SUBTRACT": Operator(numpy.subtract, 0),
        }

        self.output_queue = Queue()
        self.input_queue = input_queue
        self.operator_stack = Stack()

    def calculate_expression(self, txt):
        self.create_input_queue(txt)
        self._logger.debug(f"inp_text: {txt}")
        self._logger.debug(f"inp_queue: {self.input_queue}")
        self.create_output_queue()
        temp = Stack()

        self._logger.debug("\n\n\n\n\n\nSTART CALCULATE\n\n\n\n")
        while not self.output_queue.is_empty():
            self._logger.debug(f"output_queue: {self.output_queue}")
            self._logger.debug(f"temp: {temp}")
            top_peek = self.output_queue.peek()
            if isinstance(top_peek, Function):
                func = self.output_queue.pop()
                temp.push(func.execute(temp.pop()))
            elif isinstance(top_peek, Operator):
                operator = self.output_queue.pop()
                temp1 = temp.pop()
                temp2 = temp.pop()
                temp.push(operator.execute(temp2, temp1))
            else:
                temp.push(self.output_queue.pop())
        self._logger.info(f"result: {temp}")
        return temp

    def create_output_queue(self):
        self.output_queue = Queue()
        while not self.input_queue.is_empty():
            elem = self.input_queue.pop()

            if isinstance(elem, numbers.Number):
                self.output_queue.push(elem)

            if isinstance(elem, str) and len(elem) > 1:
                elem = elem.upper()
                if elem in self.functions.keys():
                    elem = self.functions[elem]
                if elem in self.operators.keys():
                    elem = self.operators[elem]

            if isinstance(elem, Function) or elem == "(":
                self.operator_stack.push(elem)

            if elem == ")":
                while self.operator_stack.peek() != "(":
                    operator = self.operator_stack.pop()
                    self.output_queue.push(operator)

                if self.operator_stack.peek() == "(":
                    self.operator_stack.pop()

                if isinstance(self.operator_stack.peek(), Function):
                    func = self.operator_stack.pop()
                    self.output_queue.push(func)

            if isinstance(elem, Operator):
                while True:
                    top_elem = self.operator_stack.peek()
                    if (
                        self.operator_stack.is_empty()
                        or top_elem == "("
                        or (
                            isinstance(top_elem, Operator)
                            and top_elem.get_strength() < elem.get_strength()
                        )
                    ):
                        break
                    operator = self.operator_stack.pop()
                    self.output_queue.push(operator)

                self.operator_stack.push(elem)

            self._logger.debug(f"output_queue: {self.output_queue}")

        while not self.operator_stack.is_empty():
            operator = self.operator_stack.pop()
            self.output_queue.push(operator)

        return self.output_queue

    def create_input_queue(self, text):
        text = text.upper()
        text = text.replace("(", "( ")
        text = text.replace(")", " )")
        input_list = text.split()
        self.input_queue = Queue()
        for elem in input_list:
            if elem.isnumeric() or elem[0] == "-" or "." in elem:
                print("numeric: ", elem)
                elem = float(elem)
            self.input_queue.push(elem)
        return self.input_queue
