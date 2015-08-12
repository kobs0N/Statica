import sys
import os

class Scanner:
    AllowFileType = ["html", "html", "js"]

    def __init__(self, path):
        if os.path.isdir(path) == False:
            print "Wrong Argument"
            sys.exit(0)

        self.FileLists = []
        self.FileScanned = 0
        self.FileFounds = 0
        self.Path = path

        print "Starting Scan Of Folder: " + path
        self.Scan(path)
    def Scan(self, path):
        try:
            fileList = os.listdir(path)
            for file in fileList:
                self.FileScanned = self.FileScanned + 1
                filePath = path + "\\" + file
                if os.path.isdir(filePath):
                    self.Scan(filePath)
                    continue
                spliter = filePath.split(".")
                if (len(spliter) < 2): continue
                Ext = spliter[1]
                if Ext in Scanner.AllowFileType:
                    self.FileFounds = self.FileFounds + 1
                    self.FileLists.append(filePath)
        except WindowsError:
            return

        if (self.Path == path):
            print "Scanned " + str(self.FileScanned) + " Files - Found " + str(self.FileFounds) + " Intersting Files"
	