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
            serial_conn.send_command("FORWARD")
        elif key == ord('s'):
            serial_conn.send_command("BACKWARD")
        elif key == ord('a'):
            serial_conn.send_command("LEFT")
        elif key == ord('d'):
            serial_conn.send_command("RIGHT")
        elif key == ord(' '):
            serial_conn.send_command("STOP")
        elif key == ord('q'):  # Quit program
            break

curses.wrapper(main)
serial_conn.close()
