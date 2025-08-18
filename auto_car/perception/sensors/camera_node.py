"""
camera_node.py
Captures frames from a PiCamera2 device.
Designed for reuse in manual or autonomous control pipelines.
"""

from picamera2 import Picamera2
import cv2
import time
import numpy as np


class CameraNode:
    def __init__(self, camera_index=0, resolution=(800, 600), flip_front=False):
        """
        :param camera_index: int - Camera device index (0 = rear, 1 = front)
        :param resolution: tuple - (width, height)
        :param flip_front: bool - Flip the image if it's the front camera
        """
        self.camera_index = camera_index
        self.flip_front = flip_front and camera_index == 1
        self.picam = Picamera2(camera_index)

        # Force full sensor mode, match aspect ratio to avoid cropping
        cfg = self.picam.create_preview_configuration(
            main={"size": resolution},
            raw={"size": self.picam.sensor_resolution},  # ensures full FOV
            buffer_count=4
        )
        self.picam.configure(cfg)

    def start(self):
        """Start the camera stream."""
        self.picam.start()

    def stop(self):
        """Stop the camera stream."""
        self.picam.stop()

    def get_frame(self):
        """Capture a frame, apply optional flip, and return as BGR."""
        frame = self.picam.capture_array()

        if self.flip_front:
            frame = cv2.flip(frame, -1)

        # # Crop bottom for rear camera
        # if self.camera_index == 0:
        #     crop_fraction = 0.195  # cut off bottom of image
        #     h = frame.shape[0]
        #     frame = frame[:int(h * (1 - crop_fraction)), :]

        return cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)


if __name__ == "__main__":
    cam_front = CameraNode(camera_index=1)
    cam_rear = CameraNode(camera_index=0)

    cam_front.start()
    cam_rear.start()

    time.sleep(1)  # ensure both cameras are ready

    try:
        while True:
            frame_front = cam_front.get_frame()
            frame_rear = cam_rear.get_frame()

            cv2.imshow("Front", frame_front)
            cv2.imshow("Rear", frame_rear)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    finally:
        cam_front.stop()
        cam_rear.stop()
        cv2.destroyAllWindows()
