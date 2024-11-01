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
TG_ADMIN_CHAT = int(os.environ.get("TG_ADMIN_CHAT"))
TG_API_URL = "https://api.telegram.org/bot" + TG_TOKEN

# ----- [[ SETTINGS ]] -----

MAX_AVATAR_SIZE = 1024 * 1024 * 3 # Bytes
CLASS_LITERAL = Literal[
    "10И",
    "11И",
    "10П",
    "11П",
    "10Ч",
    "11Ч",
    "10К",
    "11К",
    "10С",
    "11С",
    "10Ю",
    "11Ю",
    "10А",
    "11А",
    "10Ф",
    "10Ж",
    "11Ж",
    "10Б",
    "11Б",
    "10Н",
    "11Н",
    "10О",
    "11О",
    "9О",
    "9И",
    "9Н",
]

# ----- [[ OTHER ]] -----

API_URL = os.environ.get("API_URL")
ROOT_PATH = os.environ.get("ROOT_PATH", "")