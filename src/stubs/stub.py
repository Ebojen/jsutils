from typing import Callable


class Stub:
    """
    TODO: From Sinon Stubs
      * .createStubInstance
      * .withArgs
      * .value
    """
    def __init__(self):
        self.call_count = 0
        self.call_history = []
        self.return_values = []
        self.fake = None
        self.error = None

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
