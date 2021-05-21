import os
from psychopy import logging

BASE = {
    "test": False,
    "mouse_visible": False,
    "window_dimensions": "full_screen",
    "logging_level": logging.INFO,
    "exp_name": "FH_WordOA_PostTest",
}

TEST = {"test": True, "logging_level": logging.DEBUG,
        "exp_name": "TestExp"}


PRODUCTION = {
    "env": "production",
    "test": False,
    "logging_level": logging.INFO,
    "mouse_visible": False,
    "window_dimensions": "full_screen",
    "exp_name": "FH_WordOA_PostTest",
}

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
