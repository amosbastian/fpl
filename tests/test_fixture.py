import unittest

from fpl import FPL
from fpl.models.player import Player
from fpl.utils import _run


class FixtureTest(unittest.TestCase):
    def setUp(self):
        self.fpl = FPL()
        self.fixture = _run(self.fpl.get_fixture(6))

    def test_get_goalscorers(self):
        goalscorers = self.fixture.get_goalscorers()
        self.assertIsInstance(goalscorers, dict)

    def test_get_assisters(self):
        assisters = self.fixture.get_assisters()
        self.assertIsInstance(assisters, dict)

    def test_get_own_goalscorers(self):
        own_goalscorers = self.fixture.get_own_goalscorers()
        self.assertIsInstance(own_goalscorers, dict)

    def test_get_yellow_cards(self):
        yellow_cards = self.fixture.get_yellow_cards()
        self.assertIsInstance(yellow_cards, dict)

    def test_get_red_cards(self):
        red_cards = self.fixture.get_red_cards()
        self.assertIsInstance(red_cards, dict)

    def test_get_penalty_saves(self):
        penalty_saves = self.fixture.get_penalty_saves()
        self.assertIsInstance(penalty_saves, dict)

    def test_get_penalty_misses(self):
        penalty_misses = self.fixture.get_penalty_misses()
        self.assertIsInstance(penalty_misses, dict)

    def test_get_saves(self):
        saves = self.fixture.get_saves()
        self.assertIsInstance(saves, dict)

    def test_get_bonus(self):
        bonus = self.fixture.get_bonus()
        self.assertIsInstance(bonus, dict)

    def test_get_bps(self):
        bps = self.fixture.get_bps()
        self.assertIsInstance(bps, dict)

if __name__ == '__main__':
    unittest.main()
