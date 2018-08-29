import unittest
import warnings

from fpl import FPL


class FPLTest(unittest.TestCase):
    def setUp(self):
        self.fpl = FPL()
        warnings.filterwarnings("ignore", category=ResourceWarning,
                                message="unclosed.*<ssl.SSLSocket.*>")
        self.player = self.fpl.get_player(1)

    def test_games_played(self):
        pass

    def test_pp90(self):
        pass


if __name__ == '__main__':
    unittest.main()
