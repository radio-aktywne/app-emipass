from collections.abc import Generator
from contextlib import contextmanager

from emipass.api.routes.stream import errors as e
from emipass.api.routes.stream import models as m
from emipass.streaming import errors as se
from emipass.streaming import models as sm
from emipass.streaming.streamer import Streamer


class Service:
    """Service for the stream endpoint."""

    def __init__(self, streamer: Streamer) -> None:
        self._streamer = streamer

    @contextmanager
    def _handle_errors(self) -> Generator[None]:
        try:
            yield
        except se.NoPortsAvailableError as ex:
            raise e.StreamerBusyError(ex.message) from ex
        except se.StreamingError as ex:
            raise e.ServiceError(ex.message) from ex

    async def stream(self, request: m.StreamRequest) -> m.StreamResponse:
        """Starts a stream."""

        stun = request.data.stun
        codec = request.data.codec
        format = request.data.format
        srt = request.data.srt

        stun = (
            sm.STUNServer(
                host=stun.host,
                port=stun.port,
            )
            if stun
            else None
        )
        srt = sm.SRTServer(
            host=srt.host,
            port=srt.port,
            password=srt.password,
        )

        with self._handle_errors():
            response = await self._streamer.stream(
                sm.StreamRequest(
                    stun=stun,
                    codec=codec,
                    format=format,
                    srt=srt,
                )
            )

        port = response.port
        stun = response.stun

        stun = m.STUNServer(
            host=stun.host,
            port=stun.port,
        )
        data = m.StreamResponseData(
            port=port,
            stun=stun,
        )
        return m.StreamResponse(
            data=data,
        )
