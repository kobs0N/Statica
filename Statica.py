# Build by Idan Cohen (Odahviing)
# Contributors: Roei Jacobovich
# Version 0.1

# Imports
import platform, os, argparse
import sys, time
import Helper, Threat
from datetime import datetime
from Scanner import Scanner
from Threat import Url, Xss, Comments
from multiprocessing.dummy import Pool as ThreadPool
import Spider

# Globals
objFile = Helper.StoreFile

# Main function that will preform the search in files
def search_for_threats(filename):
    lines = [line.rstrip('\n') for line in open(filename)]
    Threat.per.increase()

    if cfile is not None:
        cfile.write("\n***\t"+filename+"\t***\n\n")

    num_of_lines = Helper.Counter()
    for line in lines:
        num_of_lines.add()
        result = Xss.detect(filename, line.lower(), num_of_lines)
        if result is True:
            Xss.FoundFile = True

        result = Url.detect(filename, line.lower(), num_of_lines)
        if result is True:
            Url.FoundFile = True

        if cfile is not "":
            result = Comments.detect(filename, line.lower(), num_of_lines)
            Comments.longComment = False # Reset for the next file
            if result is True and cfile is not None: # result is the number of the line, -1 if False
                Comments.FoundFile = True
                cfile.write("@" + str(num_of_lines.value()) + ":\t" + line + "\n")

    Xss.count_files()
    Url.count_files()
    Comments.count_files()
    Threat.count_files()


# Printer
def print_summary(TimeStarted):
    TimeStarted = datetime.now() - TimeStarted
    print "\nFound " + Xss.OverallAmount.string() + " Hits In " + \
          Xss.OverallFiles.string() + " Files With domXSS Potential"
    print "Found " + Url.OverallAmount.string() + " Urls In " + \
          Url.OverallFiles.string() + " Files With External Urls"
    print "Found " + Comments.OverallAmount.string() + " Comments In " + \
          Comments.OverallFiles.string() + " Files With Comments"
    print "Found overall (Without Comments): " + Threat.OverallIssuesAmount.string() + " Issues In " \
          + Threat.overallFilesAmount.string() + " Files" \
          + " (" + str(TimeStarted)+ ")\n"


def Menu():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filename", help="Save to file", dest="filename", metavar="FILE",default="results.statica")
    parser.add_argument("-u", "--url", action="store_true",dest="url",help="Do online static analysis [Future Use]", default=False)
    parser.add_argument("-c", "--comments", help="Save all comments into one file", dest="cfilepath",default="commentsFile.statica")
    parser.add_argument("-t", "--target",help="Target folder or file to scan",dest="scannedTarget",type=str,required=True)
    (options) = vars(parser.parse_args())

    if options['url'] is True:
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
    if result['cfilepath'] is not "":
        global cfile
        cfile = open(result['cfilepath'], 'w')
    else:
        cfile = None

    Helper.FileHandler = Helper.StoreFile(result['filename'])

    # Get Suspicious File List
    main_scanner = Scanner(result['scannedTarget'])
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

    if cfile is not None:
        cfile.close()

if __name__ == "__main__":
    main()
	# Online On Work
    #Spider.pages_scan("http://www.walla.co.il")