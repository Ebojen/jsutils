"""Converts a dict and its subsets to immutable types"""

from collections import namedtuple


class TuplePlus(tuple):
    # TODO: refactor to reduce duplicate code
    def get(self, index_str: str):
        open_bracket_idx = index_str.find('[')
        close_bracket_idx = index_str.find(']')
        if open_bracket_idx == 0 and close_bracket_idx > 0:
            int_index_str = index_str[open_bracket_idx + 1: close_bracket_idx]
            index = int(int_index_str)
            if close_bracket_idx == len(index_str) - 1:
                return self[index]
            sub_tuple_plus = self[index]
            return sub_tuple_plus.get(index_str[close_bracket_idx + 1:])
        index = int(index_str)
        return self[index]

    def has(self, index_str: str) -> bool:
        open_bracket_idx = index_str.find('[')
        close_bracket_idx = index_str.find(']')
        if open_bracket_idx == 0 and close_bracket_idx > 1:
            int_index_str = index_str[open_bracket_idx + 1: close_bracket_idx]
            index = int(int_index_str)
            if close_bracket_idx == len(index_str) - 1:
                return index >= 0 and index < len(self)
            if index >= 0 and index < len(self):
                sub_tuple_plus = self[index]
                return sub_tuple_plus.has(index_str[close_bracket_idx + 1:])
            return False
        index = int(index_str)
        return index >= 0 and index < len(self)


def convert(value, name):
    """converts a value to an immutable type"""
    if isinstance(value, list):
        converted_entries = map(
            lambda x: convert(x[1], f"{name}{x[0]}"), enumerate(value)
        )
        return TuplePlus(converted_entries)
    if isinstance(value, dict):
        type_name = name.title().replace("_", "")
        attributes = " ".join(value.keys())
        new_type = namedtuple(type_name, attributes)

        def get(self, key):
            dot_index = key.find('.')
            if dot_index == 0:
                return self.get(key[1:])

            open_bracket_index = key.find('[')

            if dot_index < 0 and open_bracket_index < 0:
                return getattr(self, key)

            if dot_index > 0 and open_bracket_index < 0:
                simple_key_end = dot_index
                next_key_start = dot_index + 1

            if dot_index < 0 and open_bracket_index >= 0:
                simple_key_end = open_bracket_index
                next_key_start = open_bracket_index

            if dot_index > 0 and open_bracket_index >= 0:
                simple_key_end = min(dot_index, open_bracket_index)

            if simple_key_end == dot_index:
                next_key_start = dot_index + 1
            else:
                next_key_start = open_bracket_index

            next_obj = self.get(key[:simple_key_end])
            return next_obj.get(key[next_key_start:])

        def has(self, key):
            dot_index = key.find('.')
            if dot_index == 0:
                return self.has(key[1:])

            open_bracket_index = key.find('[')

            if dot_index < 0 and open_bracket_index < 0:
                return hasattr(self, key)

            if dot_index > 0 and open_bracket_index < 0:
                simple_key_end = dot_index
                next_key_start = dot_index + 1

            if dot_index < 0 and open_bracket_index >= 0:
                simple_key_end = open_bracket_index
                next_key_start = open_bracket_index

            if dot_index > 0 and open_bracket_index >= 0:
                simple_key_end = min(dot_index, open_bracket_index)

            if simple_key_end == dot_index:
                next_key_start = dot_index + 1
            else:
                next_key_start = open_bracket_index

            if self.has(key[:simple_key_end]):
                next_obj = self.get(key[:simple_key_end])
                return next_obj.has(key[next_key_start:])

            return False

        new_type_plus = type(
            f'{type_name}Plus',
            (new_type,),
            {
                'get': get,
                'has': has,
            }
        )

        converted_values = map(lambda x: convert(x[1], x[0]), value.items())
        return new_type_plus(*converted_values)
    return value
