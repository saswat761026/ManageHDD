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


