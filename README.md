# LDBoxer

LDBoxer is a command-line utility originally designed by Tore Eriksson to help you replace LDraw parts that have no visible studs or tubes with simpler boxes. This saves rendering time and CPU power.

* Usage:  `LDBoxer_2017a.exe  ldraw_library_location  ldraw_model_location_for_conversion`
* Usage example:  `LDBoxer_2017a.exe  "F:\LDRAW"  "F:\LDraw\models\car.dat"`

Alternately, if you have Python installed on your system, you can execute the Python script directly.

* Usage example: `python.exe  "E:\LDBoxer.py"  "F:\LDRAW"  "F:\LDraw\models\car.dat"`

Better yet, if you have pypy installed, you can substitute it for CPython and gain a very nice speed boost.

* Usage example: `pypy.exe  "E:\LDBoxer.py"  "F:\LDRAW"  "F:\LDraw\models\car.dat"`

There is also an optional `-v` parameter which will print verbose information to the screen.

* Usage example: `pypy.exe  "E:\LDBoxer.py"  "F:\LDRAW"  "F:\LDraw\models\car.dat" -v`

# Boxed Parts

1. Boxed parts need to go in the "LDraw\parts\b" folder. Boxed primitives need to go in the "LDraw\parts\b\s" folder. Create these folders if they don't exist already.
1. Copy the Tore Eriksson's original boxed parts (inside the "boxes\b_tore" directory) into "LDraw\parts\b" first; then copy the newer boxed parts (in the "boxes\b_new" directory) into the same folder, replacing files when prompted to.
1. Many "top" and "bottom" versions of boxed parts are missing, and still need to be created. Still, most of the important ones have already been made.
1. I may have removed edge lines from several parts before I realized that that is not a good thing to do. I can't remember which parts I did this to, unfortunately. - MJH
1. The spreadsheet "boxes_checklist.xlsx" is used to keep track of all the boxed parts.
