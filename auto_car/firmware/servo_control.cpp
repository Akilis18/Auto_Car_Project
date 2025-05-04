#include "servo_control.h"
#include <Servo.h>
#include <Arduino.h>

#define SERVO_PIN 6         // PWM pin connected to the servo
#define WHEELBASE 15.0      // Distance between front and rear wheels (in cm)

// Servo settings
#define STEERING_CENTER 90      // Center position (straight)
#define MAX_STEERING_ANGLE 30    // Degrees left/right from center

Servo steeringServo;

// --- Initialization ---
void servoSetup() {
    steeringServo.attach(SERVO_PIN);
    servoCenter();
}

// --- Discrete manual control ---
void servoLeft() {
    steeringServo.write(STEERING_CENTER - MAX_STEERING_ANGLE);
}

void servoRight() {
    steeringServo.write(STEERING_CENTER + MAX_STEERING_ANGLE);
}

void servoCenter() {
    steeringServo.write(STEERING_CENTER);
}

// --- Real-time Pure Pursuit control from LOOK:x,y commands ---
void servoUpdate() {
    if (Serial.available()) {
        String input = Serial.readStringUntil('\n');
        input.trim();

        if (input.startsWith("LOOK:")) {
            input.remove(0, 5);  // Remove the prefix

            int commaIndex = input.indexOf(',');
            if (commaIndex != -1) {
                float lx = input.substring(0, commaIndex).toFloat();    // Lookahead X
                float ly = input.substring(commaIndex + 1).toFloat();   // Lookahead Y

                float steerAngle = computePurePursuitAngle(lx, ly);
                applySteering(steerAngle);
            }
        }
    }
}

// --- Pure Pursuit Calculation ---
float computePurePursuitAngle(float lx, float ly) {
    float L = WHEELBASE;
    float ld = sqrt(lx * lx + ly * ly);  // Lookahead distance

    if (ld == 0) return 0;

    float curvature = (2 * lx) / (ld * ld);
    float angleRad = atan(curvature * L);
    float angleDeg = angleRad * 180.0 / PI;

    Serial.print("Computed Steering Angle (deg): ");
    Serial.println(angleDeg);

    return angleDeg;
}

// --- Servo movement based on calculated steering angle ---
void applySteering(float angle) {
    angle = constrain(angle, -MAX_STEERING_ANGLE, MAX_STEERING_ANGLE);
    int servoPos = map(angle, -MAX_STEERING_ANGLE, MAX_STEERING_ANGLE,
                       STEERING_CENTER - MAX_STEERING_ANGLE,
                       STEERING_CENTER + MAX_STEERING_ANGLE);
    steeringServo.write(servoPos);
}
