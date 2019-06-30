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

1. Extract this archive and copy the contents of the "LDBoxer\boxes\parts" folder into your "LDraw\parts" folder, replacing and overwriting files when prompted.
1. Boxed parts need to go in the "LDraw\parts\b" folder. Boxed sub-parts need to go in the "LDraw\parts\s\b" folder.
1. Many "top" and "bottom" versions of boxed parts are missing, and still need to be created. Still, most of the important parts are finished.
1. The spreadsheet "boxes_checklist.xlsx" is used to keep track of all the boxed parts.
1. LDBoxer currently cannot process any SNOT parts. Limited handling of SNOT parts may be added in the future.
1. Note that many boxed parts still have incorrect or missing back face culling (BFC) information, and need to be fixed/updated. They throw quite a few other errors in LDView, too.
