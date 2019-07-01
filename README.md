# Python exercises

These are some small exercises from the python course I am studying - Check it out at [Píldoras informáticas][pycurso] (by Juan Díaz). I will be uploading my programs here until I complete it. This is also my first time using git!

Exercises are divided into folders:
- [CALC](#calc) - Basic calculator using Tkinter.
- [CRUD_GUI](#crud-gui) - CRUD app using Tkinter and SQLite3.

---

## Calc
This is a calculator that let us do some basic aritmethic operations. Tkinter library was used for the GUI. Decimal format: 3,14.

![calc][imgcalc]

---

## Crud Gui
This is an application that let us Create, Read, Update and Delete (CRUD) info from different users in a local database. Tkinter was used for the GUI, sqlite3 to work with the SQLite database, and passlib for hashing passwords. SQLite queries are parameterized to improve security, and the OS library was used for compatibility between Windows-UNIX systems.

![crud_gui][imgcrud_gui]

[pycurso]: https://www.youtube.com/playlist?list=PLU8oAlHdN5BlvPxziopYZRd55pdqFwkeS
[imgcalc]: media/calc.png
[imgcrud_gui]: media/crud-gui.png
