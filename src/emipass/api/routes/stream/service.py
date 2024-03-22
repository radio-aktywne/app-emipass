from emipass.api.routes.stream import errors as e
from emipass.api.routes.stream.models import StreamRequest, StreamResponse
from emipass.streaming import errors as re
from emipass.streaming.streamer import Streamer


class Service:
    """Service for the stream endpoint."""

    def __init__(self, streamer: Streamer) -> None:
        self._streamer = streamer

    async def stream(self, request: StreamRequest) -> StreamResponse:
        """Starts a stream."""

        try:
            return await self._streamer.stream(request)
        except re.NoPortsAvailableError as error:
            raise e.StreamerBusyError(error.message) from error
        except re.StreamingError as error:
            raise e.ServiceError(error.message) from error
