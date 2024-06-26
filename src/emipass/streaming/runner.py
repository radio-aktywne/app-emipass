from socket import gethostbyname

from pystreams.gstreamer import GStreamerNode, GStreamerStreamMetadata
from pystreams.process import ProcessBasedStreamFactory, ProcessBasedStreamMetadata
from pystreams.stream import Stream

from emipass.config.models import Config
from emipass.streaming.models import Codec, Format, SRTServer, STUNServer


class StreamRunner:
    """Utility class for building and running a stream."""

    def __init__(self, config: Config) -> None:
        self._config = config

    def _build_input_node(
        self, port: int, stun: STUNServer, codec: Codec
    ) -> GStreamerNode:
        """Builds an input node."""

        codecs = {
            Codec.OPUS: "OPUS",
        }

        return GStreamerNode(
            element="customwhipserversrc",
            properties={
                "address": f"http://{self._config.server.host}:{port}",
                "stun": f"stun://{stun.host}:{stun.port}",
                "min": self._config.server.ports.rtp.min,
                "max": self._config.server.ports.rtp.max,
                "codec": codecs[codec],
            },
        )

    def _build_watchdog_node(self) -> GStreamerNode:
        """Builds a watchdog node."""

        return GStreamerNode(
            element="watchdog",
            properties={
                "timeout": int(self._config.streamer.timeout.total_seconds() * 1000),
            },
        )

    def _build_extractor_node(self, codec: Codec) -> GStreamerNode:
        """Builds an extractor node."""

        match codec:
            case Codec.OPUS:
                return GStreamerNode(element="rtpopusdepay")

    def _build_parser_node(self, codec: Codec) -> GStreamerNode:
        """Builds a parser node."""

        match codec:
            case Codec.OPUS:
                return GStreamerNode(element="opusparse")

    def _build_muxer_node(self, format: Format) -> GStreamerNode:
        """Builds a muxer node."""

        match format:
            case Format.OGG:
                return GStreamerNode(element="oggmux")

    def _build_output_node(self, srt: SRTServer) -> GStreamerNode:
        """Builds an output node."""

        properties = {"uri": f"srt://{gethostbyname(srt.host)}:{srt.port}"}

        if srt.password is not None:
            properties["passphrase"] = srt.password

        return GStreamerNode(element="srtsink", properties=properties)

    def _build_stream_metadata(
        self,
        port: int,
        stun: STUNServer,
        codec: Codec,
        format: Format,
        srt: SRTServer,
    ) -> GStreamerStreamMetadata:
        """Builds stream metadata."""

        return GStreamerStreamMetadata(
            nodes=[
                self._build_input_node(port, stun, codec),
                self._build_watchdog_node(),
                self._build_extractor_node(codec),
                self._build_parser_node(codec),
                self._build_muxer_node(format),
                self._build_output_node(srt),
            ]
        )

    async def _run_stream(self, metadata: ProcessBasedStreamMetadata) -> Stream:
        """Run the stream with the given metadata."""

        return await ProcessBasedStreamFactory().create(metadata)

    async def run(
        self,
        port: int,
        stun: STUNServer,
        codec: Codec,
        format: Format,
        srt: SRTServer,
    ) -> Stream:
        """Run the stream."""

        metadata = self._build_stream_metadata(port, stun, codec, format, srt)
        return await self._run_stream(metadata)
