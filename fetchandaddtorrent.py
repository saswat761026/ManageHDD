import os
import json
import requests
from requests_html import HTML
import datetime
import re
from util import Util

class TorrentHandler:
    def __init__(self):
        self.util = Util()


    def loadjson(self, path):
        anime_to_download = None
        with open(path, "r") as f:
            anime_to_download = json.load(f)
        return anime_to_download

    def create_torrent_obj(self, links, textArr):
        obj = {}
        obj["name"] = textArr[0]
        #arr = re.findall("([0-9]\w+)", textArr[0])
        obj["date"] = textArr[5]
        obj["magnet"] = list(links[2].links)[0]
        arr = textArr[0].split('-')
        matches = re.findall("([0-9]\w+)", arr[1])
        obj["episode"] = matches[0]
        obj["quality"] = matches[1]
        obj["size"] = textArr[1]
        obj["isbatch"] = True if ('Batch' or 'batch' in textArr[0]) else False 
        return obj
        
            

    def assemble_torrents(self, html):
        torrents = []
        resultTable = html.find('#torrentListResults')
        try: 
            listTr = resultTable[0].find('tr')
            for element in listTr:
                textArr = element.text.split('\n')
                torrents.append(self.create_torrent_obj(element.find('a'), textArr))
        except:
            print("Something went wrong..")
        return torrents

    def get_torrents(self, animeName, pageNumber=1):
        name = animeName.replace(" ", "+")
        URL = f"https://nyaa.net/search/{pageNumber}?c=_&q=*{name}"
        result = requests.get(URL)
        html = HTML(html=result.text)
        torrents = self.assemble_torrents(html)
        return torrents


    def fetch_anime_list(self):
        todayWeekDay = datetime.datetime.today().weekday()
        current_year = datetime.datetime.today().year
        current_month = datetime.datetime.today().month
        season = self.util.get_season(current_month)
        data = self.loadjson(f"{season}_{current_year}.json")
        anime_list = data[self.util.get_weekday(todayWeekDay)]
        return anime_list

    def select_torrents(self, anime, torrents):
        print(anime)
        print(torrents)


    def torrent_handler(self):
        anime_list = self.fetch_anime_list()
        for anime in anime_list:
            torrentList = self.get_torrents(anime["title"])
            print(torrentList)
        



th = TorrentHandler()
th.torrent_handler()


