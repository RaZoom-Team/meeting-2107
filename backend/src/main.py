from infrastructure.application import create_app
from api import UserRouter, AttachmentRouter

app = create_app(
    routers=[
        UserRouter,
        AttachmentRouter
    ]
)