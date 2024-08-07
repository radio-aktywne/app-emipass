from typing import Annotated

from litestar import Controller as BaseController
from litestar import handlers
from litestar.di import Provide
from litestar.params import Body
from litestar.response import Response

from emipass.api.exceptions import ConflictException
from emipass.api.routes.stream import errors as e
from emipass.api.routes.stream import models as m
from emipass.api.routes.stream.service import Service
from emipass.api.validator import Validator
from emipass.state import State


class DependenciesBuilder:
    """Builder for the dependencies of the controller."""

    async def _build_service(self, state: State) -> Service:
        return Service(
            streaming=state.streaming,
        )

    def build(self) -> dict[str, Provide]:
        return {
            "service": Provide(self._build_service),
        }


class Controller(BaseController):
    """Controller for the stream endpoint."""

    dependencies = DependenciesBuilder().build()

    @handlers.post(
        summary="Request a stream",
        raises=[
            ConflictException,
        ],
    )
    async def stream(
        self,
        service: Service,
        data: Annotated[
            m.StreamRequestData,
            Body(
                description="Data for the request.",
            ),
        ],
    ) -> Response[m.StreamResponseData]:
        """Request a stream."""

        data = Validator[m.StreamRequestData]().object(data)

        req = m.StreamRequest(
            data=data,
        )

        try:
            res = await service.stream(req)
        except e.ServiceBusyError as ex:
            raise ConflictException(extra=str(ex)) from ex

        rdata = res.data

        return Response(rdata)
