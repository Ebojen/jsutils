"""Converts a dict and its subsets to immutable types"""
from collections import namedtuple
from typing import Any, Tuple


class TuplePlus(tuple):
    """Extention of tuple adding get and has methods"""
    def _find_brackets(self, index_str: str) -> Tuple[int, int]:
        """Finds the brackets in an index_str"""
        open_idx = index_str.find('[')
        close_idx = index_str.find(']')
        if open_idx > -1 and close_idx < -1:
            raise IndexError('Invalid query string')
        if close_idx > -1 and open_idx != 0:
            raise IndexError('Invalid query string')
        return (open_idx, close_idx)

    def _is_bracketed(self, bracket_idxs: Tuple[int, int]) -> bool:
        """Determines if a index string was bracketed"""
        return bracket_idxs[0] == 0 and bracket_idxs[1] > 1

    def _get_index(self, index_str: str, bracket_locs: Tuple[int, int]) -> int:
        """Extracts the next index from the index str"""
        if self._is_bracketed(bracket_locs):
            return int(index_str[bracket_locs[0] + 1: bracket_locs[1]])
        return int(index_str)

    def _is_bracket_contained(self, index_str: str, close_idx: int) -> bool:
        """Determines if the index string is bounded by brackets
        Assumes the index string is bracketed"""
        return len(index_str) == close_idx + 1

    # TODO: refactor to reduce duplicate code
    def get(self, index_str: str) -> Any:
        """Fetches the value at an index derived from the index_str
        if a tuple has a given index

        the index string can be directly convertable to an int or embedded
        in brackets in a query string. The following are all valid: '1',
        '[2].some_key', '[21][-4]'.

        """
        bracket_locs = self._find_brackets(index_str)
        index = self._get_index(index_str, bracket_locs)
        if self._is_bracketed(bracket_locs):
            target_value = self[index]
            if self._is_bracket_contained(index_str, bracket_locs[1]):
                return target_value
            return target_value.get(index_str[bracket_locs[1] + 1:])
        return self[index]

    def has(self, index_str: str) -> bool:
        """Determines if the tuple has the specified index"""
        bracket_locs = self._find_brackets(index_str)
        index = self._get_index(index_str, bracket_locs)
        if self._is_bracketed(bracket_locs):
            if self._is_bracket_contained(index_str, bracket_locs[1]):
                return abs(index) < len(self)
            if abs(index) < len(self):
                return self[index] \
                    .has(index_str[bracket_locs[1] + 1:])
            return False
        return abs(index) < len(self)


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
