import json
from faststream.rabbit.types import AioPikaSendableMessage
from pydantic import BaseModel

from infrastructure.rabbit import broker
from models.admin import RequestResponse


async def send_rpc[T: BaseModel](body: AioPikaSendableMessage, queue: str, response_class: T = BaseModel) -> RequestResponse[T]:
    res = await broker.request(
        body,
        queue
    )
    await res.ack()
    return RequestResponse[response_class](**json.loads(res.body.decode()))