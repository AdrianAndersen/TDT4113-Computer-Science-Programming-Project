from Container import Container


class Queue(Container):
    def __init__(self):
        super(Queue, self).__init__()

    def peek(self):
        if not self.is_empty():
            return self._items[0]

    def pop(self):
        if not self.is_empty():
            return self._items.pop(0)
