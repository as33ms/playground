#!/usr/bin/env python
"""
@author: ashakunt
@summary: Enter a test case name and its status (pass / fail) and get a
junit compatible output file. Main aim of this useless utility is to make
Jenkins job status reflect in TestLink.
          
Project setup:
    1. Jenkins configured with various Test Jobs (e.g. Unit, Functional,
    UI, Performance)

Problem's precondition:
    1. Hook Jenkins and TestLink (e.g. Job name: TestLink_Bridge)
    2. Create a test plan in TestLink and add test cases to it.
    3. The custom field in each Test Case is name of a Jenkins job
    4. Iterative strategy is used when running the tests

When TestLink_Bridge is run, then it fetches all test cases from TestLink.
All these test cases are actually name of separate Jenkins Jobs. Now, the
TestLink_Bridge job triggers the specified JENKINS_JOBS defined in the custom
field of each testcase in TestLink.

Real problem:
The result seeking strategy for the Jenkins TestLink plugin cannot be run
in iterative manner as the tests thus setting the build as pass / fail and
hence, TestLink_Bridge reporting its status to TestLink accordingly. Because
of this, the TestPlan is marked as not executed in TestLink.

This script hence, based on conditional run plugin, stores the status of
the child job in a junit file which is available to the TestLink plugin
for creating test statistics and reporting status to TestLink.
"""

import os
import sys

TESTCASE_NAME = 0
TESTCASE_STATUS = 1

def show_info(info):
    print (" [INFO]: %s" % info)
    return

def show_error(error, exit=True):
    print ("[ERROR]: %s" % error)
    if exit:
        sys.exit(1)
    return

def usage():
    script = os.path.basename(__file__)
    print
    print ("$ %s test_case_name <pass / fail / Pass / Fail>" % script)
    print

#Import the superstar
try: 
    from lxml import etree
except ImportError:
    show_error("Cant find etree in lxml! Do you have python-lxml installed?")
    sys.exit(1)

def parse_file(infile):
    """
    parse the junit file and return the data
    """
    try: 
        data = etree.parse(infile)
    except etree.XMLSyntaxError:
        print ("File [%s] is not in proper xml syntax" % infile)
        sys.exit(1)
    return data

if __name__ == "__main__":
    args = sys.argv[1:]
    
    if len(args) != 2:
        show_error("Invalid script usage!", False)
        usage()
        sys.exit(1)

    doc = 'junit-report-full.xml'
    tc_name = args[TESTCASE_NAME]
    tc_status = args[TESTCASE_STATUS]
    
    if tc_status not in ["Pass", "Fail", "pass", "fail"]:
        show_error("Not a valid status for testcase", True)

    if (os.path.exists(os.path.basename(doc))):
        existing_data = parse_file(os.path.basename(doc))
        
        existing_tests = existing_data.xpath("/testsuite/testcase")
        
        total = u'%s' % str(len(existing_tests) + 1)
        
        testsuite = etree.Element("testsuite", tests=total)
        junitdoc = etree.ElementTree(testsuite)
        
        for test in existing_tests:
            t = etree.SubElement(testsuite, "testcase",
                                 name=test.attrib['name'],
                                 result=test.attrib['result'])
            t.text = test.text
            
        new_test = etree.SubElement(testsuite, "testcase",
                                    name=tc_name,
                                    result=tc_status)
        if tc_status in ['Fail', 'fail']:
            new_test.text = "Job execution failed. Please check Jenkins"
    else:
        testsuite = etree.Element("testsuite", tests=u'1');
        junitdoc = etree.ElementTree(testsuite);
        
        testcase = etree.SubElement(testsuite, "testcase",
                                    name=tc_name,
                                    result=tc_status)
        
        if tc_status in ['Fail', 'fail']:
            testcase.text = "Job execution failed. Please check Jenkins"
            
    outfile = open(doc, "wb")
    junitdoc.write(outfile, xml_declaration=True, encoding='utf-8')
    show_info("Added '%s' to %s (result: %s)" % (tc_name, doc, tc_status))