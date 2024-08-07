from pydantic import Field

from emipass.models.base import SerializableModel, datamodel, serializable
from emipass.services.streaming import models as sm


@serializable
@datamodel
class SRTServer(sm.SRTServer):
    password: str | None = None

    def map(self) -> sm.SRTServer:
        return sm.SRTServer(**vars(self))


@serializable
@datamodel
class STUNServer(sm.STUNServer):
    @staticmethod
    def rmap(stun: sm.STUNServer) -> "STUNServer":
        return STUNServer(**vars(stun))

    def map(self) -> sm.STUNServer:
        return sm.STUNServer(**vars(self))


class StreamRequestData(SerializableModel):
    """Data for a stream request."""

    codec: sm.Codec = sm.Codec.OPUS
    """Audio codec."""

    format: sm.Format = sm.Format.OGG
    """Audio format."""

    srt: SRTServer
    """SRT server configuration."""

    stun: STUNServer | None = None
    """STUN server configuration."""


class StreamResponseData(SerializableModel):
    """Data for a stream response."""

    stun: STUNServer
    """STUN server configuration."""

    port: int = Field(..., ge=1, le=65535)
    """Port to stream to."""


@datamodel
class StreamRequest:
    """Request to stream."""

    data: StreamRequestData
    """Data for the request."""


@datamodel
class StreamResponse:
    """Response for stream."""

    data: StreamResponseData
    """Data for the response."""
