"""
FPL API Documentation Docs
https://cheatography.com/sertalpbilal/cheat-sheets/fpl-api-endpoints/
"""
API_BASE_URL = "https://fantasy.premierleague.com/api/"
API_AUTH_BASE_URL = "https://account.premierleague.com/"

API_URLS = {
    "dynamic": "{}bootstrap-dynamic/".format(API_BASE_URL),
    "fixtures": "{}fixtures/".format(API_BASE_URL),
    "gameweeks": "{}events/".format(API_BASE_URL),
    "gameweek_fixtures": "{}fixtures/?event={{}}".format(API_BASE_URL),
    "gameweek_live": "{}event/{{}}/live".format(API_BASE_URL),
    "league_classic": "{}leagues-classic/{{}}/standings/".format(API_BASE_URL),
    "league_h2h": "{}leagues-h2h/{{}}/standings/".format(API_BASE_URL),
    "league_h2h_fixtures": "{}leagues-h2h-matches/league/{{}}/?{{}}page={{}}".format(
        API_BASE_URL
    ),
    "league_h2h_fixture": "{}leagues-h2h-matches/league/{{}}/?{{}}".format(
        API_BASE_URL
    ),
    "players": "{}elements/".format(API_BASE_URL),
    "player": "{}element-summary/{{}}/".format(API_BASE_URL),
    "settings": "{}game-settings/".format(API_BASE_URL),
    "static": "{}bootstrap-static/".format(API_BASE_URL),
    "teams": "{}teams/".format(API_BASE_URL),
    "transfers": "{}transfers/".format(API_BASE_URL),
    "user": "{}entry/{{}}/".format(API_BASE_URL),
    "user_cup": "{}entry/{{}}/cup/".format(API_BASE_URL),
    "user_history": "{}entry/{{}}/history/".format(API_BASE_URL),
    "user_picks": "{}entry/{{}}/event/{{}}/picks/".format(API_BASE_URL),
    "user_team": "{}my-team/{{}}/".format(API_BASE_URL),
    "user_transfers": "{}entry/{{}}/transfers/".format(API_BASE_URL),
    "user_latest_transfers": "{}entry/{{}}/transfers-latest/".format(API_BASE_URL),
    "watchlist": "{}watchlist/".format(API_BASE_URL),
    "me": "{}me/".format(API_BASE_URL),
    "auth": "{}as/authorize".format(API_AUTH_BASE_URL),
    "start": "{}davinci/policy/262ce4b01d19dd9d385d26bddb4297b6/start".format(
        API_AUTH_BASE_URL
    ),
    "login": "{}davinci/connections/0d8c928e4970386733ce110b9dda8412/capabilities/customHTMLTemplate".format(
        API_AUTH_BASE_URL
    ),
    "resume": "{}as/resume".format(API_AUTH_BASE_URL),
    "token": "{}as/token".format(API_AUTH_BASE_URL),
}

PICKS_FORMAT = "{} {}{}"
MYTEAM_FORMAT = "{}{}"

MIN_GAMEWEEK = 1
MAX_GAMEWEEK = 47
