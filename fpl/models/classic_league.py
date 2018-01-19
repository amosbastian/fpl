import json
import requests

class ClassicLeague(object):
    """
    A class representing a classic league in the Fantasy Premier League.
    """
    def __init__(self, league):
        self.__dict__ = league