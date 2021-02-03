import os
import json
import requests
from requests_html import HTML
import datetime
import re
from util import Util
from logger import Logger

class TorrentHandler:
    def __init__(self):
        self.util = Util()
        self.logger = Logger()

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

    def make_https_call(self, name, pageNumber=1):
         URL = f"https://nyaa.net/search/{pageNumber}?c=_&q=*{'Yakusoku+no+Neverland+2nd'}"
         result = requests.get(URL)
         html = HTML(html=result.text)
         return html    

    def get_torrents(self, anime, pageNumber=1):
        search_query = anime["title"]
        name = search_query.replace(" ", "+")
        html = self.make_https_call(name, pageNumber)     
        if 'No results found' in html.text:
            for query in anime['search_queries']:
                name = query.replace(" ", "+")
                html = self.make_https_call(name, pageNumber)
                if 'No results found' not in html.text:
                    break
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

    def select_torrents(self, anime, torrents, download_logs):
        pass        

    def torrent_handler(self):
        anime_list = self.fetch_anime_list()
        download_logs = self.logger.log_read('download_logger.json')
        for anime in anime_list:
            torrentList = self.get_torrents(anime)
            self.select_torrents(anime, torrentList, download_logs)


        
th = TorrentHandler()
th.torrent_handler()


