import numbers

from logger.Logger import Logger


class Function:
    _logger = Logger()

    def __init__(self, func):
        self.func = func

    def execute(self, element):
        if not isinstance(element, numbers.Number):
            raise TypeError("The element must be a number")
        result = float(self.func(element))

        self._logger.debug(f"Function: {self.func.__name__}({element}) = {result}")

        return result

    def __str__(self):
        return str(self.func.__name__)
