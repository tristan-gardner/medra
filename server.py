import grpc
import time
from concurrent import futures
import cv2
import numpy as np
from video_pb2 import VideoFrame, VideoFrameRequest, HealthCheckReply, HealthCheckReq
from video_pb2_grpc import VideoStreamerServicer, add_VideoStreamerServicer_to_server

class VideoStreamer(VideoStreamerServicer):
    def __init__(self):
        self.camera_id = '0'  # Default camera ID

    def StreamFrames(self, request, context):
        while True:
            # Capture screen using cv2
            screen = self.capture_screen()

            # Send video frame
            frame = VideoFrame(
                camera_id=request.camera_id,
                img=screen,
                time_stamp=int(time.time() * 1000)  # Milliseconds timestamp
            )
            yield frame
            time.sleep(1 / 30)  # Simulate 30 fps streaming

    def GetFrames(self, request, context):
        # Capture screen using cv2
        screen = self.capture_screen()

        return VideoFrame(
            camera_id=self.camera_id,
            img=screen,
            time_stamp=int(time.time() * 1000)
        )

    def HealthCheck(self, request, context):
        return HealthCheckReply(ok=True)

    def capture_screen(self):
        # Capture the screen using cv2
        screen = np.array(cv2.VideoCapture(0).read()[1])  # Capture from primary display or you can specify a screen capture method
        screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)  # Convert to RGB if needed
        _, img_bytes = cv2.imencode('.jpg', screen, [cv2.IMWRITE_JPEG_QUALITY, 50])
        img_bytes = img_bytes.tobytes()
        return img_bytes


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_VideoStreamerServicer_to_server(VideoStreamer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server running on port 50051")
    try:
        while True:
            time.sleep(60 * 60 * 24)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
