import aiohttp
import pytest

from fpl import FPL
from fpl.models import Fixture, H2HLeague, User, ClassicLeague
from tests.test_classic_league import classic_league_data
from tests.test_fixture import fixture_data
from tests.test_h2h_league import h2h_league_data
from tests.test_user import user_data


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
    session = aiohttp.ClientSession()
    fpl = FPL(session)
    gameweek = await fpl.get_gameweek(6)
    yield gameweek
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
