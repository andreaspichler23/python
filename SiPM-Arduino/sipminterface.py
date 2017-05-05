#!/bin/python
import sys
import os
import serial
import serial.tools.list_ports
import exceptions
import time

ACK = chr(0x06)
EOT = chr(0x04)

class DACOverflow(Exception):
    """Exception class for DAC out of range, raised if value exceeds 12 bit"""
    def __init__(self,value):
        self.status = "{0} is out of DAC range!".format(value)
    def __str__(self):
        return repr(self.status)

class DACUnderflow(Exception):
    """Exception class for DAC out of range, raised if value is below 0"""
    def __init__(self,value):
        self.status = "{0} is out of DAC range!".format(value)
    def __str__(self):
        return repr(self.status)

class ChannelError(Exception):
    """Exception is raised if channel number is nor valid in current setup"""
    def __init__(self,value):
        self.status = "{0} is out of range!".format(value)
    def __str__(self):
        return repr(self.status)

class BoardOpenError(Exception):
    """Exception is raised if serial connection couldn't be opened """
    def __init__(self,device):
        self.status = "Couldn't open SiPM board on {0}!".format(device)
    def __str__(self):
        return repr(self.status)

class TransmissionError(Exception):
    """Exception is raisen whenever a transmission failes """
    def __init__(self,value):
        self.status = value
    def __str__(self):
        return repr(self.status)

def checkusb(val):
    if "usb" in val[2]:
        return True
    else:
        return False

def getdevicelist():
    """This function returns a list of serial USB ports """
    portlist = serial.tools.list_ports.comports()
    #print portlist[4][2]
    #for i in range(len(portlist)):
    somelist = [i for i in portlist if checkusb(i)]
    #for i in range(len(portlist)):
    #    if "USB" not in portlist[i][2]:
    #        del portlist[i]
    #print somelist        
    return somelist


class sipm:
    """This class describes the control interface for the Arduino Leonardo
    SiPM boards.

    The command structure is:
    SG[channelbyte][gainhighbyte][gainlowbyte] - to set the gain of a channel
    ST[channelbyte][threshighbyte][threslowbyte] - to set the gain of a channel
    SV - saves the set values to the EEPROM
    G  - returns the number of channels connected to the board
    A  - appy the set values, send them to the sipm boards and activate them
    R  - load values from board
    returnvalue for everything except 'G' is always the ACK byte (0x06)
    'G' returns the channelnumber and ACK
    'R' returns two arrays, containing the gain and threshold values
    """
    def __init__(self, device):
        #print device
        self.ser = serial.Serial(device,9600,timeout=1)
        for i in range (10):
            if self.ser.isOpen():
                break
            else:
                time.sleep(0.1)
        if not self.ser.isOpen():
            raise BoardOpenError(device)
        self.ser.write('G\n')
        self.channelnumber = ord(self.ser.read(1)) + 1
        #print self.channelnumber
        val = self.ser.read(1)
        #print val
        if val != ACK:
            raise TransmissionError("Couldn't get channelnumber!")

    def __del__(self):
        self.ser.close()
    
    def check_value(self, value):
        if value>4095:
            raise DACOverflow(value)
        if value<0:
            raise DACUnderflow(value)

    def check_channel(self,value):
        if value not in range(self.channelnumber):
            raise ChannelError(value)
    
    def setgain(self,channel,value):
        self.check_value(value)
        self.check_channel(channel)
        lowbyte = value & 0xFF
        highbyte = value >> 8
        self.ser.write('S'+'G'+chr(channel)+chr(highbyte)+chr(lowbyte))
        byte = self.ser.read(1)
        if byte != ACK:
            raise TransmissionError("Couldn't set gain for channel {0}".format(channel))
    
    def setthreshold(self, channel, value):
        self.check_value(value)
        self.check_channel(channel)
        lowbyte = value & 0xFF
        highbyte = value >> 8
        self.ser.write('S'+'T'+chr(channel)+chr(highbyte)+chr(lowbyte))
        byte = self.ser.read(1)
        if byte != ACK:
            raise TransmissionError("Couldn't set threshold for channel {0}".format(channel))

    def savetoeeprom(self):
        self.ser.write("SV")
        time.sleep(5) # 5 seconds is the time it takes to write the EEPROM
        byte = self.ser.read(1)
        if byte != ACK:
            raise TransmissionError("Couldn't save to EEPROM")

    def applyvalues(self):
        self.ser.write("A")
        byte = self.ser.read(1)
        if byte != ACK:
            raise TransmissionError("Something strange happens, couldn't apply the set values!")

    def readvalues(self):
        self.ser.write("R")
        gbuffer = self.ser.read(2*(self.channelnumber))
        tbuffer = self.ser.read(2*(self.channelnumber))
        #print gbuffer, len(gbuffer)
        #print 
        #print tbuffer, len(tbuffer)
        gain = []
        threshold = []
        for i in range(0,2*self.channelnumber,2):
            #print ord(tbuffer[i]), ord(tbuffer[i+1])
            gain.append((ord(gbuffer[i])<<8) + ord(gbuffer[i+1]))
            threshold.append((ord(tbuffer[i])<<8) + ord(tbuffer[i+1]))
        byte = self.ser.read(1)
        #print threshold, len(threshold)
        #print threshold
        #print ord(byte)
        if (byte != EOT):
            raise TransmissionError("Data transmission not finished! check connected channels!") 
        return [gain,threshold]

    def mvtodacval(self, mv):
        pass
    def dacvaltomv(self, dacval):
        pass

# small test program
if __name__ == "__main__":
    devices = getdevicelist();
    print "devices:", devices
    s = sipm(devices[2][0])
    #s.setgain(200,800)
    print "Channelnumber=", s.channelnumber
    val = s.readvalues()
    #s.setthreshold(0,100)
    #s.setthreshold(1,200)
    #s.setthreshold(2,400)
    #s.setthreshold(3,800)
    print "Thresholds:", val[1]
    print "Gain values:", val[0]
