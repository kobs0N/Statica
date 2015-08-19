import threading


def ToTime(dateTime):
    return dateTime.strftime('%d-%m-%Y %H:%M:%S')

# Helper Classes
class Counter:
    def __init__(self):
        self.lock = threading.Lock()
        self.count = 0

    def add(self, value=1):
        self.lock.acquire()
        self.count += value
        self.lock.release()

    def string(self):
        return str(self.count)

    def value(self):
        return int(self.count)

    def reset(self):
        self.count = 0


# Taking care of the process bar - Percent
# We have to increase it every time we scan a file
class Percent:
    def __init__(self):
        self.lock = threading.Lock()
        self.countAll = 1
        self.countCurrent = 0

    def increase(self):
        self.lock.acquire()
        self.countCurrent += 1
        self.lock.release()

    def percent(self):  # The percent itself
        res = (float(self.countCurrent) / self.countAll) * 100
        return "%.2f" % res     # Two decimal places after the point


class AsciiColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        self.HEADER = ''
        self.OKBLUE = ''
        self.OKGREEN = ''
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''


class StoreFile:
    def __init__(self, path):
        self.file_path = path
        self.active = False
        try:
            self._file = open(self.file_path, 'a')
            self.active = True
        except TypeError:
            pass

    def save(self, text):
        if self.active is True:
            self._file.write(text)

    def close(self):
        if self.active is True:
            self._file.close()

# Consts
MAX_LINE = 250
MAX_TEXT = "Long Line"

# Globals
FileHandler = " "
