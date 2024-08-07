class ServiceError(Exception):
    """Base class for service errors."""

    pass


class NoPortsAvailableError(ServiceError):
    """Raised when no ports are available."""

    def __init__(self) -> None:
        super().__init__("No ports available.")
