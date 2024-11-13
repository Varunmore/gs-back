import asyncio
import cv2
from aiortc import VideoStreamTrack
from av import VideoFrame
import subprocess

class MoonlightStreamTrack(VideoStreamTrack):
    def __init__(self, game_id):
        super().__init__()
        self.game_id = game_id
        # Launch Moonlight in subprocess to capture video
        self.moonlight_proc = subprocess.Popen(
            ["moonlight", "stream", "103.211.112.53", "-app", self.game_id],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        self.fps = 60
        self.delay = 1 / self.fps

    async def recv(self):
        # Capture frames from Moonlight’s output
        loop = asyncio.get_event_loop()
        ret, frame = await loop.run_in_executor(None, self._capture_frame)
        if not ret:
            raise Exception("Failed to capture frame.")
        video_frame = VideoFrame.from_ndarray(frame, format="bgr24")
        await asyncio.sleep(self.delay)
        return video_frame

    def _capture_frame(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        return ret, frame

    def stop(self):
        self.moonlight_proc.terminate()
