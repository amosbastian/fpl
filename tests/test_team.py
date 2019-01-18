import unittest

from fpl import FPL
from fpl.models.player import Player
from fpl.utils import _run


class TeamTest(unittest.TestCase):
    def setUp(self):
        self.fpl = FPL()
        self.team = _run(self.fpl.get_team(1))

    def test_team(self):
        self.assertEqual(self.team.__str__(), self.team.name)

    def test_get_players(self):
        players = _run(self.team.get_players())
        self.assertIsInstance(players, list)
        self.assertIsInstance(players[0], Player)

        players = _run(self.team.get_players(return_json=True))
        self.assertIsInstance(players, list)
        self.assertIsInstance(players[0], dict)

    def test_get_fixtures(self):
        fixtures = _run(self.team.get_fixtures())
        self.assertIsInstance(self.team.fixtures, list)
        self.assertTrue(len(self.team.fixtures) > 0)

        fixtures = _run(self.team.get_fixtures(return_json=True))
        self.assertIsInstance(self.team.fixtures, list)
        self.assertTrue(len(self.team.fixtures) > 0)

if __name__ == '__main__':
    unittest.main()
