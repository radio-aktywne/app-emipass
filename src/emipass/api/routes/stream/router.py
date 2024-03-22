from litestar import Router

from emipass.api.routes.stream.controller import Controller

router = Router(
    path="/stream",
    route_handlers=[
        Controller,
    ],
)
