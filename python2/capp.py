# -*- coding: utf-8 -*-

'''
Calc Add-In Preprocessor for Python 2.x.x

This Python script can be used to pre-processes the Python source file of
a LibreOffice calc add-in to generate files needed to package the add-in.

The script takes three arguments:
    generate   - what to generate, one of idl, xcu or xml
    moduleName - the name of the add-in module
    sourceFile - the path of the add-in's Python source files
Output is to standard output.

Most, but not all, the information used to generate the description files
appears as comments in the Python source file.  If the information is missing
or not in the form expected by the script, the output will be incomplete.

For more information see the module documentation in capp-help.py.
'''

'''
    Copyright (C) 2012, 2016, NewForester
    Released under the terms of the GNU GPL v2
'''

import sys, re

'''
Regular expressions that support simple parsing of the Python source
'''
_reComponent  = re.compile(r'^unoComponentId\s*=\s*"([^"]*)"')
_reFromImport = re.compile(r'^from\s+(\S+)\s+import\s+(\S+)')
_reClassDef   = re.compile(r'^class\s+(\S+)\s*\(\s*unohelper.Base\s*,\s*(\S+)\s*\)\s*:')
_reMethodDef  = re.compile(r'^\s+def\s+(\S*)\s*\(\s*self\s*,([^)]+)\)\s*:')
_reTripleQ    = re.compile(r'^\s*"""\s*$')
_reTripleA    = re.compile(r"^\s*'''\s*$")

def strip(item):
    '''
    functional programming aid
    '''
    return item.strip()

def processInput(sourceFile,moduleName,generate):
    '''
    process the input a line at a time, generating output when convenient

    Regular expressions trigger state changes as input lines of significance are recognised.
    Certain state changes trigger the generation of output.
    What is generated is determined by the generate parameter.
    '''
    interfaceName = 'X' + moduleName
    moduleVersion = "1.00"
    displayName   = ""
    publisherLink = ""
    publisherName = ""

    state = "Seeking";

    for line in sourceFile:
        if state == "Seeking":
            if _reTripleQ.match(line) or _reTripleA.match(line):
                state = "Display Name"
                continue
            result = _reFromImport.match(line)
            if result:
                if interfaceName == result.group(2):
                    unoModuleId = result.group(1)
                    state = "Have UNO Module Id"
        elif state == "Display Name":
            displayName = line.strip()
            state = "Module Description"
        elif state == "Module Description":
            if _reTripleQ.match(line) or _reTripleA.match(line):
                state = "Seeking"
            elif line.find('=') != -1:
                work = map(strip,line.split('='))
                if len(work) == 2:
                    if work[0] == "moduleVersion":
                        moduleVersion = work[1]
                    elif work[0] == "publisherLink":
                        publisherLink = work[1]
                    elif work[0] == "publisherName":
                        publisherName = work[1]
        elif state == "Method Description":
            methodDescription = line.strip().capitalize()
            state = "Parameter Descriptions"
        elif state == "Have UNO Module Id":
            result = _reComponent.match(line)
            if result:
                unoComponentId = result.group(1)
                continue
            result = _reClassDef.match(line)
            if result:
                if interfaceName == result.group(2):
                    if moduleName == result.group(1):
                        if generate == "idl":
                            idlGeneratePreamble(unoModuleId,interfaceName)
                        if generate == "xcu":
                            xcuGeneratePreamble(unoComponentId)
                        state = "Class Implementation"
        elif state == "Class Implementation" or state == "Method Implementation":
            result = _reMethodDef.match(line)
            if result:
                if result.group(1)[0] != '_':
                    methodName = result.group(1)
                    methodDescription = ""
                    parameterNames = map(strip,result.group(2).split(','))
                    parameterDescriptions = {}
                    idlSignature = []
                    state = "Method Declaration"
        elif state == "Method Declaration":
            if _reTripleQ.match(line) or _reTripleA.match(line):
                state = "Method Description"
        elif state == "Method Description":
            methodDescription = line.strip().capitalize()
            state = "Parameter Descriptions"
        elif state == "Parameter Descriptions":
            if _reTripleQ.match(line) or _reTripleA.match(line):
                if generate == "idl":
                    idlGenerateSignature(idlSignature)
                if generate == "xcu":
                    xcuGenerateNode(moduleName,methodName,methodDescription,parameterNames,parameterDescriptions)
                state = "Method Implementation"
            elif line.find(':') != -1:
                work = map(strip,line.split(':'))
                if len(work) == 2:
                    idlSignature.append(work[1])
            elif line.find('-') != -1:
                work = map(strip,line.split('-'))
                if len(work) == 2:
                    parameterDescriptions[work[0]] = work[1]

    if state != "Seeking":
        if generate == "xml":
            xmlGenerateDescription(unoModuleId,moduleVersion,displayName,publisherLink,publisherName)
        if generate == "idl":
            idlGeneratePostamble(unoModuleId)
        if generate == "xcu":
            xcuGeneratePostamble()

    return sourceFile

def xmlGenerateDescription(unoModuleId,moduleVersion,displayName,publisherLink,publisherName):
    '''
    generate the XML description of the module`
    '''
    print '<?xml version="1.0" encoding="UTF-8"?>'
    print '<description xmlns="http://openoffice.org/extensions/description/2006"'
    print '  xmlns:d="http://openoffice.org/extensions/description/2006"'
    print '  xmlns:xlink="http://www.w3.org/1999/xlink">'
    print ''
    print '  <dependencies>'
    print '    <OpenOffice.org-minimal-version value="2.4" d:name="OpenOffice.org 2.4"/>'
    print '  </dependencies>'
    print ''
    print '  <identifier value="' + unoModuleId + '" />'
    print '  <version value="' + moduleVersion + '" />'
    print '  <display-name><name lang="en">' + displayName + '</name></display-name>'
    if publisherLink:
        print '  <publisher><name xlink:href="' + publisherLink + '" lang="en">' + publisherName + '</name></publisher>'
    else:
        print '  <publisher><name lang="en">' + publisherName + '</name></publisher>'
    print ''
    print '</description>'

def idlGeneratePreamble(unoModuleId,interfaceName):
    '''
    generate the IDL file's head comprising
        the interface clause declaration within the UNO module's namespace
    '''
    print '#include <com/sun/star/uno/XInterface.idl>'
    print
    for item in unoModuleId.split('.'):
        print 'module ' + item + ' {',
    print
    print
    print '    interface ' + interfaceName
    print '    {'

def idlGeneratePostamble(unoModuleId):
    '''
    generate the IDL file's tail comprising
        closing braces matching the open braces of the IDL file's head
    '''
    print '    };'
    print
    for dummy in unoModuleId.split('.'):
        print '};',
    print

def idlGenerateSignature(idlSignature):
    '''
    generate the IDL signature for a Python method
        found in the comments documenting the method
    '''
    for item in idlSignature:
        print '        ' + item

def xcuGeneratePreamble(unoComponentId):
    '''
    generate the XCU file's head including
        the identification of the magic UNO node of the Python component
    '''
    print '<?xml version="1.0" encoding="UTF-8"?>'
    print '<oor:component-data xmlns:oor="http://openoffice.org/2001/registry" xmlns:xs="http://www.w3.org/2001/XMLSchema" oor:name="CalcAddIns" oor:package="org.openoffice.Office">'
    print '  <node oor:name="AddInInfo">'
    print '    <node oor:name="' + unoComponentId + '" oor:op="replace">'
    print '      <node oor:name="AddInFunctions">'

def xcuGeneratePostamble():
    '''
    generate the XCU file's tail
        closing XML elements opened in the XCU file's head
    '''
    print '      </node>'
    print '    </node>'
    print '  </node>'
    print '</oor:component-data>'

def xcuGenerateNode(moduleName,methodName,methodDescription,parameterNames,parameterDescriptions):
    '''
    generate the XCU signature for a Python method
        from comments documenting the method
    '''
    xlsName = 'AutoAddIn.' + moduleName + '.' + methodName
    print '        <node oor:name="' + methodName + '" oor:op="replace">'
    print '          <prop oor:name="DisplayName"><value xml:lang="en">' + methodName + '</value></prop>'
    print '          <prop oor:name="Description"><value xml:lang="en">' + methodDescription + '</value></prop>'
    print '          <prop oor:name="Category"><value>' + 'Add-In' + '</value></prop>'
    print '          <prop oor:name="CompatibilityName"><value xml:lang="en">' + xlsName + '</value></prop>'
    print '          <node oor:name="Parameters">'

    for name in parameterNames:
        print '            <node oor:name="' + name +'" oor:op="replace">'
        print '              <prop oor:name="DisplayName"><value xml:lang="en">' + name + '</value></prop>'
        print '              <prop oor:name="Description"><value xml:lang="en">' + parameterDescriptions[name] + '</value></prop>'
        print '            </node>'

    print '          </node>'
    print '        </node>'


if sys.argv[0].find('pydoc') ==  -1:
    '''
    Recognise the first argument
    '''

    if not sys.argv[1] in ['idl', 'xcu', 'xml']:
        print ("I need to know what to generate - my first argument must be one of ['idl', 'xcu', 'xml']")
        sys.exit(1)

    '''
    Open the python source file
    '''

    try:
        sourceFile = open(sys.argv[3],"r")
    except:
        print "I need a python module to process - the module name and the path to the module's implementation"
        sys.exit(1)

    '''
    Preprocess the python source file ...
    '''
    processInput(sourceFile,sys.argv[2],sys.argv[1]).close()

# EOF
