from socket import gethostbyname

from pystreams.gstreamer import GStreamerNode, GStreamerStreamMetadata
from pystreams.process import ProcessBasedStreamFactory, ProcessBasedStreamMetadata
from pystreams.stream import Stream

from emipass.config.models import Config
from emipass.services.streaming import models as m


class Runner:
    """Utility class for building and running a stream."""

    def __init__(self, config: Config) -> None:
        self._config = config

    def _build_input_node(
        self, port: int, codec: m.Codec, stun: m.STUNServer
    ) -> GStreamerNode:
        codecs = {
            m.Codec.OPUS: "OPUS",
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
        return GStreamerNode(
            element="watchdog",
            properties={
                "timeout": int(self._config.streamer.timeout.total_seconds() * 1000),
            },
        )

    def _build_extractor_node(self, codec: m.Codec) -> GStreamerNode:
        match codec:
            case m.Codec.OPUS:
                return GStreamerNode(
                    element="rtpopusdepay",
                )

    def _build_parser_node(self, codec: m.Codec) -> GStreamerNode:
        match codec:
            case m.Codec.OPUS:
                return GStreamerNode(
                    element="opusparse",
                )

    def _build_muxer_node(self, format: m.Format) -> GStreamerNode:
        match format:
            case m.Format.OGG:
                return GStreamerNode(
                    element="oggmux",
                )

    def _build_output_node(self, srt: m.SRTServer) -> GStreamerNode:
        properties = {"uri": f"srt://{gethostbyname(srt.host)}:{srt.port}"}

        if srt.password is not None:
            properties["passphrase"] = srt.password

        return GStreamerNode(
            element="srtsink",
            properties=properties,
        )

    def _build_stream_metadata(
        self,
        port: int,
        codec: m.Codec,
        format: m.Format,
        srt: m.SRTServer,
        stun: m.STUNServer,
    ) -> GStreamerStreamMetadata:
        return GStreamerStreamMetadata(
            nodes=[
                self._build_input_node(port, codec, stun),
                self._build_watchdog_node(),
                self._build_extractor_node(codec),
                self._build_parser_node(codec),
                self._build_muxer_node(format),
                self._build_output_node(srt),
            ],
        )

    async def _run_stream(self, metadata: ProcessBasedStreamMetadata) -> Stream:
        return await ProcessBasedStreamFactory().create(metadata)

    async def run(
        self,
        port: int,
        codec: m.Codec,
        format: m.Format,
        srt: m.SRTServer,
        stun: m.STUNServer,
    ) -> Stream:
        """Run the stream."""

        metadata = self._build_stream_metadata(port, codec, format, srt, stun)
        return await self._run_stream(metadata)
