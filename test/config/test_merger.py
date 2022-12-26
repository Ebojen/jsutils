from jsutils.config.merger import merge_dicts


class TestMerger:
    def test_should_create_a_dict_with_all_keys_from_both_inputs(self):
        base = {"col1": 1, "col2": 2}
        updater = {"col3": 3, "col4": 4}
        expected = {"col1": 1, "col2": 2, "col3": 3, "col4": 4}

        result = merge_dicts(base, updater)

        assert result == expected

    def test_should_override_base_values_on_key_collision(self):
        base = {"col1": 1, "col2": 2}
        updater = {"col2": "two", "col3": 3}
        expected = {"col1": 1, "col2": "two", "col3": 3}

        result = merge_dicts(base, updater)

        assert result == expected

    def test_should_override_deep_base_values_on_key_collision(self):
        base = {"col1": {"col2": 2, "col3": 3}}
        updater = {"col1": {"col2": "two", "col4": 4}}
        expected = {"col1": {"col2": "two", "col3": 3, "col4": 4}}

        result = merge_dicts(base, updater)

        assert result == expected
