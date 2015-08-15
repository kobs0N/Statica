# Helper Classes
class Counter:
    def __init__(self):
        self.count = 0

    def add(self, value=1):
        self.count += value

    def string(self):
        return str(self.count)

    def value(self):
        return int(self.count)

    def reset(self):
        self.count = 0


# Consts
MAX_LINE = 200
MAX_TEXT = "Long Line"
