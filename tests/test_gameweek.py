import unittest

from fpl import FPL
from fpl.models.player import Player


class GameweekTest(unittest.TestCase):
    def setUp(self):
        self.fpl = FPL()
        self.gameweek = self.fpl.get_gameweek(1)

    def test_gameweek(self):
        self.assertEqual(
            self.gameweek.__str__(), "Gameweek 1 - 2018-08-10T18:00:00Z")

    def test_fixtures(self):
        self.assertIsInstance(self.gameweek.fixtures, list)

    def test_get_players(self):
        self.gameweek.get_players()
        self.assertIsInstance(self.gameweek.players, list)
        self.assertIsInstance(self.gameweek.players[0], Player)

if __name__ == '__main__':
    unittest.main()
