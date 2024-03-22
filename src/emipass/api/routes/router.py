from litestar import Router

from emipass.api.routes.ping.router import router as ping_router
from emipass.api.routes.stream.router import router as stream_router

router = Router(
    path="/",
    route_handlers=[
        ping_router,
        stream_router,
    ],
)
