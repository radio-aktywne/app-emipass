class ServiceError(Exception):
    """Base class for service errors."""

    pass


class ServiceBusyError(ServiceError):
    """Raised when the service is busy."""

    pass
