import asyncio
import ssl
from datetime import datetime
from functools import update_wrapper
from json import JSONDecodeError

import aiohttp
import certifi
from aiohttp import ClientResponse

from fpl.constants import API_URLS

# headers = {"User-Agent": ""}

ssl_context = ssl.create_default_context(cafile=certifi.where())


def _get_request_headers(access_token) -> dict:
    return {"X-API-Authorization": f"Bearer {access_token}"}


async def fetch(session, url, access_token, retries=10, cooldown=1):
    retries_count = 0
    while True:
        try:
            response = session.get(url, headers=_get_request_headers(access_token))
            result = response.json()
            return result
        except aiohttp.client_exceptions.ContentTypeError:
            retries_count += 1

            if retries_count > retries:
                raise Exception(f"Could not fetch {url} after {retries} retries")

            if cooldown:
                await asyncio.sleep(cooldown)


async def post(session, url, payload, access_token):
    async with session.post(
        url, data=payload, headers=_get_request_headers(access_token)
    ) as response:
        return await response.json()


async def post_transfer(session, url, payload, access_token):
    async with session.post(
        url, data=payload, headers=_get_request_headers(access_token)
    ) as response:
        return await check_response(response)


async def check_response(response: ClientResponse) -> None:
    if response.status == 200:
        return
    try:
        result = await response.json(content_type=None)
    except JSONDecodeError:
        result = await response.text()
        raise Exception(
            f"Unknown error while requesting {response.url}. {response.status} - {result}"
        )

    if result.get("errorCode"):
        message = result.get("error")

        raise Exception(message if message else result)


async def get_total_players(session):
    """Returns the total number of registered players.

    :param aiohttp.ClientSession session: A logged in user's session.
    :rtype: int
    """
    static = await fetch(
        session, "https://fantasy.premierleague.com/api/bootstrap-static/"
    )

    return static["total_players"]


async def get_current_gameweek(session):
    """Returns the current gameweek.

    :param aiohttp.ClientSession session: A logged in user's session.
    :rtype: int
    """
    static = await fetch(
        session, "https://fantasy.premierleague.com/api/bootstrap-static/"
    )

    current_gameweek = next(event for event in static["events"] if event["is_current"])

    return current_gameweek["id"]


def team_converter(team_id):
    """Converts a team's ID to their actual name."""
    team_map = {
        1: "Arsenal",
        2: "Aston Villa",
        3: "Bournemouth",
        4: "Brentford",
        5: "Brighton",
        6: "Burnley",
        7: "Chelsea",
        8: "Crystal Palace",
        9: "Everton",
        10: "Fulham",
        11: "Liverpool",
        12: "Luton",
        13: "Man City",
        14: "Man Utd",
        15: "Newcastle",
        16: "Nott'm Forest",
        17: "Sheffield United",
        18: "Spurs",
        19: "West Ham",
        20: "Wolves",
        None: None,
    }
    return team_map[team_id]


def short_name_converter(team_id):
    """Converts a team's ID to their short name."""
    short_name_map = {
        1: "ARS",
        2: "AVL",
        3: "BOU",
        4: "BRE",
        5: "BHA",
        6: "BUR",
        7: "CHE",
        8: "CRY",
        9: "EVE",
        10: "FUL",
        11: "LIV",
        12: "LUT",
        13: "MCI",
        14: "MUN",
        15: "NEW",
        16: "NFO",
        17: "SHU",
        18: "TOT",
        19: "WHU",
        20: "WOL",
        None: None,
    }
    return short_name_map[team_id]


def position_converter(position):
    """Converts a player's `element_type` to their actual position."""
    position_map = {1: "Goalkeeper", 2: "Defender", 3: "Midfielder", 4: "Forward"}
    return position_map[position]


def chip_converter(chip):
    """Converts a chip name to usable string."""
    chip_map = {"3xc": "TC", "wildcard": "WC", "bboost": "BB", "freehit": "FH"}
    return chip_map[chip]


def date_formatter(date):
    """ "Converts a datetime string from iso format into a more readable format."""
    date_obj = datetime.strptime(date, "%Y-%m-%dT%H:%M:%SZ")
    return date_obj.strftime("%a %d %b %H:%M")


def scale(value, upper, lower, min_, max_):
    """Scales value between upper and lower values, depending on the given
    minimun and maximum value.
    """
    numerator = (lower - upper) * float((value - min_))
    denominator = float((max_ - min_))
    return numerator / denominator + upper


def average(iterable):
    """Returns the average value of the iterable."""
    try:
        return sum(iterable) / float(len(iterable))
    except ZeroDivisionError:
        return 0.0


def logged_in(session):
    """Checks that the user is logged in within the session.

    :param session: http session
    :type session: aiohttp.ClientSession
    :return: True if user is logged in else False
    :rtype: bool
    """
    # return "csrftoken" in session.cookie_jar.filter_cookies(
    #     "https://users.premierleague.com/")
    return "interactionToken" in session.cookies.get_dict()


def coroutine(func):
    func = asyncio.coroutine(func)

    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(func(*args, **kwargs))

    return update_wrapper(wrapper, func)


def get_headers(referer):
    """Returns the headers needed for the transfer request."""
    return {
        "Content-Type": "application/json;charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": referer,
    }


async def get_current_user(session, access_token):
    user = await fetch(session, API_URLS["me"], access_token=access_token)
    return user
