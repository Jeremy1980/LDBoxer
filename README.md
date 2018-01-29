# LDBoxer

A command-line utility to help you replace LDraw parts with no visible studs or tubes with boxes. 
Saves rendering time and CPU power.

Usage:  `LDBoxer_2017a.exe  ldraw_library_location  ldraw_model_location_for_conversion`

Usage example:  `LDBoxer_2017a.exe  "F:\LDRAW"  "F:\LDraw\models\car.dat"`

Alternately, if you have Python installed on your system, you can execute the Python script directly.

Usage example: `python.exe  "E:\LDBoxer.py"  "F:\LDRAW"  "F:\LDraw\models\car.dat"`

Better yet, if you have pypy installed, you can substitute it for CPython and gain a very nice speed boost.

Usage example: `pypy.exe  "E:\LDBoxer.py"  "F:\LDRAW"  "F:\LDraw\models\car.dat"`

There is also an optional `-v` parameter which will print verbose information to the screen.

Usage example: `pypy.exe  "E:\LDBoxer.py"  "F:\LDRAW"  "F:\LDraw\models\car.dat" -v`
