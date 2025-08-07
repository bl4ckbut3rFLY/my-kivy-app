from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from typing import Dict
import json

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

clients: Dict[str, WebSocket] = {}
logs: Dict[str, list] = {}
AUTHORIZED_TOKENS = {"my_secure_token_123"}

@app.get("/")
async def dashboard():
    with open("static/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())

@app.get("/clients")
def list_clients():
    return {"clients": list(clients.keys())}

@app.get("/logs/{client_id}")
def get_logs(client_id: str):
    return {"logs": logs.get(client_id, [])}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        token = await websocket.receive_text()
        if token not in AUTHORIZED_TOKENS:
            await websocket.send_text("403 Forbidden: Invalid token")
            await websocket.close()
            return

        client_ip = websocket.client.host
        client_id = f"{client_ip}_{token[-4:]}"
        clients[client_id] = websocket
        logs.setdefault(client_id, []).append("[CONNECTED]")
        await websocket.send_text("200 OK: Connected")

        while True:
            data = await websocket.receive_text()
            logs[client_id].append(f"[RECEIVED] {data}")
    except WebSocketDisconnect:
        logs[client_id].append("[DISCONNECTED]")
        clients.pop(client_id, None)

@app.post("/send/{client_id}")
async def send_command(client_id: str, payload: Dict):
    if client_id not in clients:
        return {"error": "Client not connected"}
    command = payload.get("command")
    if not command:
        return {"error": "No command provided"}
    try:
        await clients[client_id].send_text(json.dumps({"type": "command", "command": command}))
        logs[client_id].append(f"[SENT] {command}")
        return {"status": "sent"}
    except Exception as e:
        return {"error": str(e)}
