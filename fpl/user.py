import requests

API_BASE_URL = "https://fantasy.premierleague.com/drf/"


class User(object):
    """
    A class representing a user of the Fantasy Premier League.
    """
    def __init__(self, user_id):
        self.id = user_id
        self._information = self._get_information()
        self._entry = self._information["entry"]

        #: The user's first name.
        self.first_name = self._entry["player_first_name"]
        #: The user's second name.
        self.second_name = self._entry["player_last_name"]
        #: The user's team's name.
        self.team_name = self._entry["name"]
        #: The user's email address.
        self.email = self._entry["email"]
        #: The user's favourite team.
        self.favourite_team = self._entry["favourite_team"]

        #: The user's region's ID.
        self.region_id = self._entry["player_region_id"]
        #: The user's region's name.
        self.region_name = self._entry["player_region_name"]
        #: The user's region's short ISO.
        self.region_short = self._entry["player_region_short_iso"]

        #: The user's overall points.
        self.overall_points = self._entry["summary_overall_points"]
        #: The user's overall rank.
        self.overall_rank = self._entry["summary_overall_rank"]

        #: The user's points in the current gameweek.
        self.gameweek_points = self._entry["summary_event_points"]
        #: The user's rank in the current gameweek.
        self.gameweek_rank = self._entry["summary_event_rank"]
        #: The amount of transfers made by the user in the current gameweek.
        self.gameweek_transfers = self._entry["event_transfers"]
        #: The gameweek the user started playing.
        self.gameweek_started = self._entry["started_event"]
        #: The point hit the user took in the current gameweek.
        self.gameweek_hit = self._entry["event_transfers_cost"]
        #: Information about the user's current gameweek performance.
        self.current_gameweek = self._entry["current_event"]

        #: The user's total transfers.
        self.total_transfers = self._entry["total_transfers"]
        #: The amount of money the user has in the bank.
        self.bank = self._entry["bank"] / 10.0
        #: The user's team's value.
        self.team_value = self._entry["value"] / 10.0
        #: The amount of free transfers the user currently has.
        self.free_transfers = self._entry["extra_free_transfers"]

        #: The user's cup status.
        self.cup_status = self._information["cup_status"]
        #: The user's cup matches.
        self.cup_matches = self._information["cup_matches"]

    def _get_information(self):
        """
        Returns some general information about the user.
        """
        return requests.get(
            "{}entry/{}/cup".format(API_BASE_URL, self.id)).json()

    @property
    def history(self):
        """
        Returns a dictionary containing the history of the user.
        """
        return requests.get(
            "{}entry/{}/history".format(API_BASE_URL, self.id)).json()

    @property
    def season(self):
        """
        Returns a list containing information about each of the seasons the
        user has participated in.
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
        Returns a list containing information about all the classic leagues
        that the user is currently participating in.
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
        Returns a dictionary containing information about the user's chip
        usage, automatic substitutions and picks, alongside general
        information about each gameweek.
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

        :param int player_id: The gameweek (1-38)
        """
        return self.picks[gameweek]["picks"]

    def chip(self, gameweek):
        """
        Returns the chip used by the user in the specified gameweek.

        :param int player_id: The gameweek (1-38)
        """
        return self.picks[gameweek]["active_chip"]

    def automatic_substitutions(self, gameweek):
        """
        Returns a list of the automatic substitutions of the user in the
        specified gameweek.

        :param int player_id: The gameweek (1-38)
        """
        return self.picks[gameweek]["automatic_subs"]

    @property
    def transfers(self):
        """
        Returns a dictionary containing information about all the transfers the
        user has made so far.
        """
        return requests.get(
            "{}entry/{}/transfers".format(API_BASE_URL, self.id)).json()

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
        Returns a list containing information about the user's transfer
        history.
        """
        return self.transfers["history"]

    def __str__(self):
        return "{} {} - {}".format(
            self.first_name, self.second_name, self.region_name)
