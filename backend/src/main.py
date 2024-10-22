from infrastructure.application import create_app
from infrastructure.db import init_models
from api import UserRouter

app = create_app(
    routers=[
        UserRouter
    ],
    startup_tasks=[
        init_models
    ]
)