from typing import Any, Callable


class FakeBehavior:
    """Implements behavior using an overriding callable"""
    def __init__(self, fake: Callable = None):
        self._fake = fake

    def calls_fake(self, fake: Callable):
        """Sets the _fake attribute"""
        self._fake = fake

    def __call__(self, *args, **kwargs) -> Any:
        """Executes the fake with the provided args"""
        return self._fake(*args, **kwargs)
