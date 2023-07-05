# Library Managing System

This is a simple, open-source implementation of a managing application for small libraries, built with Python and GTK3+. It does not use DBMS such as SQL, but depends on importing/exporting JSON files to/from Gtk.TreeModel objects, and synchronizes the data during import.

## Installation
The following prerequistes need to be met first:

1- Python 3.7

2- PyGObject (and it will be accompanied automatically with Gtk3)

3- Pandas

After that, launching the application will be a peace of cake.
First, follow [the docs of PyGObject](https://pygobject.readthedocs.io/en/latest/getting_started.html#windows-getting-started) (except the GTK4 part) and that should install PyGObject.
Just a few notes:

For windows users: when using mysys2, make sure to use the `mingw-w64-x86_64` packages (these are the ones that did not cause issues on the windows machine during compilation).

For MacOS: there is currently no mac-compiled version (since I am compiling using pyinstaller), but some of the issues which Mac users would come across would be:

1- `note: This error originates from a subprocess, and is likely not a problem with pip.` This error seems to be fixed through....

2- `Namespace GTK not available` even though `import gi` works
