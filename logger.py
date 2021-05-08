import os
import json

class Logger:
    def __init__(self):
        pass

    def log_write(self, filename, data):
        mode = "a+" if os.path.exists(filename) and filename !='directory_logger.json' else "w+"
        with open(filename, mode, encoding='utf-8') as f:
            json.dump(data, f)

    def log_read(self, filename):
        data = []
        if os.path.exists(filename):
            with open(filename, "r", encoding='utf-8') as f:
                data = json.load(f)
        else:
            raise Exception(f"Log file with {filename} doesn't exists.")
        return data

    def create_download_obj(self, name, torrent_name, episode, quality, folder_name, iscontinuing,date):
        return{'name':name, 'torrent_name': torrent_name, 'episode': episode, 'quality': quality, 'folder name':folder_name, 'is continuing': iscontinuing,'date':date}            


