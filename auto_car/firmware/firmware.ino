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
    long count = getEncoderCount();
    Serial.println(count);
    Serial.println(((count*60)/11.0)/78.0);
    delay(1000);
}
