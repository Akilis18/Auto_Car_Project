import serial
import time

class SerialComm:
    def __init__(self, port="/dev/ttyUSB0", baudrate=115200, timeout=1):
        try:
            self.ser = serial.Serial(port, baudrate, timeout=timeout)
            time.sleep(2)  # Give time for connection to establish
            print(f"Connected to {port} at {baudrate} baud.")
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            self.ser = None

    def send_command(self, command):
        """Send a command over UART."""
        if self.ser and self.ser.is_open:
            cmd_str = command.strip() + "\n"  # Ensure newline for Arduino parsing
            self.ser.write(cmd_str.encode("utf-8"))
            print(f"Sent: {cmd_str}")

    def receive_response(self):
        """Receive response from Arduino."""
        if self.ser and self.ser.is_open:
            try:
                response = self.ser.readline().decode("utf-8").strip()
                if response:
                    print(f"Received: {response}")
                    return response
            except Exception as e:
                print(f"Error reading from serial: {e}")
        return None

    def close(self):
        """Close the serial connection."""
        if self.ser:
            self.ser.close()
            print("Serial connection closed.")

# Test script (Run this only to test serial communication)
if __name__ == "__main__":
    serial_comm = SerialComm()
    serial_comm.send_command("TEST")
    response = serial_comm.receive_response()
    serial_comm.close()
