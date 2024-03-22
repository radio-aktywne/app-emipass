from enum import StrEnum

from pydantic import Field

from emipass.models.base import SerializableModel


class Format(StrEnum):
    OGG = "ogg"


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
        description="Password to use for the SRT stream.",
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


class Request(SerializableModel):
    """Request for a stream."""

    stun: STUNServer | None = Field(
        None,
        title="Request.STUN",
        description="STUN server to use.",
    )
    format: Format = Field(
        Format.OGG,
        title="Request.Format",
        description="Format of the output audio.",
    )
    srt: SRTServer = Field(
        ...,
        title="Request.SRT",
        description="SRT server to send the stream to.",
    )


class Response(SerializableModel):
    """Response to a streaming request."""

    port: int = Field(
        ...,
        ge=1,
        le=65535,
        title="Response.Port",
        description="Port to use to connect to the stream.",
    )
    stun: STUNServer = Field(
        ...,
        title="Response.STUN",
        description="STUN server to use.",
    )
