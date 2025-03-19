#include<RPLidar.h>

RPLidar lidar;

#define RPLIDAR_MOTOR 3

void setup() {
  // put your setup code here, to run once:
  lidar.begin(Serial);

  pinMode(RPLIDAR_MOTOR, OUTPUT);

}

void loop() {
  if (IS_OK(lidar.waitPoint())){
    float distance = lidar.getCurrentPoint().distance;
    float angle = lidar.getCurrentPoint().angle;
    bool startBit = lidar.getCurrentPoint().startBit;
    byte quality = lidar.getCurrentPoint().quality;

    SerialUSB.print("dist: ");
    SerialUSB.print(distance);
    SerialUSB.print("\tangle: ");
    SerialUSB.print(angle);
    SerialUSB.print("\tstarBit: ");
    SerialUSB.print(startBit);
    SerialUSB.print("\tquality: ");
    SerialUSB.print(quality);

  } else{
    analogWrite(RPLIDAR_MOTOR, 0);
    
    rplidar_response_device_into_t info;
    if (IS_OK(lidar.getDeviceInfo(info, 100))){
      lidar.startScan();

      analogWrite(RPLIDAR_MOTOR, 255);
      delay(1000);
    }
  }
  // put your main code here, to run repeatedly:

}
