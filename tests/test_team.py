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


class TestTeam(object):
    def test_init(self):
        session = None
        team = Team(team_data, session)
        assert team._session is session
        for k, v in team_data.items():
            assert getattr(team, k) == v

    @staticmethod
    def test_str(loop, team):
        assert str(team) == getattr(team, "name")

    async def test_get_players_return_json_is_false(self, loop, team):
        players = await team.get_players(return_json=False)
        print(players)
        assert isinstance(players, list)
        assert len(players) == len(team.players)

        for player in players:
            assert isinstance(player, Player)
            assert getattr(player, "team") == getattr(team, "id")

    async def test_get_players_return_json_is_true(self, loop, team):
        players = await team.get_players(return_json=True)
        assert isinstance(players, list)
        assert players == team.players

    async def test_get_fixtures(self, loop, team):
        fixtures = await team.get_fixtures(return_json=True)
        assert isinstance(fixtures, list)
        assert fixtures == team.fixtures
