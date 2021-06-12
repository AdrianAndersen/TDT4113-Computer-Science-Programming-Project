from Container import Container


class Stack(Container):
    def __init__(self):
        super(Stack, self).__init__()

    def peek(self):
        if not self.is_empty():
            return self._items[-1]

    def pop(self):
        if not self.is_empty():
            return self._items.pop()
