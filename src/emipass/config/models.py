from datetime import timedelta
from typing import Annotated, Any, Self

from pydantic import BaseModel, Field, field_validator, model_validator

from emipass.config.base import BaseConfig


class ServerRTPPortsConfig(BaseModel):
    """Configuration for the server RTP ports."""

    min: int = Field(
        11002,
        ge=1,
        le=65535,
        title="Minimum",
        description="Minimum port to select from when listening for RTP connections.",
    )
    max: int = Field(
        11002,
        ge=1,
        le=65535,
        title="Maximum",
        description="Maximum port to select from when listening for RTP connections.",
    )

    @model_validator(mode="after")
    def validate_ports(self) -> Self:
        if self.min > self.max:
            message = "Minimum port cannot be greater than maximum port."
            raise ValueError(message)

        return self


class ServerPortsConfig(BaseModel):
    """Configuration for the server ports."""

    http: int = Field(
        11000,
        ge=0,
        le=65535,
        title="HTTP",
        description="Port to listen for HTTP requests on.",
    )
    whip: set[Annotated[int, Field(..., ge=1, le=65535)]] = Field(
        {11001},
        min_length=1,
        title="WHIP",
        description="Ports to select from when listening for WHIP requests.",
    )
    rtp: ServerRTPPortsConfig = Field(
        ServerRTPPortsConfig(),
        title="RTP",
        description="Configuration for the server RTP ports.",
    )

    @field_validator("whip", mode="before")
    @classmethod
    def validate_whip(cls, v: Any) -> Any:
        if isinstance(v, int):
            v = {v}
        elif isinstance(v, str):
            v = set(v.split(","))

        return v


class ServerConfig(BaseModel):
    """Configuration for the server."""

    host: str = Field(
        "0.0.0.0",
        title="Host",
        description="Host to run the server on.",
    )
    ports: ServerPortsConfig = Field(
        ServerPortsConfig(),
        title="Ports",
        description="Configuration for the server ports.",
    )


class STUNConfig(BaseModel):
    """Configuration for the STUN server."""

    host: str = Field(
        "stun.l.google.com",
        title="Host",
        description="Host of the STUN server.",
    )
    port: int = Field(
        19302,
        ge=0,
        le=65535,
        title="Port",
        description="Port of the STUN server.",
    )


class StreamerConfig(BaseModel):
    """Configuration for the streamer."""

    stun: STUNConfig = Field(
        STUNConfig(),
        title="STUN",
        description="Configuration for the STUN server.",
    )
    timeout: timedelta = Field(
        timedelta(minutes=1),
        ge=0,
        title="Timeout",
        description="Time after which a stream will be stopped if no connections are made.",
    )


class Config(BaseConfig):
    """Configuration for the application."""

    server: ServerConfig = Field(
        ServerConfig(),
        title="Server",
        description="Configuration for the server.",
    )
    streamer: StreamerConfig = Field(
        StreamerConfig(),
        title="Streamer",
        description="Configuration for the streamer.",
    )
