from litestar import Controller as BaseController
from litestar import post
from litestar.di import Provide
from litestar.response import Response

from emipass.api.exceptions import ConflictException
from emipass.api.routes.stream.errors import StreamerBusyError
from emipass.api.routes.stream.models import StreamRequest, StreamResponse
from emipass.api.routes.stream.service import Service
from emipass.state import State


class DependenciesBuilder:
    """Builder for the dependencies of the controller."""

    async def _build_service(self, state: State) -> Service:
        return Service(state.streamer)

    def build(self) -> dict[str, Provide]:
        return {
            "service": Provide(self._build_service),
        }


class Controller(BaseController):
    """Controller for the stream endpoint."""

    dependencies = DependenciesBuilder().build()

    @post(
        summary="Request a stream",
        description="Request a stream.",
        raises=[ConflictException],
    )
    async def stream(
        self, data: StreamRequest, service: Service
    ) -> Response[StreamResponse]:
        try:
            response = await service.stream(data)
        except StreamerBusyError as error:
            raise ConflictException(extra=error.message) from error

        return Response(response)
