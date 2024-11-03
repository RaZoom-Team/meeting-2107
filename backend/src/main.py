from infrastructure.application import create_app
from infrastructure.rabbit import rabbit
from interface.rabbit import AdminRouter
from interface.api import UserRouter, AttachmentRouter, LikesRouter, SystemRouter
from config import ROOT_PATH

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
    ignoring_log_endpoints=[("/system/ping", "GET")]
)