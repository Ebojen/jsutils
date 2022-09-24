"""Reads configurations, merges them on priority,
and returns configuration object
"""

import json
import os

from src.converter import ValueConverter
from src.merger import merge_dicts

if 'ENV' in os.environ:
    default_environment = os.environ['ENV']
else:
    default_environment = 'test'


def get_config(configuration_directory='./config',
               environment=default_environment):
    """Collects the default configuration and environment
    configuration from the configuration_directory and
    updates the default values with values from the
    environment configuration
    """
    files = os.listdir(configuration_directory)

    if 'default.json' in files:
        path = f'{configuration_directory}/default.json'
        with open(path, 'r', encoding='UTF-8') as default_file:
            default_config = json.load(default_file.read())

    if f'{environment}.json' in files:
        path = f'{configuration_directory}/{environment}.json'
        with open(path, 'r', encoding='UTF-8') as env_file:
            env_config = json.load(env_file.read())
    else:
        raise ImportError(
            f'No configuration for {environment} environment found.'
        )

    total_config = merge_dicts(default_config, env_config)
    value_converter = ValueConverter()
    return value_converter.convert(total_config)
