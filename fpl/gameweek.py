import json
import requests

API_BASE_URL = "https://fantasy.premierleague.com/drf/"

class Gameweek(object):
    """
    A class representing a gameweek of the Fantasy Premier League
    """
    def __init__(self, gameweek):
        self.__dict__ = gameweek
        self.additional = self._additional()

    def _additional(self):
        return requests.get("{}event/{}/live".format(API_BASE_URL,
            self.id)).json()

    @property
    def fixtures(self):
        return self.additional["fixtures"]