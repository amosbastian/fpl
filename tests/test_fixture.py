import unittest

from fpl import FPL
from fpl.models.player import Player


class FixtureTest(unittest.TestCase):
    def setUp(self):
        self.fpl = FPL()
        self.fixture = self.fpl.get_fixture(6)

    def test_get_goalscorers(self):
        self.fixture.get_goalscorers()
        self.assertIsInstance(self.fixture.goalscorers, dict)
        for location in ["away", "home"]:
            for player in self.fixture.goalscorers[location]:
                self.assertIsInstance(player["player"], Player)

    def test_get_assisters(self):
        self.fixture.get_assisters()
        self.assertIsInstance(self.fixture.assisters, dict)
        for location in ["away", "home"]:
            for player in self.fixture.assisters[location]:
                self.assertIsInstance(player["player"], Player)

    def test_get_own_goalscorers(self):
        self.fixture.get_own_goalscorers()
        self.assertIsInstance(self.fixture.own_goalscorers, dict)
        for location in ["away", "home"]:
            for player in self.fixture.own_goalscorers[location]:
                self.assertIsInstance(player["player"], Player)

    def test_get_yellow_cards(self):
        self.fixture.get_yellow_cards()
        self.assertIsInstance(self.fixture.yellow_cards, dict)
        for location in ["away", "home"]:
            for player in self.fixture.yellow_cards[location]:
                self.assertIsInstance(player["player"], Player)

    def test_get_red_cards(self):
        self.fixture.get_red_cards()
        self.assertIsInstance(self.fixture.red_cards, dict)
        for location in ["away", "home"]:
            for player in self.fixture.red_cards[location]:
                self.assertIsInstance(player["player"], Player)

    def test_get_penalty_saves(self):
        self.fixture.get_penalty_saves()
        self.assertIsInstance(self.fixture.penalty_saves, dict)
        for location in ["away", "home"]:
            for player in self.fixture.penalty_saves[location]:
                self.assertIsInstance(player["player"], Player)

    def test_get_penalty_misses(self):
        self.fixture.get_penalty_misses()
        self.assertIsInstance(self.fixture.penalty_misses, dict)
        for location in ["away", "home"]:
            for player in self.fixture.penalty_misses[location]:
                self.assertIsInstance(player["player"], Player)

    def test_get_saves(self):
        self.fixture.get_saves()
        self.assertIsInstance(self.fixture.saves, dict)
        for location in ["away", "home"]:
            for player in self.fixture.saves[location]:
                self.assertIsInstance(player["player"], Player)

    def test_get_bonus(self):
        self.fixture.get_bonus()
        self.assertIsInstance(self.fixture.bonus, dict)
        for location in ["away", "home"]:
            for player in self.fixture.bonus[location]:
                self.assertIsInstance(player["player"], Player)

    def test_get_bps(self):
        self.fixture.get_bps()
        self.assertIsInstance(self.fixture.bps, dict)
        for location in ["away", "home"]:
            for player in self.fixture.bps[location]:
                self.assertIsInstance(player["player"], Player)

if __name__ == '__main__':
    unittest.main()
