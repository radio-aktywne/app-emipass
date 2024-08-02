from dataclasses import dataclass

from pydantic import Field

from emipass.models.base import SerializableModel
from emipass.streaming import models as sm


class SRTServer(SerializableModel):
    """SRT server configuration."""

    host: str = Field(
        ...,
        title="SRTServer.Host",
        description="Host of the SRT server.",
    )
    port: int = Field(
        ...,
        ge=1,
        le=65535,
        title="SRTServer.Port",
        description="Port of the SRT server.",
    )
    password: str | None = Field(
        None,
        title="SRTServer.Password",
        description="Password of the SRT server.",
    )


class STUNServer(SerializableModel):
    """STUN server configuration."""

    host: str = Field(
        ...,
        title="STUNServer.Host",
        description="Host of the STUN server.",
    )
    port: int = Field(
        ...,
        ge=1,
        le=65535,
        title="STUNServer.Port",
        description="Port of the STUN server.",
    )


class StreamRequestData(SerializableModel):
    """Data for a stream request."""

    stun: STUNServer | None = Field(
        None,
        title="StreamRequestData.STUN",
        description="STUN server to use.",
    )
    codec: sm.Codec = Field(
        sm.Codec.OPUS,
        title="StreamRequestData.Codec",
        description="Codec of the media in the stream.",
    )
    format: sm.Format = Field(
        sm.Format.OGG,
        title="StreamRequestData.Format",
        description="Format of the media in the stream.",
    )
    srt: SRTServer = Field(
        ...,
        title="StreamRequestData.SRT",
        description="SRT server to send the stream to.",
    )


class StreamResponseData(SerializableModel):
    """Data for a stream response."""

    port: int = Field(
        ...,
        ge=1,
        le=65535,
        title="StreamResponseData.Port",
        description="Port to use to connect to the stream.",
    )
    stun: STUNServer = Field(
        ...,
        title="StreamResponseData.STUN",
        description="STUN server to use.",
    )


@dataclass(kw_only=True)
class StreamRequest:
    """Request for a stream."""

    data: StreamRequestData


@dataclass(kw_only=True)
class StreamResponse:
    """Response to a streaming request."""

    data: StreamResponseData
