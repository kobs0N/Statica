import sys
import os
import Helper


class Scanner:
    AllowFileType = ["html", "htm", "js"]
    AllowFilesName = ["jquery"]

    def __init__(self, path):
        if os.path.isdir(path) is False:
            print "Wrong Argument"
            sys.exit(0)

        self.FileLists = []
        self.FileScanned = Helper.Counter()
        self.FileFounds = Helper.Counter()
        self.Path = path

        print "Starting Scan of Folder: " + path
        self.scan(path)

    def scan(self, path):
        try:
            file_list = os.listdir(path)
            for file_name in file_list:
                self.FileScanned.add()
                file_path = path + "\\" + file_name
                if os.path.isdir(file_path):
                    self.scan(file_path)
                    continue

                is_allowed = True
                for allowed in Scanner.AllowFilesName:
                    if allowed in file_name:
                        is_allowed = False
                        break
                if is_allowed is False: continue

                split_point = file_path.split(".")
                if len(split_point) < 2: continue
                ext = split_point[len(split_point) - 1]
                if ext in Scanner.AllowFileType:
                    self.FileFounds.add()
                    self.FileLists.append(file_path)
        except WindowsError:
            return

        if self.Path == path:
            print "Scanned " + self.FileScanned.string() + " Files - Found " + \
                  self.FileFounds.string() + " Interesting Files"
