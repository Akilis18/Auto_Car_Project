from remote_control import RemoteControl
from lane_detection import LaneDetector
import cv2
from picamera2 import Picamera2
import threading

# Create a global stop event
stop_event = threading.Event()

def run_remote_control():
    control = RemoteControl()
    control.start()  # Start the curses interface

def main():
    # Start the remote control in a separate thread
    control_thread = threading.Thread(target=run_remote_control, daemon=True)
    control_thread.start()

    # Initialize lane detector
    lane_detector = LaneDetector(kernel_size=5, low_t=50, high_t=150)

    # Initialize cameras (0 = Rear camera, 1 = Front camera)
    rear_cam = Picamera2(0)
    front_cam = Picamera2(1)

    # Configure cameras for optimized performance (640x480 for speed)
    rear_config = rear_cam.create_preview_configuration(main={"size": (640, 480)})
    front_config = front_cam.create_preview_configuration(main={"size": (640, 480)})

    rear_cam.configure(rear_config)
    front_cam.configure(front_config)

    # Start both cameras
    rear_cam.start()
    front_cam.start()

    while not stop_event.is_set():
        # Capture frames
        rear_frame = rear_cam.capture_array()  # Rear camera (RGB)
        front_frame = front_cam.capture_array()  # Front camera (RGB)

        # Flip the front frame for correct orientation
        front_frame = cv2.flip(front_frame, -1)

        # Convert from RGB to BGR for OpenCV
        rear_frame = cv2.cvtColor(rear_frame, cv2.COLOR_RGB2BGR)
        front_frame = cv2.cvtColor(front_frame, cv2.COLOR_RGB2BGR)

        # Apply lane detection
        rear_frame = lane_detector.process_frame(rear_frame)
        front_frame = lane_detector.process_frame(front_frame)

        # Display both frames
        cv2.imshow("Rear Camera - Lane Detection", rear_frame)
        cv2.imshow("Front Camera - Lane Detection", front_frame)

        # Exit on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_event.set()
            break

    # Stop cameras and close windows
    rear_cam.stop()
    front_cam.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
