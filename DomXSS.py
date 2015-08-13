import Helper

SuspiciousFunctions = [".innerHTML", ".outerHTML", "document.write", "document.writeln", "eval(", ".html"]


def detect_dom_xss(filename, line):
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

                Helper.overall_hits_amount.add()
                print "(" + Helper.overall_hits_amount.string() + " - XSS) " + filename + "(" + func + ") : " + line
                return True
            except ValueError:
                pass
    return False


def only_quotes_verbs(func, line):
    if (cmp(func,".outerHTML") and cmp(func,".innerHTML")):
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
    if (cmp(func,"document.write") and cmp(func,".html")):
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


