import asyncio
from functools import update_wrapper


async def fetch(session, url):
    while True:
        try:
            async with session.get(url) as response:
                assert response.status == 200
                return await response.json()
        except Exception:
            pass


async def post(session, url, payload, headers):
    async with session.post(url, data=payload, headers=headers) as response:
        return await response.json()


async def get_current_gameweek(session):
    """Returns the current gameweek.

    :param aiohttp.ClientSession session: A logged in user's session.
    :rtype: int
    """
    dynamic = await fetch(
        session, "https://fantasy.premierleague.com/drf/bootstrap-dynamic")

    return dynamic["entry"]["current_event"]


def team_converter(team_id):
    """Converts a team's ID to their actual name."""
    team_map = {
        1: "Arsenal",
        2: "Aston Villa",
        3: "Bournemouth",
        4: "Brighton",
        5: "Burnley",
        6: "Chelsea",
        7: "Crystal Palace",
        8: "Everton",
        9: "Leicester",
        10: "Liverpool",
        11: "Man City",
        12: "Man Utd",
        13: "Newcastle",
        14: "Norwich",
        15: "Sheffield Utd",
        16: "Southampton",
        17: "Spurs",
        18: "Watford",
        19: "West Ham",
        20: "Wolves",
        None: None
    }
    return team_map[team_id]


def position_converter(position):
    """Converts a player's `element_type` to their actual position."""
    position_map = {
        1: "Goalkeeper",
        2: "Defender",
        3: "Midfielder",
        4: "Forward"
    }
    return position_map[position]


def chip_converter(chip):
    """Converts a chip name to usable string."""
    chip_map = {
        "3xc": "TC",
        "wildcard": "WC",
        "bboost": "BB",
        "freehit": "FH"
    }
    return chip_map[chip]


def scale(value, upper, lower, min_, max_):
    """Scales value between upper and lower values, depending on the given
    minimun and maximum value.
    """
    numerator = ((lower - upper) * float((value - min_)))
    denominator = float((max_ - min_))
    return numerator / denominator + upper


def average(iterable):
    """Returns the average value of the iterable."""
    return sum(iterable) / float(len(iterable))


def logged_in(session):
    """Checks that the user is logged in within the session.

    :param session: http session
    :type session: aiohttp.ClientSession
    :return: True if user is logged in else False
    :rtype: bool
    """
    return "csrftoken" in session.cookie_jar.filter_cookies(
        "https://users.premierleague.com/")


def coroutine(func):
    func = asyncio.coroutine(func)

    def wrapper(*args, **kwargs):
        loop = asyncio.get_event_loop()
        return loop.run_until_complete(func(*args, **kwargs))
    return update_wrapper(wrapper, func)


def get_headers(referer):
    """Returns the headers needed for the transfer request."""
    return {
        "Content-Type": "application/json; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": referer
    }
