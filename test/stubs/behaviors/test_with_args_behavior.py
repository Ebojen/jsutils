import pytest

from jsutils.stubs.behaviors.with_args_behavior import (
    CallNotImplementedError,
    WithArgsBehavior,
)


@pytest.fixture
def behavior():
    return WithArgsBehavior()


def test_should_implement_default_return_behavior(behavior):
    behavior.with_args(42, test_key='test_value').returns(False)
    behavior.with_args('test_arg', test_exception_key=0).raises(RuntimeError())

    assert behavior(42, test_key='test_value') is False
    with pytest.raises(RuntimeError):
        behavior('test_arg', test_exception_key=0)


def test_should_implement_call_count_behavior(behavior):
    behavior.with_args(42, test_key='test_value') \
        .on_call(0).returns(True) \
        .on_call(1).returns(False) \
        .on_call(2).raises(KeyError())

    assert behavior(42, test_key='test_value') is True
    assert behavior(42, test_key='test_value') is False
    with pytest.raises(KeyError):
        behavior(42, test_key='test_value')


def test_should_use_default_behavior_if_call_count_behavior_is_not_configured(behavior):  # NOQA: E501
    behavior.with_args('test_arg').returns(0)
    behavior.with_args('test_arg') \
        .on_call(1) \
        .returns(4)

    assert behavior('test_arg') == 0
    assert behavior('test_arg') == 4
    assert behavior('test_arg') == 0


def test_should_raise_call_not_implemented_if_not_behavior_is_configured(behavior):  # NOQA: #501
    behavior.with_args('test_arg').returns(50)

    assert behavior('test_arg') == 50
    with pytest.raises(CallNotImplementedError):
        behavior(1, 2, 3)
