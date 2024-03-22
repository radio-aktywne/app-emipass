from litestar.datastructures import State as LitestarState

from emipass.config.models import Config
from emipass.streaming.streamer import Streamer


class State(LitestarState):
    """Use this class as a type hint for the state of your application.

    Attributes:
        config: Configuration for the application.
        streamer: Streamer for managing streams.
    """

    config: Config
    streamer: Streamer
