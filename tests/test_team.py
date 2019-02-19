from fpl.models import Player, Team
from tests.helper import AsyncMock

team_data = {
    "id": 1,
    "current_event_fixture": [
        {
            "is_home": False,
            "month": 2,
            "event_day": 1,
            "id": 254,
            "day": 9,
            "opponent": 10
        }
    ],
    "next_event_fixture": [
        {}
    ],
    "name": "Arsenal",
    "code": 3,
    "short_name": "ARS",
    "unavailable": False,
    "strength": 4,
    "position": 0,
    "played": 0,
    "win": 0,
    "loss": 0,
    "draw": 0,
    "points": 0,
    "form": None,
    "link_url": "",
    "strength_overall_home": 1260,
    "strength_overall_away": 1320,
    "strength_attack_home": 1240,
    "strength_attack_away": 1270,
    "strength_defence_home": 1310,
    "strength_defence_away": 1340,
    "team_division": 1
}

team_fixtures = [
    {"id": 261, "team_h": 1},
    {"id": 271, "team_h": 1}
]

player_summary = {
    "fixtures": team_fixtures
}

team_players_data = [
    {"id": 1, "team": 1},
    {"id": 2, "team": 1},
    {"id": 3, "team": 1}
]

team_players_mixed_data = list(team_players_data) + [{"id": 4, "team": 2}, {"id": 5, "team": 3}]


class TestTeam(object):
    def test_init(self):
        session = None
        team = Team(team_data, session)
        assert team.session is session
        for k, v in team_data.items():
            assert getattr(team, k) == v

    @staticmethod
    def test_str(loop, team):
        assert str(team) == getattr(team, "name")

    async def test_get_players_cached_return_json_is_false(self, loop, mocker, team):
        team.players = team_players_data
        mocked_fetch = mocker.patch("fpl.models.team.fetch",
                                    return_value={},
                                    new_callable=AsyncMock)
        players = await team.get_players(return_json=False)
        assert isinstance(players, list)
        assert len(players) == len(team.players)
        for player in players:
            assert isinstance(player, Player)
            assert getattr(player, "team") == getattr(team, "id")
        mocked_fetch.assert_not_called()

    async def test_get_players_cached_return_json_is_true(self, loop, mocker, team):
        team.players = team_players_data
        mocked_fetch = mocker.patch("fpl.models.team.fetch",
                                    return_value={},
                                    new_callable=AsyncMock)
        players = await team.get_players(return_json=True)
        assert isinstance(players, list)
        assert players == team.players
        mocked_fetch.assert_not_called()

    async def test_get_players_non_cached_return_json_is_false(self, loop, mocker, team):
        mocked_fetch = mocker.patch("fpl.models.team.fetch",
                                    return_value=team_players_mixed_data,
                                    new_callable=AsyncMock)
        players = await team.get_players(return_json=False)
        assert isinstance(players, list)
        assert len(players) == len(team.players)
        for player in players:
            assert isinstance(player, Player)
            assert getattr(player, "team") == getattr(team, "id")
        mocked_fetch.assert_called_once()

    async def test_get_players_non_cached_return_json_is_true(self, loop, mocker, team):
        mocked_fetch = mocker.patch("fpl.models.team.fetch",
                                    return_value=team_players_mixed_data,
                                    new_callable=AsyncMock)
        players = await team.get_players(return_json=True)
        assert isinstance(players, list)
        assert players == team.players
        mocked_fetch.assert_called_once()

    async def test_get_fixtures_cached_return_json_is_true(self, loop, mocker, team):
        team.fixtures = team_fixtures
        mocked_fetch = mocker.patch("fpl.models.team.fetch",
                                    return_value={},
                                    new_callable=AsyncMock)
        fixtures = await team.get_fixtures(return_json=True)
        assert isinstance(fixtures, list)
        assert fixtures == team.fixtures
        mocked_fetch.assert_not_called()

    async def test_get_fixtures_non_cached_fixtures_return_json_is_true(self, loop, mocker, team):
        team.players = team_players_data  # cached team players
        mocked_fetch = mocker.patch("fpl.models.team.fetch",
                                    return_value=player_summary,
                                    new_callable=AsyncMock)
        fixtures = await team.get_fixtures(return_json=True)
        assert isinstance(fixtures, list)
        assert fixtures == team_fixtures
        mocked_fetch.assert_called_once()

    async def test_get_fixtures_non_cached_fixtures_non_cached_players_return_json_is_true(self, loop, mocker, team):
        mocked_fetch = mocker.patch("fpl.models.team.fetch",
                                    side_effect=[team_players_data, player_summary],
                                    new_callable=AsyncMock)
        fixtures = await team.get_fixtures(return_json=True)
        assert isinstance(fixtures, list)
        assert fixtures == team_fixtures
        assert mocked_fetch.call_count == 2
