#include "communication.h"
#include "motor_control.h"
#include "servo_control.h"
#include "encoder.h"
#include <Arduino.h>

void processSerialCommand() {
    if (Serial.available()) {
        // Get command
        String command = Serial.readString();
        char cmd = command.charAt(0);

        if (cmd == 'F' || cmd == 'B' || cmd == 'Q') {
            int delimiterIdx = command.indexOf(',');

            String speedStr = command.substring(delimiterIdx + 1); // Get speed value
            float carSpeed = speedStr.toFloat();

            if (cmd == 'F') {
                motorForward(carSpeed);
            }
            else if (cmd == 'B') {
                motorBackward(carSpeed);
            }
            else {
                motorStop();
            }
        }
        else {
            switch (cmd) {
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
}
