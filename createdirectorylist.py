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
        counter = 0
        notMatch = 'Not Matched'
        # with open('dirList.txt', 'w') as u:
        #     u.writelines([f'{s}\n' for s in listOfDirectories])
        f = open('print.txt', 'a+')
        r = re.compile('^\/([a-zA-Z\/ ]\w+)+.(Season )\d$')
        for dirc in listOfDirectories:
            counter = counter + 1
            s = r.match(dirc)
            f.write(f'counter: {counter} directory: {dirc}, regex:{s.groups() if s else notMatch}')
            if s:
                print(s)
                if dirc not in filteredList:
                    filteredList.append(dirc)
            if counter>200:
                break
        f.close()            
        print(filteredList)


dd = DirectoryDetails()
dd.createDirectoryDetails()
        
