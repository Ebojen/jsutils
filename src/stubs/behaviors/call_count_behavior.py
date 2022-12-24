from typing import Any

from src.stubs.behaviors.default_behavior import DefaultBehavior


class CallNotImplementedError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class CallCountBehavior:
    def __init__(self):
        self._call_specs = {}
        self._current_index = None

    def on_call(self, index: int) -> 'CallCountBehavior':
        self._current_index = index
        if self._current_index not in self._call_specs:
            behavior = DefaultBehavior()
            self._call_specs[self._current_index] = behavior
        return self

    def on_first_call(self) -> 'CallCountBehavior':
        return self.on_call(0)

    def on_second_call(self) -> 'CallCountBehavior':
        return self.on_call(1)

    def on_third_call(self) -> 'CallCountBehavior':
        return self.on_call(2)

    def returns(self, return_value: Any) -> 'CallCountBehavior':
        if self._current_index is not None:
            self._call_specs[self._current_index].returns(return_value)
        else:
            raise CallNotImplementedError('No call index initialized.')
        return self

    def raises(self, exception: Exception) -> 'CallCountBehavior':
        if self._current_index is not None:
            self._call_specs[self._current_index].raises(exception)
        return self

    def __call__(self, index: int) -> Any:
        if index in self._call_specs:
            return self._call_specs[index]()
        raise CallNotImplementedError(
            'No call behavior configured for this call.'
        )
