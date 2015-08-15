# Build by Idan Cohen
# Version 0.01 - Only Alpha

# Imports
import sys, time
import Helper, Threat
from Scanner import Scanner
from Threat import Url, Xss


# Main function that will preform the search in files
def search_for_threats(filename):
    lines = [line.rstrip('\n') for line in open(filename)]

    num_of_lines = Helper.Counter()
    for line in lines:
        num_of_lines.add()
        result = Xss.detect(filename, line.lower(), num_of_lines)
        if result is True:
            Xss.FoundFile = True

        result = Url.detect(filename, line.lower(), num_of_lines)
        if result is True:
            Url.FoundFile = True

    Xss.count_files()
    Url.count_files()
    Threat.count_files()


# Printer
def print_summary():
    print "\nFound " + Xss.OverallAmount.string() + " Hits In " + \
          Xss.OverallFiles.string() + " Files With domXSS Potential"
    print "Found " + Url.OverallAmount.string() + " Urls In " + \
          Url.OverallFiles.string() + " Files With External Urls"
    print "Found overall: " + Threat.OverallIssuesAmount.string() + " Issues" + " In " + Threat.overallFilesAmount.string() + " Files"


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
    time.sleep(1)

    for file_name in files_to_scan:
        search_for_threats(file_name)
        file_finished.add()

    print_summary()

if __name__ == "__main__":
    main()