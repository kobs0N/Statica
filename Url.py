import Helper

allow_included_files = ["/wp_", "/wp-"]
OverallUrlAmount = Helper.Counter()
OverallUrlFiles = Helper.Counter()


def detect_url(filename, line, num):
    if "src=" in line:
        if only_external_scripts(line) is False:
            return False

        if allowed_scripts(line) is False:
            return False

        for included in allow_included_files:
            if included in line:
                return False

        OverallUrlAmount.add()
        Helper.overall_issues_amount.add()

        if len(line) > Helper.MAX_LINE:
            line = Helper.MAX_TEXT

        Helper.print_single_issue(Helper.overall_issues_amount.string(), "URL", filename,
                                num, line, "")
        return True

    # line = line[line.index(func):line.index(';')+1]


def only_external_scripts(line):
    if "href=" in line:
        return False
    if "<img" in line:
        return False
    if "http:" not in line:
        return False
    return True


def allowed_scripts(line):
    if "jquery." in line:
        return False
    return True
