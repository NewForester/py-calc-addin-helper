# -*- coding: utf-8 -*-
'''
The doobie-tastic Add-In example.

# DoobieDoo OOo Calc Add-in implementation.
# Created by jan@biochemfusion.com April 2009.
# Adapted by pbr@custards.entadsl.com Sept 2012.

moduleVersion = 0.25
publisherName = Doobie Company
publisherLink = http://www.doobiecompany.com
'''

import uno, unohelper
from com.doobiecompany.examples.DoobieDoo import XDoobieDoo

unoComponentId = "com.doobiecompany.examples.DoobieDoo.python.DoobieDoo"

class DoobieDoo (unohelper.Base, XDoobieDoo):
    def __init__ (self, ctx):
        self.ctx = ctx

    def doobieMult (self, a, b):
        """
        Multiplies two integers quite fantastically
            a - the first integer
            b - the second integer
        idl: long doobieMultv ([in] long a, [in] long b);
        """
        return a * b

    def doobieDiv (self, a, b):
        """
        Divides two floating point numbers in a marvellous way
            a - the first floating point number
            b - the second floating point number
        idl: double doobieDiv ([in] double a, [in] double b);
        """
        return a / b

    def doobieConcat (self, s1, s2):
        """
        Concatenates two strings without hesitation
            s1 - the first string
            s2 - the second string
        idl: string doobieConcat ([in] string s1, [in] string s2);
        """
        return str(s1) + str(s2)

    def doobieConcatOptional (self, s1, s2, s3):
        """
        Concatenates two, perhaps three, strings without further ado
            s1 - the very first string
            s2 - the second, or middle, string
            s3 - the third string which may, or may not be, present
        idl: string doobieConcatOptional ([in] string s1, [in] string s2, [in] any s3);
        """
        if s3 == None:
            return str(s1) + str(s2)
        else:
            return str(s1) + str(s2) + str(s3)

def createInstance (ctx):
    return DoobieDoo (ctx)

g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation (
    createInstance, unoComponentId, ("com.sun.star.sheet.AddIn",) )

# EOF
