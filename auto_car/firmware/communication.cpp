#include "communication.h"
#include "motor_control.h"
#include "servo_control.h"
#include "encoder.h"
#include <Arduino.h>

void processSerialCommand() {
    if (Serial.available()) {
        String input = Serial.readStringUntil('\n');
        input.trim();
        
        if (input.startsWith("SPEED:")) {
            int speedValue = input.substring(6).toInt();
            setMotorSpeed(speedValue);  // from motor_control.cpp
        }
        else if (input.startsWith("STEER:")) {
            int angle = input.substring(6).toInt();
            setServoAngle(angle);  // from servo_control.cpp
        }
        else if (input == "E") {
            long count = getEncoderCount();
            Serial.print("ENC:");
            Serial.print(count);
        }
    }
}
