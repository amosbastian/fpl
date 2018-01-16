import json
import requests

API_BASE_URL = "https://fantasy.premierleague.com/drf/"

class User(object):
    """
    A class representing a user of the Fantasy Premier League.
    """

    def __init__(self, user_id):
        self.id = user_id

        self.cup = self._cup()
        self.entry = self._entry()
        self.history = self._history()
        self.leagues = self._leagues()
        self.leagues_entered = self._leagues_entered()
        self.picks = self._picks()
        self.transfers = self._transfers()

    def _cup(self):
        """
        Returns a dictionary with information about the cup progression of the
        user.
        """
        return requests.get("{}entry/{}/cup".format(API_BASE_URL,
            self.id)).json()

    def _entry(self):
        """
        Returns a dictionary containing information about the user.
        """
        return requests.get("{}entry/{}".format(API_BASE_URL,
            self.id)).json()["entry"]

    def _history(self):
        """
        Returns a dictionary containing the history of the user.
        """
        return requests.get("{}entry/{}/history".format(API_BASE_URL,
            self.id)).json()

    def _leagues(self):
        """
        Returns a dictionary with information about all leagues that the user is
        participating in.
        """
        return requests.get("{}entry/{}".format(API_BASE_URL, self.id)).json()

    def _leagues_entered(self):
        """
        Returns a dictionary with information about all leagues that the user is
        participating in.
        """
        return requests.get("{}leagues-entered/{}".format(API_BASE_URL,
            self.id)).json()

    def _picks(self):
        """
        Returns a dictionary containing all the picks of the user.
        """
        picks = {}
        for gameweek in range(1, 39):
            pick = requests.get("{}entry/{}/event/{}/picks".format(
                API_BASE_URL, self.id, gameweek))

            if pick.status_code == 404:
                return picks

            picks[gameweek] = pick.json()

        return picks

    def _transfers(self):
        """
        Returns a dictionary with all the transfers made by the user.
        """
        return requests.get("{}entry/{}/transfers".format(API_BASE_URL,
            self.id)).json()

    @property
    def name(self):
        return "{} {}".format(self.first_name, self.last_name)

    @property
    def first_name(self):
        return self.entry["player_first_name"]

    @property
    def last_name(self):
        return self.entry["player_last_name"]

    @property
    def region_long(self):
        return self.entry["player_region_name"]

    @property
    def region_short(self):
        return self.entry["player_region_short_iso"]

    @property
    def total_transfers(self):
        return self.entry["total_transfers"]

    @property
    def joined_time(self):
        return self.entry["joined_time"]

    @property
    def team_value(self):
        return self.entry["value"] / 10.0

    @property
    def bank(self):
        return self.entry["bank"] / 10.0

    @property
    def total_value(self):
        return self.team_value * self.bank

    @property
    def favourite_team(self):
        return self.entry["favourite_team"]

if __name__ == '__main__':
    user = User(3523615)
    print(user.name)