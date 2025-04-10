import grpc
import time
from video_pb2 import VideoFrameRequest, GetFrameRequest, HealthCheckReq
from video_pb2_grpc import VideoStreamerStub
import cv2
import numpy as np

def run():
    channel = grpc.insecure_channel('localhost:50051')
    stub = VideoStreamerStub(channel)

    hc = stub.HealthCheck(HealthCheckReq(ok=True))
    print("Health Check:", hc.ok)

    # Create request
    request = VideoFrameRequest(camera_id='0')

    # Stream frames
    for frame in stub.StreamFrames(request):
        print(f"Received frame from {frame.camera_id} at {frame.time_stamp}: Latency {int(time.time() * 1000) - frame.time_stamp} ms")
        # Here, you can process the frame.img bytes (e.g., display it on a UI)
        time.sleep(1 / 30)  # Simulate 30 fps

        # Code to show image as debug
        # img_array = np.frombuffer(frame.img, dtype=np.uint8)
        # img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)  # Decode the byte array into an image

        # # Display the image
        # cv2.imshow('Video Stream', img)

        # Wait for a key press (to keep the window open), break the loop if 'q' is pressed
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     break

if __name__ == '__main__':
    run()
