import aiohttp
import pytest

from fpl.models.user import (User, _id_to_element_type, _ids_to_lineup,
                             _set_captain, _set_element_type, valid_gameweek)
from fpl.constants import MIN_GAMEWEEK, MAX_GAMEWEEK
from tests.helper import AsyncMock

user_data = {
    "id": 91928,
    "joined_time": "2019-06-27T18:35:50.271699Z",
    "started_event": 1,
    "favourite_team": 12,
    "player_first_name": "Amos",
    "player_last_name": "Bastian",
    "player_region_id": 152,
    "player_region_name": "Netherlands",
    "player_region_iso_code_short": "NL",
    "player_region_iso_code_long": "NLD",
    "summary_overall_points": 0,
    "summary_overall_rank": 0,
    "summary_event_points": 0,
    "summary_event_rank": 0,
    "current_event": 1,
    "leagues": {
        "cup": [

        ],
        "h2h": [

        ],
        "classic": []
    }
}


def get_picks():
    return [
        {
            "element": 145,
            "position": 5,
            "is_captain": False,
            "is_vice_captain": False,
            "can_captain": True,
        },
        {
            "element": 302,
            "position": 6,
            "is_captain": False,
            "is_vice_captain": True,
            "can_captain": True,
        },
        {
            "element": 253,
            "position": 7,
            "is_captain": False,
            "is_vice_captain": False,
            "can_captain": True,
        },
        {
            "element": 270,
            "position": 8,
            "is_captain": True,
            "is_vice_captain": False,
            "can_captain": True,
        }
    ]


user_player_ids = [145, 302, 253, 270]


class TestHelpers:
    @staticmethod
    def test_valid_gameweek_gameweek_out_of_range():
        with pytest.raises(ValueError):
            valid_gameweek(MIN_GAMEWEEK - 1)
        with pytest.raises(ValueError):
            valid_gameweek(MAX_GAMEWEEK + 1)

    @staticmethod
    def test_valid_gameweek_valid_gameweek():
        assert valid_gameweek(1) is True

    @staticmethod
    def test__ids_to_lineup():
        lineup = [{
            "element": 400
        }]
        assert _ids_to_lineup([400], lineup) == lineup

    @staticmethod
    def test__id_to_element_type():
        players = [{
            "id": 1,
            "element_type": 1
        }]
        assert _id_to_element_type(1, players) == 1

    @staticmethod
    def test__set_element_type():
        lineup = [{
            "element": 400
        }]
        players = [{
            "id": 400,
            "element_type": 1
        }]
        _set_element_type(lineup, players)
        assert lineup[0]["element_type"] == players[0]["element_type"]

    @staticmethod
    def test__set_captain_captain_to_captain():
        user_picks = get_picks()
        captain = next(p for p in user_picks if p["is_captain"])
        _set_captain(user_picks, 270, "is_captain", user_player_ids)
        new_captain = next(p for p in user_picks if p["is_captain"])

        assert new_captain["element"] == captain["element"]

    @staticmethod
    def test__set_captain_vice_to_vice():
        user_picks = get_picks()
        vice_captain = next(p for p in user_picks if p["is_vice_captain"])
        _set_captain(user_picks, 302, "is_vice_captain", user_player_ids)
        new_vice_captain = next(p for p in user_picks if p["is_vice_captain"])

        assert new_vice_captain["element"] == vice_captain["element"]

    @staticmethod
    def test__set_captain_captain_to_vice():
        user_picks = get_picks()
        captain = next(p for p in user_picks if p["is_captain"])
        vice_captain = next(p for p in user_picks if p["is_vice_captain"])
        _set_captain(user_picks, 270, "is_vice_captain", user_player_ids)

        new_captain = next(p for p in user_picks if p["is_captain"])
        new_vice_captain = next(p for p in user_picks if p["is_vice_captain"])

        assert new_captain["element"] == vice_captain["element"]
        assert new_vice_captain["element"] == captain["element"]

    @staticmethod
    def test__set_captain_vice_to_captain():
        user_picks = get_picks()
        captain = next(p for p in user_picks if p["is_captain"])
        vice_captain = next(p for p in user_picks if p["is_vice_captain"])
        _set_captain(user_picks, 302, "is_captain", user_player_ids)

        new_captain = next(p for p in user_picks if p["is_captain"])
        new_vice_captain = next(p for p in user_picks if p["is_vice_captain"])

        assert new_vice_captain["element"] == captain["element"]
        assert new_captain["element"] == vice_captain["element"]

    @staticmethod
    def test__set_captain_captain():
        user_picks = get_picks()
        captain = next(p for p in user_picks if p["is_captain"])
        _set_captain(user_picks, 145, "is_captain", user_player_ids)

        new_captain = next(p for p in user_picks if p["is_captain"])

        assert new_captain["element"] == 145
        assert not captain["is_captain"]

    @staticmethod
    def test__set_captain_vice():
        user_picks = get_picks()
        vice_captain = next(p for p in user_picks if p["is_vice_captain"])
        _set_captain(user_picks, 145, "is_vice_captain", user_player_ids)

        new_vice_captain = next(p for p in user_picks if p["is_vice_captain"])

        assert new_vice_captain["element"] == 145
        assert not vice_captain["is_vice_captain"]


class TestUser:
    @pytest.mark.asyncio
    async def test_init(self):
        session = aiohttp.ClientSession()
        user = User(user_data, session)
        assert user._session is session
        assert user.leagues is user_data["leagues"]
        for k, v in user_data.items():
            assert getattr(user, k) == v
        await session.close()

    @pytest.mark.asyncio
    async def test_get_gameweek_history_unknown_gameweek_cached(
            self, user):
        history = await user.get_gameweek_history()
        assert history is user._history["current"]
        assert isinstance(history, list)

    @pytest.mark.asyncio
    async def test_get_gameweek_history_unknown_gameweek_non_cached(
            self, user):
        history = await user.get_gameweek_history()
        assert isinstance(history, list)

    @pytest.mark.asyncio
    async def test_get_gameweek_history_known_gameweek_cached(
            self, user):
        history = await user.get_gameweek_history(gameweek=1)
        assert history is user._history["current"][0]
        assert isinstance(history, dict)

    @pytest.mark.asyncio
    async def test_get_gameweek_history_known_gameweek_non_cached(
            self, user):
        history = await user.get_gameweek_history(gameweek=1)
        assert isinstance(history, dict)

    @pytest.mark.asyncio
    async def test_get_season_history(self, user):
        season_history = await user.get_season_history()
        assert season_history is user._history["past"]
        assert isinstance(season_history, list)

    @pytest.mark.asyncio
    async def test_get_chips_history(self, user):
        chips_history = await user.get_chips_history()
        assert chips_history is user._history["chips"]
        assert isinstance(chips_history, list)

        chips_history = await user.get_chips_history(gameweek=1)
        assert not chips_history

    @pytest.mark.asyncio
    async def test_leagues(self, user):
        leagues = user.leagues
        assert isinstance(leagues, dict)

    @pytest.mark.asyncio
    async def test_get_picks_should_return_dict(self, user):
        picks = await user.get_picks()
        assert isinstance(picks, dict)

    @pytest.mark.asyncio
    async def test_get_picks_invalid_gameweek_should_raise_exception(
            self, user):
        with pytest.raises(ValueError):
            await user.get_picks(gameweek=0)

    @pytest.mark.asyncio
    async def test_get_picks_valid_gameweek_should_return_dict_with_one_item(
            self, user):
        picks = await user.get_picks(gameweek=1)
        assert len(picks) == 1

    @pytest.mark.asyncio
    async def test_get_picks_cached_with_unknown_gameweek(
            self, user):
        picks_one = await user.get_picks()
        picks_two = await user.get_picks()
        assert len(picks_one) == len(picks_two)

    @pytest.mark.asyncio
    async def test_get_picks_non_cached_with_unknown_gameweek(
            self, user):
        picks = await user.get_picks()
        assert len(picks[1]) == 15

    @pytest.mark.asyncio
    async def test_get_picks_cached_with_known_gameweek(
            self, user):
        picks_one = await user.get_picks(gameweek=1)
        picks_two = await user.get_picks(gameweek=1)
        assert picks_one == picks_two

    @pytest.mark.asyncio
    async def test_get_picks_non_cached_with_known_gameweek(
            self, user):
        picks = await user.get_picks(gameweek=1)
        assert len(picks[1]) == 15

    @pytest.mark.asyncio
    async def test_get_active_chips(self, user):
        active_chips = await user.get_active_chips()
        assert isinstance(active_chips, list)
        active_chips = await user.get_active_chips(gameweek=1)
        assert not active_chips

    @pytest.mark.asyncio
    async def test_get_automatic_substitutions(self, user):
        substitutions = await user.get_automatic_substitutions()
        assert isinstance(substitutions, list)
        substitutions = await user.get_automatic_substitutions(gameweek=1)
        assert not substitutions

    @pytest.mark.asyncio
    async def test_get_team_not_authenticated(self, mocker, user):
        mocked_logged_in = mocker.patch("fpl.models.user.logged_in",
                                        return_value=False)
        with pytest.raises(Exception):
            await user.get_team()
        mocked_logged_in.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_team_authenticated_not_matching_credentials_with_user_id(
            self, mocker, user):
        mocked_logged_in = mocker.patch("fpl.models.user.logged_in",
                                        return_value=True)
        mocked_fetch = mocker.patch("fpl.models.user.fetch",
                                    return_value={
                                        "detail": "Not found."},
                                    new_callable=AsyncMock)
        with pytest.raises(Exception):
            await user.get_team()
        mocked_logged_in.assert_called_once()
        mocked_fetch.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_team_authenticated_matching_credentials_with_user_id(
            self, mocker, user):
        mocked_logged_in = mocker.patch("fpl.models.user.logged_in",
                                        return_value=True)
        data = {"picks": [{"element": 1}, {"element": 2}]}
        mocked_fetch = mocker.patch("fpl.models.user.fetch",
                                    return_value=data,
                                    new_callable=AsyncMock)
        team = await user.get_team()
        assert isinstance(team, list)
        mocked_logged_in.assert_called_once()
        mocked_fetch.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_transfers(self, user):
        transfers = await user.get_transfers()
        assert isinstance(transfers, list)

        transfers = await user.get_transfers(gameweek=1)
        assert isinstance(transfers, list)

    @pytest.mark.asyncio
    async def test_get_latest_transfers_not_authenticated(
            self, mocker, user):
        mocked_logged_in = mocker.patch("fpl.models.user.logged_in",
                                        return_value=False)
        with pytest.raises(Exception):
            await user.get_team()
        mocked_logged_in.assert_called_once()

    @pytest.mark.skip(reason="Cannot currently test it.")
    async def test_get_wildcards_cached(self, user):
        transfers = await user.get_wildcards()
        assert isinstance(transfers, list)

    @pytest.mark.asyncio
    async def test_get_watchlist_not_authenticated(self, mocker, user):
        mocked_logged_in = mocker.patch("fpl.models.user.logged_in",
                                        return_value=False)
        with pytest.raises(Exception):
            await user.get_watchlist()
        mocked_logged_in.assert_called_once()

    @pytest.mark.asyncio
    async def test_get_watchlist_authenticated(self, mocker, user):
        mocked_logged_in = mocker.patch("fpl.models.user.logged_in",
                                        return_value=True)
        data = {"watched": []}
        mocked_fetch = mocker.patch("fpl.models.user.fetch",
                                    return_value=data,
                                    new_callable=AsyncMock)
        watchlist = await user.get_watchlist()
        assert watchlist == data["watched"]
        mocked_logged_in.assert_called_once()
        mocked_fetch.assert_called_once()

    @pytest.mark.asyncio
    async def test__get_transfer_payload(self, user):
        pass

    @pytest.mark.asyncio
    async def test_transfer(self, user):
        # TODO: expand tests
        data = {
            "transfers": [{
                "element_in": 172, "cost": 4, "purchase_price": 72,
                "element_out": 300, "selling_price": 67
            }],
            "freehit": False,
            "wildcard": False,
            "spent_points": 4
        }

        with pytest.raises(Exception):
            await user.transfer([1], [2])

    @pytest.mark.asyncio
    async def test__create_new_lineup(self, user):
        pass

    @pytest.mark.asyncio
    async def test__post_substitutions(self, user):
        pass

    @pytest.mark.asyncio
    async def test__captain_helper(self, user):
        pass

    @pytest.mark.asyncio
    async def test_captain(self, user):
        # TODO: expand tests
        with pytest.raises(Exception):
            await user.captain(1)

    @pytest.mark.asyncio
    async def test_vice_captain(self, user):
        # TODO: expand tests
        with pytest.raises(Exception):
            await user.vice_captain(1)

    @pytest.mark.asyncio
    async def test_substitute(self, user):
        # TODO: expand tests
        with pytest.raises(Exception):
            await user.substitute([1], [2])
