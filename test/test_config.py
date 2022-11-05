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
