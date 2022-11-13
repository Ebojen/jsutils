import pytest

from src.configgetter.converter import TuplePlus, convert


class TestConvertValue:
    def test_should_return_strings_with_no_changes(self):
        test_data = "this is a string"

        result = convert(test_data, "test_data")

        assert result == test_data

    def test_should_return_ints_with_no_changes(self):
        test_data = 45

        result = convert(test_data, "test_value")

        assert result == test_data

    def test_should_return_floats_with_no_changes(self):
        test_data = 3.14

        result = convert(test_data, "test_data")

        assert result == test_data

    def test_should_return_booleans_with_no_changes(self):
        test_data = [True, False]

        for bool in test_data:
            result = convert(bool, "test_data")

            assert result == bool

    def test_should_return_None_with_no_changes(self):
        test_data = None

        result = convert(test_data, "test_data")

        assert result == test_data

    def test_should_convert_lists_of_primitives_as_tuples(self):
        num_data = [1, 2.71, 3]
        string_data = ["one", "two"]
        singleton_data = [True, False, None]

        num_result = convert(num_data, "num_data")
        string_result = convert(string_data, "string_data")
        other_result = convert(singleton_data, "singleton_data")

        assert num_result == (1, 2.71, 3)
        assert string_result == ("one", "two")
        assert other_result == (True, False, None)

    def test_should_covert_dicts_of_primitives_as_named_tuples(self):
        test_data = {
            "str_key": "one",
            "num_key": 2,
            "singleton_key": False,
        }
        string_repr = "TestDataPlus(str_key='one', num_key=2, singleton_key=False)"
        attributes = ("str_key", "num_key", "singleton_key")

        result = convert(test_data, "test_data")

        assert str(result) == string_repr
        assert result._fields == attributes
        assert result.str_key == "one"
        assert result.num_key == 2
        assert result.singleton_key is False

    def test_should_convert_arrays_of_complex_types(self):
        test_data = [
            [1, 3, {"first": "one"}],
            {"array_key": [1, True, None], "dict_key": {"col1": 1}},
        ]
        string_repr = (
            "((1, 3, TestArray02Plus(first='one')), "
            "TestArray1Plus(array_key=(1, True, None), "
            "dict_key=DictKeyPlus(col1=1)))"
        )

        result = convert(test_data, "test_array")

        assert str(result) == string_repr

    def test_should_convert_dictionaries_of_complex_types(self):
        test_data = {
            "array_key": [1, True, None],
            "dict_key": {"col1": 1},
            "str_key": "Hello PyConfig",
            "num_key": 1.62,
            "singleton_key": True,
        }
        string_repr = (
            "TestDataPlus(array_key=(1, True, None), "
            "dict_key=DictKeyPlus(col1=1), str_key='Hello PyConfig', "
            "num_key=1.62, singleton_key=True)"
        )

        result = convert(test_data, "test_data")

        assert str(result) == string_repr

    class TestGet:
        def test_should_return_the_value_at_the_key_if_final_value_in_access_string(self):  # noqa: E501
            test_data = {
                "str_key": "Hello Configurator",
                "num_key": 1.62,
                "singleton_key": True,
            }

            new_obj = convert(test_data, "test_data")

            assert new_obj.get("str_key") == "Hello Configurator"
            assert new_obj.get("num_key") == 1.62
            assert new_obj.get("singleton_key") is True

        def test_should_call_get_on_the_sub_object_for_multipart_keys(self):
            test_data = {"col1": {"col2": 2.0}}

            new_obj = convert(test_data, "test_data")

            assert new_obj.get("col1.col2") == 2.0

        def test_should_raise_exception_if_the_key_has_too_much_depth(self):
            test_data = convert({"col1": "a1"}, "test_data")

            with pytest.raises(AttributeError):
                test_data.get("col1.col2")

        def test_should_return_the_value_for_a_simple_int_convertable_index(self):  # noqa: E501
            test_data = convert(["a", "b", "c"], "test_list")

            assert test_data.get("0") == "a"
            assert test_data.get("1") == "b"
            assert test_data.get("2") == "c"

        def test_should_return_the_value_for_a_int_string_in_brackets(self):
            test_data = convert(["a", "b", "c"], "test_list")

            assert test_data.get("[0]") == "a"
            assert test_data.get("[1]") == "b"
            assert test_data.get("[2]") == "c"

        def test_should_return_the_value_for_a_chain_of_bracketed_ints(self):
            test_data = convert([["a1", "b1"], ["a2", "b2"]], "test_data")

            assert test_data.get("[0][0]") == "a1"
            assert test_data.get("[0][1]") == "b1"
            assert test_data.get("[1][0]") == "a2"
            assert test_data.get("[1][1]") == "b2"

        def test_should_return_the_value_for_a_list_index_in_a_dict(self):
            test_data = convert(
                {"col1": ["a1", "a2", "a3"]},
                "test_data",
            )

            assert test_data.get("col1[0]") == "a1"
            assert test_data.get("col1[1]") == "a2"
            assert test_data.get("col1[2]") == "a3"

        def test_should_return_the_value_for_a_dict_key_in_a_list(self):
            test_data = convert([{"col1": 1.0}], "test_data")

            assert test_data.get("[0].col1") == 1.0

        def test_should_return_the_value_for_a_long_key(self):
            test_data = convert(
                {
                    "col0": [{"idx0col0": "a", "idx0col1": "b"}],
                    "col1": {"col1col1": ["a11", "b11"]},
                },
                "test_data",
            )

            assert test_data.get("col0[0].idx0col1") == "b"

    class TestHas:
        def test_should_return_true_if_key_is_final_value_in_access_string(
            self,
        ):
            test_data = {
                "str_key": "Hello Configurator",
                "num_key": 1.62,
                "singleton_key": True,
            }

            new_obj = convert(test_data, "test_data")

            assert new_obj.has("str_key") is True
            assert new_obj.has("num_key") is True
            assert new_obj.has("singleton_key") is True

        def test_should_return_false_if_a_simple_key_is_not_present(self):
            test_data = {"col1": 1}

            new_obj = convert(test_data, "test_data")

            assert new_obj.has("col2") is False

        def test_should_call_get_on_the_sub_object_for_multipart_keys(self):
            test_data = {"col1": {"col2": 2.0}}

            new_obj = convert(test_data, "test_data")

            assert new_obj.has("col1.col2") is True

        def test_should_return_false_if_the_initial_key_is_not_present(self):
            test_data = {"col1": {"col2": 2.0}}

            new_obj = convert(test_data, "test_data")

            assert new_obj.has("col3.col2") is False

        def test_should_return_false_if_deep_key_values_are_not_present(self):
            test_data = {"col1": {"col2": 2.0}}

            new_obj = convert(test_data, "test_data")

            assert new_obj.has("col1.col3") is False

        def test_should_return_true_for_a_simple_int_convertable_index_that_is_present(  # noqa: E501
            self,
        ):
            test_data = convert(["a", "b", "c"], "test_list")

            assert test_data.has("0") is True
            assert test_data.has("1") is True
            assert test_data.has("2") is True

        def test_should_return_the_value_for_a_int_string_in_brackets(self):
            test_data = convert(["a", "b", "c"], "test_list")

            assert test_data.has("[0]") is True
            assert test_data.has("[1]") is True
            assert test_data.has("[2]") is True

        def test_should_return_the_value_for_a_chain_of_bracketed_ints(self):
            test_data = convert([["a1", "b1"], ["a2", "b2"]], "test_data")

            assert test_data.has("[0][0]") is True
            assert test_data.has("[0][1]") is True
            assert test_data.has("[1][0]") is True
            assert test_data.has("[1][1]") is True

        def test_should_return_false_if_a_simple_index_is_out_of_bounds(self):
            test_data = convert(["a", "b", "c"], "test_list")

            assert test_data.has("3") is False

        def test_should_return_false_if_the_first_index_in_a_chain_is_not_present(self):  # noqa: E501
            test_data = convert([["a1", "b1"]], "test_list")

            assert test_data.has("[3][0]") is False

        def test_should_return_true_for_a_valid_list_index_in_a_dict(self):
            test_data = convert(
                {"col1": ["a1", "a2", "a3"]},
                "test_data",
            )

            assert test_data.has("col1[0]") is True
            assert test_data.has("col1[1]") is True
            assert test_data.has("col1[2]") is True

        def test_should_return_the_value_for_a_dict_key_in_a_list(self):
            test_data = convert([{"col1": 1.0}], "test_data")

            assert test_data.has("[0].col1") is True

        def test_should_return_the_value_for_a_long_key(self):
            test_data = convert(
                {
                    "col0": [{"idx0col0": "a", "idx0col1": "b"}],
                    "col1": {"col1col1": ["a11", "b11"]},
                },
                "test_data",
            )

            assert test_data.has("col0[0].idx0col1") is True

        def test_should_return_false_if_any_intermediate_key_is_not_present(self):
            test_data = convert(
                {
                    "col0": [{"idx0col0": "a", "idx0col1": "b"}],
                    "col1": {"col1col0": ["a11", "b11"]},
                },
                "test_data",
            )

            assert test_data.has("col2[0]") is False
            assert test_data.has("col0[2]") is False
            assert test_data.has("col0[0]idx0col2") is False
            assert test_data.has("col1.col1col0[2]") is False
