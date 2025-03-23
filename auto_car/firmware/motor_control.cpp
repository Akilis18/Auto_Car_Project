#include "motor_control.h"
#include <Arduino.h>

#define MOTOR_A1A 10  // Motor driver input A-1A (PWM)
#define MOTOR_A1B 9   // Motor driver input A-1B (PWM)

void motorSetup() {
    pinMode(MOTOR_A1A, OUTPUT);
    pinMode(MOTOR_A1B, OUTPUT);
}

void motorForward() {
    digitalWrite(MOTOR_A1A, HIGH);
    digitalWrite(MOTOR_A1B, LOW);
    Serial.println("Motor Forward");
}

void motorBackward() {
    digitalWrite(MOTOR_A1A, LOW);
    digitalWrite(MOTOR_A1B, HIGH);
    Serial.println("Motor Backward");
}

void motorStop() {
    digitalWrite(MOTOR_A1A, LOW);
    digitalWrite(MOTOR_A1B, LOW);
    Serial.println("Motor Stopped");
}
