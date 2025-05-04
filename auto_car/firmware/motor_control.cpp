#include "motor_control.h"
#include "encoder.h"
#include <Arduino.h>

#define MOTOR_A1A 10  // Motor driver input A-1A (PWM)
#define MOTOR_A1B 9   // Motor driver input A-1B (PWM)

// PID constants
#define KP 2.0        // Proportional constant
#define KI 0.1        // Integral constant
#define KD 1.0        // Derivative constant

// Variables for PID control
float currentSpeed = 0.0; // Measured speed
float previousError = 0.0;
float integral = 0.0;
unsigned long lastTime = 0; // Last time the encoder count was read
unsigned long interval = 100; // Interval to update motor speed (ms)

void motorSetup() {
    pinMode(MOTOR_A1A, OUTPUT);
    pinMode(MOTOR_A1B, OUTPUT);
}


// Function to calculate the PID control
float calculatePID(float target, float current) {
    unsigned long now = millis();
    float dt = (now - lastTime) / 1000.0;  // Convert ms to seconds

    if (dt <= 0.0) dt = 0.001; // prevent division by zero

    float error = target - current;

    integral += error * dt;  // Integrate over time
    float derivative = (error - previousError) / dt;  // Derivative over time

    float output = KP * error + KI * integral + KD * derivative;

    Serial.print("Computed PID output: ");
    Serial.println(output);

    previousError = error;
    lastTime = now;  // update lastTime for next dt

    return constrain(output, -255, 255);
}



void updateMotorSpeed() {
    static int previousEncoderCount = 0;
    unsigned long currentTime = millis();
    
    // If enough time has passed, update the speed
    if (currentTime - lastTime >= interval) {
        int encoderDelta = getEncoderCount();  // Get the encoder count
        currentSpeed = encoderDelta / (float)(currentTime - lastTime) * 1000.0;  // Speed in counts per second (convert to suitable unit)
        lastTime = currentTime;
        
        Serial.print("Current Speed: ");
        Serial.println(currentSpeed);  // For debugging purposes
    }
}


void motorForward(float targetSpeed) {
    float pidOutput = calculatePID(targetSpeed, currentSpeed);
    if (pidOutput < 0) {
        pidOutput *= -1;
    }
    // analogWrite(MOTOR_A1A, pidOutput);
    // analogWrite(MOTOR_A1A, 255);
    digitalWrite(MOTOR_A1A, HIGH);
    digitalWrite(MOTOR_A1B, LOW);
    Serial.println("Motor Forward");
}

void motorBackward(float targetSpeed) {
    float pidOutput = calculatePID(targetSpeed, currentSpeed);
    if (pidOutput > 0) {
        pidOutput *= -1;
    }
    digitalWrite(MOTOR_A1A, LOW);
    // analogWrite(MOTOR_A1B, -pidOutput);
    // analogWrite(MOTOR_A1B, 255);
    digitalWrite(MOTOR_A1B, HIGH);
    Serial.println("Motor Backward");
}

void motorStop() {
    digitalWrite(MOTOR_A1A, LOW);
    digitalWrite(MOTOR_A1B, LOW);
    Serial.println("Motor Stopped");
}
