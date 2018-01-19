import json
import requests

class H2HLeague(object):
    """
    A class representing a h2h league in the Fantasy Premier League.
    """
    def __init__(self, league):
        self.__dict__ = league