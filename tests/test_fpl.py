import unittest

from fpl import FPL
from fpl.models.classic_league import ClassicLeague
from fpl.models.fixture import Fixture
from fpl.models.gameweek import Gameweek
from fpl.models.h2h_league import H2HLeague
from fpl.models.player import Player
from fpl.models.team import Team
from fpl.models.user import User
from pymongo import MongoClient


class FPLTest(unittest.TestCase):
    def setUp(self):
        self.fpl = FPL()

    def test_user(self):
        user = self.fpl.get_user("3523615")
        self.assertIsInstance(user, User)

    def test_team(self):
        team = self.fpl.get_team(1)
        self.assertIsInstance(team, Team)

    def test_teams(self):
        teams = self.fpl.get_teams()
        self.assertIsInstance(teams, list)
        self.assertEqual(len(teams), 20)
        self.assertIsInstance(teams[0], Team)

    def test_player(self):
        player = self.fpl.get_player(1)
        self.assertIsInstance(player, Player)

    def test_players(self):
        players = self.fpl.get_players()
        self.assertIsInstance(players, list)
        self.assertIsInstance(players[0], Player)

    def test_fixture(self):
        fixture = self.fpl.get_fixture(6)
        self.assertIsInstance(fixture, Fixture)
        fixture = self.fpl.get_fixture(6, gameweek=1)
        self.assertIsInstance(fixture, Fixture)

    def test_fixtures(self):
        fixtures = self.fpl.get_fixtures()
        self.assertIsInstance(fixtures, list)
        self.assertIsInstance(fixtures[0], Fixture)
        fixtures = self.fpl.get_fixtures(gameweek=1)
        self.assertEqual(len(fixtures), 10)
        self.assertIsInstance(fixtures, list)
        self.assertIsInstance(fixtures[0], Fixture)

    def test_gameweeks(self):
        gameweeks = self.fpl.get_gameweeks()
        self.assertIsInstance(gameweeks, list)
        self.assertEqual(len(gameweeks), 38)

    def test_gameweek(self):
        gameweek = self.fpl.get_gameweek("20")
        self.assertIsInstance(gameweek, Gameweek)

    def test_game_settings(self):
        game_settings = self.fpl.game_settings()
        self.assertIsInstance(game_settings, dict)

    def test_classic_league(self):
        classic_league = self.fpl.get_classic_league("890172")
        self.assertIsInstance(classic_league, ClassicLeague)

    def test_h2h_league(self):
        h2h_league = self.fpl.get_h2h_league("760869")
        self.assertIsInstance(h2h_league, H2HLeague)

    def test_update_mongodb(self):
        self.fpl.update_mongodb()
        client = MongoClient()
        database = client.fpl

        teams = database.teams.find()
        self.assertEqual(teams.count(), 20)
        team = database.teams.find_one({"team_id": 1})
        self.assertIsInstance(team["fixtures"], list)
        self.assertTrue("FDR" in team.keys())
        self.assertTrue(len(team["fixtures"]) > 0)
        self.assertTrue("FDR" in team["fixtures"][0].keys())

        player = database.players.find_one({"player_id": 1})
        self.assertEqual(player["player_id"], 1)

    def test_get_points_against(self):
        points_against = self.fpl.get_points_against()
        self.assertIsInstance(points_against, dict)
        self.assertEqual(len(points_against), 20)

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

        def test_mongodb():
            fdr = self.fpl.FDR(True)
            test_main(fdr)

if __name__ == '__main__':
    unittest.main()
