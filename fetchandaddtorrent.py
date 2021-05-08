import os
import json
import requests
from requests_html import HTML
import datetime
import re
from util import Util
from logger import Logger
from dateutil.parser import parse
import sys , subprocess


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
        obj["date"] = parse(textArr[5])
        obj["magnet"] = list(links[2].links)[0]
        arr = textArr[0].split('-')
        matches = re.findall("([0-9]\w+)", arr[1])
        obj["episode"] = re.split('(\d+)', matches[0])[0]
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
    
    def get_log(self, anime,logs,property):
        reqLog = None
        for log in reversed(logs):
            if anime[property] == log['name']:
                reqLog = log
                break
        return reqLog    

    def apply_torrent_policies(self, anime, torrentList):
        torrentNames = anime['torrentnames'].split(' | ')
        qulities = anime['quality'].split(' | ')
        obj = {}
        for tn in torrentNames:
            for qu in qulities:
                for torrent in torrentList:
                    if tn in torrent['name'] and qu == torrent['quality']:
                        if f'{tn}_{qu}' in obj.keys():
                            obj[f'{tn}_{qu}'].append(torrent)
                        else:
                            obj[f'{tn}_{qu}'] = [torrent]
        torrents = []
        for key in obj.keys():
            max = -1
            if len(obj[key]) > max:
                max = len(obj[key])
                torrents = obj[key]
        return torrents

    def select_torrents(self, anime, torrents, download_logs, directory_details):
        dlog = self.get_log(anime, download_logs, 'title')
        dirlog = self.get_log(anime, directory_details, 'folder_name')
        req_torrent_list = None
        if anime['airing_start'].astimezone() < datetime.datetime.now().astimezone():
            if dlog != None:
                req_torrents = [torrent for torrent in torrents if torrent['date'].astimezone()>=dlog['date'].astimezone() and torrent['date'].astimezone()<=datetime.datetime.now().astimezone()]
            elif dirlog != None:
                req_torrents = [torrent for torrent in torrents if torrent['episode'] > dirlog['last_episode']]
            else:
                req_torrents = [torrent for torrent in torrents if torrent['date'].astimezone()>=anime['airing_start'].astimezone() and torrent['date'].astimezone()<=datetime.datetime.now().astimezone()]
            req_torrent_list = self.apply_torrent_policies(anime, req_torrents)    
        req_torrent_list                     

    def open_magnet(self, magnet):
            """Open magnet according to os."""
            if sys.platform.startswith('linux'):
                subprocess.Popen(['xdg-open', magnet],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            elif sys.platform.startswith('win32'):
                os.startfile(magnet)
            elif sys.platform.startswith('cygwin'):
                os.startfile(magnet)
            elif sys.platform.startswith('darwin'):
                subprocess.Popen(['open', magnet],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            else:
                subprocess.Popen(['xdg-open', magnet],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    def torrent_handler(self):
        anime_list = self.fetch_anime_list()
        download_logs = self.logger.log_read('download_logger.json')
        copy_logs = self.logger.log_read('copy_logger.json')
        directory_details = self.logger.log_read('directory_logger.json')

        for anime in anime_list:
            torrentList = self.get_torrents(anime)
            selectedTorrents = self.select_torrents(anime, torrentList, download_logs, directory_details)
            for torrent in selectedTorrents:
                self.open_magnet(torrent['magnet'])
                obj = self.logger.create_download_obj(anime['title'], torrent['name'], torrent['episode'], torrent['quality'], anime['folder_name'], anime['continuing'] ,datetime.datetime.now())
                self.logger.log_write('download_logger.json', obj)

        
th = TorrentHandler()
th.torrent_handler()


