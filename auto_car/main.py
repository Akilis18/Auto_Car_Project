"""
Main entry point for Raspberry Pi GPIO car control
"""

import threading
import cv2
import sys
import curses
from datetime import datetime
import pathlib
import time

from perception.sensors.camera_node import CameraNode
from perception.lane_detection import lane_origin
from planning import decision_maker

import control.manual_control as manual_control
import control.trajectory_follower as trajectory_follower


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

    # ------------------ Manual Control ------------------
    def run_remote_control(self):
        remote = manual_control.RemoteControl()  # Uses RPI_GPIO_Car instance

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

                    # --- Map keys to GPIOZero methods ---
                    if key == ord('w'):
                        remote.car.Car_Run(255)
                    elif key == ord('s'):
                        remote.car.Car_Back(180)
                    elif key == ord('a'):
                        remote.car.Ctrl_Servo(50)
                    elif key == ord('d'):
                        remote.car.Ctrl_Servo(130)
                    elif key == ord('x'):
                        remote.car.Car_Stop()
                    elif key == ord('c'):
                        remote.car.Ctrl_Servo(90)
                    elif key == ord('q'):
                        self.stop_event.set()
                        break

        curses.wrapper(run_with_feedback)

    # ------------------ Camera Handling ------------------
    def run_cameras(self):
        cam_rear = CameraNode(camera_index=0, resolution=(640, 480))
        cam_front = CameraNode(camera_index=1, resolution=(640, 480), flip_front=True)

        cam_rear.start()
        cam_front.start()

        try:
            while not self.stop_event.is_set():
                frame_rear = cam_rear.get_frame()
                frame_front = cam_front.get_frame()

                if frame_front is not None:
                    cv2.imshow("Front", frame_front)
                if frame_rear is not None:
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

    # ------------------ Autonomous Mode ------------------
    def auto_mode(self):
        print("Auto mode starting...")

        remote = manual_control.RemoteControl()
        remote.car.Car_Stop()
        remote.car.Ctrl_Servo(90)  # Center steering

        cam = CameraNode(camera_index=1, resolution=(640, 480), flip_front=True)
        cam.start()

        try:
            while not self.stop_event.is_set():
                frame = cam.get_frame()
                if frame is None:
                    continue

                result_frame, success, lane_info = lane_origin.process_one_frame(
                    frame, plot=False, show_real_time=True
                )

                if success and lane_info:
                    pp = trajectory_follower.PurePursuit(
                        wheelbase=2.8,
                        lookahead_m=15.0,
                        ploty=lane_info.get("ploty"),
                        leftx=lane_info.get("leftx"),
                        rightx=lane_info.get("rightx"),
                        lefty=lane_info.get("lefty"),
                        righty=lane_info.get("righty"),
                        center_offset=lane_info.get("center_offset"),
                        YM_PER_PIX=lane_info.get("YM_PER_PIX", 7.0 / 400),
                        XM_PER_PIX=lane_info.get("XM_PER_PIX", 3.7 / 255),
                    )

                    # steer_deg = lane_info.get("steer_deg", 0.0)
                    steer_deg = pp.compute_turn_command()[1]

                    # --- Control Logic ---
                    base_speed = 150          # Base PWM speed
                    steering_gain = 1.5

                    steer_angle = 90 + steer_deg
                    steer_angle = max(40, min(140, steer_angle))

                    speed = base_speed - steering_gain * abs(steer_deg)
                    speed = max(130, min(200, speed))

                    # --- GPIOZero Method Calls ---
                    remote.car.Car_Run(int(speed))
                    remote.car.Ctrl_Servo(int(steer_angle))
                else:
                    remote.car.Car_Stop()

                # Optional: display processed frame
                # cv2.imshow("Auto Mode - Lane Detection", result_frame if result_frame is not None else frame)

                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    self.stop_event.set()
                    break

        finally:
            remote.car.Car_Stop()
            remote.car.Ctrl_Servo(90)
            cam.stop()
            time.sleep(0.2)
            cv2.destroyAllWindows()
            print("Auto mode finished.")

    # ------------------ Manual Mode ------------------
    def manual_mode(self):
        print("Manual mode starting...")
        control_thread = threading.Thread(target=self.run_remote_control, daemon=True)
        cam_thread = threading.Thread(target=self.run_cameras)

        control_thread.start()
        cam_thread.start()

        control_thread.join()
        cam_thread.join()
        print("Manual mode finished.")

    # ------------------ Start ------------------
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
