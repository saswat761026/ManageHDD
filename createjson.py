import os
import json
from jikanpy import Jikan
import datetime
import copy
from dateutil.parser import parse
from util import Util


class CreateJson:

    def __init__(self):
        self.util = Util()

    def loadjson(self, path):
        data = None
        with open(path, "r") as f:
            data = json.load(f)
        return data                       

    def get_json(self, req_anime_list, season, year):
        jikan = Jikan()
        animes_this_season = jikan.season(year=year, season=season)
        animes = []
        for anime in animes_this_season['anime']:
            for req_anime in req_anime_list:
                if anime['title'] == req_anime['name']:
                    ani = copy.deepcopy(anime)
                    ani['torrentname'] = req_anime['torrentname']
                    ani['quality'] = req_anime['quality']
                    animes.append(ani)
        return animes            


    def rearrange_animes_list(self, animes):
        req_json = {}
        for anime in animes:
            airing_date = parse(anime['airing_start'])
            day = self.util.get_weekday(airing_date.weekday())
            if day in req_json.keys():
                req_json[day].append(anime)
            else:
                req_json[day] = [anime]    
        return req_json        


    def create_json_file(self, filename, data):
        with open(filename, "w") as f:
            json.dump(data, f) 


    def CreateJson(self):
        now = datetime.datetime.now()
        current_date = now.day
        current_month = now.month
        current_year = now.year
        season = self.util.get_season(current_month)
        data = self.loadjson("AnimeToDownload.json")
        animes = self.get_json(data, season, current_year)
        animes_json = self.rearrange_animes_list(animes)
        if len(animes_json) > 0:
            self.create_json_file(f"{season}_{current_year}.json", animes_json)
        else:
            print('There is no content to write.')    

cj = CreateJson()
cj.CreateJson()