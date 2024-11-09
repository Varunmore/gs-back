from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.utils.rtc import handle_offer, handle_candidate, cleanup
import json

router = APIRouter()

@router.websocket("/ws/stream")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            action = message.get("action")
            payload = message.get("data")
            
            if action == "offer":
                response = await handle_offer(payload)
                await websocket.send_text(json.dumps(response))
            elif action == "ice-candidate":
                await handle_candidate(payload)
    except WebSocketDisconnect:
        await cleanup()
