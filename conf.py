from datetime import date

import settings


class MissingSettingException(Exception):
    pass


class Config:

    def __init__(self, **kwargs):
        self.defaults = kwargs

    def __getattr__(self, name):
        try:
            return getattr(settings, name)
        except Exception:
            if name not in self.defaults:
                raise MissingSettingException('Missing setting {}'.format(name))


def pretty_logfile(date):
    return '{day}-{month}-{year}'.format(day=date.day, month=date.month, year=date.year)


if __name__ != '__main__':
    conf = Config(
        server='irc.twitch.tv',
        port=6667,
        auth_type='simple',  # or oauth
        verbose=False,
        logging=False,
        logfile=pretty_logfile(date.today())
    )
