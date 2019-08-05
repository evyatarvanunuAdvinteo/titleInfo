import ftplib
import os
import param
import re
import datetime


class Tool:
    ftp = None
    dest_dir = None

    def __init__(self):

        self.dest_dir = os.getcwd()
        self.connect()

    def connect(self, host=param.FTP_HOST, user=param.FTP_USER, password=param.FTP_PASSWORD):
        self.ftp = ftplib.FTP(host)
        self.ftp.login(user, password)

    def download(self, file_name, dest=None):
        if not dest:
            dest = self.dest_dir

        file_path = dest + '/' + file_name

        if not os.path.isfile(file_path):
            try:
                self.ftp.retrbinary('RETR {}'.format(file_name), open(file_path, 'wb').write)
            except ftplib.error_temp:
                self.connect()
                self.ftp.retrbinary('RETR {}'.format(file_name), open(file_path, 'wb').write)

            return 1

        return 0

    def get_file_date(self, file_name):

        try:
            timestamp = self.ftp.sendcmd('MDTM ' + file_name)
        except ftplib.error_temp:
            self.connect()
            timestamp = self.ftp.sendcmd('MDTM ' + file_name)


        timestamp = re.search('[0-9]*$', timestamp).group()
        time_tuple = (int(timestamp[0:4]), int(timestamp[4:6]), int(timestamp[6:8]),
                      int(timestamp[8:10]), int(timestamp[10:12]), int(timestamp[12:14]))

        return datetime.datetime(*time_tuple[0:6])

    def get_file_list(self, remote_dir='/'):
        try:
            return self.ftp.nlst(remote_dir)
        except ftplib.error_temp:
            self.connect()
            return self.ftp.nlst(remote_dir)





















