import json
import requests

API_BASE_URL = "https://fantasy.premierleague.com/drf/"

class Player(object):
    """
    A class representing a player in the Fantasy Premier League.
    """
    def __init__(self, player):
        self.__dict__ = player
        self.additional = self._additional()

    def _additional(self):
        """
        Returns additional information that isn't included in the other list of
        players.
        """
        return requests.get("{}element-summary/{}".format(API_BASE_URL,
            self.id)).json()

    @property
    def history_past(self):
        """
        Returns a list containing information about the player's performance
        in previous seasons.
        """
        return self.additional["history_past"]

    @property
    def fixtures_summary(self):
        """
        Returns a list containing a summary of the player's upcoming fixtures.
        """
        return self.additional["fixtures_summary"]

    @property
    def explain(self):
        """
        Returns a list containing some information about something (I'm not
        exactly sure what it is yet).
        """
        return self.additional["explain"]

    @property
    def history_summary(self):
        """
        Returns a list containing a summary of the player's history.
        """
        return self.additional["history_summary"]

    @property
    def fixtures(self):
        """
        Returns a list of the player's upcoming fixtures.
        """
        return self.additional["fixtures"]

    @property
    def history(self):
        """
        Returns a list of the player's history.
        """
        return self.additional["history"]