import configparser

config = configparser.ConfigParser()
config.read("credentials.cfg")

TEMP_ENV_VARS = {
    "FPL_EMAIL": config["CREDENTIALS"]["FPL_EMAIL"],
    "FPL_PASSWORD": config["CREDENTIALS"]["FPL_PASSWORD"]
}

ENV_VARS_TO_SUSPEND = [
]
