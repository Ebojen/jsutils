import json
import importlib

import pytest

from src.configgetter import config


class TestGetConfig:
    def test_should_look_in_the_config_directory_by_default(self):
        with pytest.raises(FileNotFoundError):
            config.get_config()

    def test_should_default_to_test_environment_if_not_set_or_provided(self, tmp_path):
        d = tmp_path / "config"
        d.mkdir()
        default = d / "default.json"
        default.write_text(json.dumps({"default_key": "default_value"}))
        test = d / "test.json"
        test.write_text(json.dumps({"test_key": "test_value"}))

        result = config.get_config(directory=d)

        assert result.default_key == "default_value"
        assert result.test_key == "test_value"

    def test_should_use_the_ENV_value_for_default_if_available(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setenv("ENV", "test_env")
        importlib.reload(config)
        d = tmp_path / "config"
        d.mkdir()
        default = d / "default.json"
        default.write_text(json.dumps({"default_key": "default_value"}))
        test = d / "test.json"
        test.write_text(json.dumps({"test_key": "test_value"}))
        test_env = d / "test_env.json"
        test_env.write_text(json.dumps({"test_env_key": "test_env_value"}))

        result = config.get_config(directory=d)

        assert result.default_key == "default_value"
        assert result.test_env_key == "test_env_value"
        assert "test_key" not in result._fields

    def test_should_read_in_then_custom_env_vars(self, tmp_path, monkeypatch):
        monkeypatch.setenv("TOP_LEVEL_VALUE", "top_level_value")
        monkeypatch.setenv("NESTED_OVERWRITTEN_VALUE", "nested_overwritten_value")  # noqa: E501
        monkeypatch.setenv("NESTED_CREATED_VALUE", "nested_created_value")
        importlib.reload(config)
        d = tmp_path / "config"
        d.mkdir()
        default = d / "default.json"
        default.write_text(json.dumps({"default_key": "default_value"}))
        test = d / "test.json"
        test.write_text(json.dumps({
            "test_key": "test_value",
            "nested_top": {
                "nested_not_overwritten_key": "nested_not_overwritten",
                "nested_overwritten_key": "value_to_be_overwritten",
            }
        }))
        custom_env_vars = d / "custom_environment_variables.json"
        custom_env_vars.write_text(json.dumps({
            "top_level_key": "TOP_LEVEL_VALUE",
            "nested_top": {
                "nested_overwritten_key": "NESTED_OVERWRITTEN_VALUE",
                "nested_created_key": "NESTED_CREATED_VALUE"
            }
        }))

        result = config.get_config(directory=d)

        assert result.get('default_key') == 'default_value'
        assert result.get('test_key') == 'test_value'
        assert result.get('top_level_key') == 'top_level_value'
        assert result.get('nested_top.nested_not_overwritten_key') == 'nested_not_overwritten'  # noqa: E501
        assert result.get('nested_top.nested_overwritten_key') == 'nested_overwritten_value'  # noqa: E501
        assert result.get('nested_top.nested_created_key') == 'nested_created_value'  # noqa: E501


    def test_should_raise_an_exception_if_there_is_not_a_config_for_the_env(
        self, tmp_path, monkeypatch
    ):
        monkeypatch.setenv("ENV", "test_env")
        importlib.reload(config)
        d = tmp_path / "config"
        d.mkdir()
        default = d / "default.json"
        default.write_text(json.dumps({"default_key": "default_value"}))
        test = d / "test.json"
        test.write_text(json.dumps({"test_key": "test_value"}))

        with pytest.raises(
            ImportError, match="No configuration for test_env environment found."
        ):
            config.get_config(directory=d)

    def test_should_only_create_the_config_object_once(self, tmp_path):
        importlib.reload(config)
        d = tmp_path / "config"
        d.mkdir()
        default = d / "default.json"
        default.write_text(json.dumps({"default_key": "default_value"}))
        test = d / "test.json"
        test.write_text(json.dumps({"test_key": "test_value"}))

        first_config = config.get_config(directory=d)
        second_config = config.get_config(directory=d)

        assert first_config is second_config
