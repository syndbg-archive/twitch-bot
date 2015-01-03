import re
import socket
from sys import exit


class IRC:

    def __init__(self, config):
        self.conf = config
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        destination = '{0}:{1}'.format(self.conf.server, self.conf.port)
        try:
            self.sock.settimeout(30)
            if self.conf.verbose:
                print('Attempting to connect to', destination)
            self.sock.connect((self.conf.server, self.conf.port))
        except Exception as e:
            if self.conf.verbose:
                print('Failed to connect to', destination)
            exit(1)
        if self.conf.verbose:
            print('Connected to', destination)
        self.sock.settimeout(None)
        return self.sock

    def is_logged(self, response):
        response = response.decode('UTF-8')
        print(response)
        if 'Login unsuccessful' in response:
            return False
        return True

    def serialize(self, string):
        return bytes(string, 'UTF-8')

    def auth(self):
        if self.conf.auth_type == 'token':
            self.sock.send(self.serialize('PASS {0}\r\n'.format(self.conf.token)))
        elif self.conf.auth_type == 'simple':
            self.sock.send(self.serialize('USER {0}\n'.format(self.conf.username)))
            self.sock.send(self.serialize('PASS {0}\r\n'.format(self.conf.password)))
        else:
            raise ValueError('Invalid setting for auth_type')
        self.sock.send(self.serialize('NICK {0}\r\n'.format(self.conf.username)))
        response = self.sock.recv(1024)
        if self.is_logged(response):
            print('Successful auth!')
        else:
            print('Something went wrong :(')
        return self.sock

    def ping_pong(self, response):
        if response[:4] == 'PING':
            self.sock.send('PONG')

    def msg(self, channel, message):
        self.sock.send('PRIVMSG {0} :{1}\n'.format(channel, message.encode('utf-8')))

    def join(self, *channels):
        self.sock.send('JOIN {0}\r\n'.format(channels))

    def leave(self, *channels):
        self.sock.send('PART {0}\r\n'.format(channels))
