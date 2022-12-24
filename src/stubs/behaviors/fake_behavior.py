from typing import Any, Callable


class FakeBehavior:
    """Implements behavior using an overriding callable"""
    def __init__(self, fake: Callable = None):
        self._fake = fake

    def calls_fake(self, fake: Callable):
        self._fake = fake

    def __call__(self, *args, **kwargs) -> Any:
        return self._fake(*args, **kwargs)
