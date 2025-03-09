class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, item):
        self.items.append(item)

    def dequeue(self):
        if self.isEmpty():
            return "Queue is empty"
        return self.items.pop(0)

    def peek(self):
        if self.isEmpty():
            return "Queue is empty"
        return self.items[0]

    def isEmpty(self):
        return self.size() == 0

    def size(self):
        return len(self.items)