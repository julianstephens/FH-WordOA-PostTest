import os
from psychopy import logging

BASE = {
    "test": False,
    "mouse_visible": False,
    "logging_level": logging.INFO,
    "exp_name": "FH_WordOA_PostTest",
    "log_file": "./test_log.xlsx"
}

TEST = {"test": True, "logging_level": logging.DEBUG, "exp_name": "TestExp"}

PRODUCTION = {"test": False, "logging_level": logging.INFO}

DEV = {
    "env": "dev",
    "window_dimensions": "full_screen",
    "button_box": None,
    "n_runs": 1,
}


def get_settings(env, test=False):
    settings = BASE
    settings.update(TEST) if test else settings.update(PRODUCTION)

    if env == "dev":
        settings.update(DEV)
    else:
        raise ValueError('Environment "{0}" not supported.'.format(env))

    return settings
