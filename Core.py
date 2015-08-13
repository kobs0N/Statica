import sys
import os
import Helper


class Scanner:
    AllowFileType = ["html", "html", "js"]

    def __init__(self, path):
        if os.path.isdir(path) == False:
            print "Wrong Argument"
            sys.exit(0)

        self.FileLists = []
        self.FileScanned = Helper.Counter()
        self.FileFounds = Helper.Counter()
        self.Path = path

        print "Starting Scan Of Folder: " + path
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
                spliter = filePath.split(".")
                if (len(spliter) < 2): continue
                Ext = spliter[1]
                if Ext in Scanner.AllowFileType:
                    self.FileFounds.Add()
                    self.FileLists.append(filePath)
        except WindowsError:
            return

        if (self.Path == path):
            print "Scanned " + self.FileScanned.String() + " Files - Found " + self.FileFounds.String() + " Intersting Files"
	