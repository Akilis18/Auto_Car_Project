import curses
import serial
import time

class RemoteControl:
    def __init__(self, port="/dev/ttyUSB0", baudrate=115200):
        self.serial_conn = serial.Serial(port=port, baudrate=baudrate, timeout=1)
        time.sleep(2)  # Give time for Arduino to reset

    def send_command(self, command):
        if self.serial_conn.is_open:
            self.serial_conn.write((command + '\n').encode('utf-8'))

    def close_connection(self):
        if self.serial_conn.is_open:
            self.serial_conn.close()

    def start(self):
        curses.wrapper(self.run)

    def run(self, stdscr):
        stdscr.clear()
        stdscr.addstr("Use W/A/S/D to move, Space to stop, Q to quit\n")
        stdscr.refresh()

        while True:
            key = stdscr.getch()
            stdscr.addstr(2, 0, f"Key pressed: {chr(key) if key != -1 else 'None'}      ")  # show key
            stdscr.refresh()

            if key == ord('w'):
                self.send_command("SPEED:255")
            elif key == ord('s'):
                self.send_command("SPEED:-180")
            elif key == ord('a'):
                self.send_command("STEER:60")
            elif key == ord('d'):
                self.send_command("STEER:120")
            elif key == ord('x'):
                self.send_command("SPEED:0")
            elif key == ord('c'):
                self.send_command("STEER:90")
            elif key == ord('e'):
                self.send_command("E")
            elif key == ord('q'):
                break

        self.close_connection()

if __name__ == "__main__":
    remote_control = RemoteControl()
    remote_control.start()
