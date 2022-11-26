class DefaultBehavior:
    """Creates a default return and exception behavior"""
    def __init__(self, return_value=None, exception=None):
        self._return_value = return_value
        self._exception = exception

    def returns(self, return_value):
        self._return_value = return_value

    def raises(self, exception):
        self._exception = exception

    def __call__(self, *args, **kwargs):
        if self._exception is not None:
            raise self._exception
        return self._return_value
