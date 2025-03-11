#include <Servo.h>

#define MOTOR_A1A 10  // Motor driver input A-1A (PWM)
#define MOTOR_A1B 9   // Motor driver input A-1B (PWM)
#define ENCODER_A 2   // Hall encoder signal A (Interrupt 0)
#define ENCODER_B 5   // Hall encoder signal B (Optional)
#define SERVO_PIN 6   // Servo motor control

Servo myServo;                  // Create servo object
volatile int encoderCount = 0;   // Counter for encoder pulses

void encoderISR() {
  encoderCount++;  // Increment on each pulse
}

void setup() {
  Serial.begin(115200);  // UART communication
  pinMode(MOTOR_A1A, OUTPUT);
  pinMode(MOTOR_A1B, OUTPUT);
  pinMode(ENCODER_A, INPUT_PULLUP);
  pinMode(ENCODER_B, INPUT_PULLUP);

  attachInterrupt(digitalPinToInterrupt(ENCODER_A), encoderISR, RISING);

  myServo.attach(SERVO_PIN);  // Attach the servo
  myServo.write(90);          // Set servo to neutral position (90°)

  Serial.println("Arduino Ready");
}

void loop() {
  if (Serial.available()) {
    char command = Serial.read();

    switch (command) {
      case 'F':  // Move motor forward
        digitalWrite(MOTOR_A1A, HIGH);
        digitalWrite(MOTOR_A1B, LOW);
        Serial.println("Motor Forward");
        break;

      case 'B':  // Move motor backward
        digitalWrite(MOTOR_A1A, LOW);
        digitalWrite(MOTOR_A1B, HIGH);
        Serial.println("Motor Backward");
        break;

      case 'Q':  // Stop motor
        digitalWrite(MOTOR_A1A, LOW);
        digitalWrite(MOTOR_A1B, LOW);
        Serial.println("Motor Stopped");
        break;

      case 'L':  // Turn servo left
        myServo.write(45);
        Serial.println("Servo Left");
        break;

      case 'R':  // Turn servo right
        myServo.write(135);
        Serial.println("Servo Right");
        break;

      case 'C':  // Center servo
        myServo.write(90);
        Serial.println("Servo Center");
        break;

      case 'E':  // Send encoder count
        Serial.print("Encoder: ");
        Serial.println(encoderCount);
        encoderCount = 0;  // Reset counter
        break;
    }
  }
}