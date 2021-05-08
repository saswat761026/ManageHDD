import re
class Util:

    def __init__(self):
        self.weekDays = ("Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday")

    def get_season(self, month):
        if month==1 or month==2 or month==3:
            return "winter"
        elif month==4 or month==5 or month==6:
            return "spring"
        elif month==7 or month==8 or month==9:
            return "summer" 
        elif month==10 or month==11 or month==12:
            return "fall"

    def get_weekday(self, day):
        weekday = self.weekDays[day]
        return weekday    

    def getNumber(self, fileName, pattern):
        if fileName is None:
            return None
        matches = re.findall(pattern, fileName)
        return matches[0] if len(matches)>0 else None

    def getLastEpisode(self, episodes, pattern):
        for episode in reversed(episodes):
            res = re.findall(pattern ,episode)
            if len(res) > 0:
                return episode
        return None 

    def getEpisodes(self, episodes, pattern):
        files = []
        for episode in episodes:
            res = re.findall(pattern ,episode)
            if len(res) > 0:
                files.append(episode)
        return files     