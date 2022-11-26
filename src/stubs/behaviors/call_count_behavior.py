from src.stubs.behaviors.default_behavior import DefaultBehavior


class CallNotImplementedError(Exception):
    pass


class CallCountBehavior:
    def __init__(self):
        self._call_specs = {}
        self._current_index = None

    def on_call(self, index):
        self._current_index = index
        if self._current_index not in self._call_specs:
            behavior = DefaultBehavior()
            self._call_specs[self._current_index] = behavior
        return self

    def on_first_call(self):
        return self.on_call(0)

    def on_second_call(self):
        return self.on_call(1)

    def on_third_call(self):
        return self.on_call(2)

    def returns(self, return_value):
        if self._current_index is not None:
            self._call_specs[self._current_index].returns(return_value)
        return self

    def raises(self, exception):
        if self._current_index is not None:
            self._call_specs[self._current_index].raises(exception)
        return self

    def __call__(self, index):
        if index in self._call_specs:
            return self._call_specs[index]()
        raise CallNotImplementedError()
