from aiortc import VideoStreamTrack
from av import VideoFrame
import cv2
import numpy as np
import asyncio

class GameStreamTrack(VideoStreamTrack):
    """
    A video stream track that captures frames from a game or screen.
    """
    def __init__(self):
        super().__init__()  # Initialize base class
        self.cap = cv2.VideoCapture(0)  # Replace with actual game capture device or screen
        if not self.cap.isOpened():
            raise Exception("Could not open video source")
        self.fps = 30  # Set desired frames per second
        self.delay = 1 / self.fps

    async def recv(self):
        loop = asyncio.get_event_loop()
        ret, frame = await loop.run_in_executor(None, self.cap.read)
        if not ret:
            raise Exception("Failed to read frame from video source")
        
        # Process frame (resize, encode, etc.)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        video_frame = VideoFrame.from_ndarray(frame, format="rgb24")
        video_frame.pts = None
        video_frame.time_base = None
        await asyncio.sleep(self.delay)
        return video_frame

    def __del__(self):
        if self.cap.isOpened():
            self.cap.release()
