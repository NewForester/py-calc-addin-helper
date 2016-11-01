# py-calc-addin-helper
Helper scripts for creating and managing LibreOffice calc add-ins written in Python.

---

The bash script _liboaddon_ eases the installation &c of add-on packages for LibreOffice.
For more information try:

    liboaddon --help

The Python script _capp.py_ (calc add-in pre-processor) facilitates the generation
of a particular type of add-on called a calc add-in.  A calc add-in represents
one or more user defined functions that can be used in LibreOffice calc spreadsheets.

The _capp.py_ script is written in Python.
The original, Python 2, version was written in 2012 for use with LibreOffice 3.x.
The upgraded, Python 3, version was created in 2016 for use with LibreOffice 5.x.

The _capp.py_ script supports calc add-ins written in Python only.
It uses the DRY principle to generate three files required to package
a calc add-in directly from the Python source.

The _capp.py_ script was first written from notes provided with the 2009 _doobiedoo_ example by jan@biochemfusion.com.
The _doobiedoo_ example, adapted for use with _capp.py_, is provided as an example.

To package the example, try:

   liboaddon package doobiedoo python3/doobiedoo

The result should be a directory _doobiedoo_, which may be deleted, and the package _doobiedoo.oxt_.
The package may be installed with:

   liboaddon install doobiedoo.oxt

---

Correct generation of the add-on package places a number of requirements on the python source.
These are to be documented.

---

The _liboaddon_ script has only ever been used with LibreOffice versions installed using
Open Document Foundation deb packages.
Generation of the add-on package requires the LibreOffice SDK be installed.

The _liboaddon_ script has only ever been used under Linux.

It will select the correction version of _capp.py_ based on the version of LibreOffice installed
but it is presently unclear how it selects the correct version of Python.

The reliance on symbolic links is to be removed.

---

Copyright NewForester, 2012, 2016

except _doobiedoo.py_ Copyright jan@biochemfusion.com, 2009

---

Repository contents are provided as-is.
Validation is in progress.

    NewForester, October 2016.
