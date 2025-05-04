import curses
import serial_comm

class RemoteControl:
    def __init__(self, port="/dev/ttyUSB0", baudrate=115200):
        self.serial_conn = serial_comm.SerialComm(port=port, baudrate=baudrate)
        self.speed = 0.0
        self.speed_step = 0.1

    def send_command(self, command):
        self.serial_conn.send_command(command)

    def close_connection(self):
        self.serial_conn.close()

    def start(self):
        curses.wrapper(self.run)

    def run(self, stdscr):
        stdscr.clear()
        stdscr.addstr("Use W/A/S/D to move, Space to stop, Q to quit\n")
        stdscr.refresh()

        while True:
            key = stdscr.getch()  # Wait for key press
            if key == ord('w'):
                self.speed = min(self.speed + self.speed_step, 1.0)
                self.send_command(f"F,{self.speed}")
            elif key == ord('s'):
                self.speed = max(self.speed - self.speed_step, -1.0)
                self.send_command(f"B,{self.speed}")
            elif key == ord('a'):
                self.send_command("L")
            elif key == ord('d'):
                self.send_command("R")
            elif key == ord('x'):
                self.speed = 0.0
                self.send_command(f"Q,{self.speed}")
            elif key == ord('c'):
                self.send_command("C")
            elif key == ord('e'):
                self.send_command("E")
            elif key == ord('q'):  # Quit program
                break

        self.close_connection()
