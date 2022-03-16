from configparser import ConfigParser


class Settings:
    def __init__(self):
        self._repo = ''
        self._movies = ''
        self._clients = ''
        self._rentals = ''
        self._ui = ''
        self.set_atr()

    def set_atr(self):
        config = ConfigParser()
        cfilepath = r'D:\Faculty\G\a10-913-Amalia-Duma\settings\settings.properties'
        config.read(cfilepath)
        self._repo = config.get('DatabaseSection', 'repository')
        self._movies = config.get('DatabaseSection', 'movies')
        self._clients = config.get('DatabaseSection', 'clients')
        self._rentals = config.get('DatabaseSection', 'rentals')
        self._ui = config.get('DatabaseSection', 'ui')

    @property
    def repo(self):
        return self._repo

    @property
    def movies(self):
        return self._movies

    @property
    def clients(self):
        return self._clients

    @property
    def rentals(self):
        return self._rentals

    @property
    def ui(self):
        return self._ui
