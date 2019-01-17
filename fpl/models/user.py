import asyncio

from ..constants import API_URLS
from ..utils import fetch, team_converter


def valid_gameweek(gameweek):
    """Returns True if the gameweek is valid."""
    if not isinstance(gameweek, int) and (gameweek < 1 or gameweek > 38):
        raise "Gameweek must be a number between 1 and 38."
    return True


class User():
    """A class representing a user of the Fantasy Premier League."""
    def __init__(self, user_information, session):
        self._session = session
        self._information = user_information
        self._entry = self._information["entry"]
        self.id = self._entry["id"]
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

    async def get_history(self):
        """Returns a dictionary containing the history of the user."""
        return await fetch(self._session, API_URLS["user_history"].format(
            self.id))

    async def get_season_history(self):
        """Returns a list containing information about each of the seasons the
        user has participated in.
        """
        try:
            history = self.history
        except:
            history = await self.get_history()
        return history["season"]

    async def get_chips_history(self):
        """Returns a list containing information about the usage of the
        player's chips.
        """
        try:
            history = self.history
        except:
            history = await self.get_history()
        return history["chips"]

    async def get_leagues(self):
        """Returns a dictionary containing information about all the leagues
        that the user is participating in.
        """
        try:
            history = self.history
        except:
            history = await self.get_history()
        return history["leagues"]

    async def get_classic_leagues(self):
        """Returns a list containing information about all the classic leagues
        that the user is currently participating in.
        """
        try:
            leagues = self.leagues
        except:
            leagues = await self.get_leagues()
        return leagues["classic"]

    async def get_h2h_leagues(self):
        """Returns a list containing information about all the h2h leagues that
        the user is currently participating in.
        """
        try:
            leagues = self.leagues
        except:
            leagues = await self.get_leagues()
        return leagues["h2h"]

    async def get_picks(self):
        """Returns a dictionary containing information about the user's chip
        usage, automatic substitutions and picks, alongside general
        information about each gameweek.
        """
        until = self.current_gameweek + 1
        tasks = [asyncio.ensure_future(
                 fetch(self._session,
                       API_URLS["user_picks"].format(self.id, gw)))
                 for gw in range(1, until)]

        picks = await asyncio.gather(*tasks)

        return picks

    async def my_team(self):
        """Returns a logged in user's current team."""
        if not self._session:
            raise "User must be logged in."

        response = await fetch(
            self._session, API_URLS["user_team"].format(self.id))

        if response == {"details": "You cannot view this entry"}:
            raise ValueError("User ID does not match provided email address!")

        return response["picks"]

    async def get_team(self, gameweek=None):
        """Returns a list of all of the user's teams so far, or the user's team
        in the specified gameweek.

        :param int gameweek: A gameweek (1-38)
        """
        try:
            picks = self.picks
        except:
            picks = await self.get_picks()

        if gameweek:
            valid_gameweek(gameweek)
            return picks[gameweek]["picks"]

        teams = []
        for gameweek_id in range(1, self.current_gameweek):
            team = picks[gameweek_id]["picks"]
            teams.append(team)

        return teams

    async def get_chips(self, gameweek=None):
        """Returns a list of chips used by the user so far, or the chip used
        by the user in the specified gameweek.

        :param int gameweek: A gameweek (1-38)
        """
        try:
            picks = self.picks
        except:
            picks = await self.get_picks()

        if gameweek:
            valid_gameweek(gameweek)
            return picks[gameweek]["active_chip"]

        active_chips = []
        for gameweek_id in range(1, self.current_gameweek):
            active_chip = picks[gameweek_id]["active_chip"]
            active_chips.append(active_chip)

        return active_chips

    async def get_automatic_substitutions(self, gameweek=None):
        """Returns a list of all automatic substitions made for the user so
        far, or the automatic substitutions made for the user in the specified
        gameweek.

        :param int gameweek: A gameweek (1-38)
        """
        try:
            picks = self.picks
        except:
            picks = await self.get_picks()

        if gameweek:
            valid_gameweek(gameweek)
            return picks[gameweek]["automatic_subs"]

        automatic_substitutions = []
        for gameweek_id in range(1, self.current_gameweek):
            automatic_substitution = picks[gameweek_id]["automatic_subs"]
            automatic_substitutions.append(automatic_substitution)

        return automatic_substitutions

    async def get_gameweek_history(self, gameweek=None):
        """Returns a list of the user's history per gameweek, or the history
        of a specific gameweek.

        :param int gameweek: A gameweek (1-38)
        """
        try:
            picks = self.picks
        except:
            picks = await self.get_picks()

        if gameweek:
            valid_gameweek(gameweek)
            return picks[gameweek]["entry_history"]

        histories = []
        for gameweek_id in range(1, self.current_gameweek):
            history = picks[gameweek_id]["entry_history"]
            histories.append(history)

        return histories

    async def get_transfers(self):
        """Returns a dictionary containing information about all the transfers
        the user has made so far.
        """
        return await fetch(self._session, API_URLS["user_transfers"].format(
            self.id))

    async def get_wildcards(self):
        """Returns a list containing information about the usage of the
        player's wildcard(s).
        """
        try:
            transfers = self.transfers
        except:
            transfers = await self.get_transfers()

        return transfers["wildcards"]

    async def get_transfer_history(self, gameweek=None):
        """Returns a list containing information about the user's transfer
        history.

        :param int gameweek: A gameweek (1-38)
        """
        try:
            transfers = self.transfers
        except:
            transfers = await self.get_transfers()

        if gameweek:
            valid_gameweek(gameweek)
            transfers = [transfer for transfer in transfers["history"]
                         if transfer["event"] == gameweek]
            return transfers

        return transfers["history"]

    def get_watchlist(self):
        """Returns the user's watchlist."""
        if not self._session:
            raise "User must be logged in."

        return fetch(self._session, API_URLS["watchlist"])

    def __str__(self):
        return "{} {} - {}".format(
            self.first_name, self.second_name, self.region_name)
