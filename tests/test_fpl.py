import unittest
import warnings

from fpl import FPL
from fpl.models.classic_league import ClassicLeague
from fpl.models.gameweek import Gameweek
from fpl.models.h2h_league import H2HLeague
from fpl.models.player import Player
from fpl.models.team import Team
from fpl.models.user import User


class FPLTest(unittest.TestCase):
    def setUp(self):
        self.fpl = FPL()
        warnings.filterwarnings("ignore", category=ResourceWarning,
                                message="unclosed.*<ssl.SSLSocket.*>")

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


if __name__ == '__main__':
    unittest.main()
