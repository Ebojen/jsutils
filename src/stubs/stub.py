from types import MethodType
from typing import Callable


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
        self.return_values = []
        self.fake = None
        self.original_object = original_object
        self.method_name = method_name
        self.original_behavior = getattr(self.original_object, method_name) if method_name else None

    def returns(self, return_value: any) -> None:
        self.return_values.append(return_value)

        return self

    def on_call_count(self, index: int):
        if len(self.return_values) == 0 and index == 0:
            return self

        if index != len(self.return_values):
            raise ValueError("Prior calls not set")

        return self

    def on_first_call(self):
        return self.on_call_count(0)

    def on_second_call(self):
        return self.on_call_count(1)

    def on_third_call(self):
        return self.on_call_count(2)

    def calls_fake(self, fake: Callable):
        self.fake = fake
        return self

    def raises(self, error):
        return self.returns(error)

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

        if self.fake is not None:
            return self.fake(*args, **kwargs)

        if len(self.return_values) > 0:
            return_value = self.return_values[self.call_count - 1]
            if isinstance(return_value, Exception):
                raise return_value
            return self.return_values[self.call_count - 1]
        return None


def get_stub(obj: any = None, method: str = None) -> Stub:
    if obj is not None and method is not None:
        method_stub = Stub(original_object=obj, method_name=method)
        setattr(obj, method, method_stub)
        return method_stub

    return Stub()
