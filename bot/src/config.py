import os, dotenv

IS_PROD = os.getenv("IS_PROD", False)
if not IS_PROD:
    dotenv.load_dotenv(".env.development")

TG_TOKEN = os.environ.get("TG_TOKEN")
TG_ADMIN_CHAT = int(os.environ.get("TG_ADMIN_CHAT"))
RABBIT_URL = os.environ.get("RABBIT_URL")