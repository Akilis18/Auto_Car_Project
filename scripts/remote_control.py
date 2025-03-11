import curses
import serial_comm

serial_conn = serial_comm.SerialComm(port="/dev/ttyUSB0")

def main(stdscr):
    stdscr.clear()
    stdscr.addstr("Use W/A/S/D to move, Space to stop, Q to quit\n")
    stdscr.refresh()

    while True:
        key = stdscr.getch()  # Wait for key press
        if key == ord('w'):
            serial_conn.send_command("F")
        elif key == ord('s'):
            serial_conn.send_command("B")
        elif key == ord('a'):
            serial_conn.send_command("L")
        elif key == ord('d'):
            serial_conn.send_command("R")
        elif key == ord('x'):
            serial_conn.send_command("Q")
        elif key == ord('c'):
            serial_conn.send_command("C")
        elif key == ord('q'):  # Quit program
            break

curses.wrapper(main)
serial_conn.close()
