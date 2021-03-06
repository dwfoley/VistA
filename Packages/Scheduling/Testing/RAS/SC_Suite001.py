#---------------------------------------------------------------------------
# Copyright 2013 PwC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#---------------------------------------------------------------------------

## @package SC_Suite001
## Scheduling Package Tests (Suite)

'''
These are the Scheduling package Suite001 tests, implemented as Python functions.

Each test has a unique name derived from the test method name.
Each test has a unique result log with a filename derived from the testname and a datestamp.
There is a parent resultlog that is also used for pass/fail logging.
In general each test establishes a connection to the target application (VistA),
signs on as a user, provider, or programmer and then performs a set of test functions.
When testing is complete the connection is closed and a pass/fail indicate is written
to the resultlog.

Created on Jun 14, 2012
@author: pbradley
@copyright PwC
@license http://www.apache.org/licenses/LICENSE-2.0
'''

import sys
sys.path = ['./Functional/RAS/lib'] + ['./dataFiles'] + ['./Python/vista'] + sys.path
from SCActions import SCActions
from Actions import Actions
import TestHelper
import datetime
import logging

def sc_test001(resultlog, result_dir, namespace):
    '''
    Test for basic appointment management options.
    Make an Appointment, Check in, Check Out
    '''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir, namespace)
        SC = SCActions(VistA, scheduling='Scheduling')
        time = SC.schtime()
        SC.signon()
        tclinic = SC.getclinic()
        SC.makeapp(patient='333224444', clinic=tclinic, datetime=time)
        time = SC.schtime(plushour=1)
        now = datetime.datetime.now()
        hour = now.hour + 1
        SC.signon()
        SC.checkin(clinic=tclinic, vlist=['Three', str(hour), 'CHECKED-IN:'])
        SC.signon()
        SC.checkout(clinic=tclinic, vlist1=['Three', str(hour), 'Checked In'],
                    vlist2=['305.91', 'OTHER DRUG', 'RESULTING'], icd='305.91')
        SC.signon()
        SC.makeapp_bypat(clinic=tclinic, patient='333224444', datetime=time, fresh='No', prevCO='yes')
        SC.signoff()
    except TestHelper.TestError, e:
        resultlog.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*****exception*********' + str(e))
    else:
        resultlog.write('Pass\n')

def sc_test002(resultlog, result_dir, namespace):
    '''
    Test basic appointment management options.
    Make an Appointment (Scheduled and Unscheduled),
    record a No-Show, Cancel an appointment and change patients
    '''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir, namespace)
        SC = SCActions(VistA, scheduling='Scheduling')
        time = SC.schtime()
        SC.signon()
        tclinic = SC.getclinic()
        SC.makeapp(clinic=tclinic, patient='655447777', datetime=time)
        time = SC.schtime(plushour=1)
        SC.signon()
        SC.unschvisit(clinic=tclinic, patient='345678233', patientname='Twelve')
        SC.signon()
        SC.noshow(clinic=tclinic, appnum='3')
        SC.signon()
        SC.canapp(clinic=tclinic, mult='1')
        SC.signon()
        SC.chgpatient(clinic=tclinic, patient1='345678233', patient2='345238901',
                      patientname1='Twelve', patientname2='Ten')
        SC.signoff()
    except TestHelper.TestError, e:
        resultlog.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*****exception*********' + str(e))
    else:
        resultlog.write('Pass\n')

def sc_test003(resultlog, result_dir, namespace):
    '''
    This tests clinic features such as change clinic, change date-range,
    expand the entry, add and edit, and Patient demographics
    '''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir, namespace)
        SC = SCActions(VistA, scheduling='Scheduling')
        SC.signon()
        tclinic = SC.getclinic()
        SC.chgclinic()
        SC.signon()
        SC.chgdaterange(clinic=tclinic)
        SC.signon()
        SC.teaminfo(clinic=tclinic)
        SC.signoff()
    except TestHelper.TestError, e:
        resultlog.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*****exception*********' + str(e))
    else:
        resultlog.write('Pass\n')

def sc_test004(resultlog, result_dir, namespace):
    '''
    This tests clinic features such as expand the entry, add and edit, and Patient demographics
    '''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir, namespace)
        SC = SCActions(VistA, scheduling='Scheduling')
        time = SC.schtime(plushour=1)
        SC.signon()
        tclinic = SC.getclinic()
        SC.makeapp(clinic=tclinic, patient='345238901', datetime=time)
        SC.signon()
        SC.patdem(clinic=tclinic, name='Ten', mult='2')
        SC.signon()
        SC.expandentry(clinic=tclinic, vlist1=['TEN', 'SCHEDULED', '30'],
                       vlist2=['Event', 'Date', 'User', 'TESTMASTER'],
                       vlist3=['NEXT AVAILABLE', 'NO', '0'], vlist4=['1933', 'MALE', 'UNANSWERED'],
                       vlist5=['Combat Veteran:', 'No check out information'], mult='3')
        SC.signon()
        SC.addedit(clinic=tclinic, name='354623902', icd='305.91')
        SC.signoff()
    except TestHelper.TestError, e:
        resultlog.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*****exception*********' + str(e))
    else:
        resultlog.write('Pass\n')

def sc_test005(resultlog, result_dir, namespace):
    '''
    This test checks a patient into a clinic, then discharges him, then deletes his checkout
    '''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir, namespace)
        SC = SCActions(VistA)
        SC.signon()
        tclinic = SC.getclinic()
        SC.enroll(clinic=tclinic, patient='543236666')
        SC = SCActions(VistA, scheduling='Scheduling')
        time = SC.schtime(plushour=1)
        SC.signon()
        SC.makeapp(clinic=tclinic, patient='543236666', datetime=time)
        SC.signon()
        SC.discharge(clinic=tclinic, patient='543236666', appnum='3')
        SC.signon()
        SC.checkout(clinic=tclinic, vlist1=['One', 'No Action'],
                    vlist2=['305.91', 'RESULTING'], icd='305.91', mult='4')
        SC = SCActions(VistA, user='fakedoc1', code='1Doc!@#$')
        SC.signon()
        SC.deletecheckout(clinic=tclinic, appnum='3')
        SC.signoff()
    except TestHelper.TestError, e:
        resultlog.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*****exception*********' + str(e))
    else:
        resultlog.write('Pass\n')

def sc_test006(resultlog, result_dir, namespace):
    '''
    This test will exercise the wait list functionality
    '''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir, namespace)
        SC = SCActions(VistA, user='fakedoc1', code='1Doc!@#$')
        SC.signon()
        tclinic = SC.getclinic()
        SC.waitlistentry(clinic=tclinic, patient='323123456')
        SC.waitlistdisposition(clinic=tclinic, patient='323123456')
        SC.signoff()
    except TestHelper.TestError, e:
        resultlog.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*****exception*********' + str(e))
    else:
        resultlog.write('Pass\n')


def sc_test007(resultlog, result_dir, namespace):
    '''
    This is a basic appointment, similar to sc_test001 but specifying patient name not clinic at first prompt
    This test will also use the space-bar to check recall feature works.
    Make an Appointment, Check in, Check Out
    '''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir, namespace)
        SC = SCActions(VistA, scheduling='Scheduling')
        time = SC.schtime()
        SC.signon()
        tclinic = SC.getclinic()
        SC.makeapp_bypat(clinic=tclinic, patient='656454321', datetime=time, loopnum=2)
        SC.signon()
        SC.use_sbar(clinic=tclinic, patient='656454321', fresh='No')
        time = SC.schtime(plushour=1)
        now = datetime.datetime.now()
        hour = now.hour + 1
        SC.signon()
        SC.checkin(clinic=tclinic, vlist=['Five', str(hour), 'CHECKED-IN:'], mult='5')
        SC.signon()
        SC.checkout(clinic=tclinic, vlist1=['Five', str(hour), 'Checked In'],
                    vlist2=['305.91', 'OTHER DRUG', 'RESULTING'], icd='305.91', mult='5')
        SC.signon()
        SC.ver_actions(clinic=tclinic, patient='4444',
                       PRvlist=['THREE,PATIENT C', 'ALEXANDER,ROBERT'],
                       DXvlist=['305.91', 'OTHER DRUG', 'RESULTING'],
                       CPvlist=['THREE,PATIENT C'])
        SC.signoff()
    except TestHelper.TestError, e:
        resultlog.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*****exception*********' + str(e))
    else:
        resultlog.write('Pass\n')

def sc_test008(resultlog, result_dir, namespace):
    '''
    This test makes future appointments and verifies, and also checks case sensitivity (cLiNiCx, ClInIcX, etc.)
    '''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir, namespace)
        SC = SCActions(VistA, scheduling='Scheduling')
        time = SC.schtime()
        SC.signon()
        tclinic = SC.getclinic()
        SC.makeapp_bypat(clinic='cLiNiCx', patient='323678904', datetime='t+5@8PM')
        SC.signon()
        SC.verapp_bypat(patient='323678904', vlist=['THIRTEEN,PATIENT M', 'Clinicx', 'Future'])
        SC.signon()
        SC.makeapp_bypat(clinic='cLiNiCx', patient='222559876', datetime='t+6@8PM', CLfirst='Yes')
        SC.signon()
        SC.verapp_bypat(patient='222559876', vlist=['SIXTEEN,PATIENT P', 'Clinicx', 'Future'],
                        CInum=['1', '1'], COnum=['1', '2'])
        SC.signon()
        SC.verapp(clinic='cLiNiCx',
                  vlist=['Thirteen,Patient M', 'Future', 'Sixteen,Patient P', 'Future'],
                  CInum=['2', '1'], COnum=['2', '2'])
        SC.signon()
        SC.canapp(clinic='cLiNiCx', mult='2', future=1, rebook=1)
        SC.signoff()
    except TestHelper.TestError, e:
        resultlog.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*****exception*********' + str(e))
    else:
        resultlog.write('Pass\n')

def sc_test009(resultlog, result_dir, namespace):
    '''
    This test makes appointments with variable length and makes appointment in distant future for EWL
    '''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir, namespace)
        SC = SCActions(VistA, scheduling='Scheduling')
        time = SC.schtime()
        SC.signon()
        tclinic = SC.getclinic()
        SC.makeapp_var(clinic='CLInicA', patient='323678904', datetime='t+7@7AM', fresh='No')
        SC.signon()
        SC.verapp_bypat(patient='323678904', vlist=['THIRTEEN,PATIENT M', 'Clinica', '7:00', 'Future'],)
        SC.signon()
        SC.makeapp_var(clinic='CLInicA', patient='323678904', datetime='t+122@6AM', fresh='No')
        SC.signon()
        SC.makeapp_var(clinic='CLInicA', patient='323678904', datetime='t+10@4AM', fresh='No', nextaval='No')
        SC.signon()
        SC.verapp_bypat(patient='323678904', vlist=['THIRTEEN,PATIENT M', 'Clinica', '4:00', 'Future'],
                        ALvlist=['THIRTEEN,PATIENT M', 'Clinicx', 'Clinica', 'Clinica'],
                        EPvlist=['THIRTEEN,PATIENT M', 'CLINICX', '8904', 'FUTURE', 'SCHEDULED', 'REGULAR'])
        SC.signoff()
    except TestHelper.TestError, e:
        resultlog.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*****exception*********' + str(e))
    else:
        resultlog.write('Pass\n')

def sc_test010(resultlog, result_dir, namespace):
    '''
    This test makes appointments and saves demographics
    '''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir, namespace)
        SC = SCActions(VistA, scheduling='Scheduling')
        time = SC.schtime()
        # this signon() and fix_demographics() is a workaround for gtm bug
        if VistA.type == 'GTM':
            SC.signon()
            SC.fix_demographics(clinic='CLInicA', patient='323123456',
                                dgrph=[['COUNTRY', ''],
                                     ['STREET ADDRESS', ''],
                                     ['ZIP', '20005'],
                                     ['CITY', 'WASHINGTON'],
                                     ['PHONE NUMBER', ''],
                                     ['PHONE NUMBER', ''],
                                     ['BAD ADDRESS INDICATOR', ''],
                                     ['save the above changes', 'yes']])
        #
        SC.signon()
        tclinic = SC.getclinic()
        SC.set_demographics(clinic='CLInicA', patient='323123456',
                        dgrph=[['COUNTRY', ''],
                                 ['STREET ADDRESS', '123 SMITH STREET'],
                                 ['STREET ADDRESS', ''],
                                 ['ZIP', '20005'],
                                 ['CITY', 'WASHINGTON'],
                                 ['PHONE NUMBER', '2021112222'],
                                 ['PHONE NUMBER', ''],
                                 ['BAD ADDRESS INDICATOR', ''],
                                 ['save the above changes', 'yes'],
                                 ['Press ENTER to continue', ''],
                                 ['SEX', 'MALE'] ,
                                 ['Select ETHNICITY', 'N'],
                                 ['Select RACE', 'Black'],
                                 ['new RACE INFORMATION', 'Yes'],
                                 ['RACE', ''],
                                 ['MARITAL STATUS', 'MARRIED'],
                                 ['RELIGIOUS PREFERENCE', 'CELTICISM'],
                                 ['TEMPORARY ADDRESS ACTIVE', 'NO'],
                                 ['PHONE NUMBER', ''],
                                 ['PAGER NUMBER', ''],
                                 ['EMAIL ADDRESS', '']])
        SC.signon()
        SC.get_demographics(patient='323123456',
                        vlist=[['COUNTRY: UNITED STATES', ''],
                                 ['123 SMITH STREET', ''],
                                 ['STREET ADDRESS', ''],
                                 ['20005', ''],
                                 ['CITY: WASHINGTON', ''],
                                 ['2021112222', ''],
                                 ['PHONE NUMBER', ''],
                                 ['BAD ADDRESS INDICATOR', ''],
                                 ['save the above changes', 'no'],
                                 ['Press ENTER to continue', ''],
                                 ['SEX: MALE', ''],
                                 ['Select ETHNICITY INFORMATION: NOT HISPANIC OR LATINO', ''],
                                 ['ETHNICITY: NOT HISPANIC OR LATINO', ''],
                                 ['Select RACE INFORMATION: BLACK OR AFRICAN AMERICAN', ''],
                                 ['RACE: BLACK OR AFRICAN AMERICAN', ''],
                                 ['Select RACE INFORMATION', ''],
                                 ['MARITAL STATUS', 'MARRIED'],
                                 ['RELIGIOUS PREFERENCE: CELTICISM', ''],
                                 ['ADDRESS ACTIVE', ''],
                                 ['PHONE NUMBER', ''],
                                 ['PAGER NUMBER', ''],
                                 ['EMAIL ADDRESS', '']])
        SC.signoff()
    except TestHelper.TestError, e:
        resultlog.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*****exception*********' + str(e))
    else:
        resultlog.write('Pass\n')

def sc_test011(resultlog, result_dir, namespace):
    '''
    This makes appointments via Multiple Clinic Display and then verifies the appointments
    '''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA = connect_VistA(testname, result_dir, namespace)
        SC = SCActions(VistA, user='fakedoc1', code='1Doc!@#$')
        SC.signon()
        SC.multiclinicdisplay(cliniclist=['Clinic1', 'ClinicX'], patient='656454321', timelist=['7', '5'], pending=None)
        SC.gotoApptMgmtMenu()
        SC.verapp_bypat(patient='656454321', vlist=['Clinic1', '7:00', 'Future', 'Clinicx', '17:00', 'Future'],)
        SC.signoff()
    except TestHelper.TestError, e:
        resultlog.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*****exception*********' + str(e))
    else:
        resultlog.write('Pass\n')

def sc_test012(resultlog, result_dir, namespace):
    '''
    This test adds a new user with SDOB keys and creates & verifies appointments in timeslots outside a clinic's normal operating window
    '''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        # Create new user with SDOB keys
        VistA1 = connect_VistA(testname, result_dir, namespace)
        SC = Actions(VistA1, user='SM1234', code='SM12345!!')
        SC.signon()
        SC.adduser(name='CRANE,JON', ssn='000000065', gender='M', initials='JC', acode='fakejon1', vcode1='1SWUSH1234!!')
        SC.signoff()
        VistA1 = connect_VistA(testname + '_01', result_dir, namespace)
        SC = Actions(VistA1)
        SC.sigsetup(acode='fakejon1', vcode1='1SWUSH1234!!', vcode2='1SWUSH12345!!', sigcode='JONC123')
        SC.signoff()
        # Create appointment outside Clinic1's operating hours via fakedoc1
        VistA2 = connect_VistA(testname + '_02', result_dir, namespace)
        SC = SCActions(VistA2, user='fakedoc1', code='1Doc!@#$')
        SC.signon()
        SC.gotoApptMgmtMenu()
        SC.makeapp(patient='333224444', clinic='Clinic1', datetime='t+5@9AM', fresh='No', badtimeresp='noslot')
        SC.signoff()
        # Create appointment outside Clinic1's operating hours via fakejon1 (SDOB key)
        VistA3 = connect_VistA(testname + '_02', result_dir, namespace)
        SC = SCActions(VistA3, user='fakejon1', code='1SWUSH12345!!')
        SC.signon()
        SC.gotoApptMgmtMenu()
        SC.makeapp(patient='333224444', clinic='Clinic1', datetime='t+10@9AM', fresh='No', badtimeresp='overbook')
        SC.signoff()
    except TestHelper.TestError, e:
        resultlog.write('\nEXCEPTION ERROR:' + str(e))
        logging.error('*****exception*********' + str(e))
    else:
        resultlog.write('Pass\n')

def startmon(resultlog, result_dir, namespace):
    '''
    This method starts the Coverage Monitor
    '''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', '
                    + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        VistA1 = connect_VistA(testname, result_dir, namespace)
        VistA1.startCoverage(routines=['SC*', 'SD*'])
    except TestHelper.TestError, e:
        resultlog.write(e.value)
        logging.error(testname + ' EXCEPTION ERROR: Unexpected test result')
    finally:
        '''
        Close Vista
        '''
        VistA1.write('^\r^\r^\r')
        VistA1.write('h\r')

def stopmon (resultlog, result_dir, humanreadable, namespace):
    '''
    This method stops the Coverage Monitor
    '''
    testname = sys._getframe().f_code.co_name
    resultlog.write('\n' + testname + ', '
                    + str(datetime.datetime.today()) + ': ')
    logging.debug('\n' + testname + ', ' + str(datetime.datetime.today()) + ': ')
    try:
        # Connect to VistA
        VistA1 = connect_VistA(testname, result_dir, namespace)
        path = (result_dir + '/' + timeStamped('Scheduling_coverage.txt'))
        VistA1.stopCoverage(path, humanreadable)
    except TestHelper.TestError, e:
        resultlog.write(e.value)
        logging.error(testname + ' EXCEPTION ERROR: Unexpected test result')
    finally:
        '''
        Close Vista
        '''
        VistA1.write('^\r^\r^\r')
        VistA1.write('h\r')

def timeStamped(fname, fmt='%Y-%m-%d-%H-%M-%S_{fname}'):
    '''
    This method appends a date/time stamp to a filename
    '''
    return datetime.datetime.now().strftime(fmt).format(fname=fname)

def connect_VistA(testname, result_dir, namespace):
    '''
    This method is used to establish the connection to VistA via ConnectToMUMPS
    '''
    logging.debug('Connect_VistA' + ', Namespace: ' + namespace)
    from OSEHRAHelper import ConnectToMUMPS, PROMPT
    VistA = ConnectToMUMPS(logfile=result_dir + '/' + timeStamped(testname + '.txt'), instance='', namespace=namespace)
    if VistA.type == 'cache':
        try:
            VistA.ZN(namespace)
        except IndexError, no_namechange:
            pass
    VistA.wait(PROMPT)
    return VistA
