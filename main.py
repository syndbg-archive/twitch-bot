from conf import conf
from connection import IRC


class MisterRoboto:

    def __init__(self, socket):
        self.socket = socket

    def run(self):
        self.socket.connect()
        self.socket.auth()

        while True:
            response = self.socket.recv(2048).rstrip()

            if len(response) == 0:
                self.socket = self.socket.connect()
                self.socket = self.socket.auth()

            self.socket.ping_pong(response)


if __name__ == '__main__':
    irc = IRC(conf)
    bot = MisterRoboto(irc.sock)
