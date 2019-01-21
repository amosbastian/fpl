import pytest

from fpl import FPL
from fpl.models.classic_league import ClassicLeague
from fpl.models.fixture import Fixture
from fpl.models.gameweek import Gameweek
from fpl.models.h2h_league import H2HLeague
from fpl.models.player import Player, PlayerSummary
from fpl.models.team import Team
from fpl.models.user import User


class TestFPL(object):
    async def test_user(self, loop, fpl):
        user = await fpl.get_user("3523615")
        assert isinstance(user, User)

        user = await fpl.get_user("3523615", True)
        assert isinstance(user, dict)

    async def test_team(self, loop, fpl):
        team = await fpl.get_team(1)
        assert isinstance(team, Team)

        team = await fpl.get_team(1, True)
        assert isinstance(team, dict)

    async def test_teams(self, loop, fpl):
        teams = await fpl.get_teams()
        assert isinstance(teams, list)
        assert len(teams) == 20
        assert isinstance(teams[0], Team)

        teams = await fpl.get_teams(return_json=True)
        assert isinstance(teams, list)
        assert len(teams) == 20
        assert isinstance(teams[0], dict)

        teams = await fpl.get_teams(team_ids=[1, 2, 3])
        assert isinstance(teams, list)
        assert len(teams) == 3
        assert isinstance(teams[0], Team)
        assert [team.id for team in teams] == [1, 2, 3]

    async def test_player_summary(self, loop, fpl):
        player_summary = await fpl.get_player_summary(123)
        assert isinstance(player_summary, PlayerSummary)

        player_summary = await fpl.get_player_summary(123, True)
        assert isinstance(player_summary, dict)

    async def test_player_summaries(self, loop, fpl):
        player_summaries = await fpl.get_player_summaries([1, 2, 3])
        assert isinstance(player_summaries, list)
        assert isinstance(player_summaries[0], PlayerSummary)
        assert len(player_summaries) == 3

        player_summaries = await fpl.get_player_summaries([1, 2, 3], True)
        assert isinstance(player_summaries[0], dict)

    async def test_player(self, loop, fpl):
        player = await fpl.get_player(1)
        assert isinstance(player, Player)

        player = await fpl.get_player(1, return_json=True)
        assert isinstance(player, dict)

        player_with_summary = await fpl.get_player(1, include_summary=True)

        assert isinstance(player_with_summary.fixtures, list)

    async def test_players(self, loop, fpl):
        players = await fpl.get_players()
        assert isinstance(players, list)
        assert isinstance(players[0], Player)

        players = await fpl.get_players(return_json=True)
        assert isinstance(players, list)
        assert isinstance(players[0], dict)

        players = await fpl.get_players([1, 2, 3])
        assert len(players) == 3

        players = await fpl.get_players([1, 2, 3], True)
        assert len(players) == 3
        assert isinstance(players[0].fixtures, list)

    async def test_fixture(self, loop, fpl):
        fixture = await fpl.get_fixture(6)
        assert isinstance(fixture, Fixture)

        fixture = await fpl.get_fixture(6, return_json=True)
        assert isinstance(fixture, dict)

    async def test_fixtures_by_id(self, loop, fpl):
        fixtures = await fpl.get_fixtures_by_id([100, 200, 300])
        assert isinstance(fixtures, list)
        assert isinstance(fixtures[0], Fixture)

        fixtures = await fpl.get_fixtures_by_id(
            [100, 200, 300], return_json=True)
        assert isinstance(fixtures, list)
        assert isinstance(fixtures[0], dict)

        fixture_ids = [fixture["id"] for fixture in fixtures]
        assert [100, 200, 300] == fixture_ids

    async def test_fixtures_by_gameweek(self, loop, fpl):
        for gameweek in range(1, 39):
            fixtures = await fpl.get_fixtures_by_gameweek(gameweek)
            assert len(fixtures) == 10
            assert isinstance(fixtures, list)
            assert isinstance(fixtures[0], Fixture)

            fixtures = await fpl.get_fixtures_by_gameweek(
                gameweek, return_json=True)
            assert isinstance(fixtures[0], dict)

    async def test_fixtures(self, loop, fpl):
        fixtures = await fpl.get_fixtures()
        assert len(fixtures) == 380
        assert isinstance(fixtures, list)
        assert isinstance(fixtures[0], Fixture)

        fixtures = await fpl.get_fixtures(return_json=True)
        assert isinstance(fixtures[0], dict)

    async def test_gameweeks(self, loop, fpl):
        gameweeks = await fpl.get_gameweeks()
        assert isinstance(gameweeks, list)
        assert len(gameweeks) == 38
        assert isinstance(gameweeks[0], Gameweek)

        gameweeks = await fpl.get_gameweeks([1, 2, 3], return_json=True)
        assert isinstance(gameweeks, list)
        assert len(gameweeks) == 3
        assert isinstance(gameweeks[0], dict)

    async def test_gameweek(self, loop, fpl):
        gameweek = await fpl.get_gameweek(20)
        assert isinstance(gameweek, Gameweek)
        assert gameweek.id == 20

        gameweek = await fpl.get_gameweek(20, return_json=True)
        assert isinstance(gameweek, dict)

    async def test_game_settings(self, loop, fpl):
        game_settings = await fpl.game_settings()
        assert isinstance(game_settings, dict)

    async def test_classic_league(self, loop, fpl):
        classic_league = await fpl.get_classic_league(890172)
        assert isinstance(classic_league, ClassicLeague)

        classic_league = await fpl.get_classic_league(890172, return_json=True)
        assert isinstance(classic_league, dict)

    async def test_h2h_league(self, loop, fpl):
        h2h_league = await fpl.get_h2h_league(760869)
        assert isinstance(h2h_league, H2HLeague)

        h2h_league = await fpl.get_h2h_league(760869, True)
        assert isinstance(h2h_league, dict)

    async def test_login(self, loop, fpl):
        with pytest.raises(ValueError):
            await fpl.login(123, 123)

        await fpl.login()
        user = await fpl.get_user(3808385)
        team = await user.get_team()
        assert isinstance(team, list)

    async def test_points_against(self, loop, fpl):
        points_against = await fpl.get_points_against()
        assert isinstance(points_against, dict)

    async def test_FDR(self, loop, fpl):
        def test_main(fdr):
            assert isinstance(fdr, dict)
            assert len(fdr) == 20

            location_extrema = {"H": [], "A": []}
            for team, positions in fdr.items():
                for location in positions.values():
                    location_extrema["H"].append(location["H"])
                    location_extrema["A"].append(location["A"])

            assert max(location_extrema["H"]) == 5.0
            assert min(location_extrema["H"]) == 1.0
            assert max(location_extrema["A"]) == 5.0
            assert min(location_extrema["A"]) == 1.0

        fdr = await fpl.FDR()
        test_main(fdr)
