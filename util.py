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
