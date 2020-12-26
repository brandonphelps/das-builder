"""
Helper functions
"""

import os
import toml

# move this to shared module for utils.
CONFIG_FILE_NAME = "das_builder.toml"


def search_for_root(search_start=os.getcwd(), file_search=CONFIG_FILE_NAME):
    """
    return the path containing the configuration file to read from for loading up and running.
    """

    current_dir = os.path.abspath(search_start)
    if os.path.exists(os.path.join(current_dir, file_search)):
        return current_dir
    prev_p = current_dir
    next_p = os.path.dirname(current_dir)
    while next_p != prev_p and not os.path.exists(os.path.join(next_p, file_search)):
        prev_p = next_p
        next_p = os.path.dirname(prev_p)
    if os.path.exists(os.path.join(next_p, file_search)):
        return next_p
    else:
        return None


def load_config(config_file):
    with open(config_file, "r") as config_file:
        loaded_c = toml.loads(config_file.read())

    # todo: add some validation here.
    return loaded_c
