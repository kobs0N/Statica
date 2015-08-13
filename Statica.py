# Build by Idan Cohen
# Version 0.01 - Only Alpha

# Imports
import sys
import time
import Helper
from Core import Scanner
from DomXSS import detect_dom_xss


# Main function that will preform the search in files
def search_for_weakness(filename):
    hits_amount = Helper.Counter()
    lines = [line.rstrip('\n') for line in open(filename)]

    for line in lines:
        result = detect_dom_xss(filename, line)
        if result is True:
            hits_amount.add()
    return hits_amount.value()


# Main function
def main():
    # Arguments Care
    if len(sys.argv) != 2:
        print "Missing Argument: Statica.exe Folder"
        sys.exit(0)

    # Get Suspicious File List
    main_scanner = Scanner(sys.argv[1])
    files_to_scan = main_scanner.FileLists

    # Set Up Counters
    file_finished = Helper.Counter()
    file_with_xss = Helper.Counter()
    overall_hits = Helper.Counter()
    time.sleep(1)

    for file_name in files_to_scan:
        hits_amount = search_for_weakness(file_name)
        overall_hits.add(hits_amount)
        if hits_amount != 0:
            file_with_xss.add()
        file_finished.add()

    print "Found " + overall_hits.string() + " Hits In " + file_with_xss.string() + " Files With domXSS Potential"

if __name__ == "__main__":
    main()