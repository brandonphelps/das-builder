import docker
import os
from jinja2 import Environment, FileSystemLoader


def extract_args(config_file):
    """
    Read from the config file and pull out the intresting arguments to pass to the execu line
    """
