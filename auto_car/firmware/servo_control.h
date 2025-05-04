#ifndef SERVO_CONTROL_H
#define SERVO_CONTROL_H

void servoSetup();
void servoLeft();
void servoRight();
void servoCenter();

void servoUpdate();  // New: Check for LOOK:x,y commands and steer dynamically

float computePurePursuitAngle(float lx, float ly);
void applySteering(float angle);

#endif
