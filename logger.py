import os

class Logger:
    def __init__(self):
        pass

    def log_write(filename, data):
        mode = "a+" if os.path.exists(filename) else "w+"
        with open(filename, "w+") as f:
            f.writelines(["%s\n" % item  for item in data]) 

    def log_read(filename):
        data = []
        if os.path.exists(filename):
            with open(filename, "r") as f:
                data = f.readlines()
        else:
            raise Exception(f"Log file with {filename} doesn't exists.")
        return data
    def create_download_obj(name, torrent_name, episode, quality, date):
        return{'name':name, 'torrent_name': torrent_name, 'episode': episode, 'quality': quality, 'date':date}            


