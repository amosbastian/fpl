import json
import requests

API_BASE_URL = "https://fantasy.premierleague.com/drf/"

class ClassicLeague(object):
    """
    A class representing a classic league in the Fantasy Premier League.
    """
    def __init__(self, league):
        self.__dict__ = league