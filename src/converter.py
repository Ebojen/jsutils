"""Converts a dict and its subsets to immutable types"""

from collections import namedtuple


class ValueConverter:
    def __init__(self):
        self._num_types_created = 0

    def convert(self, value):
        """converts a value to an immutable type"""
        if type(value) == list:
            converted_entries = map(self.convert, value)
            return tuple(converted_entries)
        if type(value) == dict:
            type_name = f'DictType{self._num_types_created}'
            self._num_types_created += 1
            attributes = ' '.join(value.keys())
            new_type = namedtuple(type_name, attributes)
            converted_values = map(self.convert, value.values())
            return new_type(*converted_values)
        return value
