// Using 3 axis accelerometer ADXL335 to rotate 3d mesh
//
// VCC 3.3v
// ANALOG PIN 0 - X Axis
// ANALOG PIN 1 - Y Axis
// ANALOG PIN 2 - Z Axis
//
#ifndef ACCELEROMETER_H
#define ACCELEROMETER_H

#define ACCEL_XPIN A0                              // x-axis of the accelerometer
#define ACCEL_YPIN A1                              // y-axis
#define ACCEL_ZPIN A2                              // z-axis (only on 3-axis models)
#define ACCEL_NUMREADINGS 10

struct {
  struct {
    int x[ACCEL_NUMREADINGS],
        y[ACCEL_NUMREADINGS],
        z[ACCEL_NUMREADINGS];
  } readings = {{0}, {0}, {0}};
  struct {
    unsigned char x, y, z;
  } index = {0, 0, 0};
  struct {
    int x, y, z;
  } total = {0, 0, 0};
} accel;

int accel_get_value(unsigned char *index, int *readings, int *total, int AXIS) {
  int average;
  *total -= readings[*index];
  readings[*index] = analogRead(AXIS);
  *total += readings[*index];
  average = (int)((*total / ACCEL_NUMREADINGS))%360;
  *index += 1;
  if (*index >= ACCEL_NUMREADINGS)
    *index = 0;
  return average;
}

#endif  // ACCELEROMETER_H
