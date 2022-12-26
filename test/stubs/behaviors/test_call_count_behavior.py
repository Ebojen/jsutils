import pytest

from jsutils.stubs.behaviors.call_count_behavior import (
    CallCountBehavior,
    CallNotImplementedError,
)
from jsutils.stubs.behaviors.default_behavior import DefaultBehavior


@pytest.fixture
def behavior():
    return CallCountBehavior()


def test_should_set_the_call_behavior_and_return_itself(behavior):
    result = behavior.on_call(0)

    assert isinstance(behavior._call_specs[0], DefaultBehavior)
    assert result == behavior


def test_should_return_the_configured_return_value_for_the_configured_call(behavior):  # NOQA: E501
    behavior.on_call(2).returns('test_value_2')

    assert behavior(2) == 'test_value_2'


def test_should_raise_the_configured_exception(behavior):
    behavior.on_call(0).returns('you dont need me')
    behavior.on_call(1).raises(RuntimeError('Oh No!'))

    assert behavior(0) == 'you dont need me'
    with pytest.raises(RuntimeError, match='Oh No!'):
        behavior(1)


def test_should_allow_method_chaining(behavior):
    behavior.on_call(0).returns('test_0') \
        .on_call(1).returns('test_1') \
        .on_call(2).raises(RuntimeError('It all went south'))

    assert behavior(0) == 'test_0'
    assert behavior(1) == 'test_1'
    with pytest.raises(RuntimeError, match='It all went south'):
        behavior(2)


def test_should_raise_call_not_implemented_error_if_the_behavior_is_not_configured(behavior):  # NOQA: E501
    behavior.on_call(0).returns('Happy Day')

    assert behavior(0)
    with pytest.raises(CallNotImplementedError):
        behavior(1)
