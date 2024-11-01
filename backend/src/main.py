from infrastructure.application import create_app
from api import UserRouter, AttachmentRouter, LikesRouter, SystemRouter
from config import ROOT_PATH

app = create_app(
    routers=[
        UserRouter,
        LikesRouter,
        AttachmentRouter,
        SystemRouter
    ],
    root_path=ROOT_PATH
)