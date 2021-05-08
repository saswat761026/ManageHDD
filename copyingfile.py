import os
import re
import shutil
from util import Util
from logger import Logger


class Copy:
    def __init__(self, src_dir, des_dir):
        self.srcDir = src_dir
        self.desDir = des_dir
        self.episodeRegex = "(\.mp4|\.webm|\.mpg|\.avi|\.flv|\.wmv|\.m4v|\.mkv|\.avchd|\.mov)$"
        self.util = Util()
        self.logger = Logger()

    def copyfile(self, src, des, filesToMove):
        src_path = os.path.join(self.abs_src_dir, src)
        files_present = os.listdir(src_path)

        des_path = os.path.join(self.abs_des_dir, des)

        print(f"Total number of files to move{len(filesToMove)}\n")

        for item in filesToMove:
            if shutil.move(os.path.join(src_path, item), os.path.join(des_path, item)):
                print(f"Successfully moved {item}\n")
            else:
                print(f"Failed to move {item}\n")    
        print(f"Completly moved the pattern: {pattern}")



    def selectFilesToMove(self):
        dirAndFiles = {}
        for (dirpath, dirnames, filenames) in os.walk(self.srcDir):
            dirAndFiles[dirpath] = filenames
        print(dirAndFiles)
        r = re.compile("")
        filesToTransfer = []
        for key in dirAndFiles.keys():
            files = dirAndFiles[key]
            episodes = self.util.getEpisodes(files, self.episodeRegex)
            if len(episodes) > 0:
                filesToTransfer.extend([os.path.join(key,episode) for episode in episodes])
        return filesToTransfer    
            
        





         
cp = Copy("/run/media/avish/Elements/Series/Anime", "/home/avish")
filesToTransfer = cp.selectFilesToMove()







