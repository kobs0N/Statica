import sys
import time
from Core import Scanner
from DomXSS import Search as XSS_Search

def Main():
    if (len(sys.argv) != 2):
        print "Missing Argument: Statica.exe Folder"
        sys.exit(0)

    mainScanner = Scanner(sys.argv[1])
    filesToScan = mainScanner.FileLists
    fileAmount = mainScanner.FileFounds
    fileFinished = 0
    fileWithXss = 0
    overallHits = 0
    time.sleep(1)
    for file in filesToScan:
        hits = XSS_Search(file)
        if (hits != 0):
            fileWithXss = fileWithXss + 1
            overallHits = overallHits + hits
        fileFinished = fileFinished + 1

    print "Found " + str(overallHits) + " Hits In " + str(fileWithXss) + " Files With XSS Potential"

Main()
	