from datetime import timedelta
from typing import Annotated

from pydantic import BaseModel, Field, field_validator

from emipass.config.base import BaseConfig


class ServerConfig(BaseModel):
    """Configuration for the server."""

    host: str = Field(
        "0.0.0.0",
        title="Host",
        description="Host to run the server on.",
    )
    port: int = Field(
        11000,
        ge=0,
        le=65535,
        title="Port",
        description="Port to run the server on.",
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

    host: str = Field(
        "0.0.0.0",
        title="Host",
        description="Host to listen for connections on.",
    )
    ports: set[Annotated[int, Field(..., ge=1, le=65535)]] = Field(
        {11001},
        min_length=1,
        title="Ports",
        description="Ports to select from when listening for connections.",
    )
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

    @field_validator("ports", mode="before")
    @classmethod
    def validate_ports(cls, v):
        if isinstance(v, int):
            v = {v}
        elif isinstance(v, str):
            v = set(v.split(","))

        return v


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
