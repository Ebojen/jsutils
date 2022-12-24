from typing import Any, Dict, Tuple

from src.stubs.behaviors.call_count_behavior import (
    CallCountBehavior,
    CallNotImplementedError,
)
from src.stubs.behaviors.default_behavior import DefaultBehavior


class ArgBehavior:
    """Implements the behavior for a single call signature"""
    def __init__(self):
        self.calls: int = 0
        self.default: DefaultBehavior = DefaultBehavior()
        self.call_count: CallCountBehavior = CallCountBehavior()

    def on_call(self, index: int) -> 'ArgBehavior':
        return self.call_count.on_call(index)

    def returns(self, return_value: Any) -> 'ArgBehavior':
        self.default.returns(return_value)
        return self

    def raises(self, exception: Exception) -> 'ArgBehavior':
        self.default.raises(exception)
        return self

    def __call__(self) -> Any:
        self.calls += 1
        if self.calls - 1 in self.call_count._call_specs:
            return self.call_count(self.calls - 1)
        if (
            self.default._exception is not None
            or self.default._return_value is not None
        ):
            return self.default()
        raise CallNotImplementedError()


class WithArgsBehavior:
    """Implements behavior for multiple call signatures"""
    def __init__(self):
        self.call_specs = {}
        self.current_spec = None

    def convert_spec_to_string(
        self,
        args: Tuple[Any],
        kwargs: Dict[str, Any]
    ) -> str:
        """Converts a call signature to a hashable type (str)"""
        return repr((args, kwargs))

    def with_args(self, *args, **kwargs) -> ArgBehavior:
        call_repr = self.convert_spec_to_string(args, kwargs)
        if call_repr not in self.call_specs:
            self.call_specs[call_repr] = ArgBehavior()
        return self.call_specs[call_repr]

    def __call__(self, *args, **kwargs) -> Any:
        call_repr = self.convert_spec_to_string(args, kwargs)
        if call_repr in self.call_specs:
            return self.call_specs[call_repr]()
        raise CallNotImplementedError(
            'Behavior with this signature not implemented'
        )
