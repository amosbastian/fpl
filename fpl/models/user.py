import asyncio
import json

import aiohttp
from urllib3.util import response

from ..constants import API_URLS, MIN_GAMEWEEK, MAX_GAMEWEEK
from ..utils import fetch, logged_in, post, get_headers

is_c = "is_captain"
is_vc = "is_vice_captain"


def valid_gameweek(gameweek):
    """Returns True if the gameweek is valid.

    :param gameweek: The gameweek.
    :type gameweek: int or string
    :raises ValueError: if gameweek is not a number between 1 and 38
    """
    gameweek = int(gameweek)
    if (gameweek < MIN_GAMEWEEK) or (gameweek > MAX_GAMEWEEK):
        raise ValueError(f"Gameweek must be a number between {MIN_GAMEWEEK} and {MAX_GAMEWEEK}.")
    return True


def _ids_to_lineup(player_ids, user_team):
    """Helper for converting list of player IDs to usable lineup.

    :param player_ids: List of player IDS.
    :type player_ids: list
    :param user_team: The user's current team.
    :type user_team: list
    :return: A usable lineup.
    :rtype: list
    """
    return [next(player for player in user_team
                 if player["element"] == player_id)
            for player_id in player_ids]


def _id_to_element_type(player_id, players):
    """Helper for converting a player's ID to their respective element type:
    1, 2, 3 or 4.

    :param player_id: A player's ID.
    :type player_id: int
    :param players: List of all players in the Fantasy Premier League.
    :type players: list
    :return: The player's element type.
    :rtype: int
    """
    player = next(player for player in players
                  if player["id"] == player_id)
    return player["element_type"]


def _set_element_type(lineup, players):
    """Helper for setting the players' element types.

    :param lineup: The user's current lineup.
    :type lineup: list
    :param players: List of all players in the Fantasy Premier League.
    :type players: list
    """
    for player in lineup:
        element_type = _id_to_element_type(player["element"], players)
        player["element_type"] = element_type


def _set_captain(lineup, captain, captain_type, player_ids):
    """Sets the given captain's captain_type to True.

    :param lineup: List of players.
    :type lineup: list
    :param captain: ID of the captain.
    :type captain: int or str
    :param captain_type: The captain type: 'is_captain' or 'is_vice_captain'.
    :type captain_type: string
    :param player_ids: List of the team's players' IDs.
    :type player_ids: list
    """
    if captain and captain not in player_ids:
        raise ValueError(
            "Cannot (vice) captain player who isn't in user's team.")

    current_captain = next(player for player in lineup if player[captain_type])
    chosen_captain = next(player for player in lineup
                          if player["element"] == captain)

    # If the chosen captain is already a (vice) captain, then give his previous
    # role to the current (vice) captain.
    if chosen_captain[is_c] or chosen_captain[is_vc]:
        current_captain[is_c], chosen_captain[is_c] = (
            chosen_captain[is_c], current_captain[is_c])
        current_captain[is_vc], chosen_captain[is_vc] = (
            chosen_captain[is_vc], current_captain[is_vc])

    for player in lineup:
        player[captain_type] = False

        if player["element"] == captain:
            player[captain_type] = True


class User():
    """A class representing a user of the Fantasy Premier League.

    >>> from fpl import FPL
      >>> import aiohttp
      >>> import asyncio
      >>>
      >>> async def main():
      ...     async with aiohttp.ClientSession() as session:
      ...         fpl = FPL(session)
      ...         user = await fpl.get_user(3808385)
      ...     print(user)
      ...
      >>> asyncio.run(main())
      Amos Bastian - Netherlands
    """

    def __init__(self, user_information, session):
        self._session = session
        for k, v in user_information.items():
            setattr(self, k, v)

    async def get_gameweek_history(self, gameweek=None):
        """Returns a list containing the gameweek history of the user.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/entry/91928/history

        :param gameweek: (optional): The gameweek. Defaults to ``None``.
        :rtype: list if gameweek is ``None``, otherwise dict.
        """
        if hasattr(self, "_history"):
            history = self._history
        else:
            history = await fetch(
                self._session, API_URLS["user_history"].format(self.id))

        self._history = history

        if gameweek is not None:
            valid_gameweek(gameweek)
            return next(gw for gw in history["current"]
                        if gw["event"] == gameweek)

        return history["current"]

    async def get_season_history(self):
        """Returns a list containing the seasonal history of the user.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/entry/91928/history

        :rtype: list
        """
        if hasattr(self, "_history"):
            history = self._history
        else:
            history = await fetch(
                self._session, API_URLS["user_history"].format(self.id))

        self._history = history
        return history["past"]

    async def get_chips_history(self, gameweek=None):
        """Returns a list containing the chip history of the user.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/entry/91928/history

        :param gameweek: (optional): The gameweek. Defaults to ``None``.
        :rtype: list
        """
        if hasattr(self, "_history"):
            history = self._history
        else:
            history = await fetch(
                self._session, API_URLS["user_history"].format(self.id))

        self._history = history

        if gameweek is not None:
            valid_gameweek(gameweek)
            try:
                return next(chip for chip in history["chips"]
                            if chip["event"] == gameweek)
            except StopIteration:
                return None

        return history["chips"]

    async def get_picks(self, gameweek=None):
        """Returns a dict containing the user's picks each gameweek.

        Key is the gameweek number, value contains picks of the gameweek.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/entry/91928/event/1/picks/

        :param gameweek: (optional): The gameweek. Defaults to ``None``.
        :rtype: dict
        """
        if hasattr(self, "_picks"):
            picks = self._picks
        else:
            tasks = [asyncio.ensure_future(
                     fetch(self._session,
                           API_URLS["user_picks"].format(self.id, gameweek)))
                     for gameweek in range(self.started_event,
                                           self.current_event + 1)]
            picks = await asyncio.gather(*tasks)
            self._picks = picks

        if gameweek is not None:
            valid_gameweek(gameweek)
            try:
                pick = next(pick for pick in picks
                            if pick["entry_history"]["event"] == gameweek)
            except StopIteration:
                return {}
            else:
                return {pick["entry_history"]["event"]: pick["picks"]}

        picks_out = {}
        for pick in picks:
            try:
                picks_out[pick["entry_history"]["event"]] = pick["picks"]
            except KeyError:
                pass
        return picks_out

    async def get_cup_matches(self, gameweek=None):
        """Returns either a list of all the user's cup matches, dictionary
        of the cup match in the given gameweek (gameweek 17 and onwards).

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/entry/91928/cup/

        :param gameweek: (optional): The gameweek. Defaults to ``None``.
        :rtype: list or dict
        """
        cup = getattr(self, "_cup", None)
        if not cup:
            cup = await fetch(
                self._session, API_URLS["user_cup"].format(self.id))
            self._cup = cup

        if gameweek is not None:
            valid_gameweek(gameweek)
            return [cup_match for cup_match in cup["cup_matches"]
                    if cup_match["event"] == gameweek]

        return cup["cup_matches"]

    async def get_cup_status(self):
        """Returns the user's cup status.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/entry/91928/cup/

        :rtype: dict
        """
        cup = getattr(self, "_cup", None)
        if not cup:
            cup = await fetch(
                self._session, API_URLS["user_cup"].format(self.id))
            self._cup = cup

        return cup["cup_status"]

    async def get_active_chips(self, gameweek=None):
        """Returns a list containing the user's active chip for each gameweek,
        or the active chip of the given gameweek.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/entry/91928/event/1/picks/

        :param gameweek: (optional): The gameweek. Defaults to ``None``.
        :rtype: list
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

        if gameweek is not None:
            valid_gameweek(gameweek)
            try:
                return [next(pick["active_chip"] for pick in picks
                             if pick["entry_history"]["event"] == gameweek)][0]
            except StopIteration:
                return None

        return [pick["active_chip"] for pick in picks]

    async def get_automatic_substitutions(self, gameweek=None):
        """Returns a list containing the user's automatic substitutions each
        gameweek.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/entry/91928/event/1/picks/

        :param gameweek: (optional): The gameweek. Defaults to ``None``.
        :rtype: list
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

        if gameweek is not None:
            valid_gameweek(gameweek)
            try:
                return next(pick["automatic_subs"] for pick in picks
                            if pick["entry_history"]["event"] == gameweek)
            except StopIteration:
                return None

        return [p for pick in picks for p in pick["automatic_subs"]]

    async def get_user_history(self, gameweek=None):
        """Returns a list containing the user's history for each gameweek,
        or a dictionary of the user's history for the given gameweek.

        :rtype: list or dict
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

        if gameweek is not None:
            valid_gameweek(gameweek)
            try:
                return next(pick["entry_history"] for pick in picks
                            if pick["entry_history"]["event"] == gameweek)
            except StopIteration:
                return None

        return [history["entry_history"] for history in picks]

    async def get_team(self):
        """Returns a logged in user's current team. Requires the user to have
        logged in using ``fpl.login()``.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/my-team/91928/

        :rtype: list
        """
        if not logged_in(self._session):
            raise Exception("User must be logged in.")

        response = await fetch(
            self._session, API_URLS["user_team"].format(self.id))

        if response == {"details": "You cannot view this entry"}:
            raise ValueError("User ID does not match provided email address!")

        return response["picks"]

    async def get_chips(self):
        """Returns a logged in user's list of chips. Requires the user to have
        logged in using ``fpl.login()``.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/my-team/91928/

        :rtype: list
        """
        if not logged_in(self._session):
            raise Exception("User must be logged in.")

        response = await fetch(
            self._session, API_URLS["user_team"].format(self.id))

        if response == {"details": "You cannot view this entry"}:
            raise ValueError("User ID does not match provided email address!")

        return response["chips"]

    async def get_transfers_status(self):
        """Returns a logged in user's transfer status, which is a dictionary
        containing their bank value, how many free transfers they have left
        and so on. Requires the user to have logged in using ``fpl.login()``.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/my-team/91928/

        :rtype: dict
        """
        if not logged_in(self._session):
            raise Exception("User must be logged in.")

        response = await fetch(
            self._session, API_URLS["user_team"].format(self.id))

        if response == {"details": "You cannot view this entry"}:
            raise ValueError("User ID does not match provided email address!")

        return response["transfers"]

    async def get_transfers(self, gameweek=None):
        """Returns either a list of all the user's transfers, or a list of
        transfers made in the given gameweek.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/entry/91928/transfers/

        :param gameweek: (optional): The gameweek. Defaults to ``None``.
        :rtype: list
        """
        transfers = getattr(self, "_transfers", None)
        if not transfers:
            transfers = await fetch(
                self._session, API_URLS["user_transfers"].format(self.id))
            self._transfers = transfers

        if gameweek is not None:
            valid_gameweek(gameweek)
            return [transfer for transfer in transfers
                    if transfer["event"] == gameweek]

        return transfers

    async def get_latest_transfers(self):
        """Returns a list of transfers made by the user in the current
        gameweek. Requires the user to have logged in using ``fpl.login()``.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/entry/91928/transfers-latest/

        :rtype: list
        """
        if not logged_in(self._session):
            raise Exception("User must be logged in.")

        transfers = await fetch(
            self._session, API_URLS["user_latest_transfers"].format(self.id))

        return transfers

    # async def get_wildcards(self):
    #     """Returns a list containing information about when (and if) the user
    #     has played their wildcard(s).

    #     Information is taken from e.g.:
    #         https://fantasy.premierleague.com/drf/entry/3808385/transfers

    #     :rtype: list
    #     """
    #     if hasattr(self, "_transfers"):
    #         return self._transfers["wildcards"]

    #     transfers = await fetch(
    #         self._session, API_URLS["user_transfers"].format(self.id))

    #     self._transfers = transfers
    #     return transfers["wildcards"]

    async def get_watchlist(self):
        """Returns the user's watchlist. Requires the user to have logged in
        using ``fpl.login()``.

        Information is taken from here:
            https://fantasy.premierleague.com/api/me/

        :rtype: list
        """
        if not logged_in(self._session):
            raise Exception("User must be logged in.")

        me = await fetch(self._session, API_URLS["me"])
        return me["watched"]

    def _get_transfer_payload(
            self, players_out, players_in, user_team, players, wildcard,
            free_hit):
        """Returns the payload needed to make the desired transfers."""
        payload = {
            "confirmed": False,
            "entry": self.id,
            "event": self.current_event + 1,
            "transfers": [],
            "wildcard": wildcard,
            "freehit": free_hit
        }

        for player_out_id, player_in_id in zip(players_out, players_in):
            player_out = next(player for player in user_team
                              if player["element"] == player_out_id)
            player_in = next(player for player in players
                             if player["id"] == player_in_id)
            payload["transfers"].append({
                "element_in": player_in["id"],
                "element_out": player_out["element"],
                "purchase_price": player_in["now_cost"],
                "selling_price": player_out["selling_price"]
            })

        return payload

    async def transfer(self, players_out, players_in, max_hit=60,
                       wildcard=False, free_hit=False):
        """Transfers given players out and transfers given players in.

        :param players_out: List of IDs of players who will be transferred out.
        :type players_out: list
        :param players_in: List of IDs of players who will be transferred in.
        :type players_in: list
        :param max_hit: Maximum hit that should be taken by making the
            transfer(s), defaults to 60
        :param max_hit: int, optional
        :param wildcard: Boolean for playing wildcard, defaults to False
        :param wildcard: bool, optional
        :param free_hit: Boolean for playing free hit, defaults to False
        :param free_hit: bool, optional
        :return: Returns the response given by a succesful transfer.
        :rtype: dict
        """
        if wildcard and free_hit:
            raise Exception("Can only use 1 of wildcard and free hit.")

        if not logged_in(self._session):
            raise Exception("User must be logged in.")

        if not players_out or not players_in:
            raise Exception(
                "Lists must both contain at least one player's ID.")

        if len(players_out) != len(players_in):
            raise Exception("Number of players transferred in must be same as "
                            "number transferred out.")

        if not set(players_in).isdisjoint(players_out):
            raise Exception("Player ID can't be in both lists.")

        user_team = await self.get_team()
        team_ids = [player["element"] for player in user_team]

        if not set(team_ids).isdisjoint(players_in):
            raise Exception(
                "Cannot transfer a player in who is already in the user's team.")

        if set(team_ids).isdisjoint(players_out):
            raise Exception(
                "Cannot transfer a player out who is not in the user's team.")

        players = await fetch(self._session, API_URLS["players"])
        player_ids = [player["id"] for player in players]

        if set(player_ids).isdisjoint(players_in):
            raise Exception("Player ID in `players_in` does not exist.")

        # Send POST requests with `confirmed` set to False; this basically
        # checks if there are any errors from FPL's side for this transfer,
        # e.g. too many players from the same team, or not enough money.
        payload = self._get_transfer_payload(
            players_out, players_in, user_team, players, wildcard, free_hit)
        headers = get_headers(
            "https://fantasy.premierleague.com/a/squad/transfers")
        post_response = await post(
            self._session, API_URLS["transfers"], json.dumps(payload), headers)

        if "non_form_errors" in post_response:
            raise Exception(post_response["non_form_errors"])

        if post_response["spent_points"] > max_hit:
            raise Exception(
                f"Point hit for transfer(s) [-{post_response['spent_points']}]"
                f" exceeds max_hit [{max_hit}].")

        # Everything is okay, so push the transfer through!
        payload["confirmed"] = True
        post_response = await post(
            self._session, API_URLS["transfers"], json.dumps(payload), headers)
        return post_response

    async def _create_new_lineup(self, players_in, players_out, lineup):
        """Helper for creating the new lineup of players.

        :param players_in: List of IDs of players who will be substituted in.
        :type players_in: list
        :param players_out: List of IDs of players who will be substituted out.
        :type players_out: list
        :param lineup: List containing the user's current lineup.
        :type lineup: list
        :return: Returns the new lineup.
        :rtype: list
        """

        players = await fetch(self._session, API_URLS["static"])
        players = players["elements"]
        _set_element_type(lineup, players)

        subs_in = _ids_to_lineup(players_in, lineup)
        subs_out = _ids_to_lineup(players_out, lineup)

        for sub_out, sub_in in zip(subs_out, subs_in):
            # Get indices of sub out and sub in, then swap their position in
            # the lineup
            out_i, in_i = lineup.index(sub_out), lineup.index(sub_in)
            lineup[out_i], lineup[in_i] = lineup[in_i], lineup[out_i]

            # Swap position and (vice) captaincy
            lineup[out_i]["position"], lineup[in_i]["position"] = (
                lineup[in_i]["position"], lineup[out_i]["position"])
            lineup[out_i][is_c], lineup[in_i][is_c] = (
                lineup[in_i][is_c], lineup[out_i][is_c])
            lineup[out_i][is_vc], lineup[in_i][is_vc] = (
                lineup[in_i][is_vc], lineup[out_i][is_vc])

            starters, subs = lineup[:11], lineup[11:]
            new_starters = sorted(starters, key=lambda x: (
                x["element_type"] - 1) * 100 + x["position"])
            lineup = new_starters + subs

            for position, player in enumerate(lineup):
                player["position"] = position + 1

        new_lineup = [{
            "element": player["element"],
            "position": player["position"],
            "is_captain": player[is_c],
            "is_vice_captain": player[is_vc]
        } for player in lineup]

        return new_lineup

    async def _post_substitutions(self, lineup):
        """Helper for sending the POST requests with the new lineup.

        :param lineup: The new lineup.
        :type lineup: list
        """
        # Get CSRF token and create payload + headers
        payload = json.dumps({"chip": None, "picks": lineup})
        headers = get_headers("https://fantasy.premierleague.com/a/team/my")

        await post(
            self._session, API_URLS["user_team"].format(self.id) + "/",
            payload=payload, headers=headers)

    async def _captain_helper(self, captain, captain_type):
        """Helper for setting the (vice) captain of the user's team."""
        if not logged_in(self._session):
            raise Exception("User must be logged in.")

        user_team = await self.get_team()
        team_ids = [player["element"] for player in user_team]
        _set_captain(user_team, captain, captain_type, team_ids)
        lineup = await self._create_new_lineup([], [], user_team)

        await self._post_substitutions(lineup)

    async def captain(self, captain):
        """Set the captain of the user's team.

        :param captain: ID of the captain.
        :type captain: int
        """
        await self._captain_helper(captain, is_c)

    async def vice_captain(self, vice_captain):
        """Set the vice captain of the user's team.

        :param vice_captain: ID of the vice captain.
        :type vice_captain: int
        """
        await self._captain_helper(vice_captain, is_vc)

    async def substitute(self, players_in, players_out, captain=None,
                         vice_captain=None):
        """Substitute players on the bench for players in the starting eleven.
        Also allows the user to simultaneously set the new (vice) captain(s).
        A maximum of 4 substitutes is set to force proper usage.

        :param players_in: List of IDs of players who will be substituted in.
        :type players_in: list
        :param players_out: List of IDS of players who will be substituted out.
        :type players_out: list
        :param captain: ID of the captain, defaults to None.
        :param captain: int, optional
        :param vice_captain: ID of the vice captain, defaults to None.
        :param vice_captain: int, optional
        """
        if not logged_in(self._session):
            raise Exception("User must be logged in.")

        if len(players_out) > 4 or len(players_in) > 4:
            raise Exception("Can only substitute a maximum of 4 players.")

        if len(players_out) != len(players_in):
            raise Exception("Number of players substituted in must be same as "
                            "number substituted out.")

        if not set(players_in).isdisjoint(players_out):
            raise Exception("Player ID can't be in both lists.")

        user_team = await self.get_team()
        team_ids = [player["element"] for player in user_team]
        substitution_ids = players_out + players_in

        if not set(substitution_ids).issubset(team_ids):
            raise Exception(
                "Cannot substitute players who aren't in the user's team.")

        # Set new captain or vice captain if applicable
        if captain:
            _set_captain(user_team, captain, is_c, team_ids)

        if vice_captain:
            _set_captain(user_team, vice_captain, is_vc, team_ids)

        lineup = await self._create_new_lineup(
            players_in, players_out, user_team)

        await self._post_substitutions(lineup)

    def __str__(self):
        return (f"{self.player_first_name} {self.player_last_name} - "
                f"{self.player_region_name}")
