import os, time, requests
from datetime import datetime

NGROK_API = os.getenv("NGROK_API", "http://ngrok:4040/api/tunnels")
STATE_FILE = "/state/last_port.txt"

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"

CHECK_INTERVAL = 10


def log(msg: str):
    print(f"[{datetime.now()}] {msg}", flush=True)


def send_telegram(text: str):
    try:
        r = requests.post(
            f"{TELEGRAM_API}/sendMessage",
            data={"chat_id": TELEGRAM_CHAT_ID, "text": text}
        )
        if r.status_code != 200:
            log(f"Telegram error: {r.text}")
    except Exception as e:
        log(f"Telegram exception: {e}")


def get_ngrok_info():
    try:
        j = requests.get(NGROK_API, timeout=2).json()
        tunnels = j.get("tunnels", [])
        if tunnels:
            url = tunnels[0]["public_url"]  # tcp://host:port
            host, port = url.replace("tcp://", "").split(":")
            return host, port
    except Exception:
        pass
    return None, None


def main():
    log("Notifier started")

    os.makedirs("/state", exist_ok=True)
    last_port = None

    if os.path.exists(STATE_FILE):
        last_port = open(STATE_FILE).read().strip()

    while True:
        host, port = get_ngrok_info()

        if host and port:
            if port != last_port:
                last_port = port
                with open(STATE_FILE, "w") as f:
                    f.write(port)

                msg = (
                    "🌐 MQTT Broker Online\n\n"
                    "🔌 Ngrok Tunnel\n"
                    f"Host: {host}\n"
                    f"Port: {port}"
                )
                send_telegram(msg)
                log(f"New tunnel detected → {host}:{port}")

        else:
            log("Ngrok not ready yet...")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    main()