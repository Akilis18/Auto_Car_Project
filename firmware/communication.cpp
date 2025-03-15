#include "communication.h"
#include "motor_control.h"
#include "servo_control.h"
#include "encoder.h"
#include <Arduino.h>

void processSerialCommand() {
    if (Serial.available()) {
        char command = Serial.read();

        switch (command) {
            case 'F':
                motorForward();
                break;
            case 'B':
                motorBackward();
                break;
            case 'Q':
                motorStop();
                break;
            case 'L':
                servoLeft();
                break;
            case 'R':
                servoRight();
                break;
            case 'C':
                servoCenter();
                break;
            case 'E':
                Serial.print("Encoder: ");
                Serial.println(getEncoderCount());
                break;
        }
    }
}
