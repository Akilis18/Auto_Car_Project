#include "encoder.h"
#include <Arduino.h>

#define ENCODER_A 2
#define ENCODER_B 4

volatile long encoderCount = 0;

void encoderISR() {
    bool a = digitalRead(ENCODER_A);
    bool b = digitalRead(ENCODER_B);
    
    if (a == b) {
        encoderCount++;     // Backward
    } else {
        encoderCount--;     // Backward
    }
}

void encoderSetup() {
    pinMode(ENCODER_A, INPUT_PULLUP);
    pinMode(ENCODER_B, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(ENCODER_A), encoderISR, RISING);
}

long getEncoderCount() {
    noInterrupts();
    long count = encoderCount;
    encoderCount = 0;  // Reset count after reading
    interrupts();
    return count;
}
