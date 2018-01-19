import json
import requests

API_BASE_URL = "https://fantasy.premierleague.com/drf/"

class Player(object):
    """
    A class representing a player in the Fantasy Premier League.
    """
    def __init__(self, player_id):
        self.id = player_id

    @property
    def specific(self):
        """
        Returns the player with the specific player_id.
        """
        return requests.get("{}element-summary/{}".format(API_BASE_URL,
            self.id)).json()

    @property
    def additional(self):
        """
        Returns additional information that isn't included in the other list of
        players.
        """
        response = requests.get("{}elements".format(API_BASE_URL)).json()
        for player in response:
            if player["id"] == self.id:
                return player