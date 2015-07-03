1. What this code can do?
It can be used for script file translation, .gim image opening and .pak file reading and saving (if it contained text data). ROM patch is also included.

2. What this code can't do?
Generate fonts (BDH's DR1 font generator was used), pack/unpack .cpk, sync translation between many people... Well, it lacks many features.

3. How to use it?
Simple way - translating string from script:
a) File -> Check progress -> Open one of the files
b) Go down by the left column (script actions) until you will see the line you need printed in three edit fields on the right side. Use pictures as a reference
c) Translate it. The common rule is that char count should stop at ~90, but it depends on char width, situation, font, etc.
d) Save file

Harded - need to add one more string (aka string too long):
a) All the same as a simple case a) to c)
b) After translating the first part go to the "Strings" tab and press "Add string"
c) Add the new string, click ok and _remember_ the string number.
d) Check what actions whould you need from the main string. Usually it goes between get_line_idx and print_line, sometimes clt aka "colored text" are added.
e) Using "ADD OP" button add all the operations you need (like get_line_idx with the string number, print_lines, etc). Note: print_line is somewhere in the end of the list.
f) Check line length, add one more line (print_line) if needed.
g) Save

Bulk translation way:
a) Go to "Strings" tab
b) Find the first line of the part you want to translate
c) Copy-paste-set-copy-paste-set...

4. Why was it made this hard to use?
This code targets lower level than a standard translation IDE. You can even create a whole new script here if you want (and if you have time). It helps a bit, e.g. i've added some effects where i think they needed to be, etc. 
In short, it's a script editor, not a translation tool.

5. Why there is no backgrounds?
I'm too lazy to reverse .p3d and to create a real 3D scene, i'm only grabbing textures from those.
