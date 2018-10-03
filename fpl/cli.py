from fpl import FPL
from .utils import chip_converter
from.constants import MYTEAM_FORMAT, PICKS_FORMAT
import click
import os


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


def format_myteam(user):
    """Formats the team and echoes it to the terminal."""
    team = user.my_team()
    players = sorted(get_picks(team), key=lambda x: x.team_position)

    goalkeeper = get_starters(players[:11], "Goalkeeper")
    defenders = get_starters(players[:11], "Defender")
    midfielders = get_starters(players[:11], "Midfielder")
    forwards = get_starters(players[:11], "Forward")
    substitutes = players[-4:]

    width = team_width([defenders, midfielders, forwards])

    for position in [goalkeeper, defenders, midfielders, forwards]:
        player_names = []
        for player in position:
            player_names.append(MYTEAM_FORMAT.format(player.name, player.role))

        player_string = " - ".join(player_names)
        formatted_string = "{:^{}}".format(player_string, width)
        click.echo(formatted_string)

    click.echo("\nSubstitutes: {}".format(", ".join(
        [player.name for player in substitutes])))

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


def format_mypicks(user):
    user_information = user.picks[len(user.picks)]
    picks = sorted(get_picks(user_information["picks"]),
                   key=lambda x: x.team_position)

    goalkeeper = get_starters(picks[:11], "Goalkeeper")
    defenders = get_starters(picks[:11], "Defender")
    midfielders = get_starters(picks[:11], "Midfielder")
    forwards = get_starters(picks[:11], "Forward")
    substitutes = sorted(picks, key=lambda x: x.team_position)[-4:]

    width = team_width([defenders, midfielders, forwards], True)

    for position in [goalkeeper, defenders, midfielders, forwards]:
        player_names = []
        for player in position:
            player_names.append(PICKS_FORMAT.format(
                player.gameweek_points, player.name, player.role))

        player_string = " - ".join(player_names)
        formatted_string = "{:^{}}".format(player_string, width)
        click.echo(formatted_string)

    click.echo("\nSubstitutes: {}".format(", ".join(
        ["{} {}".format(player.gameweek_points, player.name)
            for player in substitutes])))


@cli.command()
@click.argument("user_id")
def picks(user_id):
    user = fpl.get_user(user_id)
    format_mypicks(user)
