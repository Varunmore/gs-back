from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from aiortc import RTCPeerConnection, RTCSessionDescription
from utils.game_stream import MoonlightStreamTrack
import json

app = FastAPI()
sessions = {}

@app.websocket("/ws/game/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: str):
    await websocket.accept()
    pc = RTCPeerConnection()
    track = MoonlightStreamTrack(game_id)
    sessions[websocket] = (pc, track)

    @pc.on("icecandidate")
    async def on_icecandidate(candidate):
        await websocket.send_text(json.dumps({"candidate": candidate}))

    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            if message["action"] == "offer":
                offer = RTCSessionDescription(sdp=message["sdp"], type=message["type"])
                await pc.setRemoteDescription(offer)
                pc.addTrack(track)

                answer = await pc.createAnswer()
                await pc.setLocalDescription(answer)
                await websocket.send_text(json.dumps({
                    "action": "answer",
                    "sdp": pc.localDescription.sdp,
                    "type": pc.localDescription.type
                }))
    except WebSocketDisconnect:
        await pc.close()
        track.stop()
        del sessions[websocket]
