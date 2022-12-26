import json
import os
from typing import Any, Dict


def convert_spec_to_values(spec: Dict[str, str]) -> Dict[str, Any]:
    """Converts a mapping of configuration to environment variables
    into a dict of configurationas and corresponding values
    """
    def convert_value(value):
        if isinstance(value, str):
            return os.environ[value]
        return convert_spec_to_values(value)

    return {
        key: convert_value(value)
        for key, value in spec.items()
    }


def get_custom_environment_vars(path):
    """reads in the enviorment mapping and then the related values"""
    with open(path, "r", encoding="UTF-8") as env_vars:
        spec = json.load(env_vars)
        return convert_spec_to_values(spec)
