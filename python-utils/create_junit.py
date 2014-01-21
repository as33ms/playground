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

TL_TESTPLAN_NAME = 0 #$TESTLINK_TESTPLAN_NAME
TL_TESTCASE_NAME = 1 #$TESTLINK_TESTCASE_NAME
TL_TESTCASE_ID = 2 #$TESTLINK_TESTCASE_ID
JENKINS_JOB_NAME = 3 #$JENKINSID (or the custom field)
TESTCASE_RUN_STATUS = 4 #pass/fail

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
    print ("$ %s plan_name case_name case_id jenkins_job <pass/fail>" % script)
    print ("    where, all arguments are available via envronment variables")
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

def create_testsuite (name, total, fails, errors=0, skips=0, times='0.5'):
    suite = etree.Element("testsuite", name=u'%s' % str(name),
                                       tests=u'%s' % str(total),
                                       failures=u'%s' % str(fails),
                                       skipped=u'%s' % str(skips),
                                       errors=u'%s' % str(errors),
                                       time=u'%s' % str(times))
    return suite

def add_new_testcase (rootelement, attribs):
    case = etree.SubElement(rootelement, "testcase", attrib=attribs)
    
    if attribs['result'] in ['Fail', 'fail']:
        failure = etree.SubElement(case, "failure",
                type=u'jenkins.jobExecution.Failure', message=u'null')
        failure.text = "Check '%s' for failure details" % attribs['classname'] 
    return case


if __name__ == "__main__":
    args = sys.argv[1:]
    
    if len(args) != 5:
        show_error("Invalid script usage!", False)
        usage()
        sys.exit(1)

    doc = 'junit-report-full.xml'
    tl_plan = args[TL_TESTPLAN_NAME]
    tl_case = args[TL_TESTCASE_NAME]
    tl_case_id = args[TL_TESTCASE_ID]
    jenkins_job = args[JENKINS_JOB_NAME]
    job_run_status = args[TESTCASE_RUN_STATUS]
    
    if job_run_status not in ["Pass", "Fail", "pass", "fail"]:
        show_error("Not a valid status for testcase", True)

    if (os.path.exists(os.path.basename(doc))):
        existing_data = parse_file(os.path.basename(doc))
        
        existing_tests = existing_data.xpath("/testsuite/testcase")
        
        total = u'%s' % str(len(existing_tests) + 1)

        fails = 1 if job_run_status in ['Fail', 'fail'] else 0

        for test in existing_tests:
            if test.attrib['result'] in ['Fail', 'fail']:
                fails = fails + 1

        testsuite = create_testsuite(tl_plan, total, fails)
        junitdoc = etree.ElementTree(testsuite)
        
        for test in existing_tests:
            add_new_testcase(testsuite, test.attrib)

        add_new_testcase(testsuite, {'time': u'0', 'name': u'%s' % str(tl_case),
                                    'result': u'%s' % str(job_run_status),
                                    'id': u'%s' % str(tl_case_id),
                                    'classname': u'%s' % str(jenkins_job),
                                    'JenkinsID': u'%s' % str(jenkins_job)})

        show_info("Summary [total: %s, failures:%s]" % (total, fails));
    else:
        failed = 1 if job_run_status in ['Fail', 'fail'] else 0

        testsuite = create_testsuite(tl_plan, 1, failed)
        junitdoc = etree.ElementTree(testsuite)
        
        add_new_testcase(testsuite, {'time': u'0', 'name': u'%s' % str(tl_case),
                                    'result': u'%s' % str(job_run_status),
                                    'id': u'%s' % str(tl_case_id),
                                    'classname': u'%s' % str(jenkins_job),
                                    'JenkinsID': u'%s' % str(jenkins_job)})

        show_info("Summary [total: 1, failures:%s]" % str(failed));

    outfile = open(doc, "wb")
    junitdoc.write(outfile, xml_declaration=True, encoding='utf-8')
    show_info("Added '%s' to %s (result: %s)" % (tl_case, doc, job_run_status))
