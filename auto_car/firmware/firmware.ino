#include "motor_control.h"
#include "servo_control.h"
#include "encoder.h"
#include "communication.h"

void setup() {
    Serial.begin(115200);  // Initialize UART
    motorSetup();          // Initialize motor pins
    servoSetup();          // Initialize servo
    encoderSetup();        // Set up encoder

    Serial.println("Arduino Ready");
}

void loop() {
    processSerialCommand();  // Handle UART commands
}
