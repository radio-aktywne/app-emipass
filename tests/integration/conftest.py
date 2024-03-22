from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
from litestar import Litestar
from litestar.testing import AsyncTestClient

from emipass.api.app import AppBuilder
from emipass.config.builder import ConfigBuilder
from emipass.config.models import Config


@pytest.fixture(scope="session")
def config() -> Config:
    """Loaded configuration."""

    return ConfigBuilder().build()


@pytest.fixture(scope="session")
def app(config: Config) -> Litestar:
    """Reusable application."""

    return AppBuilder(config).build()


@pytest_asyncio.fixture(scope="session")
async def client(app: Litestar) -> AsyncGenerator[AsyncTestClient, None]:
    """Reusable test client."""

    async with AsyncTestClient(app=app) as client:
        yield client
