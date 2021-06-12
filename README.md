# LDBoxer

LDBoxer is a command-line utility originally designed by Tore Eriksson to help you replace LDraw parts that have no visible studs or tubes with simpler boxes. This saves rendering time and CPU power.

* Usage:  `LDBoxer_2018h.exe  ldraw_library_location  ldraw_model_location_for_conversion`
* Usage example:  `LDBoxer_2018h.exe  "F:\LDRAW"  "F:\LDraw\models\car.dat"`

Alternately, if you have Python installed on your system, you can execute the Python script directly.

* Usage example: `python3.exe  "E:\LDBoxer.py"  "F:\LDRAW"  "F:\LDraw\models\car.dat"`

Better yet, if you have pypy installed, you can substitute it for CPython and gain a very nice speed boost.

* Usage example: `pypy3.exe  "E:\LDBoxer.py"  "F:\LDRAW"  "F:\LDraw\models\car.dat"`

There is also an optional `-v` parameter which will print verbose information to the screen.

* Usage example: `pypy3.exe  "E:\LDBoxer.py"  "F:\LDRAW"  "F:\LDraw\models\car.dat" -v`

# Boxed Parts

1. Extract this archive and copy the contents of the "LDBoxer\boxes\parts" folder into your "LDraw\parts" folder.
1. Boxed parts need to go in the "LDraw\parts\b" folder. Boxed sub-parts need to go in the "LDraw\parts\s\b" folder.
1. Many "top" and "bottom" variants of boxed parts are missing, and still need to be created. Still, most of the most common parts have been modeled.
1. The spreadsheet "boxes_checklist.xlsx" was at one point used to keep track of which parts had box variants. This file may be outdated though, as I did not refer to it during my last round of editing.

# To Do

1. Some boxed parts may still have incorrect or missing back face culling (BFC) information. (I think I fixed all this recently.)
1. Some boxed parts may be missing edge and conditional lines and need to be corrected.
1. Need to create LGEO equivalents of all the boxed parts. However, I'm not sure how LDBoxer's sub-folder structure will behave in this context. We'll see.
1. Need to start adhering more closely (or at all) to [official parts header specifications](https://www.ldraw.org/article/398.html).
1. LDBoxer currently does not correctly process SNOT parts. Limited handling of SNOT parts should be possible in the future, however, if parts sharing the same SNOT orientation are all placed in the same sub-model.
1. LDBoxer does not understand MPD model/sub-model hierarchy. It assumes all models are inlined or flattened.
