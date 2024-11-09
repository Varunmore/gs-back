# app/utils/rtc.py

import asyncio
from aiortc import RTCPeerConnection, RTCSessionDescription, RTCIceCandidate
from aiortc.contrib.media import MediaPlayer
from typing import Dict

# In-memory storage for peer connections
pcs: Dict[int, RTCPeerConnection] = {}

async def offer(data: dict):
    """
    Handle an SDP offer from the client and respond with an SDP answer.
    """
    offer = RTCSessionDescription(sdp=data["sdp"], type=data["type"])
    
    pc = RTCPeerConnection()
    pcs[1] = pc  # Using a fixed game_id (replace with dynamic as needed)

    @pc.on("iceconnectionstatechange")
    async def on_iceconnectionstatechange():
        print(f"ICE connection state: {pc.iceConnectionState}")
        if pc.iceConnectionState in ["failed", "closed", "disconnected"]:
            await pc.close()
            del pcs[1]

    # Add media tracks (Replace with actual game stream)
    player = MediaPlayer("/path/to/game/audio")  # Replace with actual game audio source
    if player.audio:
        pc.addTrack(player.audio)

    await pc.setRemoteDescription(offer)
    answer = await pc.createAnswer()
    await pc.setLocalDescription(answer)

    return {"sdp": pc.localDescription.sdp, "type": pc.localDescription.type}

async def cleanup():
    """
    Close all peer connections.
    """
    coros = [pc.close() for pc in pcs.values()]
    await asyncio.gather(*coros)
    pcs.clear()
