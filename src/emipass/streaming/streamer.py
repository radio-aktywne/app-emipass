import asyncio

from pylocks.base import Lock
from pystores.base import Store
from pystreams.stream import Stream

from emipass.config.models import Config
from emipass.streaming.errors import NoPortsAvailableError
from emipass.streaming.models import Format, Request, Response, SRTServer, STUNServer
from emipass.streaming.runner import StreamRunner


class Streamer:
    """Manages streams."""

    def __init__(self, config: Config, store: Store[set[int]], lock: Lock) -> None:
        self._config = config
        self._store = store
        self._lock = lock

    def _get_default_stun(self) -> STUNServer:
        """Gets the default STUN server to use."""

        return STUNServer(
            host=self._config.streamer.stun.host,
            port=self._config.streamer.stun.port,
        )

    async def _reserve_port(self) -> int:
        """Reserves a port for a stream."""

        async with self._lock:
            used = await self._store.get()
            available = self._config.streamer.whip.ports - used

            if not available:
                raise NoPortsAvailableError()

            port = available.pop()

            await self._store.set(used | {port})

        return port

    async def _free_port(self, port: int) -> None:
        """Marks a port as free."""

        async with self._lock:
            used = await self._store.get()
            used.remove(port)
            await self._store.set(used)

    async def _watch_stream(self, stream: Stream, port: int) -> None:
        """Watches a stream and frees the port when it ends."""

        try:
            await stream.wait()
        finally:
            await self._free_port(port)

    async def _run(
        self,
        port: int,
        stun: STUNServer,
        format: Format,
        srt: SRTServer,
    ) -> None:
        """Runs a stream."""

        runner = StreamRunner(self._config)
        stream = await runner.run(
            port=port,
            stun=stun,
            format=format,
            srt=srt,
        )

        asyncio.create_task(self._watch_stream(stream, port))

    async def stream(self, request: Request) -> Response:
        """Starts a stream."""

        port = await self._reserve_port()
        stun = request.stun or self._get_default_stun()

        try:
            await self._run(port, stun, request.format, request.srt)

            return Response(port=port, stun=stun)
        except Exception:
            await self._free_port(port)
            raise
