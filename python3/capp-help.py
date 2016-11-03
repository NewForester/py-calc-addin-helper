# -*- coding: utf-8 -*-
'''
description of the capp.py script's expectations of calc add-in Python source

The capp.py script may used during the packaging of LibreOffice calc add-in
functions written in Python.

The packaging process not only requires the Python source but also:

  - the xml description of the add-in component
  - the xcu description of the add-in's configuration
  - the idl description of the add-in's interface

The capp.py script generates these from the Python source.  It is an example
of the DRY principle.

The script assumes the Python source contains the necessary information and
that it can find this information using simple regular expressions.  It does
not complain if it cannot find information.

Ensuring the Python source does contain the necessary information and that it
can be found is described below.  This is not an onerous task.

Much of the information is taken from module and method descriptions; the rest
from lines that have to appear in the Python source anyway.

The script writes to standard output and so can generate the contents of only
one file with each invocation.  Eg:

    capp idl <module_name> <source_file> > X<module_name>.idl
    capp xcu <module_name> <source_file> > <module_name>.xcu
    capp xml <module_name> <source_file> > description.xml

The <module_name> is the case sensitive name of the Python class defined in
the source file that contains the add-in functions.  Any other classes are
ignored.

See doobiedoo.py for a Python add-in example adapted for the capp.py script.

Note: what follows is not a description of how to write a Python add-in but
a description of how to ensure a Python add-in may be used with capp.py.


The UNO Interface Name and Module Id
------------------------------------

The UNO interface name is X<module_name>.

The script expects to find an import statement of the form:

  from <uno-module-id> import <uno-interface-name>

Python cannot make sense of this statement except within the UNO-Python context.


UNO Component Id
----------------

This is similar to, but not the same as the UNO module id.

This is taken from the line:

  unoComponentId = "<uno-component-id>"

Class Signature
---------------

The script expects to find a Python class declaration of the form:

  class <module-name> (unohelper.Base, <uno-interface-name>):

The add-in functions are implemented as methods of this class.

The script is single pass.  It expects to find the UNO interface name and
module id first, then the UNO component id and then the class signature.
Unless they are all present in this order the script will generate no output.

Method Name and Description
---------------------------

Class methods with names that begin with '_' are ignored.
All others are assumed to be add-in functions to be called from calc.

Such methods are expected to have their signature on a single line followed by
a multi-line description.  The method name is taken from the signature and the
method description from the first line of the multi-line description.

The method name and description are used in the LibreOffice calc UI to
document the method.

Parameter Names and Descriptions
---------------------------------

The parameter names are taken from a method's signature and parameter
descriptions from the method's multi-line description.

Each parameter description is a single line of the form:

  name - description

The parameter names and descriptions are also used in the LibreOffice calc UI
to document the method.

IDL Signature
-------------

IDL signature is required for each add-in function.  It is used by LibreOffice
calc to call the function.  It cannot be deduced from the Python source.

The script expects the signature to appear in the Python method's multi-line
description in a line of the form:

     idl: <idl-signature>

Such signatures are copied to the IDL file verbatim and must be terminated
with a semi-colon.

Display Name
------------

The Python source file is expected to have a multi-line module description at
its head.  The display name is the first line of this description.

Module Version, Publisher Name and Publisher Link
-------------------------------------------------

The script looks for these in the multi-line module description and takes them
from lines of the form:

  moduleVersion = <module-version>
  publisherName = <publisher-name>
  publisherLink = <publisher-link>

The publisher name and link are the author's name and web-address.
'''

'''
    Copyright (C) 2012, 2016, NewForester
    Released under the terms of the GNU GPL v2
'''

# EOF
