#include <Wire.h>

const int MPU_ADDR = 0x68;
const int BUTTON_CLICK = 2;
const int BUTTON_TOGGLE = 3;

int16_t accel_x, accel_y, accel_z;
int16_t temperature;
int16_t gyro_x, gyro_y, gyro_z;
  
void setup() {
  Serial.begin(9600);
  Wire.begin();

  pinMode(BUTTON_CLICK, INPUT_PULLUP);
  pinMode(BUTTON_TOGGLE, INPUT_PULLUP);

  // Wake up the MPU6050
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x6B);
  Wire.write(0);
  Wire.endTransmission(true);

  delay(100);
}

void loop() {
  Wire.beginTransmission(MPU_ADDR);
  Wire.write(0x3B);
  Wire.endTransmission(false);

  byte count = Wire.requestFrom(MPU_ADDR, 14, true);

  if (count == 14) {
    accel_x = (int16_t)(Wire.read() << 8 | Wire.read());
    accel_y = (int16_t)(Wire.read() << 8 | Wire.read());
    accel_z = (int16_t)(Wire.read() << 8 | Wire.read());

    temperature = (int16_t)(Wire.read() << 8 | Wire.read());

    gyro_x = (int16_t)(Wire.read() << 8 | Wire.read());
    gyro_y = (int16_t)(Wire.read() << 8 | Wire.read());
    gyro_z = (int16_t)(Wire.read() << 8 | Wire.read());

    int clickState = digitalRead(BUTTON_CLICK);
    int toggleState = digitalRead(BUTTON_TOGGLE);

    // Format: accel_x,accel_y,clickState,toggleState
    Serial.print(accel_x);
    Serial.print(",");
    Serial.print(accel_y);
    Serial.print(",");
    Serial.print(clickState);
    Serial.print(",");
    Serial.println(toggleState);
  }

  delay(20);
}