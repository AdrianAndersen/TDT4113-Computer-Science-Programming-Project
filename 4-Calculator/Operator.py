import numbers

from logger.Logger import Logger


class Operator:
    _logger = Logger()

    def __init__(self, operation, strength):
        self._operation = operation
        self._strength = strength

    def execute(self, first_element, second_element):
        print(first_element, " ", second_element)
        if (
            (isinstance(first_element, numbers.Number))
            and (isinstance(second_element, numbers.Number))
            or first_element[0] == "-"
            or second_element[0] == "-"
        ):
            first_element = float(first_element)
            second_element = float(second_element)
            print(first_element, " ", second_element)
            result = float(self._operation(first_element, second_element))

            self._logger.debug(
                f"Function: {self._operation.__name__}({first_element}, {second_element}) = {result}"
            )

            return result
        raise TypeError("The elements must be numbers")

    def get_strength(self):
        return self._strength

    def __str__(self):
        return str(self._operation.__name__)
