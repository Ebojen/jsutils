class FakeBehavior:
    def __init__(self, fake=None):
        self._fake = fake

    def calls_fake(self, fake):
        self._fake = fake

    def __call__(self, *args, **kwargs):
        return self._fake(*args, **kwargs)
