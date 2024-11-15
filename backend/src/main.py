from src.infrastructure.application import create_app
from src.infrastructure.rabbit import rabbit
from src.interface.rabbit import AdminRouter
from src.interface.api import UserRouter, AttachmentRouter, LikesRouter, SystemRouter
from src.config import ROOT_PATH

rabbit.include_router(AdminRouter)

app = create_app(
    routers=[
        UserRouter,
        LikesRouter,
        AttachmentRouter,
        SystemRouter,
        rabbit
    ],
    root_path=ROOT_PATH,
    ignoring_log_endpoints=[("/system/ping", "GET"), ("/metrcis", "GET")]
)