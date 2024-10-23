from infrastructure.application import create_app
from infrastructure.db import init_models
from api import UserRouter, AttachmentRouter

app = create_app(
    routers=[
        UserRouter,
        AttachmentRouter
    ],
    startup_tasks=[
        init_models
    ]
)