import aiohttp
import pytest

from fpl.models.user import User, valid_gameweek
from tests.helper import AsyncMock

user_data = {
    "entry": {
        "id": 3808385,
        "player_first_name": "Amos",
        "player_last_name": "Bastian",
        "player_region_id": 152,
        "player_region_name": "Netherlands",
        "player_region_short_iso": "NL",
        "summary_overall_points": 1621,
        "summary_overall_rank": 22424,
        "summary_event_points": 75,
        "summary_event_rank": 839850,
        "joined_seconds": 16972,
        "current_event": 26,
        "total_transfers": 23,
        "total_loans": 0,
        "total_loans_active": 0,
        "transfers_or_loans": "transfers",
        "deleted": False,
        "email": False,
        "joined_time": "2018-08-09T22:44:21Z",
        "name": "( ͡° ͜ʖ ͡°)",
        "bank": 43,
        "value": 1024,
        "kit": "{\"kit_shirt_type\":\"plain\",\"kit_shirt_base\":\"#ff0000\",\"kit_shirt_sleeves\":\"#ff0000\",\"kit_shirt_secondary\":\"#e1e1e1\",\"kit_shirt_logo\":\"none\",\"kit_shorts\":\"#000000\",\"kit_socks_type\":\"plain\",\"kit_socks_base\":\"#ffffff\",\"kit_socks_secondary\":\"#e1e1e1\"}",
        "event_transfers": 0,
        "event_transfers_cost": 0,
        "extra_free_transfers": 1,
        "strategy": None,
        "favourite_team": 14,
        "started_event": 1,
        "player": 7425806
    },
    "leagues": {
        "cup": [

        ],
        "h2h": [

        ],
        "classic": []
    }
}


@pytest.fixture()
async def user():
    session = aiohttp.ClientSession()
    yield User(user_data, session)
    await session.close()


class TestHelpers:
    def test_valid_gameweek_gameweek_out_of_range(self):
        with pytest.raises(ValueError):
            valid_gameweek(0)
        with pytest.raises(ValueError):
            valid_gameweek(39)

    def test_valid_gameweek_valid_gameweek(self):
        assert valid_gameweek(1) is True


class TestUser(object):
    async def test_init(self, loop):
        session = aiohttp.ClientSession()
        user = User(user_data, session)
        assert user._session is session
        assert user.leagues is user_data["leagues"]
        for k, v in user_data["entry"].items():
            assert getattr(user, k) == v
        await session.close()

    async def test_get_gameweek_history_unknown_gameweek_cached(self, loop, mocker, user):
        user._history = {"history": [{"event": 1}, {"event": 2}, {"event": 3}]}
        mocked_fetch = mocker.patch("fpl.models.user.fetch", return_value={}, new_callable=AsyncMock)
        history = await user.get_gameweek_history()
        assert history is user._history["history"]
        mocked_fetch.assert_not_called()

    async def test_get_gameweek_history_unknown_gameweek_non_cached(self, loop, mocker, user):
        mocked_fetch = mocker.patch("fpl.models.user.fetch",
                                    return_value={"history": [{"event": 1}, {"event": 2}, {"event": 3}]},
                                    new_callable=AsyncMock)
        history = await user.get_gameweek_history()
        mocked_fetch.assert_called_once()
        assert isinstance(history, list)
        assert len(history) == 3

    async def test_get_gameweek_history_known_gameweek_cached(self, loop, mocker, user):
        mocked_fetch = mocker.patch("fpl.models.user.fetch",
                                    return_value={"history": []},
                                    new_callable=AsyncMock)
        events = [{"event": 1}, {"event": 2}, {"event": 3}]
        user._history = {"history": events}
        history = await user.get_gameweek_history(1)
        assert history is events[0]
        mocked_fetch.assert_not_called()

    async def test_get_gameweek_history_known_gameweek_non_cached(self, loop, mocker, user):
        events = [{"event": 1}, {"event": 2}, {"event": 3}]
        mocked_fetch = mocker.patch("fpl.models.user.fetch",
                                    return_value={"history": events},
                                    new_callable=AsyncMock)
        history = await user.get_gameweek_history(1)
        assert history is events[0]
        mocked_fetch.assert_called_once()

    async def test_get_season_history_cached(self, loop, mocker, user):
        mocked_fetch = mocker.patch("fpl.models.user.fetch",
                                    return_value={"season": [{"season": 5}]},
                                    new_callable=AsyncMock)
        seasons = [{"season": 6}]
        user._history = {"season": seasons}
        season_history = await user.get_season_history()
        mocked_fetch.assert_not_called()
        assert season_history is seasons

    async def test_get_season_history_non_cached(self, loop, mocker, user):
        mocked_fetch = mocker.patch("fpl.models.user.fetch",
                                    return_value={"season": [{"season": 5}]},
                                    new_callable=AsyncMock)
        season_history = await user.get_season_history()
        mocked_fetch.assert_called_once()
        assert season_history is mocked_fetch.return_value["season"]

    async def test_get_chips_history_cached_with_unknown_gameweek(self, loop, mocker, user):
        user._history = {"chips": [{"event": 1}, {"event": 2}, {"event": 3}]}
        mocked_fetch = mocker.patch("fpl.models.user.fetch", return_value={}, new_callable=AsyncMock)
        chips_history = await user.get_chips_history()
        assert chips_history is user._history["chips"]
        mocked_fetch.assert_not_called()

    async def test_get_chips_history_non_cached_with_unknown_gameweek(self, loop, mocker, user):
        data = {"chips": [{"event": 1}, {"event": 2}, {"event": 3}]}
        mocked_fetch = mocker.patch("fpl.models.user.fetch", return_value=data, new_callable=AsyncMock)
        chips_history = await user.get_chips_history()
        assert chips_history is mocked_fetch.return_value["chips"]
        mocked_fetch.assert_called_once()

    async def test_get_chips_history_cached_with_known_gameweek(self, loop, mocker, user):
        user._history = {"chips": [{"event": 1}, {"event": 2}, {"event": 3}]}
        mocked_fetch = mocker.patch("fpl.models.user.fetch", return_value={}, new_callable=AsyncMock)
        history = await user.get_chips_history(1)
        assert history is user._history["chips"][0]
        mocked_fetch.assert_not_called()

    async def test_get_chips_history_non_cached_with_known_gameweek(self, loop, mocker, user):
        data = {"chips": [{"event": 1}, {"event": 2}, {"event": 3}]}
        mocked_fetch = mocker.patch("fpl.models.user.fetch", return_value=data, new_callable=AsyncMock)
        chips_history = await user.get_chips_history(1)
        assert chips_history is mocked_fetch.return_value["chips"][0]
        mocked_fetch.assert_called_once()

    async def test_leagues(self, loop, user):
        leagues = user.leagues
        assert isinstance(leagues, dict)

    async def test_get_picks_cached_with_unknown_gameweek(self, loop, mocker, user):
        picks_list = [{"element": 282}, {"element": 280}, {"element": 284}, {"element": 286}]
        user._picks = [{"event": {"id": 1}, "picks": picks_list[:2]},
                       {"event": {"id": 2}, "picks": picks_list[2:]}]
        mocked_fetch = mocker.patch("fpl.models.user.fetch", return_value={}, new_callable=AsyncMock)
        picks = await user.get_picks()
        assert picks == picks_list
        mocked_fetch.assert_not_called()

    async def test_get_picks_non_cached_with_unknown_gameweek(self, loop, mocker, user):
        picks_list = [{"element": 282}, {"element": 280}]
        data = {"event": {"id": 1}, "picks": picks_list}
        mocked_fetch = mocker.patch("fpl.models.user.fetch", return_value=data, new_callable=AsyncMock)
        picks = await user.get_picks()
        assert isinstance(picks, list)
        assert len(picks) == user.current_event * len(picks_list)
        assert mocked_fetch.call_count == user.current_event

    async def test_get_picks_cached_with_known_gameweek(self, loop, mocker, user):
        picks_list = [{"element": 282}, {"element": 280}, {"element": 284}, {"element": 286}]
        user._picks = [{"event": {"id": 1}, "picks": picks_list[:2]},
                       {"event": {"id": 2}, "picks": picks_list[2:]}]
        mocked_fetch = mocker.patch("fpl.models.user.fetch", return_value={}, new_callable=AsyncMock)
        picks = await user.get_picks(1)
        assert picks == picks_list[:2]
        mocked_fetch.assert_not_called()

    async def test_get_picks_non_cached_with_known_gameweek(self, loop, mocker, user):
        picks_list = [{"element": 282}, {"element": 280}]
        data = {"event": {"id": 1}, "picks": picks_list}
        mocked_fetch = mocker.patch("fpl.models.user.fetch", return_value=data, new_callable=AsyncMock)
        picks = await user.get_picks(1)
        assert isinstance(picks, list)
        assert picks == picks_list
        assert mocked_fetch.call_count == user.current_event

    async def test_get_active_chips_cached_with_unknown_gameweek(self, loop, mocker, user):
        user._picks = [{"event": {"id": 1}, "active_chip": "chip one"},
                       {"event": {"id": 2}, "active_chip": "chip two"}]
        mocked_fetch = mocker.patch("fpl.models.user.fetch", return_value={}, new_callable=AsyncMock)
        picks = await user.get_active_chips()
        assert picks == ["chip one", "chip two"]
        mocked_fetch.assert_not_called()

    async def test_get_active_chips_non_cached_with_unknown_gameweek(self, loop, mocker, user):
        data = {"event": {"id": 1}, "active_chip": "chip one"}
        mocked_fetch = mocker.patch("fpl.models.user.fetch", return_value=data, new_callable=AsyncMock)
        picks = await user.get_active_chips()
        assert isinstance(picks, list)
        assert len(picks) == user.current_event
        assert mocked_fetch.call_count == user.current_event

    async def test_get_active_chips_cached_with_known_gameweek(self, loop, mocker, user):
        user._picks = [{"event": {"id": 1}, "active_chip": "chip one"},
                       {"event": {"id": 2}, "active_chip": "chip two"}]
        mocked_fetch = mocker.patch("fpl.models.user.fetch", return_value={}, new_callable=AsyncMock)
        picks = await user.get_active_chips(1)
        assert picks == ["chip one"]
        mocked_fetch.assert_not_called()

    async def test_get_active_chips_non_cached_with_known_gameweek(self, loop, mocker, user):
        data = {"event": {"id": 1}, "active_chip": "chip one"}
        mocked_fetch = mocker.patch("fpl.models.user.fetch", return_value=data, new_callable=AsyncMock)
        picks = await user.get_active_chips(1)
        assert picks == ["chip one"]
        assert mocked_fetch.call_count == user.current_event

    async def test_get_automatic_substitutions_cached_with_unknown_gameweek(self, loop, mocker, user):
        user._picks = [{"event": {"id": 1}, "automatic_subs": [{"id": 6812275}]},
                       {"event": {"id": 2}, "automatic_subs": [{"id": 6800000}]}]
        mocked_fetch = mocker.patch("fpl.models.user.fetch", return_value={}, new_callable=AsyncMock)
        picks = await user.get_automatic_substitutions()
        assert picks == [{"id": 6812275}, {"id": 6800000}]
        mocked_fetch.assert_not_called()

    async def test_get_automatic_substitutions_non_cached_with_unknown_gameweek(self, loop, mocker, user):
        data = {"event": {"id": 1}, "automatic_subs": [{"id": 6812275}]}
        mocked_fetch = mocker.patch("fpl.models.user.fetch", return_value=data, new_callable=AsyncMock)
        picks = await user.get_automatic_substitutions()
        assert isinstance(picks, list)
        assert len(picks) == user.current_event
        assert mocked_fetch.call_count == user.current_event

    async def test_get_automatic_substitutions_cached_with_known_gameweek(self, loop, mocker, user):
        user._picks = [{"event": {"id": 1}, "automatic_subs": [{"id": 6812275}]},
                       {"event": {"id": 2}, "automatic_subs": [{"id": 6800000}]}]
        mocked_fetch = mocker.patch("fpl.models.user.fetch", return_value={}, new_callable=AsyncMock)
        picks = await user.get_automatic_substitutions(1)
        assert picks == [{"id": 6812275}]
        mocked_fetch.assert_not_called()

    async def test_get_automatic_substitutions_non_cached_with_known_gameweek(self, loop, mocker, user):
        data = {"event": {"id": 1}, "automatic_subs": [{"id": 6812275}]}
        mocked_fetch = mocker.patch("fpl.models.user.fetch", return_value=data, new_callable=AsyncMock)
        picks = await user.get_automatic_substitutions(1)
        assert picks == [{"id": 6812275}]
        assert mocked_fetch.call_count == user.current_event

    async def test_get_team_not_authenticated(self, loop, mocker, user):
        mocked_logged_in = mocker.patch("fpl.models.user.logged_in",
                                        return_value=False)
        with pytest.raises(Exception):
            await user.get_team()
        mocked_logged_in.assert_called_once()

    async def test_get_team_authenticated_not_matching_credentials_with_user_id(self, loop, mocker, user):
        mocked_logged_in = mocker.patch("fpl.models.user.logged_in",
                                        return_value=True)
        mocked_fetch = mocker.patch("fpl.models.user.fetch",
                                    return_value={"details": "You cannot view this entry"},
                                    new_callable=AsyncMock)
        with pytest.raises(ValueError):
            await user.get_team()
        mocked_logged_in.assert_called_once()
        mocked_fetch.assert_called_once()

    async def test_get_team_authenticated_matching_credentials_with_user_id(self, loop, mocker, user):
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

    async def test_get_transfers_cached_with_unknown_gameweek(self, loop, mocker, user):
        transfers_data = [{"id": 6812275, "event": 2}, {"id": 6800000, "event": 3}]
        user._transfers = {"event": {"id": 1}, "history": transfers_data}
        mocked_fetch = mocker.patch("fpl.models.user.fetch", return_value={}, new_callable=AsyncMock)
        transfers = await user.get_transfers()
        assert transfers == transfers_data
        mocked_fetch.assert_not_called()

    async def test_get_transfers_non_cached_with_unknown_gameweek(self, loop, mocker, user):
        transfers_data = [{"id": 6812275, "event": 2}, {"id": 6800000, "event": 3}]
        data = {"event": {"id": 1}, "history": transfers_data}
        mocked_fetch = mocker.patch("fpl.models.user.fetch", return_value=data, new_callable=AsyncMock)
        transfers = await user.get_transfers()
        assert transfers == transfers_data
        mocked_fetch.assert_called_once()

    async def test_get_transfers_cached_with_known_gameweek(self, loop, mocker, user):
        transfers_data = [{"id": 6812275, "event": 2}, {"id": 6800000, "event": 3}]
        user._transfers = {"event": {"id": 1}, "history": transfers_data}
        mocked_fetch = mocker.patch("fpl.models.user.fetch", return_value={}, new_callable=AsyncMock)
        transfers = await user.get_transfers(2)
        assert transfers == [transfers_data[0]]
        mocked_fetch.assert_not_called()

    async def test_get_transfers_non_cached_with_known_gameweek(self, loop, mocker, user):
        transfers_data = [{"id": 6812275, "event": 2}, {"id": 6800000, "event": 3}]
        data = {"event": {"id": 1}, "history": transfers_data}
        mocked_fetch = mocker.patch("fpl.models.user.fetch", return_value=data, new_callable=AsyncMock)
        transfers = await user.get_transfers(2)
        assert transfers == [transfers_data[0]]
        mocked_fetch.assert_called_once()

    async def test_get_wildcards_cached(self, loop, mocker, user):
        transfers_data = [{"event": 2}, {"event": 3}]
        user._transfers = {"event": {"id": 1}, "wildcards": transfers_data}
        mocked_fetch = mocker.patch("fpl.models.user.fetch", return_value={}, new_callable=AsyncMock)
        transfers = await user.get_wildcards()
        assert transfers == transfers_data
        mocked_fetch.assert_not_called()

    async def test_get_wildcards_non_cached(self, loop, mocker, user):
        transfers_data = [{"event": 2}, {"event": 3}]
        data = {"event": {"id": 1}, "wildcards": transfers_data}
        mocked_fetch = mocker.patch("fpl.models.user.fetch", return_value=data, new_callable=AsyncMock)
        transfers = await user.get_wildcards()
        assert transfers == transfers_data
        mocked_fetch.assert_called_once()

    async def test_get_watchlist_not_authenticated(self, loop, mocker, user):
        mocked_logged_in = mocker.patch("fpl.models.user.logged_in",
                                        return_value=False)
        with pytest.raises(Exception):
            await user.get_watchlist()
        mocked_logged_in.assert_called_once()

    async def test_get_watchlist_authenticated(self, loop, mocker, user):
        mocked_logged_in = mocker.patch("fpl.models.user.logged_in",
                                        return_value=True)
        data = [{"element": 1}, {"element": 2}]
        mocked_fetch = mocker.patch("fpl.models.user.fetch",
                                    return_value=data,
                                    new_callable=AsyncMock)
        watchlist = await user.get_watchlist()
        assert watchlist == data
        mocked_logged_in.assert_called_once()
        mocked_fetch.assert_called_once()
