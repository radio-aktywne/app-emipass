from litestar import Controller as BaseController
from litestar import handlers
from litestar.di import Provide
from litestar.response import Response

from emipass.api.exceptions import ConflictException
from emipass.api.routes.stream import errors as e
from emipass.api.routes.stream import models as m
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

    @handlers.post(
        summary="Request a stream",
        description="Request a stream.",
        raises=[ConflictException],
    )
    async def stream(
        self, data: m.StreamRequestData, service: Service
    ) -> Response[m.StreamResponseData]:
        try:
            response = await service.stream(
                m.StreamRequest(
                    data=data,
                )
            )
        except e.StreamerBusyError as ex:
            raise ConflictException(extra=ex.message) from ex

        resdata = response.data

        return Response(resdata)
