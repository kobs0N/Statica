# Build by Idan Cohen
# Version 0.01 - Only Alpha

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
    print "   SSSSSSSSSSSSSSS          tttt                                     tttt            iiii                                        "
    print " SS:::::::::::::::S      ttt:::t                                  ttt:::t           i::::i                                       "
    print "S:::::SSSSSS::::::S      t:::::t                                  t:::::t            iiii                                        "
    print "S:::::S     SSSSSSS      t:::::t                                  t:::::t                                                        "
    print "S:::::S            ttttttt:::::ttttttt      aaaaaaaaaaaaa   ttttttt:::::ttttttt    iiiiiii     cccccccccccccccc  aaaaaaaaaaaaa   "
    print "S:::::S            t:::::::::::::::::t      a::::::::::::a  t:::::::::::::::::t    i:::::i   cc:::::::::::::::c  a::::::::::::a  "
    print " S::::SSSS         t:::::::::::::::::t      aaaaaaaaa:::::a t:::::::::::::::::t     i::::i  c:::::::::::::::::c  aaaaaaaaa:::::a "
    print "  SS::::::SSSSS    tttttt:::::::tttttt               a::::a tttttt:::::::tttttt     i::::i c:::::::cccccc:::::c           a::::a "
    print "    SSS::::::::SS        t:::::t              aaaaaaa:::::a       t:::::t           i::::i c::::::c     ccccccc    aaaaaaa:::::a "
    print "       SSSSSS::::S       t:::::t            aa::::::::::::a       t:::::t           i::::i c:::::c               aa::::::::::::a "
    print "            S:::::S      t:::::t           a::::aaaa::::::a       t:::::t           i::::i c:::::c              a::::aaaa::::::a "
    print "            S:::::S      t:::::t    tttttta::::a    a:::::a       t:::::t    tttttt i::::i c::::::c     ccccccca::::a    a:::::a "
    print "SSSSSSS     S:::::S      t::::::tttt:::::ta::::a    a:::::a       t::::::tttt:::::ti::::::ic:::::::cccccc:::::ca::::a    a:::::a "
    print "S::::::SSSSSS:::::S      tt::::::::::::::ta:::::aaaa::::::a       tt::::::::::::::ti::::::i c:::::::::::::::::ca:::::aaaa::::::a "
    print "S:::::::::::::::SS         tt:::::::::::tt a::::::::::aa:::a        tt:::::::::::tti::::::i  cc:::::::::::::::c a::::::::::aa:::a"
    print " SSSSSSSSSSSSSSS             ttttttttttt    aaaaaaaaaa  aaaa          ttttttttttt  iiiiiiii    cccccccccccccccc  aaaaaaaaaa  aaaa"
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