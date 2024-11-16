import os, dotenv
from typing import Literal

IS_PROD = os.getenv("IS_PROD", False)
if not IS_PROD:
    dotenv.load_dotenv(".env.development")

# ----- [[ DATABASE ]] -----

DB_DRIVER = "postgresql+asyncpg"
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_NAME = os.environ.get("DB_NAME")
DB_URL = f"{DB_DRIVER}://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# ----- [[ TELEGRAM ]] -----

TG_TOKEN = os.environ.get("TG_TOKEN")
TG_ADMIN_CHAT = os.environ.get("TG_ADMIN_CHAT")
TG_CHANNEL_ID = os.environ.get("TG_CHANNEL_ID") # Dont use in .env, if you dont want this requirement
TG_CHANNEL_LINK = os.environ.get("TG_CHANNEL_LINK")
TG_API_URL = "https://api.telegram.org/bot" + TG_TOKEN

# ----- [[ SETTINGS ]] -----

MAX_AVATAR_SIZE = 1024 * 1024 * 3 # Bytes
CLASS_LITERAL = Literal[
    "9Н",
    "9О",
    "9И",
    "9Ф",
    "9Г",
    "9В",
    "10К",
    "10С",
    "10Ю",
    "10У",
    "10Ж",
    "10З",
    "10И",
    "10Т",
    "10А",
    "10Б",
    "10Н",
    "10Ж",
    "10О",
    "10Ф",
    "11К",
    "11С",
    "11Ю",
    "11Ж",
    "11И",
    "11Т",
    "11А",
    "11Б",
    "11Ж",
    "11О",
    "11Ф",
    "11П",
    "11Ч"
]

# ----- [[ OTHER ]] -----

API_URL = os.environ.get("API_URL")
ROOT_PATH = os.environ.get("ROOT_PATH", "")
RABBIT_URL = os.environ.get("RABBIT_URL")
LOKI_URL = os.environ.get("LOKI_URL")