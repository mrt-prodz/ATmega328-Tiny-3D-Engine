#ifndef MESH_H
#define MESH_H

#define NODECOUNT 8
#define TRICOUNT 12

#define NODE(a, b) (long)(pgm_read_dword(&nodes[a][b]))
#define EDGE(a, b) pgm_read_byte(&faces[a][b])

const long nodes[NODECOUNT][3] PROGMEM = {
  {(long)(14.0*PRES), (long)(14.0*PRES), (long)(-14.0*PRES)},
  {(long)(14.0*PRES), (long)(-14.0*PRES), (long)(-14.0*PRES)},
  {(long)(-14.0*PRES), (long)(-14.0*PRES), (long)(-14.0*PRES)},
  {(long)(-14.0*PRES), (long)(14.0*PRES), (long)(-14.0*PRES)},
  {(long)(14.0*PRES), (long)(14.0*PRES), (long)(14.0*PRES)},
  {(long)(-14.0*PRES), (long)(14.0*PRES), (long)(14.0*PRES)},
  {(long)(-14.0*PRES), (long)(-14.0*PRES), (long)(14.0*PRES)},
  {(long)(14.0*PRES), (long)(-14.0*PRES), (long)(14.0*PRES)},
};

const unsigned char faces[TRICOUNT][3] PROGMEM = {
  {0, 1, 2},
  {2, 3, 0},
  {4, 5, 6},
  {6, 7, 4},
  {0, 4, 7},
  {7, 1, 0},
  {1, 7, 6},
  {6, 2, 1},
  {2, 6, 5},
  {5, 3, 2},
  {4, 0, 3},
  {3, 5, 4},
};

#endif // MESH_H
