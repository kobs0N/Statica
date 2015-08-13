class Counter:
    def __init__(self):
        self.count = 0

    def Add(self, value=1):
        self.count = self.count + value

    def String(self):
        return str(self.count)

    def Reset(self):
        self.count = 0
