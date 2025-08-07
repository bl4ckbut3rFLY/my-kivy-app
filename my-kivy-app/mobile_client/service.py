import websocket
import json
from notification import notify_user

USER_TOKEN = "my_secure_token_123"
SERVER_URL = "ws://yourserver.com/ws"

def on_message(ws, message):
    try:
        data = json.loads(message)
        if data.get("type") == "command":
            command = data.get("command")
            notify_user(f"📡 New command received")
    except Exception as e:
        notify_user("❌ error", str(e))

def run():
    ws = websocket.WebSocketApp(
        SERVER_URL,
        on_open=lambda ws: ws.send(USER_TOKEN),
        on_message=on_message
    )
    ws.run_forever()

if __name__ == "__main__":
    run()
