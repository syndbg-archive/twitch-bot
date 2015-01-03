import socket

from config import conf


class IRC:

    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        try:
            self.sock.settimeout(30)
            self.sock.connect(conf.server, conf.port)
        except Exception as e:
            print('Attempted to connect to {0}:{1}.'.format(conf.server, conf.port))
            raise e

        self.sock.settimeout(None)
        return self.sock

    def auth(self):
        self.sock.send('USER {0}'.format(conf.username))
        self.sock.send('PASSWORD {0}'.format(conf.password))
        self.sock.send('NICK {0}'.format(conf.username))
