import os
import json
from util import Util
from logger import Logger
import re

class DirectoryDetails:
    def __init__(self):
        self.logger = Logger()
        self.util = Util()
        self.ingoreDir = ['/run/media/avish/Elements/Series/Anime/Dragonball GT/Season 1']
        self.numberRegex = "[0-9]+"
        self.episodeRegex = "([0-9]\w+)"
        self.lastEpisodeRegex = "(\.mp4|\.webm|\.mpg|\.avi|\.flv|\.wmv|\.m4v|\.mkv|\.avchd|\.mov)$"

           

    def createDirectoryDetails(self):
        filteredDirctionary = {}

        dirAndFiles = {}
        for (dirpath, dirnames, filenames) in os.walk("/run/media/avish/Elements/Series/Anime"):
            dirAndFiles[dirpath] = filenames
            
        r = re.compile("^([\/A-Za-z0-9\-\'\.\!\/ ])+.(Season )\d+$")
        for dirc in dirAndFiles.keys():
            if dirc not in self.ingoreDir:
                s = r.fullmatch(dirc)
                if s:
                    dircArr = dirc.split('/')
                    name = dircArr[len(dircArr)-2]
                    season = dircArr[len(dircArr)-1]
                    seasonNumber = int(self.util.getNumber(season, self.numberRegex))
                    episodes = dirAndFiles[dirc]
                    if name in filteredDirctionary.keys():
                        if seasonNumber > filteredDirctionary[name]['season number']:
                            filteredDirctionary[name]['season'] = season
                            filteredDirctionary[name]['season number'] = seasonNumber
                            filteredDirctionary[name]['directory'] = os.path.join(*dircArr)
                            filteredDirctionary[name]['episode'] = re.split('(\d+)', self.util.getNumber(self.util.getLastEpisode(episodes, self.lastEpisodeRegex), self.episodeRegex))[0]
                            filteredDirctionary[name]['episode count'] = dirAndFiles[dirc]
                    else:
                        filteredDirctionary[name] = {}
                        filteredDirctionary[name]['name'] = name
                        filteredDirctionary[name]['season'] = season
                        filteredDirctionary[name]['season number'] = seasonNumber
                        filteredDirctionary[name]['directory'] = os.path.join(*dircArr)
                        filteredDirctionary[name]['episode'] = re.split('(\d+)', self.util.getNumber(self.util.getLastEpisode(episodes, self.lastEpisodeRegex), self.episodeRegex))[0]
                        filteredDirctionary[name]['episode count'] = dirAndFiles[dirc] 
        return filteredDirctionary
    def createList(self, dirDetails):
        arr = []
        for key in dirDetails.keys():
            arr.append(dirDetails[key])
        return arr    

    def createDirectoryLogs(self):
        dirDetails = self.createDirectoryDetails()
        dirDetailList = self.createList(dirDetails)
        self.logger.log_write('directory_logger.json', dirDetailList)




dd = DirectoryDetails()
dd.createDirectoryLogs()
        
