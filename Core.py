import sys
import os
import Helper


class Scanner:
    AllowFileType = ["html", "htm", "js"]
    AllowFilesName = ["jquery"]

    def __init__(self, path):
        if os.path.isdir(path) == False:
            print "Wrong Argument"
            sys.exit(0)

        self.FileLists = []
        self.FileScanned = Helper.Counter()
        self.FileFounds = Helper.Counter()
        self.Path = path

        print "Starting Scan of Folder: " + path
        self.Scan(path)
    def Scan(self, path):
        try:
            fileList = os.listdir(path)
            for file in fileList:
                self.FileScanned.Add()
                filePath = path + "\\" + file
                if os.path.isdir(filePath):
                    self.Scan(filePath)
                    continue

                isAllowed = True
                for allowed in Scanner.AllowFilesName:
                    if (allowed in file):
                        isAllowed = False
                        break
                if (isAllowed == False): continue

                spliter = filePath.split(".")
                if (len(spliter) < 2): continue
                Ext = spliter[len(spliter) - 1]
                if Ext in Scanner.AllowFileType:
                    self.FileFounds.Add()
                    self.FileLists.append(filePath)
        except WindowsError:
            return

        if (self.Path == path):
            print "Scanned " + self.FileScanned.String() + " Files - Found " + self.FileFounds.String() + " Intersting Files"
	