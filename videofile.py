import os
import datetime

class VideoFile:
    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.timestamp = datetime.datetime.utcfromtimestamp(os.path.getmtime(filepath))
        self.displayName = self.timestamp.strftime("%A %d %B %Y %I:%M:%S%p")