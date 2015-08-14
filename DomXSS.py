import Helper

SuspiciousFunctions = [".innerHTML", ".outerHTML", "document.write", "document.writeln", "eval(", ".html"]
OverallXssAmount = Helper.Counter()
OverallXssFiles = Helper.Counter()


def detect_dom_xss(filename, line, num):
    for func in SuspiciousFunctions:
        if func in line:
            try:
                line = line[line.index(func):line.index(';')+1]
                length = len(line)

                if length is 0:
                    return False
                if len(func) + 1 is length:
                    return False
                if only_quotes_verbs(func, line) is False:
                    return False
                if only_quotes_funcs(func, line) is False:
                    return False

                OverallXssAmount.add()
                Helper.overall_issues_amount.add()

                if len(line) > Helper.MAX_LINE:
                    line = Helper.MAX_TEXT + str(num.value())

                Helper.print_single_issue(Helper.overall_issues_amount.string(), "XSS", filename,
                                              num, line, func)
                return True
            except ValueError:
                pass
    return False


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


