import click
import os
import requests
import sqlite3

from appdirs import user_data_dir
from fpl import FPL
from prettytable import PrettyTable

from .utils import chip_converter
from .constants import MYTEAM_FORMAT, PICKS_FORMAT, API_URLS

fpl = FPL()
data_directory = user_data_dir("fpl", "fpl")
sql_file = os.path.join(data_directory, "fpl.sqlite")
connection = sqlite3.connect(sql_file)


@click.group()
def cli():
    pass


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


def myteam_table(user):
    """Print user's myteam data in a pretty table."""
    table = PrettyTable()
    table.field_names = ["Key", "Value"]
    table.add_row(["Overall points", "{:,}".format(user.overall_points)])
    table.add_row(["Overall rank", "{:,}".format(user.overall_rank)])
    table.add_row(["Gameweek points", user.gameweek_points])
    table.add_row(["Squad value", "£{}m".format(user.team_value)])
    table.add_row(["In the bank", "£{}m".format(user.bank)])
    table.add_row(["Chips used", used_chips(user.chips)])
    table.add_row(["Chips available", available_chips(user.chips)])

    table.align["Key"] = "l"
    table.align["Value"] = "r"

    click.echo(str(table).split("\n", 2)[2])


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

    myteam_table(user)


def get_account_data(index):
    """Returns account information of the first account found in the SQLite
    database.

    1: user ID
    2: email address
    3: password
    """
    cursor = connection.cursor()
    accounts = cursor.execute("SELECT * from accounts").fetchall()
    if accounts:
        return accounts[0][index]
    return ""


@cli.command()
@click.argument("user_id", default=get_account_data(1))
@click.option("--email", prompt="Email address", envvar="FPL_EMAIL",
              default=get_account_data(2), help="FPL email address",
              show_default="email saved in SQLite database")
@click.option("--password", prompt=True, hide_input=True,
              envvar="FPL_PASSWORD", default=get_account_data(3),
              help="FPL password",
              show_default="password saved in SQLite database")
def myteam(user_id, email, password):
    """Echoes a logged in user's team to the terminal."""
    fpl.login(email, password)
    try:
        user = fpl.get_user(user_id)
        format_myteam(user)
    except KeyError:
        raise click.BadParameter("email address or password.")


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


def picks_table(user, user_information, players):
    """Print user's picks data in a pretty table."""
    table = PrettyTable()
    table.field_names = ["Key", "Value"]
    table.add_row(["Gamweek points", user.gameweek_points])
    table.add_row(["Gameweek rank", "{:,}".format(user.overall_rank)])

    gameweek_transfers = user_information["entry_history"]["event_transfers"]
    point_hit = user_information["entry_history"]["event_transfers_cost"]
    if point_hit < 0:
        table.add_row(["Gameweek transfers", "{} ({})".format(
            gameweek_transfers, point_hit)])
    else:
        table.add_row(["Gameweek transfers", gameweek_transfers])

    table.add_row(["Points on bench", user_information["entry_history"][
        "points_on_bench"]])
    table.add_row(["Automatic substitutions", automatic_substitutions(
        user_information, players)])

    table.align["Key"] = "l"
    table.align["Value"] = "r"

    click.echo(str(table).split("\n", 2)[2])


def format_picks(user):
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

    picks_table(user, user_information, players)


@cli.command()
@click.argument("user_id")
def picks(user_id):
    """Echoes a user's picks to the terminal."""
    user = fpl.get_user(user_id)
    format_picks(user)


@cli.command()
@click.option("--user_id", prompt="User ID", help="user's FPL ID")
@click.option("--email", prompt="Email address", envvar="FPL_EMAIL",
              help="FPL email address")
@click.option("--password", prompt=True, hide_input=True,
              envvar="FPL_PASSWORD", help="FPL password")
def importaccount(user_id, email, password):
    """Imports an FPL account."""
    if not os.path.isdir(data_directory):
        os.makedirs(data_directory)

    def table_exists():
        """Returns True if `accounts` table exists, otherwise False."""
        query = ("SELECT name FROM sqlite_master "
                 "WHERE type='table' AND name='accounts'")
        try:
            cursor = connection.cursor()
            cursor.execute(query)
            return True if cursor.fetchone() else False
        except sqlite3.OperationalError:
            return False

    def create_table():
        """Creates the `accounts` table."""
        query = ("CREATE TABLE accounts ("
                 "id integer PRIMARY KEY,"
                 "user_id integer,"
                 "email text,"
                 "password text)")
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()

    def account_exists(user_id):
        """Checks if account with user_id already exists in the `accounts`
        table.

        :param int user_id: user's FPL ID
        """
        query = ("SELECT user_id from accounts WHERE user_id=?", (user_id,))
        cursor = connection.cursor()
        cursor.execute(*query)
        account = cursor.fetchone()
        if account:
            return True
        else:
            return False

    def add_account(user_id, email, password):
        """Add a new account to the `accounts` table.

        :param int user_id: user's FPL ID
        :param string email: user's FPL email address
        :param string password: user's FPL password
        """
        if account_exists(user_id):
            raise ValueError("Account with user ID {} already exists!".format(
                user_id))

        # Check if log in possible with provided email and password
        try:
            fpl.login(email, password)
        except ValueError as error:
            click.echo(error)
            return

        # Use my_team function to determine if user ID is associated to email
        user = fpl.get_user(user_id)
        try:
            user.my_team()
        except ValueError as error:
            click.echo(error)
            return

        query = ("INSERT INTO accounts (user_id, email, password) "
                 "VALUES (?, ?, ?)", (user_id, email, password))
        cursor = connection.cursor()
        cursor.execute(*query)
        connection.commit()

    if not table_exists():
        create_table()

    add_account(user_id, email, password)


@cli.command()
@click.argument("email")
def deleteaccount(email):
    """Deletes an imported FPL account."""
    query = ("DELETE FROM accounts WHERE email=?", (email,))
    cursor = connection.cursor()
    cursor.execute(*query)
    connection.commit()


@cli.command()
def listaccounts():
    """Lists all imported FPL accounts."""
    cursor = connection.cursor()
    accounts = cursor.execute("SELECT * from accounts").fetchall()

    if not accounts:
        click.echo("No accounts found.")
        return

    table = PrettyTable()
    table.field_names = ["User ID", "Email"]

    for account in accounts:
        table.add_row([account[1], account[2]])

    table.align["User ID"] = "l"
    click.echo(table)
