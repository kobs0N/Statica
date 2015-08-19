import sys, os, thread
import Helper
from multiprocessing.dummy import Pool as ThreadPool
from datetime import datetime


class Scanner:
    AllowFileType = ["html", "htm", "js"]
    AllowFilesName = ["jquery"]
    TimeStarted = datetime.now()
#
    FileScanned = Helper.Counter()
    FileFounds = Helper.Counter()
    FileLists = []
    Threads = ThreadPool() # We have support in multithread but its seems even slower

    def __init__(self, path):
        if os.path.isdir(path) is False:
            print "Wrong Argument"
            sys.exit(0)

        self.Path = path

        TimeStarted = datetime.now()
        print "Starting Scan of Folder: " + path + " at: " + Helper.ToTime(TimeStarted)
        self.scan(path, False)

    def scan(self, path, top = False):
        try:
            file_list = os.listdir(path)
            for file_name in file_list:
                file_path = path + "\\" + file_name
                if os.path.isdir(file_path):
                    if top is True:
                        Scanner.Threads.map(self.scan,(file_path,))
                    else:
                        self.scan(file_path)
                    continue
                Scanner.FileScanned.add()
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
                    Scanner.FileFounds.add()
                    Scanner.FileLists.append(file_path)
        except WindowsError:
            return

        if self.Path == path:
            Scanner.Threads.close()
            Scanner.Threads.join()

            timeToke = datetime.now() - Scanner.TimeStarted
            print "Scanned " + Scanner.FileScanned.string() + " Files - Found " + \
                  Scanner.FileFounds.string() + " Interesting Files (" + str(timeToke)+ ")\n"
