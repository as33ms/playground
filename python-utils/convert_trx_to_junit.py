#!/usr/bin/env python

import os
import sys
import glob

def show_info(info):
    print (" [INFO]: %s" % info)
    return

def show_error(error, exit=True):
    print ("[ERROR]: %s" % error)
    if exit:
        sys.exit(1)
    return

def usage():
    print
    print ("$ %s junit-report-1.trx ... junit-report-n.trx" % os.path.basename(__file__))
    print

#Import the superstar
try: 
    from lxml import etree
except ImportError:
    show_error("Unable to find module etree in lxml! Do you have python-lxml installed?")
    sys.exit(1)

def parse_trx(infile):
    """
    parse the trx (which is in xml format) file and return the data
    """
    try: 
        data = etree.parse(infile)
    except etree.XMLSyntaxError:
        print ("File [%s] is not in proper xml syntax" % infile)
        sys.exit(1)
    return data

if __name__ == "__main__":
    args = sys.argv[1:]

    if not args:
        show_error("Invalid script usage!", False)
        usage()
        sys.exit(1)

    testsuites = etree.Element("testsuites")
    junitdoc = etree.ElementTree(testsuites)
    
    trxfiles = []
    for arg in args:
        files = glob.glob(arg)
        
        if not files:
            trxfiles.append(arg)
        else:
            trxfiles = trxfiles + files

        
    for trxfile in trxfiles:
        print
        if os.path.exists(trxfile):
            show_info("Analyzing trxfile '%s'" % trxfile)

            filedata = parse_trx(trxfile)
            
            # TRX file might contains an xml namespace, which is:
            # root.nsmap = {None: 'http://microsoft.com/schemas/VisualStudio/TeamTest/2010'}
            
            #obtain the namespace
            nsmap = filedata.getroot().nsmap.copy()
            #remove the empty prefix (None) in the name space map and change it to xmlns
            
            xpath = {}
            
            try:
                nsmap['xmlns'] = nsmap.pop(None)
                xpath['counters'] = ".//xmlns:Counters"
                xpath['testcase'] = ".//xmlns:UnitTestResult"
            except KeyError:
                # in case, there is no nsmap associated with the file
                xpath['counters'] = "/TestRun/ResultSummary/Counters"
                xpath['testcase'] = "/TestRun/Results/UnitTestResult"

            counters = filedata.xpath(xpath['counters'], namespaces=nsmap)[0]
            
            # So far, so good, write the testsuite element
            suitename = os.path.basename(trxfile).replace(".trx", "")
            
            testsuite = etree.SubElement(testsuites, "testsuite",
                                            name=suitename,
                                            tests=counters.attrib['total'],
                                            error=counters.attrib['error'],
                                            failures=counters.attrib['failed'])
            
            testcases = filedata.xpath(xpath['testcase'], namespaces=nsmap)
            
            for case in testcases:
                show_info(" - found %s '%s'" % (case.tag, case.attrib['testName']))
                testcase = etree.SubElement(testsuite, "testcase",
                                                name=case.attrib['testName'],
                                                time=case.attrib['duration'],
                                                result=case.attrib['outcome'])
                
                debug_trace = case.xpath(".//xmlns:DebugTrace", namespaces=nsmap)[0]
                
                testcase.text = debug_trace.text
                
                if (case.attrib['outcome'] == "Failed"):
                    fail_message = case.xpath(".//xmlns:Message", namespaces=nsmap)[0]
                    stack_trace = case.xpath(".//xmlns:StackTrace", namespaces=nsmap)[0]
                    
                    failure = etree.SubElement(testcase, "failure", message="Test case failed")
                    failure.text = fail_message.text
                    
                    system_err = etree.SubElement(testcase, "system-err")
                    system_err.text = stack_trace.text
                #FIXME: Find out outcome values for Skipped / Error cases
        else:
            show_info("Can not find file '%s', skipping" % trxfile)
    print

    outfile = open("junit-report-full.xml", "wb")
    junitdoc.write(outfile, xml_declaration=True, encoding='utf-8')
    show_info("Wrote consolidated trx file results in junit format to: junit-report-full.xml")
