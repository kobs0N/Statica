# Build by Idan Cohen
# Version 0.01 - Only Alpha

# Imports
import sys, time
from Scanner import Scanner
import Helper, DomXSS, Url


# Main function that will preform the search in files
def search_for_weakness(filename):
    hits_amount = Helper.Counter()
    lines = [line.rstrip('\n') for line in open(filename)]

    num_of_lines = Helper.Counter()
    for line in lines:
        num_of_lines.add()
        result = DomXSS.detect_dom_xss(filename, line, num_of_lines)
        if result is True:
            DomXSS.OverallXssFiles.add()

        result = Url.detect_url(filename, line, num_of_lines)
        if result is True:
            Url.OverallUrlFiles.add()


# Printer
def print_summary():
    print "\nFound " + DomXSS.OverallXssAmount.string() + " Hits In " + \
          DomXSS.OverallXssFiles.string() + " Files With domXSS Potential"
    print "Found " + Url.OverallUrlAmount.string() + " Urls In " + \
          Url.OverallUrlFiles.string() + " Files With External Urls"
    print "Found overall: " + Helper.overall_issues_amount.string() + " Issues"


# Main function
def main():
    # Arguments Care
    if len(sys.argv) != 2:
        print "Missing Argument: Statica.py folder_name"
        sys.exit(0)

    # Get Suspicious File List
    main_scanner = Scanner(sys.argv[1])
    files_to_scan = main_scanner.FileLists

    # Set Up Counters
    file_finished = Helper.Counter()
    file_with_xss = Helper.Counter()
    time.sleep(1)

    for file_name in files_to_scan:
        search_for_weakness(file_name)
        file_finished.add()

    print_summary()

if __name__ == "__main__":
    main()