from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class ConnectionManager:
    def __init__(self):
        self.user_list: list[str] = []
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.active_connections.append(websocket)
        self.user_list.append(username)

    def disconnect(self, websocket: WebSocket, username: str):
        self.active_connections.remove(websocket)
        try:
            self.user_list.remove(username)
        except Exception as e:
            print(str(e))
            pass

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()


@app.get("/")
async def get(request : Request):
    return templates.TemplateResponse("index.html", context={"request": request})


@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await manager.connect(websocket, client_id)
    user_list = " ".join(manager.user_list)
    await manager.broadcast(f"Online users: {user_list}")
    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{str(client_id)} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket, client_id)
        user_list = ", ".join(manager.user_list)
        await manager.broadcast(f"Online users: {user_list}")
        await manager.broadcast(f"Client #{client_id} left the chat")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)