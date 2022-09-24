
from src.converter import ValueConverter

import pytest

class TestConvertValue:
    @pytest.fixture
    def value_converter(self):
        return ValueConverter()

    def test_should_return_strings_with_no_changes(self, value_converter):
        test_data = 'this is a string'

        result = value_converter.convert(test_data)

        assert result == test_data

    def test_should_return_ints_with_no_changes(self, value_converter):
        test_data = 45

        result = value_converter.convert(test_data)

        assert result == test_data

    def test_should_return_floats_with_no_changes(self, value_converter):
        test_data = 3.14

        result = value_converter.convert(test_data)

        assert result == test_data

    def test_should_return_booleans_with_no_changes(self, value_converter):
        test_data = [True, False]

        for bool in test_data:
            result = value_converter.convert(bool)

            assert result == bool

    def test_should_return_None_with_no_changes(self, value_converter):
        test_data = None

        result = value_converter.convert(test_data)

        assert result == test_data

    def test_should_convert_lists_of_primitives_as_tuples(self, value_converter):
        num_data = [1, 2.71, 3]
        string_data = ['one', 'two']
        other_data = [True, False, None]

        num_result = value_converter.convert(num_data)
        string_result = value_converter.convert(string_data)
        other_result = value_converter.convert(other_data)

        assert num_result == (1, 2.71, 3)
        assert string_result == ('one', 'two')
        assert other_result == (True, False, None)

    def test_should_covert_dicts_of_primitives_as_named_tuples(self, value_converter):
        test_data = {
            'str_key': 'one',
            'num_key': 2,
            'singleton_key': False,
        }
        string_repr = "DictType0(str_key='one', num_key=2, singleton_key=False)"
        attributes = ('str_key', 'num_key', 'singleton_key')

        result = value_converter.convert(test_data)

        assert str(result) == string_repr
        assert result._fields == attributes
        assert result.str_key == 'one'
        assert result.num_key == 2
        assert result.singleton_key is False

    def test_should_convert_arrays_of_complex_types(self, value_converter):
        test_data = [
            [1, 3, {'first': 'one'}],
            {'array_key': [1, True, None], 'dict_key': {'col1': 1}}
        ]
        string_repr = "((1, 3, DictType0(first='one')), DictType1(array_key=(1, True, None), dict_key=DictType2(col1=1)))"

        result = value_converter.convert(test_data)

        assert str(result) == string_repr

    def test_should_convert_dictionaries_of_complex_types(self, value_converter):
        test_data = {
            'array_key': [1, True, None],
            'dict_key': {'col1': 1},
            'str_key': 'Hello PyConfig',
            'num_key': 1.62,
            'singleton_key': True,
        }
        string_repr = (
            "DictType0(array_key=(1, True, None), "
            "dict_key=DictType1(col1=1), str_key='Hello PyConfig', "
            "num_key=1.62, singleton_key=True)"
        )

        result = value_converter.convert(test_data)

        assert str(result) == string_repr
