import click
import os

from fpl import FPL
from .utils import chip_converter
from.constants import MYTEAM_FORMAT, PICKS_FORMAT


fpl = FPL()


@click.group()
def cli():
    pass


@cli.command()
@click.argument("user_id")
def user(user_id):
    user = fpl.get_user(user_id)
    click.echo(user)


def get_starters(players, position):
    """Helper function that returns starting players in a given position."""
    starters = [player for player in players if player.position == position]
    return starters


def get_picks(team):
    """Returns a list of players with the necessary information to format the
    team's formation properly.
    """
    player_ids = [player["element"] for player in team]
    players = fpl.get_players(player_ids)

    for player_data in team:
        for player in players:
            if player_data["element"] != player.player_id:
                continue

            player.role = ""
            player.gameweek_points = (player.gameweek_points *
                                      player_data["multiplier"])
            player.team_position = player_data["position"]

            player.is_captain = player_data["is_captain"]
            if player.is_captain:
                player.role = " (C)"

            player.is_vice_captain = player_data["is_vice_captain"]
            if player.is_vice_captain:
                player.role = " (VC)"

            if player.status in ["d", "u"]:
                player.colour = "yellow"
            elif player.status in ["i"]:
                player.colour = "red"
            else:
                player.colour = None

    return players


def team_width(positions, points=False):
    """Returns the maximum string width of a team."""
    width = 0

    for position in positions:
        if points:
            player_names = [PICKS_FORMAT.format(
                player.name, player.gameweek_points,
                player.role) for player in position]
        else:
            player_names = [MYTEAM_FORMAT.format(
                player.name, player.role) for player in position]

        position_width = len(" - ".join(player_names))

        if position_width > width:
            width = position_width

    return width


def used_chips(chips):
    """Returns formatted string of used chips."""
    if not chips:
        return "NONE."
    used = ["{} (GW {})".format(chip_converter(chip["name"], chip["event"]))]
    return ", ".join(used)


def available_chips(chips):
    """Returns formatted string of available chips."""
    available = ["WC", "TC", "BB", "FH"]
    used = [chip_converter(chip["name"]) for chip in chips]
    return ", ".join(list(set(available) - set(used)))


def split_by_position(team):
    """Splits the list of list of players by their position."""
    return [
        get_starters(team[:11], "Goalkeeper"),
        get_starters(team[:11], "Defender"),
        get_starters(team[:11], "Midfielder"),
        get_starters(team[:11], "Forward"),
        team[-4:]
    ]


def team_printer(positions, formatter, points=False):
    """Prints the team using the given formatter."""
    width = team_width(positions[1:], points)

    for position in positions:
        player_names = []
        ansi_padding = 0
        for player in position:
            if points:
                player_information = (
                    player.gameweek_points, player.name, player.role)
            else:
                player_information = (player.name, player.role)

            normal_string = formatter.format(*player_information)
            ansi_string = click.style(normal_string, fg=player.colour)
            player_names.append(ansi_string)
            ansi_padding += len(ansi_string) - len(normal_string)

        player_string = " - ".join(player_names)
        formatted_string = "{:^{}}".format(player_string, width + ansi_padding)
        click.echo(formatted_string)


def format_myteam(user):
    """Formats a user's team and echoes it to the terminal."""
    team = user.my_team()
    players = sorted(get_picks(team), key=lambda x: x.team_position)

    goalkeeper, defenders, midfielders, forwards, bench = split_by_position(
        players)

    team_printer([goalkeeper, defenders, midfielders, forwards], MYTEAM_FORMAT)

    click.echo("\nSubstitutes: {}".format(", ".join(
        [click.style("{}".format(player.name), fg=player.colour)
         for player in bench])))

    free_transfers = max(0, 1 + user.free_transfers - user.gameweek_transfers)
    click.echo("\n{}FT / £{}m ITB / £{}m TV".format(
        free_transfers, user.bank, user.team_value))
    click.echo("Chips used: {}".format(used_chips(user.chips)))
    click.echo("Chips available: {}".format(available_chips(user.chips)))


@cli.command()
@click.argument("user_id")
@click.option("--email", prompt="Email address", envvar="FPL_EMAIL")
@click.option("--password", prompt=True, hide_input=True,
              envvar="FPL_PASSWORD")
def myteam(user_id, email, password):
    fpl.login(email, password)
    user = fpl.get_user(user_id)
    format_myteam(user)


def automatic_substitutions(user_information, players):
    """Formats automatic substitutions in a readable way."""
    substitution_ids = [(player["element_in"], player["element_out"])
                        for player in user_information["automatic_subs"]]

    substitutions = []
    for player_in_id, player_out_id in substitution_ids:
        player_in = [player for player in players
                     if player.player_id == player_in_id][0]
        player_out = [player for player in players
                      if player.player_id == player_out_id][0]

        substitutions.append("{} {} -> {} {}".format(
            player_out.gameweek_points,
            click.style(player_out.name, fg=player_out.colour),
            player_in.gameweek_points,
            click.style(player_in.name, fg=player_in.colour)))

    return ", ".join(substitutions)


def format_mypicks(user):
    """Formats a user's picks and echoes it to the terminal."""
    user_information = user.picks[len(user.picks)]
    players = sorted(get_picks(user_information["picks"]),
                     key=lambda x: x.team_position)

    goalkeeper, defenders, midfielders, forwards, bench = split_by_position(
        players)

    team_printer([goalkeeper, defenders, midfielders, forwards],
                 PICKS_FORMAT, True)

    click.echo("\nSubstitutes: {}".format(", ".join(
        ["{} {}".format(player.gameweek_points, click.style(
            player.name, fg=player.colour)) for player in bench])))

    click.echo("\nPoints: {}\nGameweek rank: {:,}".format(
        user_information["entry_history"]["points"],
        user_information["entry_history"]["rank"]))
    click.echo("Automatic substitutions: {}".format(
        automatic_substitutions(user_information, players)))


@cli.command()
@click.argument("user_id")
def picks(user_id):
    user = fpl.get_user(user_id)
    format_mypicks(user)
