// Using thumb joystick to rotate 3d mesh
//
// VCC 5v
// DIGITAL PIN 2 - change render type
// ANALOG  PIN 0 - X Axis
// ANALOG  PIN 1 - Y Axis
//

#ifndef JOYSTICK_H
#define JOYSTICK_H

#define JOYSTICK_XPIN A0                              // x-axis of the joystick
#define JOYSTICK_YPIN A1                              // y-axis
#define JOYSTICK_NUMREADINGS 10

struct {
  struct {
    int x[JOYSTICK_NUMREADINGS],
        y[JOYSTICK_NUMREADINGS];
  } readings = {{0}, {0}};
  struct {
    unsigned char x, y;
  } index = {0, 0};
  struct {
    int x, y;
  } total = {0, 0};
} joystick;

int joystick_get_value(unsigned char *index, int *readings, int *total, int AXIS) {
  int average;
  *total -= readings[*index];
  readings[*index] = analogRead(AXIS);
  *total += readings[*index];
  average = (int)((*total / JOYSTICK_NUMREADINGS)*0.35)%360;
  *index += 1;
  if (*index >= JOYSTICK_NUMREADINGS)
    *index = 0;
  return average;
}

#endif  // JOYSTICK_H
