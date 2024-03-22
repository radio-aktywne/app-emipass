class StreamingError(Exception):
    """Base class for all exceptions related to streaming."""

    def __init__(self, message: str | None = None) -> None:
        self._message = message

        args = (message,) if message else ()
        super().__init__(*args)

    @property
    def message(self) -> str | None:
        return self._message


class NoPortsAvailableError(StreamingError):
    """Raised when no ports are available."""

    def __init__(self) -> None:
        super().__init__("No ports available.")
