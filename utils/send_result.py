import requests, sys, os

def send(text: str) -> None:
    requests.post(f"https://api.telegram.org/bot{os.environ.get("TG_TOKEN")}/sendMessage", json={
        "chat_id": os.environ.get("TG_CHAT_ID"),
        "text": text,
        "parse_mode": "markdown"
    })

match sys.argv[1]:
    case "success":
        send("🌐 Процесс сборки успешно завершён")
    case "fail":
        send("❌ Сборка провалена.\n@zoomdevs @ramchike")