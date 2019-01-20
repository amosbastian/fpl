import unittest

from fpl import FPL
from fpl.models.player import Player
from fpl.utils import _run


class GameweekTest(unittest.TestCase):
    def setUp(self):
        self.fpl = FPL()
        self.gameweek = _run(self.fpl.get_gameweek(1))

    def test_gameweek(self):
        self.assertEqual(
            self.gameweek.__str__(), "Gameweek 1 - 10 Aug 19:00")

    def test_fixtures(self):
        self.assertIsInstance(self.gameweek.fixtures, list)

if __name__ == '__main__':
    unittest.main()
