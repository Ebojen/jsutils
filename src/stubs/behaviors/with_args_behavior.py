from src.stubs.behaviors.call_count_behavior import (
    CallCountBehavior,
    CallNotImplementedError,
)
from src.stubs.behaviors.default_behavior import DefaultBehavior


class ArgBehavior:
    def __init__(self):
        self.calls = 0
        self.default = DefaultBehavior()
        self.call_count = CallCountBehavior()

    def on_call(self, index):
        return self.call_count.on_call(index)

    def returns(self, return_value):
        self.default.returns(return_value)
        return self

    def raises(self, exception):
        self.default.raises(exception)
        return self

    def __call__(self):
        self.calls += 1
        if self.calls - 1 in self.call_count._call_specs:
            return self.call_count(self.calls - 1)
        if self.default._exception is not None or self.default._return_value is not None:
            return self.default()
        raise CallNotImplementedError()


class WithArgsBehavior:
    def __init__(self):
        self.call_specs = {}
        self.current_spec = None

    def convert_spec_to_string(self, args, kwargs):
        return repr((args, kwargs))

    def with_args(self, *args, **kwargs):
        call_repr = self.convert_spec_to_string(args, kwargs)
        if call_repr not in self.call_specs:
            behavior = ArgBehavior()
            self.call_specs[call_repr] = behavior
        return self.call_specs[call_repr]

    def __call__(self, *args, **kwargs):
        call_repr = self.convert_spec_to_string(args, kwargs)
        if call_repr in self.call_specs:
            return self.call_specs[call_repr]()
        raise CallNotImplementedError()
