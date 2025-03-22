from remote_control import RemoteControl  # Import the class from the file containing your refactored code
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

    # Initialize cameras
    picam1 = Picamera2(0)
    picam2 = Picamera2(1)

    config1 = picam1.create_preview_configuration()
    config2 = picam2.create_preview_configuration()

    picam1.configure(config1)
    picam2.configure(config2)

    picam1.start()
    picam2.start()

    while not stop_event.is_set():  # Keep running until stop_event is set
        frame1 = picam1.capture_array()
        frame2 = picam2.capture_array()
        frame2 = cv2.flip(frame2, -1)

        cv2.imshow("Cam 1", frame1)
        cv2.imshow("Cam 2", frame2)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            stop_event.set()  # Signal both threads to stop
            break

    picam1.stop()
    picam2.stop()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
