import configparser

config = configparser.ConfigParser()
config.read("credentials.cfg")

TEMP_ENV_VARS = {
    "FPL_EMAIL": config["credentials"]["FPL_EMAIL"],
    "FPL_PASSWORD": config["credentials"]["FPL_PASSWORD"]
}

ENV_VARS_TO_SUSPEND = [
]