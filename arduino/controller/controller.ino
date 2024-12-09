#include <AFMotor.h> // Adafruit Motor Shield library

// Initialize motors
AF_DCMotor motor1(1, MOTOR12_1KHZ); // Gripper motor M1
AF_DCMotor motor2(2, MOTOR12_1KHZ); // Base rotation motor M5 (Theta 1)
AF_DCMotor motor3(3, MOTOR34_1KHZ); // Elbow motor M3 (Theta 3)
AF_DCMotor motor4(4, MOTOR34_1KHZ); // Shoulder motor M4 (Theta 2)

float BaseTime, ShoulderTime, ElbowTime;
String gripperOrientation = "";

void setup() {
  Serial.begin(9600); // Communication with Python script
  motor1.setSpeed(255); // Max speed for all motors
  motor2.setSpeed(255);
  motor3.setSpeed(255);
  motor4.setSpeed(255);
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    parseData(data);
    executeMovements();
  }
}

void parseData(String data) {
  int firstComma = data.indexOf(',');
  int secondComma = data.indexOf(',', firstComma + 1);
  int thirdComma = data.indexOf(',', secondComma + 1);

  BaseTime = data.substring(0, firstComma).toFloat(); // In milliseconds
  ShoulderTime = data.substring(firstComma + 1, secondComma).toFloat();
  ElbowTime = data.substring(secondComma + 1).toFloat();
  gripperOrientation = data.substring(thirdComma + 1);
  
}

void executeMovements() {
  // Base rotation (Theta1)
  motor2.run(BACKWARD);
  delay(BaseTime);
  motor2.run(RELEASE);

  // Shoulder movement (Theta2)
  motor4.run(FORWARD);
  delay(ShoulderTime);
  motor4.run(RELEASE);

  // Elbow movement (Theta3)
  motor3.run(BACKWARD);
  delay(ElbowTime/3);
  motor3.run(RELEASE);

  // Gripper action (hardcoded for now)
  //motor1.run(FORWARD);
  //delay(1000); // Close gripper
  //motor1.run(RELEASE);

  // Gripper action: Move gripper based on orientation (open or close)
  //if (gripperOrientation == "open") {
    //motor1.run(FORWARD);  // Move gripper forward (open)
    //delay(2000);  // Adjust the delay as needed for your gripper action
    //motor1.run(RELEASE);
    //
  //} 
  //else if (gripperOrientation == "close") {
    //motor1.run(BACKWARD);  // Move gripper backward (close)
    //delay(2000);  // Adjust the delay as needed for your gripper action
    //motor1.run(RELEASE);
    //
  //} 
  //else {
    // Handle invalid gripper orientation (optional)
   // Serial.println("Invalid gripper orientation received");
  //}

  
  // back to original 

    // Elbow movement (Theta3)
  motor3.run(FORWARD);
  delay(ElbowTime/3);
  motor3.run(RELEASE);

  // Shoulder movement (Theta2)
  motor4.run(BACKWARD);
  delay(ShoulderTime);
  motor4.run(RELEASE);

  // Base rotation (Theta1)
  motor2.run(FORWARD);
  delay(BaseTime);
  motor2.run(RELEASE);
  
    //Gripper action (hardcoded for now)
  //motor1.run(FORWARD);
  //delay(1000); // open gripper
  //motor1.run(RELEASE);
}



