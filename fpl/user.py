import json
import requests

API_BASE_URL = "https://fantasy.premierleague.com/drf/"

class User(object):
    """
    A class representing a user of the Fantasy Premier League.
    """
    def __init__(self, user_id):
        self.id = user_id
        self.__dict__ = self.entry

    @property
    def cup(self):
        """
        Returns a dictionary with information about the cup progression of the
        user.
        """
        return requests.get("{}entry/{}/cup".format(API_BASE_URL,
            self.id)).json()

    @property
    def entry(self):
        """
        Returns a dictionary containing information about the user.
        """
        return self.cup["entry"]

    @property
    def history(self):
        """
        Returns a dictionary containing the history of the user.
        """
        return requests.get("{}entry/{}/history".format(API_BASE_URL,
            self.id)).json()

    @property
    def season(self):
        """
        Returns a list containing information about each of the seasons the user
        has participated in.
        """
        return self.history["season"]

    @property
    def chips(self):
        """
        Returns a list containing information about the usage of the player's
        chips.
        """
        return self.history["chips"]

    @property
    def leagues(self):
        """
        Returns a dictionary containing information about all the leagues that
        the user is participating in.
        """
        return self.history["leagues"]

    @property
    def classic(self):
        """
        Returns a list containing information about all the leagues that the
        user is currently participating in.
        """
        return self.leagues["classic"]

    @property
    def h2h(self):
        return self.leagues["h2h"]

    @property
    def picks(self):
        """
        Returns a dictionary containing information about the user's chip usage,
        automatic substitutions and picks, alongside general information about
        each gameweek.
        """
        picks = {}
        for gameweek in range(1, 39):
            pick = requests.get("{}entry/{}/event/{}/picks".format(
                API_BASE_URL, self.id, gameweek))

            if pick.status_code == 404:
                return picks

            picks[gameweek] = pick.json()

        return picks

    def team(self, gameweek):
        """
        Returns a list of the user's team in the specified gameweek.
        """
        return self.picks[gameweek]["picks"]

    def chip(self, gameweek):
        """
        Returns the chip used by the user in the specified gameweek.
        """
        return self.picks[gameweek]["active_chip"]

    def automatic_subs(self, gameweek):
        """
        Returns a list of the automatic substitutions of the user in the
        specified gameweek.
        """
        return self.picks[gameweek]["automatic_subs"]

    @property
    def transfers(self):
        """
        Returns a dictionary containing information about all the transfers the
        user has made so far.
        """
        return requests.get("{}entry/{}/transfers".format(API_BASE_URL,
            self.id)).json()

    @property
    def wildcards(self):
        """
        Returns a list containing information about the usage of the player's
        wildcard(s).
        """
        return self.transfers["wildcards"]

    @property
    def transfer_history(self):
        """
        Returns a list containing information about the user's transfer history.
        """
        return self.transfers["history"]