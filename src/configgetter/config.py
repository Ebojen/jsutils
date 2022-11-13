"""Reads configurations, merges them on priority,
and returns configuration object
"""

import json
import os
from typing import Dict

from .converter import convert
from .merger import merge_dicts


def get_default_environment():
    if "ENV" in os.environ:
        default_environment = os.environ["ENV"]
    else:
        default_environment = "test"

    return default_environment


def convert_spec_to_values(spec: Dict):
    for key, value in spec.items():
        if isinstance(value, str):
            spec[key] = os.environ[value]
        else:
            convert_spec_to_values(value)

    return spec


def get_custom_environment_vars(path):
    with open(path, "r", encoding="UTF-8") as env_vars:
        spec = json.load(env_vars)
        convert_spec_to_values(spec)
        return spec


config = None


def get_config(directory="./config", environment=get_default_environment()):
    """Collects the default configuration and environment
    configuration from the configuration_directory and
    updates the default values with values from the
    environment configuration
    """
    global config
    if config:
        return config

    files = os.listdir(directory)

    # TODO: Use proper paths, don't be a pyschopath
    if "default.json" in files:
        path = f"{directory}/default.json"
        with open(path, "r", encoding="UTF-8") as default_file:
            default_config = json.load(default_file)

    if f"{environment}.json" in files:
        path = f"{directory}/{environment}.json"
        with open(path, "r", encoding="UTF-8") as env_file:
            env_config = json.load(env_file)
    else:
        raise ImportError(
            f"No configuration for {environment} environment found."
        )  # noqa: E501

    environment_config = merge_dicts(default_config, env_config)

    if "custom_environment_variables.json" in files:
        path = f"{directory}/custom_environment_variables.json"
        custom_environment_variables = get_custom_environment_vars(path)
    else:
        custom_environment_variables = {}

    total_config = merge_dicts(environment_config, custom_environment_variables)  # noqa: E501
    config = convert(total_config, "Config")

    return config
