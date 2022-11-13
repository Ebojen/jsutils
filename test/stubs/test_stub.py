import pytest

from src.stubs.stub import Stub

class TestStub:
    def test_should_track_the_number_of_calls_to_the_stubs(self):
        stub = Stub()
        assert stub.call_count == 0

        stub()
        assert stub.call_count == 1

        stub()
        assert stub.call_count == 2

        stub()
        assert stub.call_count == 3

    def test_should_track_the_call_history(self):
        stub = Stub()
        expected1 = (
            ('arg1', 'arg2'),
            {'kwarg_key1': 'kwarg1', 'kwarg_key2': 'kwarg2'}
        )
        stub('arg1', 'arg2', kwarg_key1='kwarg1', kwarg_key2='kwarg2')

        assert stub.call_history == [expected1]

        expected2 = (
            ('arg3',),
            {'kwarg_key3': 'kwarg3', 'kwarg_key4': 'kwarg4', 'kwarg_key5': 'kwarg5'}
        )
        stub('arg3', kwarg_key3='kwarg3', kwarg_key4='kwarg4', kwarg_key5='kwarg5')

        assert stub.call_history == [expected1, expected2]

    def test_should_return_the_provided_return_value(self):
        stub = Stub()
        stub.returns('test_value')

        result = stub()

        assert result == 'test_value'

    def test_should_return_the_configured_return_values(self):
        stub = Stub()
        stub.on_call_count(0).returns('test_value_1') \
            .on_call_count(1).returns(8675309)

        result_1 = stub()
        result_2 = stub()

        assert result_1 == 'test_value_1'
        assert result_2 == 8675309

    def test_should_configure_the_first_call(self):
        stub = Stub()
        stub.on_first_call().returns('first_call')

        result = stub()

        assert result == 'first_call'

    def test_should_configure_the_second_call(self):
        stub = Stub()
        stub.on_first_call().returns('first_call') \
            .on_second_call().returns('second_call')

        result_1 = stub()
        result_2 = stub()

        assert result_1 == 'first_call'
        assert result_2 == 'second_call'

    def test_should_configure_the_third_call(self):
        stub = Stub()
        stub.on_first_call().returns('first_call') \
            .on_second_call().returns('second_call') \
            .on_third_call().raises(ValueError('Its too much'))

        result_1 = stub()
        result_2 = stub()

        assert result_1 == 'first_call'
        assert result_2 == 'second_call'

        with pytest.raises(ValueError, match='Its too much'):
            stub()

    def test_should_call_the_provided_fake(self):
        def add_two(num):
            return num + 2
        stub = Stub()
        stub.calls_fake(add_two)

        result_1 = stub(50)
        result_2 = stub(-7001)

        assert result_1 == 52
        assert result_2 == -6999

        def concat_str(first_str=None, last_str=None):
            return f'{first_str}{last_str}'
        stub2 = Stub()
        stub2.calls_fake(concat_str)
        result_3 = stub2(first_str='StringOne', last_str='StringTwo')

        assert result_3 == 'StringOneStringTwo'

    def test_should_throw_the_provided_error(self):
        stub = Stub()
        stub.raises(RuntimeError('Boom!'))

        with pytest.raises(RuntimeError, match='Boom!'):
            stub()
