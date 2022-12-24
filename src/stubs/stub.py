from typing import Any, Callable, Dict

from src.stubs.behaviors.call_count_behavior import CallCountBehavior
from src.stubs.behaviors.default_behavior import DefaultBehavior
from src.stubs.behaviors.fake_behavior import FakeBehavior
from src.stubs.behaviors.with_args_behavior import (
    ArgBehavior,
    WithArgsBehavior
)


class Stub:
    def __init__(
        self,
        original_object: Any = None,
        method_name: str = None,
        attrs: Dict[Any, Any] = {}
    ):
        self.call_count = 0
        self.call_count_behavior = CallCountBehavior()
        self.call_history = []
        self.default_behavior = DefaultBehavior()
        self.fake_behavior = FakeBehavior()
        self.method_name = method_name
        self.original_object = original_object
        self.with_args_behavior = WithArgsBehavior()
        self.current_index = None

        if method_name and hasattr(self.original_object, method_name):
            self.original_behavior = getattr(self.original_object, method_name)
        else:
            self.original_behavior = None

        for key, value in attrs.items():
            setattr(self, key, value)

    def returns(self, return_value: Any) -> 'Stub':
        self.default_behavior.returns(return_value)
        return self

    def raises(self, exception: Exception) -> 'Stub':
        self.default_behavior.raises(exception)
        return self

    def with_args(self, *args, **kwargs) -> ArgBehavior:
        return self.with_args_behavior.with_args(*args, **kwargs)

    def on_call(self, index: int) -> CallCountBehavior:
        return self.call_count_behavior.on_call(index)

    def on_first_call(self) -> CallCountBehavior:
        return self.call_count_behavior.on_first_call()

    def on_second_call(self) -> CallCountBehavior:
        return self.call_count_behavior.on_second_call()

    def on_third_call(self) -> CallCountBehavior:
        return self.call_count_behavior.on_third_call()

    def calls_fake(self, fake: Callable) -> FakeBehavior:
        self.fake_behavior.calls_fake(fake)
        return self

    def called_with(self, *args, **kwargs) -> bool:
        return (args, kwargs) in self.call_history

    def restore(self) -> None:
        if self.original_object and self.original_behavior:
            setattr(
                self.original_object,
                self.method_name,
                self.original_behavior,
            )
        self.call_count = 0
        self.call_history = []
        self.fake = None

    def __call__(self, *args, **kwargs) -> Any:
        self.call_count += 1
        self.call_history.append((args, kwargs))

        if self.fake_behavior._fake is not None:
            return self.fake_behavior(*args, **kwargs)

        args_repr = self.with_args_behavior \
            .convert_spec_to_string(args, kwargs)
        if args_repr in self.with_args_behavior.call_specs:
            return self.with_args_behavior(*args, **kwargs)

        if self.call_count - 1 in self.call_count_behavior._call_specs:
            return self.call_count_behavior(self.call_count - 1)

        return self.default_behavior()


def get_stub(
    obj: Any = None,
    method: str = None,
    attrs: Dict[Any, Any] = {}
) -> Stub:
    if obj is not None and method is not None:
        method_stub = Stub(
            original_object=obj,
            method_name=method,
        )
        setattr(obj, method, method_stub)
        return method_stub

    return Stub(attrs=attrs)
