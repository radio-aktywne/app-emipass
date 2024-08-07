from collections.abc import Generator
from contextlib import contextmanager

from emipass.api.routes.stream import errors as e
from emipass.api.routes.stream import models as m
from emipass.services.streaming import errors as se
from emipass.services.streaming import models as sm
from emipass.services.streaming.service import StreamingService


class Service:
    """Service for the stream endpoint."""

    def __init__(self, streaming: StreamingService) -> None:
        self._streaming = streaming

    @contextmanager
    def _handle_errors(self) -> Generator[None]:
        try:
            yield
        except se.NoPortsAvailableError as ex:
            raise e.ServiceBusyError(str(ex)) from ex
        except se.ServiceError as ex:
            raise e.ServiceError(str(ex)) from ex

    async def stream(self, request: m.StreamRequest) -> m.StreamResponse:
        """Start a stream."""

        codec = request.data.codec
        format = request.data.format
        srt = request.data.srt
        stun = request.data.stun

        req = sm.StreamRequest(
            codec=codec,
            format=format,
            srt=srt.map(),
            stun=stun.map() if stun else None,
        )

        with self._handle_errors():
            res = await self._streaming.stream(req)

        stun = res.stun
        port = res.port

        stun = m.STUNServer.rmap(stun)
        data = m.StreamResponseData(
            stun=stun,
            port=port,
        )
        return m.StreamResponse(
            data=data,
        )
