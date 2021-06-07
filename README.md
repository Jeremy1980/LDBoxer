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

1. Extract this archive and copy the contents of the "LDBoxer\boxes\parts" folder into your "LDraw\parts" folder, replacing and overwriting any files when prompted.
1. Boxed parts need to go in the "LDraw\parts\b" folder. Boxed sub-parts need to go in the "LDraw\parts\s\b" folder.
1. Many "top" and "bottom" variants of boxed parts are missing, and still need to be created. Still, most of the important parts have been modeled.
1. The spreadsheet "boxes_checklist.xlsx" is used to keep track of all the parts that have box variants.

# To Do

1. Many boxed parts still have incorrect or missing back face culling (BFC) information.
1. IIRC, many boxed parts are missing edge and conditional lines and need to be corrected.
1. Need to create LGEO equivalents of all the boxed parts. However, I'm not sure how LDBoxer's sub-folder structure will work in this context. We'll see.
1. Need to start adhering more closely (or at all) to [official parts header specifications](https://www.ldraw.org/article/398.html).
1. LDBoxer currently does not correctly process SNOT parts. Limited handling of SNOT parts may be possible in the future.
1. LDBoxer does not understand MPD model/sub-model hieracrhy. It assumes all models are inlined without any heirarchy.
1. Performance in LDView seems to actually be slower when using boxed parts than when using regular parts for some reason. Is this due to the lack of BFC or edge lines in some parts? I dunno.
