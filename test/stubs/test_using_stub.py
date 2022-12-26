from unittest.mock import ANY
from jsutils.stubs.stub import get_stub


class User:
    def __init__(self, name):
        self.name = name
        self.account_id = None

    def _read_from_external_source(self):
        return 1234567890

    def get_account_id(self):
        self.account_id = self._read_from_external_source()
        return f'{self.name} has account id {self.account_id}'


def test_should_replace_the_prescribed_method_using_get_stub():
    user = User('Emily Noether')
    assert user.get_account_id() == 'Emily Noether has account id 1234567890'

    stub = get_stub(user, '_read_from_external_source')
    stub.returns(2345678901)

    assert user.get_account_id() == 'Emily Noether has account id 2345678901'
    assert stub.call_count == 1

    stub.restore()
    assert user.get_account_id() == 'Emily Noether has account id 1234567890'


def test_should_be_compatible_with_monkeypatch(monkeypatch):
    stub = get_stub()
    stub.on_call(0).returns(2345678901)
    stub.on_call(1).returns(3456789012)
    monkeypatch.setattr(User, '_read_from_external_source', stub)

    user = User('Marie Curie')
    assert user.get_account_id() == 'Marie Curie has account id 2345678901'
    assert user.get_account_id() == 'Marie Curie has account id 3456789012'
    assert stub.call_count == 2


def test_should_be_compatible_with_ANY():
    stub = get_stub()
    stub.returns('Hello there')

    stub('first_call')
    stub('second_call', kwarg1='second_call_kwarg')

    assert stub.called_with('first_call')
    assert stub.called_with(ANY, kwarg1='second_call_kwarg')
    assert stub.called_with('second_call', kwarg1=ANY)
