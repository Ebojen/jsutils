from __future__ import annotations
from typing import (
    Callable,
    Dict,
    Union,
)

from src.stubs.behaviors.call_count_behavior import (
    CallCountBehavior,
    CallNotImplementedError,
)
from src.stubs.behaviors.default_behavior import DefaultBehavior
from src.stubs.behaviors.fake_behavior import FakeBehavior
from src.stubs.behaviors.with_args_behavior import WithArgsBehavior


"""
TODO: From Sinon Stubs
    * provided an object and method name, only stub the method and return the stub
    * .createStubInstance
    * .withArgs
    * .value
"""


class Stub:
    def __init__(self, original_object=None, method_name=None):
        self.call_count = 0
        self.call_history = []
        self.default_behavior = DefaultBehavior()
        self.call_count_behavior = CallCountBehavior()
        self.fake_behavior = FakeBehavior()
        self.with_args_behavior = WithArgsBehavior()
        self.original_object = original_object
        self.method_name = method_name
        self.original_behavior = getattr(self.original_object, method_name) \
            if method_name else None

    def returns(self, return_value: any) -> Stub:
        self.default_behavior.returns(return_value)
        return self

    def raises(self, exception: Exception) -> Stub:
        self.default_behavior.raises(exception)
        return self

    def with_args(self, *args, **kwargs):
        return self.with_args_behavior.with_args(*args, **kwargs)

    def on_call(self, index: int):
        return self.call_count_behavior.on_call(index)

    def on_first_call(self):
        return self.call_count_behavior.on_first_call()

    def on_second_call(self):
        return self.call_count_behavior.on_second_call()

    def on_third_call(self):
        return self.call_count_behavior.on_third_call()

    def calls_fake(self, fake: Callable):
        self.fake_behavior.calls_fake(fake)
        return self

    def restore(self):
        if self.original_object and self.original_behavior:
            setattr(
                self.original_object,
                self.method_name,
                self.original_behavior,
            )
        self.call_count = 0
        self.call_history = []
        self.fake = None

    def __call__(self, *args, **kwargs) -> any:
        self.call_count += 1
        self.call_history.append((args, kwargs))
        if self.fake_behavior._fake is not None:
            return self.fake_behavior(*args, **kwargs)
        args_repr = self.with_args_behavior.convert_spec_to_string(args, kwargs)
        if args_repr in self.with_args_behavior.call_specs:
            return self.with_args_behavior(*args, **kwargs)
        if self.call_count - 1 in self.call_count_behavior._call_specs:
            return self.call_count_behavior(self.call_count - 1)
        else:
            return self.default_behavior()


def get_stub(obj: any = None, method: str = None) -> Stub:
    if obj is not None and method is not None:
        method_stub = Stub(original_object=obj, method_name=method)
        setattr(obj, method, method_stub)
        return method_stub

    return Stub()
