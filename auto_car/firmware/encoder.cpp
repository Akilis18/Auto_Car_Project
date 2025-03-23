#include "encoder.h"
#include <Arduino.h>

#define ENCODER_A 2
#define ENCODER_B 5

volatile int encoderCount = 0;

void encoderISR() {
    encoderCount++;
}

void encoderSetup() {
    pinMode(ENCODER_A, INPUT_PULLUP);
    pinMode(ENCODER_B, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(ENCODER_A), encoderISR, RISING);
}

int getEncoderCount() {
    int count = encoderCount;
    encoderCount = 0;  // Reset count after reading
    return count;
}
