import aiohttp
import pytest

from fpl import FPL
from fpl.models.fixture import Fixture


@pytest.fixture()
async def fpl():
    session = aiohttp.ClientSession()
    fpl = FPL(session)
    yield fpl
    await session.close()


@pytest.fixture()
async def classic_league():
    session = aiohttp.ClientSession()
    fpl = FPL(session)
    classic_league = await fpl.get_classic_league(633353)
    yield classic_league
    await session.close()


@pytest.fixture()
def fixture():
    fixture = {
        "id": 6,
        "kickoff_time_formatted": "10 Aug 20:00",
        "started": True,
        "event_day": 1,
        "deadline_time": "2018-08-10T18:00:00Z",
        "deadline_time_formatted": "10 Aug 19:00",
        "stats": [
            {
                "goals_scored": {
                    "a": [{"value": 1, "element": 234}],
                    "h": [{"value": 1, "element": 286}, {"value": 1, "element": 302}],
                }
            },
            {
                "assists": {
                    "a": [{"value": 1, "element": 221}],
                    "h": [{"value": 1, "element": 295}, {"value": 1, "element": 297}],
                }
            },
            {"own_goals": {"a": [], "h": []}},
            {"penalties_saved": {"a": [], "h": []}},
            {"penalties_missed": {"a": [], "h": []}},
            {
                "yellow_cards": {
                    "a": [{"value": 1, "element": 226}],
                    "h": [{"value": 1, "element": 304}, {"value": 1, "element": 481}],
                }
            },
            {"red_cards": {"a": [], "h": []}},
            {
                "saves": {
                    "a": [{"value": 4, "element": 213}],
                    "h": [{"value": 3, "element": 282}],
                }
            },
            {
                "bonus": {
                    "a": [{"value": 1, "element": 234}],
                    "h": [{"value": 3, "element": 286}, {"value": 2, "element": 302}],
                }
            },
            {
                "bps": {
                    "a": [
                        {"value": 25, "element": 234},
                        {"value": 23, "element": 221},
                        {"value": 16, "element": 213},
                        {"value": 16, "element": 215},
                        {"value": 15, "element": 225},
                        {"value": 14, "element": 220},
                        {"value": 13, "element": 227},
                        {"value": 13, "element": 231},
                        {"value": 12, "element": 219},
                        {"value": 10, "element": 233},
                        {"value": 6, "element": 226},
                        {"value": 5, "element": 228},
                        {"value": 3, "element": 492},
                        {"value": 2, "element": 236},
                    ],
                    "h": [
                        {"value": 30, "element": 286},
                        {"value": 29, "element": 302},
                        {"value": 24, "element": 297},
                        {"value": 22, "element": 295},
                        {"value": 16, "element": 289},
                        {"value": 15, "element": 282},
                        {"value": 15, "element": 292},
                        {"value": 13, "element": 291},
                        {"value": 13, "element": 305},
                        {"value": 13, "element": 481},
                        {"value": 8, "element": 304},
                        {"value": 4, "element": 298},
                        {"value": 3, "element": 303},
                        {"value": -2, "element": 306},
                    ],
                }
            },
        ],
        "team_h_difficulty": 3,
        "team_a_difficulty": 4,
        "code": 987597,
        "kickoff_time": "2018-08-10T19:00:00Z",
        "team_h_score": 2,
        "team_a_score": 1,
        "finished": True,
        "minutes": 90,
        "provisional_start_time": False,
        "finished_provisional": True,
        "event": 1,
        "team_a": 11,
        "team_h": 14,
    }
    return Fixture(fixture)


@pytest.fixture()
async def gameweek():
    session = aiohttp.ClientSession()
    fpl = FPL(session)
    gameweek = await fpl.get_gameweek(6)
    yield gameweek
    await session.close()


@pytest.fixture()
async def h2h_league():
    session = aiohttp.ClientSession()
    fpl = FPL(session)
    await fpl.login()
    h2h_league = await fpl.get_h2h_league(760869)
    yield h2h_league
    await session.close()


@pytest.fixture()
async def player():
    session = aiohttp.ClientSession()
    fpl = FPL(session)
    player = await fpl.get_player(345, include_summary=True)
    yield player
    await session.close()


@pytest.fixture()
async def settings():
    session = aiohttp.ClientSession()
    fpl = FPL(session)
    settings = await fpl.get_settings()
    yield settings
    await session.close()


@pytest.fixture()
async def team():
    session = aiohttp.ClientSession()
    fpl = FPL(session)
    team = await fpl.get_team(14)
    yield team
    await session.close()


@pytest.fixture()
async def user():
    session = aiohttp.ClientSession()
    fpl = FPL(session)
    await fpl.login()
    user = await fpl.get_user(3808385)
    yield user
    await session.close()
