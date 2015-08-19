# Build by Idan Cohen (Odahviing)
# Contributors: Roei Jacobovich
# Version 0.1

# Imports
import platform, os
import sys, time
import Helper, Threat
from datetime import datetime
from Scanner import Scanner
from optparse import OptionParser
from Threat import Url, Xss
from multiprocessing.dummy import Pool as ThreadPool

# Globals
objFile = Helper.StoreFile


# Main function that will preform the search in files
def search_for_threats(filename):
    lines = [line.rstrip('\n') for line in open(filename)]
    Threat.per.increase()

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
def print_summary(TimeStarted):
    TimeStarted = datetime.now() - TimeStarted
    print "\nFound " + Xss.OverallAmount.string() + " Hits In " + \
          Xss.OverallFiles.string() + " Files With domXSS Potential"
    print "Found " + Url.OverallAmount.string() + " Urls In " + \
          Url.OverallFiles.string() + " Files With External Urls"
    print "Found overall: " + Threat.OverallIssuesAmount.string() + " Issues In " \
          + Threat.overallFilesAmount.string() + " Files" \
          + " (" + str(TimeStarted)+ ")\n"


def Menu():
    options = OptionParser()
    options.add_option("-f", "--filename", help="Save to file", dest="filename", metavar="FILE")
    options.add_option("-u", "--url", action="store_true", help="Do online static analysis [Future Use]", default=False)
    (options, args) = options.parse_args()

    if options.url is True:
        print "Online Scanning not available"
        sys.exit(2)

    return options


def GraphicInit():
    print "\n"
    print "  6MMMMb\                           68b                    "
    print " 6M'    `   /                 /     Y89                    "
    print " MM        /M        ___     /M     ___   ____      ___    "
    print " YM.      /MMMMM   6MMMMb   /MMMMM  `MM  6MMMMb.  6MMMMb   "
    print "  YMMMMb   MM     8M'  `Mb   MM      MM 6M'   Mb 8M'  `Mb  "
    print "      `Mb  MM         ,oMM   MM      MM MM    `'     ,oMM  "
    print "       MM  MM     ,6MM9'MM   MM      MM MM       ,6MM9'MM  "
    print "       MM  MM     MM'   MM   MM      MM MM       MM'   MM  "
    print " L    ,M9  YM.  , MM.  ,MM   YM.  ,  MM YM.   d9 MM.  ,MM  "
    print " MYMMMM9    YMMM9 `YMMM9'Yb.  YMMM9 _MM_ YMMMM9  `YMMM9'Yb."
    print "\n"


# Main function
def main():
    # Clear the shell screen, recognize OS
    currentOS = platform.system()
    if currentOS == "linux2" or currentOS == "darwin" or currentOS=="linux":    #Linux and Max OSX
        os.system('clear')
    elif currentOS == "win32" or currentOS == "cygwin"or currentOS == "Windows": #Windows
        os.system('cls')
    # Arguments Care
    Threads = ThreadPool(10)
    GraphicInit()
    result = Menu()

    if len(sys.argv) < 2:
        print "Missing Argument: Statica.py folder_name"
        sys.exit(0)

    Helper.FileHandler = Helper.StoreFile(result.filename)

    # Get Suspicious File List
    main_scanner = Scanner(sys.argv[len(sys.argv) - 1])
    files_to_scan = main_scanner.FileLists
    Threat.per.countAll = len(files_to_scan)

    # Set Up Counters
    file_finished = Helper.Counter()
    time.sleep(1)

    TimeStarted = datetime.now()
    for file_name in files_to_scan:
        Threads.map(search_for_threats,(file_name,))
        file_finished.add()

    print_summary(TimeStarted)
    Helper.FileHandler.close()

if __name__ == "__main__":
    main()