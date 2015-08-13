# Build by Idan Cohen
# Version 0.01 - Only Alpha

# Imports
import sys
import time
import Helper
from Core import Scanner
from DomXSS import Search as XSS_Search

def Main():
    if (len(sys.argv) != 2):
        print "Missing Argument: Statica.exe Folder"
        sys.exit(0)

    mainScanner = Scanner(sys.argv[1])
    filesToScan = mainScanner.FileLists
    
    fileFinished = Helper.Counter()
    fileWithXss = Helper.Counter()
    overallHits = Helper.Counter()
    time.sleep(1)
    for file in filesToScan:
        hits = XSS_Search(file)
        if (hits != 0):
            fileWithXss.Add()
            overallHits.Add(hits)
        fileFinished.Add()

    print "Found " + overallHits.String() + " Hits In " + fileWithXss.String() + " Files With domXSS Potential"

Main()
	