class ProviderException(Exception):
    """Base exception class."""

    base_message = None

    @property
    def name(self):
        return self.__class__.__name__

    @property
    def message(self):
        _messages = [self]
        if self.base_message:
            _messages.insert(0, self.base_message)
        return f"[Provider] Exception:{' | '.join(_messages)}"

    def __repr__(self):
        return self.message
