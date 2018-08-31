import requests

from ..constants import API_URLS
from ..utils import team_converter


def valid_gameweek(gameweek):
    """Returns True if the gameweek is valid."""
    if not isinstance(gameweek, int) and (gameweek < 1 or gameweek > 38):
        raise "Gameweek must be a number between 1 and 38."
    return True


class User():
    """A class representing a user of the Fantasy Premier League."""
    def __init__(self, user_id, session):
        self.user_id = user_id
        self._session = session
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
        self.favourite_team = team_converter(self._entry["favourite_team"])

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

        #: Account deletion status.
        self.deleted = self._entry["deleted"]

    def _get_information(self):
        """Returns some general information about the user."""
        return requests.get(API_URLS["user_cup"].format(self.user_id)).json()

    @property
    def history(self):
        """Returns a dictionary containing the history of the user."""
        return requests.get(API_URLS["user_history"].format(
            self.user_id)).json()

    @property
    def season_history(self):
        """Returns a list containing information about each of the seasons the
        user has participated in.
        """
        return self.history["season"]

    @property
    def chips(self):
        """Returns a list containing information about the usage of the
        player's chips.
        """
        return self.history["chips"]

    @property
    def leagues(self):
        """Returns a dictionary containing information about all the leagues
        that the user is participating in.
        """
        return self.history["leagues"]

    @property
    def classic(self):
        """Returns a list containing information about all the classic leagues
        that the user is currently participating in.
        """
        return self.leagues["classic"]

    @property
    def h2h(self):
        """Returns a list containing information about all the h2h leagues that
        the user is currently participating in.
        """
        return self.leagues["h2h"]

    @property
    def picks(self):
        """Returns a dictionary containing information about the user's chip
        usage, automatic substitutions and picks, alongside general
        information about each gameweek.
        """
        picks = {}
        for gameweek in range(1, 39):
            team = requests.get(API_URLS["user_picks"].format(
                self.user_id, gameweek))

            if team.status_code == 404:
                return picks

            picks[gameweek] = team.json()

        return picks

    def my_team(self):
        """Returns a logged in user's current team."""
        if not self._session:
            raise "User must be logged in."

        response = self._session.get(API_URLS["user_team"].format(
            self.user_id))
        return response.json()["picks"]

    def team(self, gameweek=None):
        """Returns a list of all of the user's teams so far, or the user's team
        in the specified gameweek.

        :param int gameweek: A gameweek (1-38)
        """
        if gameweek:
            valid_gameweek(gameweek)
            return self.picks[gameweek]["picks"]

        teams = []
        for gameweek_id in range(1, 39):
            try:
                team = self.picks[gameweek_id]["picks"]
                teams.append(team)
            except KeyError:
                return teams

        return teams

    def chip(self, gameweek=None):
        """Returns a list of chips used by the user so far, or the chip used
        by the user in the specified gameweek.

        :param int gameweek: A gameweek (1-38)
        """
        if gameweek:
            valid_gameweek(gameweek)
            return self.picks[gameweek]["active_chip"]

        active_chips = []
        for gameweek_id in range(1, 39):
            try:
                active_chip = self.picks[gameweek_id]["active_chip"]
                active_chips.append(active_chip)
            except KeyError:
                return active_chips

        return active_chips

    def automatic_substitutions(self, gameweek=None):
        """Returns a list of all automatic substitions made for the user so
        far, or the automatic substitutions made for the user in the specified
        gameweek.

        :param int gameweek: A gameweek (1-38)
        """
        if gameweek:
            valid_gameweek(gameweek)
            return self.picks[gameweek]["automatic_subs"]

        automatic_substitutions = []
        for gameweek_id in range(1, 39):
            try:
                automatic_substitution = self.picks[
                    gameweek_id]["automatic_subs"]
                automatic_substitutions.append(automatic_substitution)
            except KeyError:
                return automatic_substitutions

        return automatic_substitutions

    def gameweek_history(self, gameweek=None):
        """Returns a list of the user's history per gameweek, or the history
        of a specific gameweek.

        :param int gameweek: A gameweek (1-38)
        """
        if gameweek:
            valid_gameweek(gameweek)
            return self.picks[gameweek]["entry_history"]

        histories = []
        for gameweek_id in range(1, 39):
            try:
                history = self.picks[gameweek_id]["entry_history"]
                histories.append(history)
            except KeyError:
                return histories

        return history

    @property
    def transfers(self):
        """Returns a dictionary containing information about all the transfers
        the user has made so far.
        """
        return requests.get(API_URLS["user_transfers"].format(
            self.user_id)).json()

    @property
    def wildcards(self):
        """Returns a list containing information about the usage of the
        player's wildcard(s).
        """
        return self.transfers["wildcards"]

    def transfer_history(self, gameweek=None):
        """Returns a list containing information about the user's transfer
        history.

        :param int gameweek: A gameweek (1-38)
        """
        if gameweek:
            valid_gameweek(gameweek)
            transfers = [transfer for transfer in self.transfers["history"]
                         if transfer["event"] == gameweek]
            return transfers

        return self.transfers["history"]

    @property
    def watchlist(self):
        """Returns the user's watchlist."""
        if not self._session:
            raise "User must be logged in."

        return self._session.get(API_URLS["watchlist"]).json()

    def __str__(self):
        return "{} {} - {}".format(
            self.first_name, self.second_name, self.region_name)
