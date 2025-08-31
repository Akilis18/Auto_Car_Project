from gpiozero import PWMOutputDevice, DigitalOutputDevice, Servo, Button
from time import sleep
import math

class RPI_GPIO_Car:
    def __init__(self):
        # --- DC Motor Pins ---
        self.motor_en = PWMOutputDevice(18)  # ENA (PWM)
        self.motor_in1 = DigitalOutputDevice(23)  # IN1
        self.motor_in2 = DigitalOutputDevice(24)  # IN2

        # --- Servo Motor Pin ---
        self.servo = Servo(19, min_pulse_width=0.0005, max_pulse_width=0.0025, frame_width=0.02)  # GPIO 19, range -1 to 1 internally

        # --- Encoder Pin ---
        self.encoder_a = Button(17)  # Simple counter on rising edge
        self.encoder_count = 0
        self.encoder_a.when_pressed = self._increment_encoder

    # --- Encoder Callback ---
    def _increment_encoder(self):
        self.encoder_count += 1

    def read_encoder(self):
        return self.encoder_count

    # --- DC Motor Control ---
    def Ctrl_Car(self, direction, speed):
        """
        direction: 1 = forward, 0 = backward
        speed: 0-255 PWM
        """
        pwm_value = max(0, min(255, speed)) / 255.0  # Normalize 0-1 for PWMOutputDevice

        self.motor_en.value = pwm_value

        if direction == 1:
            self.motor_in1.on()
            self.motor_in2.off()
        else:
            self.motor_in1.off()
            self.motor_in2.on()

    def Car_Run(self, speed):
        self.Ctrl_Car(0, speed)

    def Car_Back(self, speed):
        self.Ctrl_Car(1, speed)

    def Car_Stop(self):
        self.motor_en.value = 0
        self.motor_in1.off()
        self.motor_in2.off()

    # --- Servo Control ---
    def Ctrl_Servo(self, angle):
        """
        angle: 0-180 degrees
        GPIOZero Servo uses -1 (0 deg) to 1 (180 deg)
        """
        angle = max(0, min(180, angle))
        normalized = (angle / 90.0) - 1  # Map 0-180 -> -1 to 1
        self.servo.value = normalized

    # --- Optional helper ---
    def reset(self):
        self.Car_Stop()
        self.Ctrl_Servo(90)
        self.encoder_count = 0
