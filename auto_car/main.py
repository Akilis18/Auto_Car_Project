# main.py
"""
This script serves as the entry point for the application.
It orchestrates the entire system.
"""

import threading
import cv2
import sys
import curses
from datetime import datetime
import pathlib

import control.manual_control as manual_control
from perception.sensors.camera_node import CameraNode


class CarApp:
    def __init__(self):
        self.stop_event = threading.Event()
        self.base_dir = pathlib.Path("images")
        self.front_dir = self.base_dir / "front"
        self.rear_dir = self.base_dir / "rear"
        self.front_dir.mkdir(parents=True, exist_ok=True)
        self.rear_dir.mkdir(parents=True, exist_ok=True)

    def suppress_libpng_warnings(self):
        sys.stderr = open('/dev/null', 'w')

    def run_remote_control(self):
        remote = manual_control.RemoteControl()

        def run_with_feedback(stdscr):
            stdscr.nodelay(True)
            stdscr.clear()
            stdscr.addstr(0, 0, "Use W/A/S/D to move, X to stop, C to center steer, Q to quit\n")
            stdscr.refresh()

            while not self.stop_event.is_set():
                key = stdscr.getch()
                if key != -1:
                    stdscr.addstr(2, 0, f"Key pressed: {chr(key) if 32 <= key <= 126 else key}   ")
                    stdscr.refresh()

                    if key == ord('w'):
                        remote.send_command("SPEED:255")
                    elif key == ord('s'):
                        remote.send_command("SPEED:-180")
                    elif key == ord('a'):
                        remote.send_command("STEER:60")
                    elif key == ord('d'):
                        remote.send_command("STEER:120")
                    elif key == ord('x'):
                        remote.send_command("SPEED:0")
                    elif key == ord('c'):
                        remote.send_command("STEER:90")
                    elif key == ord('e'):
                        remote.send_command("E")
                    elif key == ord('q'):
                        self.stop_event.set()
                        break

        curses.wrapper(run_with_feedback)
        remote.close_connection()

    def run_cameras(self):
        cam_rear = CameraNode(camera_index=0, resolution=(640, 480))
        cam_front = CameraNode(camera_index=1, resolution=(640, 480))

        cam_rear.start()
        cam_front.start()

        try:
            while not self.stop_event.is_set():
                frame_rear = cam_rear.get_frame()
                frame_front = cam_front.get_frame()

                cv2.imshow("Front", frame_front)
                cv2.imshow("Rear", frame_rear)

                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    self.stop_event.set()
                    break
                elif key == ord('g'):
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
                    rear_path = self.rear_dir / f"rear_{timestamp}.jpg"
                    front_path = self.front_dir / f"front_{timestamp}.jpg"
                    cv2.imwrite(str(rear_path), frame_rear)
                    cv2.imwrite(str(front_path), frame_front)
                    print(f"Saved: {rear_path} and {front_path}")

        finally:
            cam_rear.stop()
            cam_front.stop()
            cv2.destroyAllWindows()

    def auto_mode(self):
        print("Auto mode starting...")
        # Placeholder for autonomous driving logic (lane detection, object detection, etc.)
        self.run_cameras()
        print("Auto mode finished.")

    def manual_mode(self):
        print("Manual mode starting...")
        control_thread = threading.Thread(target=self.run_remote_control, daemon=True)
        cam_thread = threading.Thread(target=self.run_cameras)

        control_thread.start()
        cam_thread.start()

        control_thread.join()
        cam_thread.join()
        print("Manual mode finished.")

    def start(self, mode="manual"):
        self.suppress_libpng_warnings()

        if mode == "manual":
            self.manual_mode()
        elif mode == "auto":
            self.auto_mode()


if __name__ == "__main__":
    mode = input("Enter mode (manual/auto): ").strip().lower()
    app = CarApp()
    app.start(mode)
