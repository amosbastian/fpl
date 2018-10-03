

def team_converter(team_id):
    """Converts a team's ID to their actual name."""
    team_map = {
        1: "Arsenal",
        2: "Bournemouth",
        3: "Brighton",
        4: "Burnley",
        5: "Cardiff",
        6: "Chelsea",
        7: "Crystal Palace",
        8: "Everton",
        9: "Fulham",
        10: "Huddersfield",
        11: "Leicester",
        12: "Liverpool",
        13: "Man City",
        14: "Man Utd",
        15: "Newcastle",
        16: "Southampton",
        17: "Spurs",
        18: "Watford",
        19: "West Ham",
        20: "Wolves"
    }
    return team_map[team_id]


def position_converter(position):
    """Converts a player's `element_type` to their actual position."""
    position_map = {
        1: "Goalkeeper",
        2: "Defender",
        3: "Midfielder",
        4: "Forward"
    }
    return position_map[position]


def chip_converter(chip):
    """Converts a chip name to usable string."""
    chip_map = {
        "3xc": "TC",
        "wildcard": "WC",
        "bboost": "BB",
        "freehit": "FH"
    }
    return chip_map[chip]
