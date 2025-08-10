"""
The FPL module.

Fantasy Premier League API:
* /bootstrap-static
* /bootstrap-dynamic
* /elements
* /element-summary/{player_id}
* /entry/{user_id}
* /entry/{user_id}/cup
* /entry/{user_id}/event/{event_id}/picks
* /entry/{user_id}/history
* /entry/{user_id}/transfers
* /events
* /event/{event_id}/live
* /fixtures/?event={event_id}
* /game-settings
* /leagues-classic-standings/{league_id}
* /leagues-classic-standings/{league_id}
* /leagues-entries-and-h2h-matches/league/{league_id}
* /leagues-h2h-standings/{league_id}
* /my-team/{user_id}
* /teams
* /transfers
"""
import asyncio
import base64
import hashlib
import itertools
import json
import os
import re
import secrets
import uuid
from urllib.request import urlopen

import certifi
import requests

from .constants import API_URLS
from .models.classic_league import ClassicLeague
from .models.fixture import Fixture
from .models.gameweek import Gameweek
from .models.h2h_league import H2HLeague
from .models.player import Player, PlayerSummary
from .models.team import Team
from .models.user import User
from .utils import (average, fetch, get_current_user, logged_in,
                    position_converter, scale, ssl_context, team_converter)


class FPL:
    """The FPL class."""

    def __init__(self):
        self.session = None

        resp = urlopen(API_URLS["static"], context=ssl_context)
        static = json.loads(resp.read().decode("utf-8"))
        for k, v in static.items():
            try:
                v = {w["id"]: w for w in v}
            except (KeyError, TypeError):
                pass
            setattr(self, k, v)
        try:
            setattr(
                self,
                "current_gameweek",
                next(event for event in static["events"] if event["is_current"])["id"],
            )
        except StopIteration:
            setattr(self, "current_gameweek", 0)

    async def get_user(self, user_id=None, return_json=False):
        """Returns the user with the given ``user_id``.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/entry/91928/

        :param user_id: A user's ID.
        :type user_id: string or int
        :param return_json: (optional) Boolean. If ``True`` returns a ``dict``,
            if ``False`` returns a :class:`User` object. Defaults to ``False``.
        :type return_json: bool
        :rtype: :class:`User` or `dict`
        """
        if user_id:
            assert int(user_id) > 0, "User ID must be a positive number."
        else:
            # If no user ID provided get it from current session
            try:
                user = await get_current_user(
                    self.session, access_token=self.access_token
                )
                user_id = user["player"]["entry"]
            except TypeError:
                raise Exception(
                    "You must log in before using `get_user` if "
                    "you do not provide a user ID."
                )

        url = API_URLS["user"].format(user_id)
        user = await fetch(self.session, url, access_token=self.access_token)

        if return_json:
            return user
        return User(user, session=self.session)

    async def get_teams(self, team_ids=None, return_json=False):
        """Returns either a list of *all* teams, or a list of teams with IDs in
        the optional ``team_ids`` list.

        Information is taken from:
            https://fantasy.premierleague.com/api/bootstrap-static/

        :param list team_ids: (optional) List containing the IDs of teams.
            If not set a list of *all* teams will be returned.
        :param return_json: (optional) Boolean. If ``True`` returns a list of
            ``dict``s, if ``False`` returns a list of  :class:`Team` objects.
            Defaults to ``False``.
        :type return_json: bool
        :rtype: list
        """
        teams = getattr(self, "teams")

        if team_ids:
            team_ids = set(team_ids)
            teams = [team for team in teams.values() if team["id"] in team_ids]
        else:
            teams = [team for team in teams.values()]

        if return_json:
            return teams

        return [Team(team_information, self.session) for team_information in teams]

    async def get_team(self, team_id, return_json=False):
        """Returns the team with the given ``team_id``.

        Information is taken from:
            https://fantasy.premierleague.com/api/bootstrap-static/

        :param team_id: A team's ID.
        :type team_id: string or int
        :param return_json: (optional) Boolean. If ``True`` returns a ``dict``,
            if ``False`` returns a :class:`Team` object. Defaults to ``False``.
        :type return_json: bool
        :rtype: :class:`Team` or ``dict``

        For reference here is the mapping from team ID to team name:

        .. code-block:: none

             1 - Arsenal
             2 - Aston Villa
             3 - Brentford
             4 - Brighton
             5 - Burnley
             6 - Chelsea
             7 - Crystal Palace
             8 - Everton
             9 - Leicester
            10 - Leeds
            11 - Liverpool
            12 - Man City
            13 - Man Utd
            14 - Newcastle
            15 - Norwich
            16 - Southampton
            17 - Spurs
            18 - Watford
            19 - West Ham
            20 - Wolves
        """
        assert 0 < int(team_id) < 21, "Team ID must be a number between 1 and 20."
        teams = getattr(self, "teams")
        team = next(team for team in teams.values() if team["id"] == int(team_id))

        if return_json:
            return team

        return Team(team, self.session)

    async def get_player_summary(self, player_id, return_json=False):
        """Returns a summary of the player with the given ``player_id``.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/element-summary/1/

        :param int player_id: A player's ID.
        :param return_json: (optional) Boolean. If ``True`` returns a ``dict``,
            if ``False`` returns a :class:`PlayerSummary` object. Defaults to
            ``False``.
        :type return_json: bool
        :rtype: :class:`PlayerSummary` or ``dict``
        """
        assert int(player_id) > 0, "Player's ID must be a positive number"
        url = API_URLS["player"].format(player_id)
        player_summary = await fetch(self.session, url, access_token=self.access_token)

        if return_json:
            return player_summary

        return PlayerSummary(player_summary)

    async def get_player_summaries(self, player_ids, return_json=False):
        """Returns a list of summaries of players whose ID are
        in the ``player_ids`` list.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/element-summary/1/

        :param list player_ids: A list of player IDs.
        :param return_json: (optional) Boolean. If ``True`` returns a list of
            ``dict``s, if ``False`` returns a list of  :class:`PlayerSummary`
            objects. Defaults to ``False``.
        :type return_json: bool
        :rtype: list
        """
        if not player_ids:
            return []

        tasks = [
            asyncio.ensure_future(
                fetch(
                    self.session,
                    API_URLS["player"].format(player_id),
                    access_token=self.access_token,
                )
            )
            for player_id in player_ids
        ]

        player_summaries = await asyncio.gather(*tasks)

        if return_json:
            return player_summaries

        return [PlayerSummary(player_summary) for player_summary in player_summaries]

    async def get_player(
        self, player_id, players=None, include_summary=False, return_json=False
    ):
        """Returns the player with the given ``player_id``.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/bootstrap-static/
            https://fantasy.premierleague.com/api/element-summary/1/ (optional)

        :param player_id: A player's ID.
        :type player_id: string or int
        :param list players: (optional) A list of players.
        :param bool include_summary: (optional) Includes a player's summary
            if ``True``.
        :param return_json: (optional) Boolean. If ``True`` returns a ``dict``,
            if ``False`` returns a :class:`Player` object. Defaults to
            ``False``.
        :rtype: :class:`Player` or ``dict``
        :raises ValueError: Player with ``player_id`` not found
        """
        if not players:
            players = getattr(self, "elements")

        try:
            player = next(
                player for player in players.values() if player["id"] == player_id
            )
        except StopIteration:
            raise ValueError(f"Player with ID {player_id} not found")

        if include_summary:
            player_summary = await self.get_player_summary(
                player["id"], return_json=True
            )
            player.update(player_summary)

        if return_json:
            return player

        return Player(player, self.session)

    async def get_players(
        self, player_ids=None, include_summary=False, return_json=False
    ):
        """Returns either a list of *all* players, or a list of players whose
        IDs are in the given ``player_ids`` list.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/bootstrap-static/
            https://fantasy.premierleague.com/api/element-summary/1/ (optional)

        :param list player_ids: (optional) A list of player IDs
        :param boolean include_summary: (optional) Includes a player's summary
            if ``True``.
        :param return_json: (optional) Boolean. If ``True`` returns a list of
            ``dict``s, if ``False`` returns a list of  :class:`Player`
            objects. Defaults to ``False``.
        :type return_json: bool
        :rtype: list
        """
        players = getattr(self, "elements")

        if not include_summary:
            if player_ids:
                players = [
                    player
                    for player in list(players.values())
                    if player["id"] in player_ids
                ]
            else:
                players = list(players.values())

            if not return_json:
                players = [Player(player, self.session) for player in players]

            return players

        if not player_ids:
            player_ids = [player["id"] for player in list(players.values())]

        tasks = [
            asyncio.ensure_future(
                self.get_player(player_id, players, include_summary, return_json)
            )
            for player_id in player_ids
        ]
        players = await asyncio.gather(*tasks)

        return players

    async def get_fixture(self, fixture_id, return_json=False):
        """Returns the fixture with the given ``fixture_id``.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/fixtures/
            https://fantasy.premierleague.com/api/fixtures/?event=1

        :param int fixture_id: The fixture's ID.
        :param return_json: (optional) Boolean. If ``True`` returns a ``dict``,
            if ``False`` returns a :class:`Fixture` object. Defaults to
            ``False``.
        :type return_json: bool
        :rtype: :class:`Fixture` or ``dict``
        :raises ValueError: if fixture with ``fixture_id`` not found
        """
        fixtures = await fetch(
            self.session, API_URLS["fixtures"], access_token=self.access_token
        )

        try:
            fixture = next(
                fixture for fixture in fixtures if fixture["id"] == fixture_id
            )
        except StopIteration:
            raise ValueError(f"Fixture with ID {fixture_id} not found")
        fixture_gameweek = fixture["event"]

        gameweek_fixtures = await fetch(
            self.session, API_URLS["gameweek_fixtures"].format(fixture_gameweek)
        )

        try:
            fixture = next(
                fixture for fixture in gameweek_fixtures if fixture["id"] == fixture_id
            )
        except StopIteration:
            raise ValueError(
                f"Fixture with ID {fixture_id} not found in gameweek fixtures"
            )

        if return_json:
            return fixture

        return Fixture(fixture)

    async def get_fixtures_by_id(self, fixture_ids, return_json=False):
        """Returns a list of all fixtures with IDs included in the
        `fixture_ids` list.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/fixtures/
            https://fantasy.premierleague.com/api/fixtures/?event=1

        :param list fixture_ids: A list of fixture IDs.
        :param return_json: (optional) Boolean. If ``True`` returns a list of
            ``dict``s, if ``False`` returns a list of  :class:`Fixture`
            objects. Defaults to ``False``.
        :type return_json: bool
        :rtype: list
        """
        if not fixture_ids:
            return []

        fixtures = await fetch(
            self.session, API_URLS["fixtures"], access_token=self.access_token
        )
        fixture_gameweeks = set(
            fixture["event"] for fixture in fixtures if fixture["id"] in fixture_ids
        )
        tasks = [
            asyncio.ensure_future(
                fetch(self.session, API_URLS["gameweek_fixtures"].format(gameweek))
            )
            for gameweek in fixture_gameweeks
        ]

        gameweek_fixtures = await asyncio.gather(*tasks)
        merged_fixtures = list(itertools.chain(*gameweek_fixtures))

        fixtures = [
            fixture for fixture in merged_fixtures if fixture["id"] in fixture_ids
        ]

        if return_json:
            return fixtures

        return [Fixture(fixture) for fixture in fixtures]

    async def get_fixtures_by_gameweek(self, gameweek, return_json=False):
        """Returns a list of all fixtures of the given ``gameweek``.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/fixtures/
            https://fantasy.premierleague.com/api/fixtures/?event=1

        :param gameweek: A gameweek.
        :type gameweek: string or int
        :param return_json: (optional) Boolean. If ``True`` returns a list of
            ``dict``s, if ``False`` returns a list of  :class:`Player`
            objects. Defaults to ``False``.
        :type return_json: bool
        :rtype: list
        """
        fixtures = await fetch(
            self.session, API_URLS["gameweek_fixtures"].format(gameweek)
        )

        if return_json:
            return fixtures

        return [Fixture(fixture) for fixture in fixtures]

    async def get_fixtures(self, return_json=False):
        """Returns a list of *all* fixtures.
        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/fixtures/
        :param return_json: (optional) Boolean. If ``True`` returns a list of
            ``dicts``, if ``False`` returns a list of  :class:`Fixture`
            objects. Defaults to ``False``.
        :type return_json: bool
        :rtype: list
        """
        task = asyncio.ensure_future(fetch(self.session, API_URLS["fixtures"]))

        gameweek_fixtures = await asyncio.gather(task)
        fixtures = list(itertools.chain(*gameweek_fixtures))

        if return_json:
            return fixtures

        return [Fixture(fixture) for fixture in fixtures]

    async def get_gameweek(self, gameweek_id, include_live=False, return_json=False):
        """Returns the gameweek with the ID ``gameweek_id``.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/bootstrap-static/
            https://fantasy.premierleague.com/api/event/1/live/

        :param int gameweek_id: A gameweek's ID.
        :param bool include_live: (optional) Includes a gameweek's live data
            if ``True``.
        :param return_json: (optional) Boolean. If ``True`` returns a ``dict``,
            if ``False`` returns a :class:`Gameweek` object. Defaults to
            ``False``.
        :type return_json: bool
        :rtype: :class:`Gameweek` or ``dict``
        """

        static_gameweeks = getattr(self, "events")

        try:
            static_gameweek = next(
                gameweek
                for gameweek in static_gameweeks.values()
                if gameweek["id"] == gameweek_id
            )
        except StopIteration:
            raise ValueError(f"Gameweek with ID {gameweek_id} not found")

        if include_live:
            live_gameweek = await fetch(
                self.session, API_URLS["gameweek_live"].format(gameweek_id)
            )

            # Convert element list to dict
            live_gameweek["elements"] = {
                element["id"]: element for element in live_gameweek["elements"]
            }

            # Include live bonus points
            if not static_gameweek["finished"]:
                fixtures = await self.get_fixtures_by_gameweek(gameweek_id)
                fixtures = filter(lambda f: not f.finished, fixtures)
                bonus_for_gameweek = []

                for fixture in fixtures:
                    bonus = fixture.get_bonus(provisional=True)
                    bonus_for_gameweek.extend(bonus["a"] + bonus["h"])

                bonus_for_gameweek = {
                    bonus["element"]: bonus["value"] for bonus in bonus_for_gameweek
                }

                for player_id, bonus_points in bonus_for_gameweek.items():
                    if live_gameweek["elements"][player_id]["stats"]["bonus"] == 0:
                        live_gameweek["elements"][player_id]["stats"][
                            "bonus"
                        ] += bonus_points
                        live_gameweek["elements"][player_id]["stats"][
                            "total_points"
                        ] += bonus_points

            static_gameweek.update(live_gameweek)

        if return_json:
            return static_gameweek

        return Gameweek(static_gameweek)

    async def get_gameweeks(
        self, gameweek_ids=None, include_live=False, return_json=False
    ):
        """Returns either a list of *all* gamweeks, or a list of gameweeks
        whose IDs are in the ``gameweek_ids`` list.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/bootstrap-static/
            https://fantasy.premierleague.com/api/event/1/live/

        :param list gameweek_ids: (optional) A list of gameweek IDs.
        :param return_json: (optional) Boolean. If ``True`` returns a list of
            ``dict``s, if ``False`` returns a list of  :class:`Gameweek`
            objects. Defaults to ``False``.
        :type return_json: bool
        :rtype: list
        """

        if not gameweek_ids:
            gameweek_ids = range(1, 39)

        tasks = [
            asyncio.ensure_future(
                self.get_gameweek(gameweek_id, include_live, return_json)
            )
            for gameweek_id in gameweek_ids
        ]

        gameweeks = await asyncio.gather(*tasks)
        return gameweeks

    async def get_classic_league(self, league_id, return_json=False):
        """Returns the classic league with the given ``league_id``. Requires
        the user to have logged in using ``fpl.login()``.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/leagues-classic/967/standings/

        :param string league_id: A classic league's ID.
        :type league_id: string or int
        :param return_json: (optional) Boolean. If ``True`` returns a ``dict``,
            if ``False`` returns a :class:`ClassicLeague` object. Defaults to
            ``False``.
        :type return_json: bool
        :rtype: :class:`ClassicLeague` or ``dict``
        """
        if not logged_in(self.session):
            raise Exception("User must be logged in.")

        url = API_URLS["league_classic"].format(league_id)
        league = await fetch(self.session, url)

        if return_json:
            return league

        return ClassicLeague(league, session=self.session)

    async def get_h2h_league(self, league_id, return_json=False):
        """Returns a `H2HLeague` object with the given `league_id`. Requires
        the user to have logged in using ``fpl.login()``.

        Information is taken from e.g.:
            https://fantasy.premierleague.com/api/leagues-h2h-matches/league/946125/

        :param league_id: A H2H league's ID.
        :type league_id: string or int
        :param return_json: (optional) Boolean. If ``True`` returns a ``dict``,
            if ``False`` returns a :class:`H2HLeague` object. Defaults to
            ``False``.
        :type return_json: bool
        :rtype: :class:`H2HLeague` or ``dict``
        """
        if not logged_in(self.session):
            raise Exception("User must be logged in.")

        url = API_URLS["league_h2h"].format(league_id)
        league = await fetch(self.session, url, access_token=self.access_token)

        if return_json:
            return league

        return H2HLeague(league, session=self.session, access_token=self.access_token)

    def _generate_code_verifier(self):
        return secrets.token_urlsafe(64)[:128]

    def _generate_code_challenge(self, verifier):
        digest = hashlib.sha256(verifier.encode()).digest()
        return base64.urlsafe_b64encode(digest).decode().rstrip("=")

    async def login_v2(self, email: str, password: str):
        code_verifier = self._generate_code_verifier()  # code_verifier for PKCE
        code_challenge = self._generate_code_challenge(
            code_verifier
        )  # code_challenge from the code_verifier
        initial_state = uuid.uuid4().hex  # random initial state for the OAuth flow

        session = requests.Session()

        # Step 1: Request authorization page
        params = {
            "client_id": "bfcbaf69-aade-4c1b-8f00-c1cb8a193030",
            "redirect_uri": "https://fantasy.premierleague.com/",
            "response_type": "code",
            "scope": "openid profile email offline_access",
            "state": initial_state,
            "code_challenge": code_challenge,
            "code_challenge_method": "S256",
        }
        auth_response = session.get(API_URLS["auth"], params=params)
        login_html = auth_response.text

        access_token = re.search(r'"accessToken":"([^"]+)"', login_html).group(1)
        # need to read state here for when we resume the OAuth flow later on
        new_state = re.search(
            r'<input[^>]+name="state"[^>]+value="([^"]+)"', login_html
        ).group(1)

        # Step 2: Use accessToken to get interaction id and token
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }
        response = session.post(API_URLS["start"], headers=headers).json()
        interaction_id = response["interactionId"]
        interaction_token = response["interactionToken"]

        # Step 3: log in with interaction tokens (requires 2 post requests)
        response = session.post(
            API_URLS["login"],
            headers={
                "interactionId": interaction_id,
                "interactionToken": interaction_token,
            },
            json={
                "id": response["id"],
                "eventName": "continue",
                "parameters": {"eventType": "polling"},
                "pollProps": {
                    "status": "continue",
                    "delayInMs": 10,
                    "retriesAllowed": 1,
                    "pollChallengeStatus": False,
                },
            },
        )

        response = session.post(
            API_URLS["login"],
            headers={
                "interactionId": interaction_id,
                "interactionToken": interaction_token,
            },
            json={
                "id": response.json()["id"],
                "nextEvent": {
                    "constructType": "skEvent",
                    "eventName": "continue",
                    "params": [],
                    "eventType": "post",
                    "postProcess": {},
                },
                "parameters": {
                    "buttonType": "form-submit",
                    "buttonValue": "SIGNON",
                    "username": email,
                    "password": password,
                },
                "eventName": "continue",
            },
        )
        dv_response = response.json()["dvResponse"]

        # Step 4: Resume the login using the dv_response and handle redirect
        response = session.post(
            API_URLS["resume"],
            data={
                "dvResponse": dv_response,
                "state": new_state,
            },
            allow_redirects=False,
        )

        location = response.headers["Location"]
        auth_code = re.search(r"[?&]code=([^&]+)", location).group(1)

        # Step 5: Exchange auth code for access token
        response = session.post(
            API_URLS["token"],
            data={
                "grant_type": "authorization_code",
                "redirect_uri": "https://fantasy.premierleague.com/",
                "code": auth_code,  # from the parsed redirect URL
                "code_verifier": code_verifier,  # the original code_verifier generated at the start
                "client_id": "bfcbaf69-aade-4c1b-8f00-c1cb8a193030",
            },
        )

        self.access_token = response.json()["access_token"]
        response = session.get(
            API_URLS["me"],
            headers={"X-API-Authorization": f"Bearer {self.access_token}"},
        )
        # print(response.json())
        self.session = session

    @DeprecationWarning
    async def login(self, email=None, password=None, cookie=None):
        """Returns a requests session with FPL login authentication.

        :param string email: Email address for the user's Fantasy Premier
            League account.
        :param string password: Password for the user's Fantasy Premier League
            account.
        :param string cookie: Cookie extracted from the user's browser which increases
            success chance when trying to log in.
        """
        if not email and not password:
            email = os.getenv("FPL_EMAIL", None)
            password = os.getenv("FPL_PASSWORD", None)
        if not email or not password:
            raise ValueError("Email and password must be set")

        payload = {
            "login": email,
            "password": password,
            "app": "plfpl-web",
            "redirect_uri": "https://fantasy.premierleague.com/a/login",
        }

        if not cookie:
            cookie = os.getenv("FPL_COOKIE")
        headers = {
            "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 5.1; PRO 5 Build/LMY47D)",
        }
        if cookie is not None:
            headers["Cookie"] = cookie

        login_url = "https://users.premierleague.com/accounts/login/"
        async with self.session.post(
            login_url, data=payload, ssl=ssl_context, headers=headers
        ) as response:
            if response.status == 403:
                raise Exception(
                    "403 forbidden returned by FPL API, consider setting FPL_COOKIE environment variable "
                    "to the cookie in your browser when logged into the fpl website."
                )

            state = response.url.query["state"]
            if state == "fail":
                reason = response.url.query["reason"]
                raise ValueError(f"Login not successful, reason: {reason}")

    async def get_points_against(self):
        """Returns a dictionary containing the points scored against all teams
        in the Premier League, split by position and location.

        An example:

        .. code-block:: javascript

          {
            "Man City": {
                "all": {
                "H": [3, ..., 1],
                "A": [2, ..., 2]
                },
                "goalkeeper": {
                "H": [3, ..., 3],
                "A": [2, ..., 3]
                },
                "defender": {
                "H": [1, ..., 2],
                "A": [4, ..., 1]
                },
                "midfielder": {
                "H": [2, ..., 1],
                "A": [2, ..., 2]
                },
                "forward": {
                "H": [1, ..., 2],
                "A": [6, ..., 1]
                }
            },
            ...
          }

        :rtype: dict
        """
        players = await self.get_players(include_summary=True, return_json=True)
        points_against = {}

        for player in players:
            position = position_converter(player["element_type"]).lower()

            for fixture in player["history"]:
                if fixture["minutes"] == 0:
                    continue

                points = fixture["total_points"]
                opponent = team_converter(fixture["opponent_team"])
                location = "H" if fixture["was_home"] else "A"

                points_against.setdefault(
                    opponent,
                    {
                        "all": {"H": [], "A": []},
                        "goalkeeper": {"H": [], "A": []},
                        "defender": {"H": [], "A": []},
                        "midfielder": {"H": [], "A": []},
                        "forward": {"H": [], "A": []},
                    },
                )

                points_against[opponent]["all"][location].append(points)
                points_against[opponent][position][location].append(points)

        return points_against

    async def FDR(self):
        """Creates a new Fixture Difficulty Ranking (FDR) based on the number
        of points each team gives up to players in the Fantasy Premier League.
        These numbers are also between 1.0 and 5.0 to give a similar ranking
        system to the official FDR.

        An example:

        .. code-block:: javascript

          {
            "Man City": {
                "all": {
                "H": 4.4524439427082,
                "A": 5
                },
                "goalkeeper": {
                "H": 3.6208195949129,
                "A": 5
                },
                "defender": {
                "H": 3.747999604078,
                "A": 5
                },
                "midfielder": {
                "H": 4.6103045986504,
                "A": 5
                },
                "forward": {
                "H": 5,
                "A": 3.9363219561895
                }
            },
            ...,
            "Arsenal": {
                "all": {
                "H": 3.4414041151234,
                "A": 4.2904529162594
                },
                "goalkeeper": {
                "H": 4.1106924163919,
                "A": 4.3867595818815
                },
                "defender": {
                "H": 3.6720291204673,
                "A": 4.3380917450181
                },
                "midfielder": {
                "H": 3.3537357534825,
                "A": 4.0706443384718
                },
                "forward": {
                "H": 2.5143403441683,
                "A": 4.205298013245
                }
            }
          }

        :rtype: dict
        """

        def average_points_against(points_against):
            """Returns a dict with the average points scored against all teams,
            per position and location.

            :param dict points_against: A dict containing the points scored
                against each team in the Premier League.
            :rtype: dict
            """
            for team, positions in points_against.items():
                for position in positions.values():
                    position["H"] = average(position["H"])
                    position["A"] = average(position["A"])

                points_against[team] = positions

            return points_against

        def get_extrema(points_against):
            """Returns the extrema for each position and location.

            :param dict points_against: A dict containing the points scored
                against each team in the Premier League.
            :rtype: dict
            """
            averages = {}
            for _, positions in points_against.items():
                for position, average in positions.items():
                    averages.setdefault(position, {"H": [], "A": []})
                    averages[position]["H"].append(average["H"])
                    averages[position]["A"].append(average["A"])

            for position, locations in averages.items():
                min_h = min(locations["H"])
                min_a = min(locations["A"])
                max_h = max(locations["H"])
                max_a = max(locations["A"])
                averages[position]["H"] = [min_h, max_h]
                averages[position]["A"] = [min_a, max_a]

            return averages

        def calculate_fdr(average_points, extrema):
            """Returns a dict containing the FDR for each team, which is
            calculated by scaling the average points conceded per position
            between 1.0 and 5.0 using the given extrema.

            :param dict points_against: A dict containing the points scored
                against each team in the Premier League.
            :param dict extrema: A dict containing the extrema for each
                position and location.
            :rtype: dict
            """
            for team, positions in average_points.items():
                for position, locations in positions.items():
                    min_h, max_h = extrema[position]["H"]
                    min_a, max_a = extrema[position]["A"]

                    fdr_h = scale(locations["H"], 5.0, 1.0, min_h, max_h)
                    fdr_a = scale(locations["A"], 5.0, 1.0, min_a, max_a)

                    average_points[team][position]["H"] = fdr_h
                    average_points[team][position]["A"] = fdr_a

            return average_points

        points_against = await self.get_points_against()
        average_points = average_points_against(points_against)
        extrema = get_extrema(average_points)
        fdr = calculate_fdr(average_points, extrema)

        return fdr
