# Helper Classes
class Counter:
    def __init__(self):
        self.count = 0

    def add(self, value=1):
        self.count = self.count + value

    def string(self):
        return str(self.count)

    def value(self):
        return int(self.count)

    def reset(self):
        self.count = 0


# Helper Functions
def print_single_issue(overall, type, filename, num, line, func = ""):
    print "(" + overall + " - " + type + " [" + func + "]) " + filename + " (line " + num.string() + "): " + line


# Globals
overall_issues_amount = Counter()

# Consts
MAX_LINE = 100
MAX_TEXT = "Long Line - Go To Line: "
