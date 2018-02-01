import json
import requests

API_BASE_URL = "https://fantasy.premierleague.com/drf/"

class User(object):
    """
    A class representing a user of the Fantasy Premier League.
    """
    def __init__(self, user_id):
        self.id = user_id
        self._information = self._information()
        self._entry = self._information["entry"]

        # General user information
        self.first_name = self._entry["player_first_name"]
        self.second_name = self._entry["player_last_name"]
        self.team_name = self._entry["name"]
        self.email = self._entry["email"]
        self.favourite_team = self._entry["favourite_team"]
        
        # Region information
        self.region_id = self._entry["player_region_id"]
        self.region_name = self._entry["player_region_name"]
        self.region_short = self._entry["player_region_short_iso"]
        
        # Overall score
        self.overall_points = self._entry["summary_overall_points"]
        self.overall_rank = self._entry["summary_overall_rank"]

        # Gameweek information
        self.gameweek_points = self._entry["summary_event_points"]
        self.gameweek_rank = self._entry["summary_event_rank"]
        self.gameweek_transfers = self._entry["event_transfers"]
        self.gameweek_started = self._entry["started_event"]
        self.gameweek_hit = self._entry["event_transfers_cost"]
        self.current_gameweek = self._entry["current_event"]
        
        # Transfer and team value information
        self.total_transfers = self._entry["total_transfers"]
        self.bank = self._entry["bank"] / 10.0
        self.team_value = self._entry["value"] / 10.0
        self.free_transfers = self._entry["extra_free_transfers"]

        # Cup information
        self.cup_status = self._information["cup_status"]
        self.cup_matches = self._information["cup_matches"]

    def _information(self):
        """
        Returns some general information about the user.
        """
        return requests.get("{}entry/{}/cup".format(API_BASE_URL,
            self.id)).json()

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
        Returns a list containing information about all the classic leagues that
        the user is currently participating in.
        """
        return self.leagues["classic"]

    @property
    def h2h(self):
        """
        Returns a list containing information about all the h2h leagues that
        the user is currently participating in.
        """
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

    def automatic_substitutions(self, gameweek):
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

    def __str__(self):
        return "{} {} - {}".format(self.first_name, self.second_name,
            self.region_name)