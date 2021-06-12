class Container:
    def __init__(self):
        self._items = []

    def size(self):
        return len(self._items)

    def is_empty(self):
        return self.size() == 0

    def push(self, item):
        self._items.append(item)

    def pop(self):
        # Pop off the correct element of self.items, and return it
        raise NotImplementedError

    def peek(self):
        # Return the top element without removing it
        raise NotImplementedError

    def __str__(self):
        items_copy = self._items.copy()
        result = ""
        while not self.is_empty():
            item_str = str(self.pop()) + ", "
            result += item_str
        self._items = items_copy
        return result
