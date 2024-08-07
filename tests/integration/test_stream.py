import pytest
from litestar.status_codes import HTTP_201_CREATED
from litestar.testing import AsyncTestClient


@pytest.mark.asyncio(scope="session")
async def test_post(client: AsyncTestClient) -> None:
    """Test if POST /stream returns correct response."""

    request = {
        "srt": {
            "host": "example.com",
            "port": 12345,
        },
    }
    response = await client.post("/stream", json=request)

    status = response.status_code
    assert status == HTTP_201_CREATED

    data = response.json()
    assert "port" in data
    assert "stun" in data

    stun = data["stun"]
    assert "host" in stun
    assert "port" in stun

    host = stun["host"]
    assert isinstance(host, str)

    port = stun["port"]
    assert isinstance(port, int)

    port = data["port"]
    assert isinstance(port, int)
