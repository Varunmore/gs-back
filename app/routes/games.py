# app/routes/games.py

from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.models import Game
from app.utils.rtc import offer, cleanup
import json

router = APIRouter()

# Sample game data
games_db = [
    Game(id=1, name="Counter Strike", poster="/images/CS.jpg", description="A team-based tactical shooter."),
    Game(id=2, name="Far Cry 6", poster="/images/farcry.jpg", description="An open-world action-adventure game."),
    Game(id=3, name="Need For Speed Payback", poster="/images/nfspayback.jpg", description="A racing video game."),
    Game(id=4, name="God Of War", poster="/images/godofwar.jpeg", description="An action-adventure game based on Norse mythology."),
    Game(id=5, name="Assassin Creed Valhalla", poster="/images/assain.jpg", description="An action role-playing game set in the Viking Age."),
    Game(id=6, name="Max Payne 3", poster="/images/maxpayne.jpg", description="A third-person shooter video game."),
]

@router.get("/games")
def get_games():
    return games_db

@router.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            if message.get("action") == "offer":
                response = await offer(message.get("data"))
                await websocket.send_text(json.dumps(response))
    except WebSocketDisconnect:
        await cleanup()
