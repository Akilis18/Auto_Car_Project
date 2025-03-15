#include "servo_control.h"
#include <Servo.h>
#include <Arduino.h>

#define SERVO_PIN 6

Servo myServo;

void servoSetup() {
    myServo.attach(SERVO_PIN);
    myServo.write(90);
}

void servoLeft() {
    myServo.write(45);
    Serial.println("Servo Left");
}

void servoRight() {
    myServo.write(135);
    Serial.println("Servo Right");
}

void servoCenter() {
    myServo.write(90);
    Serial.println("Servo Center");
}
