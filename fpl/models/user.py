import asyncio

from ..constants import API_URLS
from ..utils import fetch


def valid_gameweek(gameweek):
    """Returns True if the gameweek is valid."""
    if not isinstance(gameweek, int) and (gameweek < 1 or gameweek > 38):
        raise "Gameweek must be a number between 1 and 38."
    return True


class User():
    """A class representing a user of the Fantasy Premier League."""
    def __init__(self, user_information, session):
        self._session = session
        for k, v in user_information["entry"].items():
            setattr(self, k, v)
        self.leagues = user_information["leagues"]

    async def get_gameweek_history(self, gameweek=None):
        """Returns a list containing the gameweek history of the user.

        :gameweek (`int`, optional): The gameweek. Defaults to None.
        """
        if hasattr(self, "_history"):
            history = self._history
        else:
            history = await fetch(
                self._session, API_URLS["user_history"].format(self.id))

        self._history = history

        if gameweek:
            valid_gameweek(gameweek)
            return next(gw for gw in history["history"]
                        if gw["event"] == gameweek)

        return history["history"]

    async def get_season_history(self):
        """Returns a list containing the seasonal history of the user."""
        if hasattr(self, "_history"):
            history = self._history["season"]
        else:
            history = await fetch(
                self._session, API_URLS["user_history"].format(self.id))

        self._history = history
        return history["season"]

    async def get_chips_history(self, gameweek=None):
        """Returns a list containing the chip history of the user.

        :gameweek (`int`, optional): The gameweek. Defaults to None.
        """
        if hasattr(self, "_history"):
            history = self._history
        else:
            history = await fetch(
                self._session, API_URLS["user_history"].format(self.id))

        self._history = history

        if gameweek:
            valid_gameweek(gameweek)
            return next(chip for chip in history["chips"]
                        if chip["event"] == gameweek)

        return history["chips"]

    async def get_picks(self, gameweek=None):
        """Returns a list containing the user's picks each gameweek.

        :gameweek (`int`, optional): The gameweek. Defaults to None.
        """
        if hasattr(self, "_picks"):
            picks = self._picks
        else:
            tasks = [asyncio.ensure_future(
                     fetch(self._session,
                           API_URLS["user_picks"].format(self.id, gameweek)))
                     for gameweek in range(1, self.current_event + 1)]
            picks = await asyncio.gather(*tasks)
            self._picks = picks

        if gameweek:
            valid_gameweek(gameweek)
            return next(pick["picks"] for pick in picks
                        if pick["event"]["id"] == gameweek)

        return [pick["picks"] for pick in picks]

    async def get_active_chips(self, gameweek=None):
        """Returns a list containing the user's active chips each gameweek.

        :gameweek (`int`, optional): The gameweek. Defaults to None.
        """
        if hasattr(self, "_picks"):
            picks = self._picks
        else:
            tasks = [asyncio.ensure_future(
                     fetch(self._session,
                           API_URLS["user_picks"].format(self.id, gameweek)))
                     for gameweek in range(1, self.current_event + 1)]
            picks = await asyncio.gather(*tasks)
            self._picks = picks

        if gameweek:
            valid_gameweek(gameweek)
            return [next(pick["active_chip"] for pick in picks
                         if pick["event"]["id"] == gameweek)]

        return [pick["active_chip"] for pick in picks]

    async def get_automatic_substitutions(self, gameweek=None):
        """Returns a list containing the user's automatic substitutions each
        gameweek.

        :gameweek (`int`, optional): The gameweek. Defaults to None.
        """
        if hasattr(self, "_picks"):
            picks = self._picks
        else:
            tasks = [asyncio.ensure_future(
                     fetch(self._session,
                           API_URLS["user_picks"].format(self.id, gameweek)))
                     for gameweek in range(1, self.current_event + 1)]
            picks = await asyncio.gather(*tasks)
            self._picks = picks

        if gameweek:
            valid_gameweek(gameweek)
            return next(pick["automatic_subs"] for pick in picks
                        if pick["event"]["id"] == gameweek)

        return [pick["automatic_subs"] for pick in picks]

    async def get_team(self):
        """Returns a logged in user's current team.

        :gameweek (`int`, optional): The gameweek. Defaults to None.
        """
        if not self._session:
            raise "User must be logged in."

        response = await fetch(
            self._session, API_URLS["user_team"].format(self.id))

        if response == {"details": "You cannot view this entry"}:
            raise ValueError("User ID does not match provided email address!")

        return response["picks"]

    async def get_transfers(self, gameweek=None):
        """Returns a list containing information about all the transfers the
        user has made so far.

        :gameweek (`int`, optional): The gameweek. Defaults to None.
        """
        if hasattr(self, "_transfers"):
            return self._transfers["history"]

        transfers = await fetch(
            self._session, API_URLS["user_transfers"].format(self.id))

        self._transfers = transfers

        if gameweek:
            valid_gameweek(gameweek)
            return [transfer for transfer in transfers["history"]
                    if transfer["event"] == gameweek]

        return transfers["history"]

    async def get_wildcards(self):
        """Returns a list containing information about all the transfers the
        user has made so far.
        """
        if hasattr(self, "_transfers"):
            return self._transfers["wildcards"]

        transfers = await fetch(
            self._session, API_URLS["user_transfers"].format(self.id))

        self._transfers = transfers
        return transfers["wildcards"]

    async def get_watchlist(self):
        """Returns the user's watchlist."""
        if not self._session:
            raise "User must be logged in."

        return await fetch(self._session, API_URLS["watchlist"])

    def __str__(self):
        return (f"{self.player_first_name} {self.player_last_name} - "
                f"{self.player_region_name}")
