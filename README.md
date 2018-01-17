# ATmega328 Tiny 3D Engine (Arduino UNO)
 
#### 3D model viewer made for the ATmega328 and Sainsmart 1.8" TFT screen (ST7735)

This is a tiny 3D engine made for the ATMEGA328 and a Sainsmart 1.8" TFT screen (ST7735).
It uses the amazingly fast Adafruit GFX library fork by XarkLabs: [github.com/XarkLabs](https://github.com/XarkLabs)

You can use the python script stl2h.py to convert STL models into header files and automatically import your meshes, just include the file and comment other mesh headers.

See stl2h.py help (./stl2h -h) for usage description.

```
Usage: ./stl2h.py -i <inputfile> -o <outputfile>
Convert a 3D mesh saved as STL format (ASCII) to header for Tiny 3D Engine.

  -i, --inputfile       3D mesh in STL file format
  -o, --outputfile      output filename of converted data
  -s, --scale           scale ratio (default 1.0)
  -n, --normals         save face normals
  -y, --yes             answer yes to all requests
  -v, --verbose         verbose output
```

Developed and tested with an Arduino UNO and a Sainsmart 1.8" TFT screen.

## Features:
* matrices for mesh transformations
* fixed point to avoid using floats
* 90 degrees fixed point look up table for sin/cos
* backface culling using shoelace algorithm
* flat colors (-unfinished/experimental/not fast enough-)
* rotate the mesh with a 3 axis accelerometer (ADXL335)
* rotate the mesh with a joystick thumb
* push button on digital PIN 2 to change the render type.

This is a project for the ATmega328 and ST7735, source will certainly need some tweaking to run on other components.

## Not implemented:
* clipping
* view/projection matrices (projection is done on world matrix directly)
* hidden surface removal

## Dependencies:
* [XarkLabs PDQ_GFX_Libs](https://github.com/XarkLabs/PDQ_GFX_Libs)

## Video:
[![Preview of Tiny 3D Engine on YouTube](http://img.youtube.com/vi/8nZam2jpIqw/0.jpg)](https://youtu.be/8nZam2jpIqw)

## Screenshot:
![Screenshot](https://raw.githubusercontent.com/mrt-prodz/ATmega328-Tiny-3D-Engine/master/screenshot.jpg)

## References:
[Wiring](http://www.tweaking4all.com/hardware/arduino/sainsmart-arduino-color-display)

[Game Loop](http://www.koonsolo.com/news/dewitters-gameloop)

[Peter Collingridge 3D graphics tutorial](http://petercollingridge.appspot.com/3D-tutorial)

[J-Snake Fixed Point Arithmetic](http://forums.tigsource.com/index.php?topic=35880.0)

[Math Open References](http://www.mathopenref.com/coordpolygonarea.html)

[World, View and Projection Transformation Matrices](http://www.codinglabs.net/article_world_view_projection_matrix.aspx)
