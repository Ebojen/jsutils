import pytest

from jsutils.stubs.behaviors.default_behavior import DefaultBehavior


@pytest.fixture
def behavior():
    return DefaultBehavior()


def test_should_set_the_return_value(behavior):
    behavior.returns('test_value')

    assert behavior._return_value == 'test_value'


def test_should_return_the_return_value_when_called(behavior):
    behavior.returns('test_value')

    result = behavior()

    assert result == 'test_value'


def test_should_set_the_exception(behavior):
    exception = RuntimeError('KaBoom!')
    behavior.raises(exception)

    assert behavior._exception == exception


def test_should_raise_the_configured_exception(behavior):
    behavior.raises(RuntimeError('Yikes!'))

    with pytest.raises(RuntimeError, match='Yikes!'):
        behavior()


def test_should_raise_the_exception_when_both_exception_and_return_value_are_set(behavior):  # NOQA: E501
    behavior.returns('this_shouldnt_happen')
    behavior.raises(RuntimeError('This should explode'))

    with pytest.raises(RuntimeError, match='This should explode'):
        behavior()
