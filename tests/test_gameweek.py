from fpl.models import Gameweek

gameweek_data = {
    "id": 1,
    "name": "Gameweek 1",
    "deadline_time": "2018-08-10T18:00:00Z",
    "average_entry_score": 53,
    "finished": True,
    "data_checked": True,
    "highest_scoring_entry": 890626,
    "deadline_time_epoch": 1533924000,
    "deadline_time_game_offset": 3600,
    "deadline_time_formatted": "10 Aug 19:00",
    "highest_score": 137,
    "is_previous": False,
    "is_current": False,
    "is_next": False,
    "fixtures": [],
    "elements": []
}


class TestGameweek(object):
    @staticmethod
    def test_init(loop):
        gameweek = Gameweek(gameweek_data)
        for k, v in gameweek_data.items():
            assert getattr(gameweek, k) == v

    @staticmethod
    def test_str(loop, gameweek):
        assert str(gameweek) == "Gameweek 1"

    @staticmethod
    def test_fixtures(loop, gameweek):
        assert isinstance(gameweek.fixtures, list)
