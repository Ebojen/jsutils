from typing import Any


class DefaultBehavior:
    """Creates a default return and exception behavior"""
    def __init__(
        self,
        return_value: Any = None,
        exception: Exception = None
    ):
        self._return_value = return_value
        self._exception = exception

    def returns(self, return_value: Any) -> None:
        self._return_value = return_value

    def raises(self, exception: Exception) -> None:
        self._exception = exception

    def __call__(self, *args, **kwargs) -> Any:
        if self._exception is not None:
            raise self._exception
        return self._return_value
