import os
import datetime
from dateutil.parser import parse
from createdirectorylist import DirectoryDetails
from createanimejson import CreateAnimeJson
from fetchandaddtorrent import TorrentHandler
from copyingfile import Copy
from logger import Logger
from util import Util


if __name__=="__main__":
    ca = CreateAnimeJson()
    ca.createjson()
    dd = DirectoryDetails()
    dd.createDirectoryLogs()
