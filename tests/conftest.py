import aiohttp
import pytest

from fpl import FPL
from fpl.models import Fixture, H2HLeague, User, ClassicLeague, Team, Gameweek
from tests.test_classic_league import classic_league_data
from tests.test_fixture import fixture_data
from tests.test_h2h_league import h2h_league_data
from tests.test_team import team_data
from tests.test_user import user_data
from tests.test_gameweek import gameweek_data


@pytest.fixture()
async def fpl():
    session = aiohttp.ClientSession()
    fpl = FPL(session)
    yield fpl
    await session.close()


@pytest.fixture()
async def classic_league():
    session = aiohttp.ClientSession()
    yield ClassicLeague(classic_league_data, session)
    await session.close()


@pytest.fixture()
async def gameweek():
    return Gameweek(gameweek_data)


@pytest.fixture()
async def player(fpl):
    yield await fpl.get_player(345, include_summary=True)


@pytest.fixture()
async def settings(fpl):
    yield await fpl.game_settings()


@pytest.fixture()
async def team():
    session = aiohttp.ClientSession()
    yield Team(team_data, session)
    await session.close()


@pytest.fixture()
def fixture():
    return Fixture(fixture_data)


@pytest.fixture()
async def h2h_league():
    session = aiohttp.ClientSession()
    yield H2HLeague(h2h_league_data, session)
    await session.close()


@pytest.fixture()
async def user():
    session = aiohttp.ClientSession()
    yield User(user_data, session)
    await session.close()
