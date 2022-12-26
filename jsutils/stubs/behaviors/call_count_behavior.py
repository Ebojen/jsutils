from typing import Any

from .default_behavior import DefaultBehavior


class CallNotImplementedError(Exception):
    """Exception for when a call is not implemented"""
    def __init__(self, message: str) -> None:
        super().__init__(message)


class CallCountBehavior:
    """Behavior based on 0 based call count"""
    def __init__(self):
        self._call_specs = {}
        self._current_index = None

    def on_call(self, index: int) -> 'CallCountBehavior':
        """sets _current_index and initializes the call_spec if necessary"""
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
        """Sets the return behavior for the _current_index spec
        Raises a CallNotImplementedError if _current_index is None"""
        if self._current_index is not None:
            self._call_specs[self._current_index].returns(return_value)
            self._current_index = None
        else:
            raise CallNotImplementedError('No call index initialized.')
        return self

    def raises(self, exception: Exception) -> 'CallCountBehavior':
        """Sets the exception behavior for the _current_index spec
        Raises a CallNotImplementedError if _current_index is None
        """
        if self._current_index is not None:
            self._call_specs[self._current_index].raises(exception)
            self._current_index = None
        else:
            raise CallNotImplementedError('No call index initialized.')
        return self

    def __call__(self, index: int) -> Any:
        """executes the behavior, raising a CallNotImplementedError if the
        behavior is not in the spec
        """
        if index in self._call_specs:
            return self._call_specs[index]()
        raise CallNotImplementedError(
            'No call behavior configured for this call.'
        )
