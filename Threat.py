import abc
import Helper
from Helper import Counter


# Threats Functions
def print_single_issue(overall, type, filename, num, line, func = ""):
    print "(" + overall + " - " + type + " [" + func + "]) " + filename + " (line " + num.string() + "): " + line


# Base Abstract Class
class Base(object):
    __metaclass__  = abc.ABCMeta

    OverallAmount = Counter()
    OverallFiles = Counter()

    @abc.abstractmethod
    def detect(filename, line, num):
         """
         :param The name of the tested File
         :param The content of the line
         :param The line number
         :return True - Found, False - Not Found
         """


# Virtual Classes
class Url(Base):
    allow_included_files = ["/wp_", "/wp-"]

    @staticmethod
    def detect(filename, line, num):
        if "src=" in line:
            if Url.only_external_scripts(line) is False:
                return False

            if Url.allowed_scripts(line) is False:
                return False

            for included in Url.allow_included_files:
                if included in line:
                    return False

            Url.OverallAmount.add()
            Helper.OverallIssuesAmount.add()

            if len(line) > Helper.MAX_LINE:
                line = Helper.MAX_TEXT

            print_single_issue(Helper.OverallIssuesAmount.string(), "URL", filename, num, line, "")
            return True

        # line = line[line.index(func):line.index(';')+1]

    @staticmethod
    def only_external_scripts(line):
        if "href=" in line:
            return False
        if "<img" in line:
            return False
        if "http:" not in line:
            return False
        return True

    @staticmethod
    def allowed_scripts(line):
        if "jquery." in line:
            return False
        return True


class Xss(Base):
    SuspiciousFunctions = [".innerHTML", ".outerHTML", "document.write", "document.writeln", "eval(", ".html"]

    @staticmethod
    def detect(filename, line, num):
        for func in Xss.SuspiciousFunctions:
            if func in line:
                try:
                    line = line[line.index(func):line.index(';')+1]
                    length = len(line)

                    if length is 0:
                        return False
                    if len(func) + 1 is length:
                        return False
                    if Xss.only_quotes_verbs(func, line) is False:
                        return False
                    if Xss.only_quotes_funcs(func, line) is False:
                        return False

                    Xss.OverallAmount.add()
                    Helper.OverallIssuesAmount.add()

                    if len(line) > Helper.MAX_LINE:
                        line = Helper.MAX_TEXT + str(num.value())

                    print_single_issue(Helper.OverallIssuesAmount.string(), "XSS", filename, num, line, func)
                    return True
                except ValueError:
                    pass
        return False

    @staticmethod
    def only_quotes_verbs(func, line):
        if cmp(func,".outerHTML") is False and cmp(func,".innerHTML") is False:
            return True
        line = line[line.index("=") + 1:]
        for char in line:
            if char == ' ':
                continue
            elif char == '\"':
                break
            elif char == '\'':
                break
            else:
                return True
        for c in reversed(line):
            if char == ';':
                continue
            elif char == ' ':
                continue
            elif char == '\"':
                break
            elif char == '\'':
                break
            else:
                return True

        return False

    @staticmethod
    def only_quotes_funcs(func, line):
        if cmp(func,"document.write") is False and cmp(func,".html") is False and cmp(func, "eval(") is False:
                return True

        if (".html#" in line): return False

        line = line[line.index(func) + len(func):line.index(";")]
        for char in line:
            if char == ' ':
                continue
            if char == '(':
                continue
            elif char == '\"':
                break
            elif char == '\'':
                break
            elif char == ')':
                break
            else:
                return True
        for c in reversed(line):
            if char == ';':
                continue
            elif char == ' ':
                continue
            elif char == ')':
                continue
            elif char == '(':
                break
            elif char == '\"':
                break
            elif char == '\'':
                break
            else:
                return True

        return False
