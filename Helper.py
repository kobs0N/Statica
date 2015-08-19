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
MAX_LINE = 200
MAX_TEXT = "Long Line"

# Globals
FileHandler = " "