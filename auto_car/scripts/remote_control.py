import curses
import serial_comm

class RemoteControl:
    def __init__(self, port="/dev/ttyUSB0", baudrate=115200):
        self.serial_conn = serial_comm.SerialComm(port=port, baudrate=baudrate)

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
                self.send_command("F")
            elif key == ord('s'):
                self.send_command("B")
            elif key == ord('a'):
                self.send_command("L")
            elif key == ord('d'):
                self.send_command("R")
            elif key == ord('x'):
                self.send_command("Q")
            elif key == ord('c'):
                self.send_command("C")
            elif key == ord('q'):  # Quit program
                break

        self.close_connection()
