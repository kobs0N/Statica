overallHitsAmount = 0

def Search(filename):
    global overallHitsAmount
    hitsAmount = 0
    SuspiciousFunctions = [".innerHTML", ".outerHTML", "document.write", "document.writeln", "eval(", ".html"]
    lines = [line.rstrip('\n') for line in open(filename)]

    for line in lines:
        for func in SuspiciousFunctions:
            if func in line:
                try:
                    line = line[line.index(func):line.index(';')+1]
                    length = len(line)

                    if (length == 0): continue
                    if (len(func) + 1 == length): continue
                    if onlyQuotesVerbs(func, line) == False: continue
                    if onlyQuotesFuncs(func, line) == False: continue

                    hitsAmount = hitsAmount + 1
                    overallHitsAmount = overallHitsAmount + 1
                    print "(" + str(overallHitsAmount) + ") " + filename + "(" + func + ") : " + line
                except ValueError:
                    pass
    return hitsAmount

def onlyQuotesVerbs(func, line):
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
def onlyQuotesFuncs(func, line):
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


