from ..utils import team_converter
from .player import Player


def add_player(location, information):
    """Appends player to the location list."""
    player = Player(information["element"])
    goals = information["value"]
    location.append({"player": player, "goals": goals})


class Fixture():
    """A class representing fixtures in the Fantasy Premier League."""
    def __init__(self, fixture):
        self.fixture_id = fixture["id"]
        self.kickoff_time_formatted = fixture["kickoff_time_formatted"]
        self.started = fixture["started"]
        self.event_day = fixture["event_day"]
        self.deadline_time = fixture["deadline_time"]
        self.deadline_time_formatted = fixture["deadline_time_formatted"]
        self.statistics = fixture["stats"]
        self.team_h_difficulty = fixture["team_h_difficulty"]
        self.team_a_difficulty = fixture["team_a_difficulty"]
        self.code = fixture["code"]
        self.kickoff_time = fixture["kickoff_time"]
        self.team_h_score = fixture["team_h_score"]
        self.team_a_score = fixture["team_a_score"]
        self.finished = fixture["finished"]
        self.minutes = fixture["minutes"]
        self.provisional_start_time = fixture["provisional_start_time"]
        self.finished_provisional = fixture["finished_provisional"]
        self.gameweek = fixture["event"]
        self.team_a = team_converter(fixture["team_a"])
        self.team_h = team_converter(fixture["team_h"])

        self.goalscorers = None
        self.assisters = None
        self.own_goalscorers = None
        self.yellow_cards = None
        self.red_cards = None
        self.penalty_saves = None
        self.penalty_misses = None
        self.saves = None
        self.bonus = None
        self.bps = None

    def _get_players(self, metric):
        """Helper function that returns a dictionary containing players for the
        given metric (away and home).
        """
        away = []
        home = []

        # Get the statistics for the given metric
        for statistic in self.statistics:
            if metric in statistic.keys():
                player_information = statistic[metric]

        # Create Player objects
        for location in ["a", "h"]:
            for information in player_information[location]:
                if location == "a":
                    add_player(away, information)
                else:
                    add_player(home, information)

        return away, home

    def get_goalscorers(self):
        """Returns all players who scored in the fixture."""
        if not self.statistics:
            return

        away, home = self._get_players("goals_scored")

        self.goalscorers = {"away": away, "home": home}

    def get_assisters(self):
        """Returns all players who made an assist in the fixture."""
        if not self.statistics:
            return

        away, home = self._get_players("assists")

        self.assisters = {"away": away, "home": home}

    def get_own_goalscorers(self):
        """Returns all players who scored an own goal in the fixture."""
        if not self.statistics:
            return

        away, home = self._get_players("own_goals")

        self.own_goalscorers = {"away": away, "home": home}

    def get_yellow_cards(self):
        """Returns all players who received a yellow card in the fixture."""
        if not self.statistics:
            return

        away, home = self._get_players("yellow_cards")

        self.yellow_cards = {"away": away, "home": home}

    def get_red_cards(self):
        """Returns all players who received a red card in the fixture."""
        if not self.statistics:
            return

        away, home = self._get_players("red_cards")

        self.red_cards = {"away": away, "home": home}

    def get_penalty_saves(self):
        """Returns all players who saved a penalty in the fixture."""
        if not self.statistics:
            return

        away, home = self._get_players("penalties_saved")

        self.penalty_saves = {"away": away, "home": home}

    def get_penalty_misses(self):
        """Returns all players who missed a penalty in the fixture."""
        if not self.statistics:
            return

        away, home = self._get_players("penalties_missed")

        self.penalty_misses = {"away": away, "home": home}

    def get_saves(self):
        """Returns all players who made a save in the fixture."""
        if not self.statistics:
            return

        away, home = self._get_players("saves")

        self.saves = {"away": away, "home": home}

    def get_bonus(self):
        """Returns all players who received bonus points in the fixture."""
        if not self.statistics:
            return

        away, home = self._get_players("bonus")

        self.bonus = {"away": away, "home": home}

    def get_bps(self):
        """Returns the bonus points of each player."""
        if not self.statistics:
            return

        away, home = self._get_players("bps")

        self.bps = {"away": away, "home": home}
