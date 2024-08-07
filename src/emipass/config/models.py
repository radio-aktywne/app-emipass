from datetime import timedelta
from typing import Annotated, Any, Self

from pydantic import BaseModel, Field, field_validator, model_validator

from emipass.config.base import BaseConfig


class ServerRTPPortsConfig(BaseModel):
    """Configuration for the server RTP ports."""

    min: int = Field(11002, ge=1, le=65535)
    """Minimum port to select from when listening for RTP connections."""

    max: int = Field(11002, ge=1, le=65535)
    """Maximum port to select from when listening for RTP connections."""

    @model_validator(mode="after")
    def validate_ports(self) -> Self:
        if self.min > self.max:
            message = "Minimum port cannot be greater than maximum port."
            raise ValueError(message)

        return self


class ServerPortsConfig(BaseModel):
    """Configuration for the server ports."""

    http: int = Field(11000, ge=0, le=65535)
    """Port to listen for HTTP requests on."""

    whip: set[Annotated[int, Field(..., ge=1, le=65535)]] = Field({11001}, min_length=1)
    """Ports to select from when listening for WHIP requests."""

    rtp: ServerRTPPortsConfig = ServerRTPPortsConfig()
    """Configuration for the server RTP ports."""

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

    host: str = "0.0.0.0"
    """Host to run the server on."""

    ports: ServerPortsConfig = ServerPortsConfig()
    """Configuration for the server ports."""

    trusted: str | list[str] | None = "*"
    """Trusted IP addresses."""


class STUNConfig(BaseModel):
    """Configuration for the STUN server."""

    host: str = "stun.l.google.com"
    """Host of the STUN server."""

    port: int = Field(19302, ge=0, le=65535)
    """Port of the STUN server."""


class StreamerConfig(BaseModel):
    """Configuration for the streamer."""

    stun: STUNConfig = STUNConfig()
    """Configuration for the STUN server."""

    timeout: timedelta = Field(timedelta(minutes=1), ge=0)
    """Time after which a stream will be stopped if no connections are made."""


class Config(BaseConfig):
    """Configuration for the application."""

    server: ServerConfig = ServerConfig()
    """Configuration for the server."""

    streamer: StreamerConfig = StreamerConfig()
    """Configuration for the streamer."""

    debug: bool = False
    """Enable debug mode."""
