from enum import StrEnum

from emipass.models.base import datamodel


class Codec(StrEnum):
    """Audio codec."""

    OPUS = "opus"


class Format(StrEnum):
    """Audio format."""

    OGG = "ogg"


@datamodel
class SRTServer:
    """SRT server configuration."""

    host: str
    """Host of the SRT server."""

    port: int
    """Port of the SRT server."""

    password: str | None
    """Password to authenticate with the SRT server."""


@datamodel
class STUNServer:
    """STUN server configuration."""

    host: str
    """Host of the STUN server."""

    port: int
    """Port of the STUN server."""


@datamodel
class StreamRequest:
    """Request to stream."""

    codec: Codec
    """Audio codec."""

    format: Format
    """Audio format."""

    srt: SRTServer
    """SRT server configuration."""

    stun: STUNServer | None
    """STUN server configuration."""


@datamodel
class StreamResponse:
    """Response for stream."""

    stun: STUNServer
    """STUN server configuration."""

    port: int
    """Port to stream to."""
