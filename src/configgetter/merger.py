"""Merges multiple dicts, replacing the keys of
the previous values"""


def merge_dicts(base: dict, updater: dict) -> dict:
    """Deep merges two dictionaries recursively, updating values
    from the first, updating with values from the second.
    """
    merged_dict = base.copy()
    for key, value in updater.items():
        if isinstance(value, dict):
            old_value = merged_dict.setdefault(key, {})
            new_value = merge_dicts(old_value, value)
            merged_dict[key] = new_value
        else:
            merged_dict[key] = value

    return merged_dict
