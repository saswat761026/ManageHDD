import os
import json
from logger import Logger
import re

class DirectoryDetails:
    def __init__(self):
        self.logger = Logger()

    def createDirectoryDetails(self):
        listOfDirectories = [x[0] for x in os.walk("/run/media/avish/Elements/Series/Anime")]
        listOfDirectories.sort(reverse=True)
        filteredList = []
        for dirc in listOfDirectories:
            s = re.match('^\/([a-zA-Z\/ ]\w+)+.(Season )\d$', dirc)
            if s:
                print(s)
                if dirc not in filteredList:
                    filteredList.append(dirc)
        print(filteredList)


dd = DirectoryDetails()
dd.createDirectoryDetails()
        
