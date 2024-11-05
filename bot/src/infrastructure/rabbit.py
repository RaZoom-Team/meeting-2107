from faststream import FastStream
from faststream.rabbit import RabbitBroker

from config import RABBIT_URL


broker = RabbitBroker(RABBIT_URL)
app = FastStream(broker)