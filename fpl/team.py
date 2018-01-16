import json
import requests

API_BASE_URL = "https://fantasy.premierleague.com/drf/"

class Team(object):
    """
    A class representing a real team in the Fantasy Premier League.
    """
    def __init__(self, team):
        self.__dict__ = team
