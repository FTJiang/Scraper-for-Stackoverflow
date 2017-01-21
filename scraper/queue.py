class Queue:
    def __init__(self):
        self.items = []
    def isEmpty(self):
        return self.items == []
    def enqueue(self, item):
        self.items.insert(0,item)

    def dequeue(self):
        if self.items == []:
            return "queue is empty"
        return self.items.pop()

    def size(self):
        return len(self.items)

    def peek(self):
        return self.items[len(self.items)-1]