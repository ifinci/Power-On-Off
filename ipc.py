'''
    ipc.py
    
    INTRODUCTION:
        This module implements the control of IPC device over serial. This in
        turn is used to control the power of a connected device.
        
        The basic API of the IPC device, is documented in "IPC API.txt". Please
        note that this is my understanding of the API, as I didn't found any
        official documentation.
    CHANGE LOG:
        Version 1.0: 27/9/2011
            first working version 
'''
__version__ = '1.0'
__author__ = "Ilan Finci (Ilan@Finci.org)"
__date__ = '27-Sep-2011'

__info__ = '''
    Version: ''' + __version__ + '''
    Author: ''' + __author__ + '''
    Date: ''' + __date__ + '''
'''
   
import time

import serial

class IPC (object) :
    # API commands:
    IPC_STATUS_CMD = "*?PS"
    IPC_POWER_ON_CMD = "*PON"
    IPC_POWER_OFF_CMD = "*POF"
    
    def __init__(self, inPort):
        self._serial = serial.Serial(
            port=inPort,
            baudrate=300,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS
        )
    
    def close(self):
        self._serial.close()
        
    def sendCommand(self, cmd):
        self._serial.write(cmd + "\n")
        out = ''
        # let's wait half a second before reading output (let's give device time to answer)
        time.sleep(0.5)
        while self._serial.inWaiting() > 0:
            out += self._serial.read(1)
        #strip our command out of the output.
        #  strip out the string that we wrote, if it's there
        strlen = len(cmd)
        if out and out[:strlen] == cmd:
            out = out[strlen:]
        return(out)
    
        
    def powerOn(self):
        res = self.sendCommand(self.IPC_POWER_ON_CMD)
        
    def powerOff(self):
        self.sendCommand(self.IPC_POWER_OFF_CMD)

    def getStatus(self):
        res = self.sendCommand(self.IPC_STATUS_CMD)
        return (res)
        
    def getVersion(self):
        res = self.getStatus()
        return res[:3]
    
    def getPowerStatus(self):
        res = self.getStatus()
        return res[3] == "1"
#------------- End of IPC class -----------------------
        
# unit testing for IPC:
import unittest
class IPCtests(unittest.TestCase):
    def setUp(self): 
        self._ipc = IPC("COM18")
    def tearDown(self):
        self._ipc.close()
        
    def test01_getStatus(self):
        ver = self._ipc.getVersion()
        self.assertEqual("2.6", ver)
        
    def test02_powerOn(self):
        self._ipc.powerOn()
        status = self._ipc.getPowerStatus()
        self.assertEqual(status, True)
        
    def test03_powerOff(self):
        self._ipc.powerOff()
        status = self._ipc.getPowerStatus()
        self.assertEqual(status, False)
        
if __name__ == "__main__":
    unittest.main()
    