import asyncio
import unittest

from fpl import FPL
from fpl.models.classic_league import ClassicLeague
from fpl.models.fixture import Fixture
from fpl.models.gameweek import Gameweek
from fpl.models.h2h_league import H2HLeague
from fpl.models.player import Player, PlayerSummary
from fpl.models.team import Team
from fpl.models.user import User


def _run(coroutine):
    return asyncio.get_event_loop().run_until_complete(coroutine)


class FPLTest(unittest.TestCase):
    def setUp(self):
        self.fpl = FPL()

    def test_user(self):
        user = _run(self.fpl.get_user("3523615"))
        self.assertIsInstance(user, User)

        user = _run(self.fpl.get_user("3523615", True))
        self.assertIsInstance(user, dict)

    def test_team(self):
        team = _run(self.fpl.get_team(1))
        self.assertIsInstance(team, Team)

        team = _run(self.fpl.get_team(1, True))
        self.assertIsInstance(team, dict)

    def test_teams(self):
        teams = _run(self.fpl.get_teams())
        self.assertIsInstance(teams, list)
        self.assertEqual(len(teams), 20)
        self.assertIsInstance(teams[0], Team)

        teams = _run(self.fpl.get_teams(return_json=True))
        self.assertIsInstance(teams, list)
        self.assertEqual(len(teams), 20)
        self.assertIsInstance(teams[0], dict)

        teams = _run(self.fpl.get_teams(team_ids=[1, 2, 3]))
        self.assertIsInstance(teams, list)
        self.assertEqual(len(teams), 3)
        self.assertIsInstance(teams[0], Team)
        self.assertListEqual([team.id for team in teams], [1, 2, 3])

    def test_player_summary(self):
        player_summary = _run(self.fpl.get_player_summary(123))
        self.assertIsInstance(player_summary, PlayerSummary)

        player_summary = _run(self.fpl.get_player_summary(123, True))
        self.assertIsInstance(player_summary, dict)

    def test_player_summaries(self):
        player_summaries = _run(self.fpl.get_player_summaries([1, 2, 3]))
        self.assertIsInstance(player_summaries, list)
        self.assertIsInstance(player_summaries[0], PlayerSummary)
        self.assertEqual(len(player_summaries), 3)

        player_summaries = _run(self.fpl.get_player_summaries([1, 2, 3], True))
        self.assertIsInstance(player_summaries[0], dict)

    def test_player(self):
        player = _run(self.fpl.get_player(1))
        self.assertIsInstance(player, Player)

        player = _run(self.fpl.get_player(1, True))
        self.assertIsInstance(player, dict)

    def test_players(self):
        players = _run(self.fpl.get_players())
        self.assertIsInstance(players, list)
        self.assertIsInstance(players[0], Player)

        players = _run(self.fpl.get_players(return_json=True))
        self.assertIsInstance(players, list)
        self.assertIsInstance(players[0], dict)

        players = _run(self.fpl.get_players([1, 2, 3]))
        self.assertEqual(len(players), 3)

    def test_fixture(self):
        fixture = _run(self.fpl.get_fixture(6))
        self.assertIsInstance(fixture, Fixture)

        fixture = _run(self.fpl.get_fixture(6, gameweek=1))
        self.assertIsInstance(fixture, Fixture)

        fixture = _run(self.fpl.get_fixture(6, gameweek=1, return_json=True))
        self.assertIsInstance(fixture, dict)

    def test_fixtures(self):
        fixtures = _run(self.fpl.get_fixtures())
        self.assertIsInstance(fixtures, list)
        self.assertIsInstance(fixtures[0], Fixture)

        fixtures = _run(self.fpl.get_fixtures(gameweek=1))
        self.assertEqual(len(fixtures), 10)
        self.assertIsInstance(fixtures, list)
        self.assertIsInstance(fixtures[0], Fixture)

        fixtures = _run(self.fpl.get_fixtures(gameweek=1, return_json=True))
        self.assertIsInstance(fixtures[0], dict)

    def test_gameweeks(self):
        gameweeks = _run(self.fpl.get_gameweeks())
        self.assertIsInstance(gameweeks, list)
        self.assertEqual(len(gameweeks), 38)
        self.assertIsInstance(gameweeks[0], Gameweek)

        gameweeks = _run(self.fpl.get_gameweeks([1, 2, 3], return_json=True))
        self.assertIsInstance(gameweeks, list)
        self.assertEqual(len(gameweeks), 3)
        self.assertIsInstance(gameweeks[0], dict)

    def test_gameweek(self):
        gameweek = _run(self.fpl.get_gameweek(20))
        self.assertIsInstance(gameweek, Gameweek)
        self.assertEqual(gameweek.id, 20)

        gameweek = _run(self.fpl.get_gameweek(20, return_json=True))
        self.assertIsInstance(gameweek, dict)

    def test_game_settings(self):
        game_settings = _run(self.fpl.game_settings())
        self.assertIsInstance(game_settings, dict)

    def test_classic_league(self):
        classic_league = _run(self.fpl.get_classic_league("890172"))
        self.assertIsInstance(classic_league, ClassicLeague)

        classic_league = _run(
            self.fpl.get_classic_league("890172", return_json=True))
        self.assertIsInstance(classic_league, dict)

    def test_h2h_league(self):
        h2h_league = _run(self.fpl.get_h2h_league("760869"))
        self.assertIsInstance(h2h_league, H2HLeague)

        h2h_league = _run(self.fpl.get_h2h_league("760869", True))
        self.assertIsInstance(h2h_league, dict)

    def test_login(self):
        with self.assertRaises(ValueError):
            _run(self.fpl.login(123, 123))
        _run(self.fpl.login())
        user = _run(self.fpl.get_user(3808385))
        my_team = _run(user.my_team())
        self.assertIsInstance(my_team, list)

    def test_points_against(self):
        points_against = _run(self.fpl.get_points_against())
        self.assertIsInstance(points_against, dict)

    def test_FDR(self):
        def test_main(fdr):
            self.assertIsInstance(fdr, dict)
            self.assertEqual(len(fdr), 20)

            location_extrema = {"H": [], "A": []}
            for team, positions in fdr.items():
                for location in positions.values():
                    location_extrema["H"].append(location["H"])
                    location_extrema["A"].append(location["A"])

            self.assertEqual(max(location_extrema["H"]), 5.0)
            self.assertEqual(min(location_extrema["H"]), 1.0)
            self.assertEqual(max(location_extrema["A"]), 5.0)
            self.assertEqual(min(location_extrema["A"]), 1.0)

        def test_default():
            fdr = self.fpl.FDR()
            test_main(fdr)


if __name__ == '__main__':
    unittest.main()
