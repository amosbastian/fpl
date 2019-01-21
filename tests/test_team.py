from fpl.models.player import Player


class TestTeam(object):
    def test_team(self, loop, team):
        assert team.__str__() == team.name

    async def test_get_players(self, loop, team):
        players = await team.get_players()
        assert isinstance(players, list)
        assert isinstance(players[0], Player)

        players = await team.get_players(return_json=True)
        assert isinstance(players, list)
        assert isinstance(players[0], dict)

    async def test_get_fixtures(self, loop, team):
        fixtures = await team.get_fixtures()
        assert isinstance(team.fixtures, list)
        assert len(team.fixtures) > 0

        fixtures = await team.get_fixtures(return_json=True)
        assert isinstance(team.fixtures, list)
        assert len(team.fixtures) > 0
