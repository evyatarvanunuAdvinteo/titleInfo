import param
import os
import json
import time


class LocalDir:
    meta_file_path = None
    meta_dict = None
    path = None
    categories = None
    last_download = None
    logfile_path = None

    def __init__(self, path):
        if path[-1] not in ['/', '\\']:
            path = path + '/'
        self.path = path
        self.meta_file_path = path + 'metafiles/metadata.json'
        self.categories_file_path = path + 'metafiles/categories.json'
        self.logfile_path = path + 'metafiles/logfile.txt'

        with open(self.meta_file_path, 'r') as file:
            self.meta_dict = json.load(file)

        with open(self.categories_file_path, 'r') as file:
            self.categories = json.load(file)
        self.last_download = self.meta_dict['last_download']

    def get_video_files(self):

        for file_name in os.listdir(self.path):
            _, file_ext = os.path.splitext(file_name)
            if os.path.isfile(self.path + file_name) and file_ext in param.VIDEO_FILE_FORMATS:
                yield self.path + file_name

    def get_xml_files(self):

        for file_name in os.listdir(self.path):
            _, file_ext = os.path.splitext(file_name)
            if os.path.isfile(self.path + file_name) and file_ext == 'xml':
                yield self.path + file_name

    def is_uploaded(self, title):
        if self.meta_dict['uploaded'].get(title):
            return True
        return False

    def insert_to_uploaded(self, title):

        if self.is_uploaded(title):
            raise ValueError('file already uploaded')

        self.meta_dict['uploaded'][title] = 1

    def export_meta_to_file(self):
        with open(self.meta_file_path, 'w') as file:
            json.dump(self.meta_dict, file, indent=4, separators=(',', ': '), sort_keys=True)

    def export_categories_to_file(self):
        if not self.categories:
            return None
        with open(self.categories_file_path, 'w') as file:
            json.dump(self.categories, file, indent=4, separators=(',', ': '), sort_keys=True)

    def set_last_download(self, timestamp):
        if not isinstance(timestamp, float):
            raise TypeError('timestamp most be float')
        self.last_download = timestamp
        self.meta_dict['last_download'] = self.last_download
        self.export_meta_to_file()

    def add_message_to_logfile(self, title, text=None):
        with open(self.logfile_path, 'a') as file:
            massage = """\n#############{title}#############\n{time}\n{text}\n###############################\n"""
            file.write(massage.format(title=title, text=text, time=time.asctime()))










