import asyncio

from pylocks.base import Lock
from pystores.base import Store
from pystreams.stream import Stream

from emipass.config.models import Config
from emipass.services.streaming import errors as e
from emipass.services.streaming import models as m
from emipass.services.streaming.runner import Runner


class StreamingService:
    """Service to manage streaming."""

    def __init__(self, config: Config, store: Store[set[int]], lock: Lock) -> None:
        self._config = config
        self._store = store
        self._lock = lock

    def _get_default_stun(self) -> m.STUNServer:
        return m.STUNServer(
            host=self._config.streamer.stun.host,
            port=self._config.streamer.stun.port,
        )

    async def _reserve_port(self) -> int:
        async with self._lock:
            used = await self._store.get()
            available = self._config.server.ports.whip - used

            if not available:
                raise e.NoPortsAvailableError()

            port = available.pop()

            await self._store.set(used | {port})

        return port

    async def _free_port(self, port: int) -> None:
        async with self._lock:
            used = await self._store.get()
            used.remove(port)
            await self._store.set(used)

    async def _watch_stream(self, stream: Stream, port: int) -> None:
        try:
            await stream.wait()
        finally:
            await self._free_port(port)

    async def _run(
        self,
        port: int,
        codec: m.Codec,
        format: m.Format,
        srt: m.SRTServer,
        stun: m.STUNServer,
    ) -> None:
        runner = Runner(self._config)
        stream = await runner.run(
            port=port,
            codec=codec,
            format=format,
            srt=srt,
            stun=stun,
        )

        asyncio.create_task(self._watch_stream(stream, port))

    async def stream(self, request: m.StreamRequest) -> m.StreamResponse:
        """Start a stream."""

        codec = request.codec
        format = request.format
        srt = request.srt
        stun = request.stun

        port = await self._reserve_port()
        stun = stun or self._get_default_stun()

        try:
            await self._run(port, codec, format, srt, stun)
        except Exception:
            await self._free_port(port)
            raise

        return m.StreamResponse(
            port=port,
            stun=stun,
        )
