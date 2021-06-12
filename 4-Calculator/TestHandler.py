import numbers

import numpy

from Calculator import Calculator
from Function import Function
from Operator import Operator
from Queue import Queue
from Stack import Stack


class TestHandler:
    _test_items = ["firstItem", "secondItem", "thirdItem", "lastItem"]

    def run(self):
        self._test_queue()
        self._test_stack()
        self._test_func()
        self._test_operator()
        self._test_calc()
        self._test_create_output_queue()
        self._test_calculate_expression()

    def _test_queue(self):
        queue = Queue()
        assert queue.is_empty()
        for item in self._test_items:
            queue.push(item)
        assert queue.size() == 4, "expected queue to be of size 4"
        assert (
            queue.peek() == "firstItem"
        ), "expected first item in queue to be firstItem"
        popped = queue.pop()
        assert queue.size() == 3
        assert queue.peek() == "secondItem"
        assert popped == "firstItem"

        while not queue.is_empty():
            queue.pop()
        assert queue.is_empty()

    def _test_stack(self):
        stack = Stack()
        assert stack.is_empty()
        for item in self._test_items:
            stack.push(item)
        assert stack.size() == 4, "expected stack to be of size 4"
        assert stack.peek() == "lastItem", "expected top item in stack to be lastItem"
        popped = stack.pop()
        assert stack.size() == 3
        assert stack.peek() == "thirdItem"
        assert popped == "lastItem"

        while not stack.is_empty():
            stack.pop()
        assert stack.is_empty()

    def _test_func(self):
        exp_func = Function(numpy.exp)
        sin_func = Function(numpy.sin)
        assert isinstance(exp_func, Function)
        assert not isinstance(numpy.exp, Function)
        assert exp_func.execute(sin_func.execute(0)) == 1.0

    def _test_operator(self):
        add_op = Operator(operation=numpy.add, strength=0)
        multiply_op = Operator(operation=numpy.multiply, strength=1)
        assert add_op.execute(1, multiply_op.execute(2, 3)) == 7

    def _test_calc(self):
        calc = Calculator()
        assert calc.functions["EXP"].execute(
            calc.operators["ADD"].execute(1, calc.operators["MULTIPLY"].execute(2, 3))
        ) == numpy.exp(7)

    def _test_create_output_queue(self):
        test_queue = Queue()
        test_queue.push("exp")
        test_queue.push("(")
        test_queue.push(1)
        test_queue.push("add")
        test_queue.push(2)
        test_queue.push("multiply")
        test_queue.push(3)
        test_queue.push(")")
        calc = Calculator(input_queue=test_queue)
        output_queue = calc.create_output_queue()
        assert str(output_queue) == "1, 2, 3, multiply, add, exp, "

    def _test_calculate_expression(self):
        text1 = "exp (1 add 2 multiply 3)"
        text2 = (
            "((15 DIVIDE (7 SUBTRACT (1 ADD 1))) MULTIPLY 3) SUBTRACT (2 ADD (1 ADD 1))"
        )
        calc = Calculator()

        input_queue1 = calc.create_input_queue(text1)
        assert str(input_queue1) == "EXP, (, 1.0, ADD, 2.0, MULTIPLY, 3.0, ), "
        output_queue1 = calc.create_output_queue()

        input_queue2 = calc.create_input_queue(text2)
        assert (
            str(input_queue2)
            == "(, (, 15.0, DIVIDE, (, 7.0, SUBTRACT, (, 1.0, ADD, 1.0, ), ), ), MULTIPLY, 3.0, ), SUBTRACT, (, 2.0, ADD, (, 1.0, ADD, 1.0, ), ), "
        )
        output_queue2 = calc.create_output_queue()
        assert (
            str(output_queue2)
            == "15.0, 7.0, 1.0, 1.0, add, subtract, true_divide, 3.0, multiply, 2.0, 1.0, 1.0, add, add, subtract, "
        )

        assert str(calc.calculate_expression(text1)).replace(", ", "") == str(
            numpy.exp(7)
        )
        assert str(calc.calculate_expression(text2)).replace(", ", "") == "5.0"
