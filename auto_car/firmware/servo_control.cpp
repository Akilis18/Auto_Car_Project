#include "servo_control.h"
#include <Servo.h>
#include <Arduino.h>

#define SERVO_PIN 6         // PWM pin connected to the servo

Servo steeringServo;

// --- Initialization ---
void servoSetup() {
    steeringServo.attach(SERVO_PIN);
    steeringServo.write(90);
}

void setServoAngle(int angle) {
    steeringServo.write(angle);
}
