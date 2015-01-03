from conf import conf
from connection import IRC


class MisterRoboto:

    def __init__(self, irc):
        self.irc = irc
        self.socket = self.irc.sock

    def run(self):
        self.irc.connect()
        self.irc.auth()

        while True:
            response = self.socket.recv(2048).rstrip()

            if len(response) == 0:
                self.socket = self.irc.connect()
                self.socket = self.irc.auth()

            print(response.decode('UTF-8'))
            self.irc.ping_pong(response)


if __name__ == '__main__':
    irc = IRC(conf)
    bot = MisterRoboto(irc)
    bot.run()
