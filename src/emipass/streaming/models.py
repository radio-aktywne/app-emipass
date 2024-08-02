from dataclasses import dataclass
from enum import StrEnum


class Codec(StrEnum):
    OPUS = "opus"


class Format(StrEnum):
    OGG = "ogg"


@dataclass(kw_only=True)
class SRTServer:
    """SRT server configuration."""

    host: str
    port: int
    password: str | None


@dataclass(kw_only=True)
class STUNServer:
    """STUN server configuration."""

    host: str
    port: int


@dataclass(kw_only=True)
class StreamRequest:
    """Request for a stream."""

    stun: STUNServer | None
    codec: Codec
    format: Format
    srt: SRTServer


@dataclass(kw_only=True)
class StreamResponse:
    """Response to a streaming request."""

    port: int
    stun: STUNServer
