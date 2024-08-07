from litestar.datastructures import State as LitestarState

from emipass.config.models import Config
from emipass.services.streaming.service import StreamingService


class State(LitestarState):
    """Use this class as a type hint for the state of the application."""

    config: Config
    """Configuration for the application."""

    streaming: StreamingService
    """Service to manage streaming."""
