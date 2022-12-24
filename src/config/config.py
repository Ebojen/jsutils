"""Reads configurations, merges them on priority,
and returns configuration object
"""

import json
import os
from pathlib import Path
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

    config_path = Path(directory)
    if not config_path.exists():
        raise FileNotFoundError(
            'Specified configuration directory not present'
        )

    default_file = config_path / 'default.json'
    environment_file = config_path / f'{environment}.json'
    custom_env_var_file = config_path / 'custom_environment_variables.json'  # NOQA: E501

    if default_file.exists():
        with open(default_file, "r", encoding="UTF-8") as default_file:
            default_config = json.load(default_file)
    else:
        default_config = {}

    if environment_file.exists():
        with open(environment_file, "r", encoding="UTF-8") as env_file:
            env_config = json.load(env_file)
    else:
        raise ImportError(
            f"No configuration for {environment} environment found."
        )  # NOQA: E501

    environment_config = merge_dicts(default_config, env_config)

    if custom_env_var_file.exists():
        custom_environment_variables = get_custom_environment_vars(custom_env_var_file)  # NOQA: E501
    else:
        custom_environment_variables = {}

    total_config = merge_dicts(environment_config, custom_environment_variables)  # NOQA: E501
    config = convert(total_config, "Config")

    return config
