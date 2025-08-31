import curses
import serial
import time
import os
import sys

# Ensure the firmware directory is always on sys.path, regardless of current working directory
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
FIRMWARE_DIR = os.path.abspath(os.path.join(CURRENT_DIR, "../firmware"))
if FIRMWARE_DIR not in sys.path:
    sys.path.insert(0, FIRMWARE_DIR)

from RPI_car import RPI_GPIO_Car  # Adjusted import to match the class name

class RemoteControl:
    def __init__(self):
        self.car = RPI_GPIO_Car()
        self.car.Car_Stop()
        self.car.Ctrl_Servo(90)  # Center steering

    def start(self):
        curses.wrapper(self.run)

    def run(self, stdscr):
        stdscr.clear()
        stdscr.addstr("Use W/A/S/D to move, Space to stop, Q to quit\n")
        stdscr.refresh()

        while True:
            key = stdscr.getch()
            stdscr.addstr(2, 0, f"Key pressed: {chr(key) if key != -1 else 'None'}      ")
            stdscr.refresh()

            if key == ord('w'):
                self.car.Car_Run(255)  # Move forward at 50% speed
            elif key == ord('s'):
                self.car.Car_Back(150)
            elif key == ord('a'):
                self.car.Ctrl_Servo(50)  # Turn left
            elif key == ord('d'):
                self.car.Ctrl_Servo(130)
            elif key == ord('x'):
                self.car.Car_Stop()
            elif key == ord('c'):
                self.car.Ctrl_Servo(90)  # Center steering
            elif key == ord('q'):
                break

if __name__ == "__main__":
    remote_control = RemoteControl()
    remote_control.start()
