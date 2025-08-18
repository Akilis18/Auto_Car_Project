#include "motor_control.h"
#include "encoder.h"
#include <Arduino.h>

#define MOTOR_A 8
#define MOTOR_B 9
#define MOTOR_PWM 5

void motorSetup() {
    pinMode(MOTOR_A, OUTPUT);
    pinMode(MOTOR_B, OUTPUT);
}

void setMotorSpeed(int speed) {
    if (speed > 0) {
        motorForward(speed);  // You must implement PWM version
    } else if (speed < 0) {
        motorBackward(-speed);
    } else {
        motorStop();
    }
}

void motorForward(int speed) {
    analogWrite(MOTOR_PWM, speed);
    digitalWrite(MOTOR_A, HIGH);
    digitalWrite(MOTOR_B, LOW);
    Serial.println("Motor Forward");
}

void motorBackward(int speed) {
    analogWrite(MOTOR_PWM, speed);
    digitalWrite(MOTOR_A, LOW);
    digitalWrite(MOTOR_B, HIGH);
    Serial.println("Motor Backward");
}

void motorStop() {
    analogWrite(MOTOR_PWM, 0);
    Serial.println("Motor Stopped");
}
