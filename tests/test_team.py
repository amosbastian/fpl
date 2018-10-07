import unittest

from fpl import FPL
from fpl.models.player import Player


class TeamTest(unittest.TestCase):
    def setUp(self):
        self.fpl = FPL()
        self.team = self.fpl.get_team(1)

    def test_team(self):
        self.assertEqual(self.team.__str__(), self.team.name)

    def test__get_information(self):
        information = self.team._get_information()
        self.assertIsInstance(information, dict)

    def test_get_players(self):
        self.team.get_players()
        self.assertIsInstance(self.team.players, list)
        self.assertIsInstance(self.team.players[0], Player)

    def test_get_fixtures(self):
        self.team.get_fixtures()
        self.assertIsInstance(self.team.fixtures, list)
        self.assertTrue(len(self.team.fixtures) > 0)

if __name__ == '__main__':
    unittest.main()
