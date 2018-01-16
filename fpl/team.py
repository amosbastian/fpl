import json
import requests

class Team(object):
    """
    A class representing a real team in the Fantasy Premier League.
    """
    def __init__(self, team):
        self.__dict__ = team
