import pytest

from src.stubs.behaviors.fake_behavior import FakeBehavior


@pytest.fixture
def behavior():
    return FakeBehavior()


def test_should_set_the_fake_attribute(behavior):
    def awesomenater(input: str) -> str:
        return f'{input} is awesome!'

    behavior.calls_fake(awesomenater)

    assert behavior._fake == awesomenater


def test_should_call_the_configured_fake(behavior):
    def awesomenater(input: str) -> str:
        return f'{input} is awesome!'

    behavior.calls_fake(awesomenater)

    assert behavior('You') == 'You is awesome!'
