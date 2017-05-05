#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys 
from PyQt4 import QtCore
from PyQt4 import QtGui 
import sipminterface
import serial 
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

def main(): 
   
    app = QtGui.QApplication(sys.argv) 
    w = MyWindow() 
    w.show() 
    
    sys.exit(app.exec_()) 
 
class DeviceChooserPopup(QtGui.QDialog):
    def __init__(self, devicelist, parent=None, msg="Please choose the USB device to connect." ):
        self.value = ""
        QtGui.QDialog.__init__(self, parent)
        self.setWindowTitle('Device Chooser')
        self.label = QtGui.QLabel(self.tr(msg))
        self.combo = QtGui.QComboBox()
        for i in devicelist:
            self.combo.addItem(i[0])

        self.button = QtGui.QPushButton('Connect', self)
        self.abort = QtGui.QPushButton('Abort', self)

        vbox  =  QtGui.QVBoxLayout()
        hbox  =  QtGui.QHBoxLayout()
        vbox.addWidget(self.label)
        vbox.addWidget(self.combo)
        
        hbox.addWidget(self.button)
        hbox.addWidget(self.abort)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
       
        self.button.clicked.connect(self.connect)
        self.abort.clicked.connect(self.abortfun)
        
    def connect(self):
        self.value = self.combo.currentText()
        self.close()

    def getselesction(self):
        return self.value
        
    def abortfun(self):
        print "Closing"
        self.close() 
        exit(-1)
    
    

class MyWindow(QtGui.QWidget): 
    def __init__(self, *args): 
        QtGui.QWidget.__init__(self, *args) 

        #### init serial connection!
        self.devices = sipminterface.getdevicelist();
        #print devices[0][0]
        d = DeviceChooserPopup(devicelist=self.devices)
        d.exec_()
        dev = d.getselesction()
        while dev == "":
            del d
            d = DeviceChooserPopup(devicelist=self.devices, msg="You HAVE TO choose a device! ")
            d.exec_()
            dev = d.getselesction()
        self.s = sipminterface.sipm(str(dev))
        self.numofboards = self.s.channelnumber/2
        ####

        # create objects
        label1 =  QtGui.QLabel(self.tr("""<center><span style=" font-size:14pt; font-weight:600; color:#aa0000;">SiPM Control Program</span></center>""")) 

        label2 =  QtGui.QLabel(self.tr("""<center><br>if you change the values, don't forget to send then to the Arduino Board by <br>pressing the "Set Values w/o activating" or "Set and Apply Values" buttons. <br></center>"""))
        #self.le =  QtGui.QLineEdit()
        #self.te =  QtGui.QTextEdit()
        self.sld = []
        self.edit = []
        
        # layout
        layout =  QtGui.QVBoxLayout(self)
        layout.addWidget(label1)
        layout.addWidget(label2)
        #layout.addWidget(self.le)
        #layout.addWidget(self.te)

        for i in range(self.numofboards):
            vbox = self.makeboardbox(i+1)
            layout.addLayout(vbox)
            
        
        #vbox2 = self.makeboardbox(2)
        #layout.addLayout(vbox2)
        #vbox3 = self.makeboardbox(3)
        #layout.addLayout(vbox3)
        mainWidget = QtGui.QWidget()
        mainWidget.setLayout(layout)  
        scrollWidget = QtGui.QScrollArea()
        scrollWidget.setWidget(mainWidget)
        scrollWidget.setWidgetResizable(True)
        
        mainLayout = QtGui.QVBoxLayout(self)
        mainLayout.addWidget(scrollWidget)

        buttonbox  =  QtGui.QHBoxLayout()
        buttonbox2 =  QtGui.QHBoxLayout()
        buttonbox3 =  QtGui.QHBoxLayout()
        self.buttoneeprom = QtGui.QPushButton('Save to EEPROM', self)
        self.buttonApply = QtGui.QPushButton('Set and Apply Values', self)
        self.buttonSet = QtGui.QPushButton('Set Values w/o activating', self)
        self.buttonApplyOnly = QtGui.QPushButton('Activate', self)
        self.buttonLoad = QtGui.QPushButton('Load Values', self)
        buttonbox.addWidget(self.buttoneeprom)
        buttonbox3.addWidget(self.buttonApply)
        buttonbox.addWidget(self.buttonLoad)
        buttonbox2.addWidget(self.buttonSet)
        buttonbox2.addWidget(self.buttonApplyOnly)
        
        mainLayout.addLayout(buttonbox)
        mainLayout.addLayout(buttonbox2)
        mainLayout.addLayout(buttonbox3)
        self.setLayout(mainLayout)
        #self.setLayout(layout) 

        # load values from sipmboards
        self.readvalues()

        # create connection
        #self.connect(self.le, QtCore.SIGNAL("returnPressed(void)"),
        #             self.run_command)
        
        for i in range(self.numofboards):
            self.edit[i*4+0].returnPressed.connect(lambda i=i: self.boxtoslider(i,0))
            self.edit[i*4+1].returnPressed.connect(lambda i=i: self.boxtoslider(i,1))
            self.edit[i*4+2].returnPressed.connect(lambda i=i: self.boxtoslider(i,2))
            self.edit[i*4+3].returnPressed.connect(lambda i=i: self.boxtoslider(i,3))
            self.sld[i*4+0].valueChanged.connect(lambda j,i=i: self.slidertobox(i,0))
            self.sld[i*4+1].valueChanged.connect(lambda j,i=i: self.slidertobox(i,1))
            self.sld[i*4+2].valueChanged.connect(lambda j,i=i: self.slidertobox(i,2))
            self.sld[i*4+3].valueChanged.connect(lambda j,i=i: self.slidertobox(i,3))
          
        self.buttonLoad.clicked.connect(self.readvalues)
        self.buttonSet.clicked.connect(self.setonly)
        self.buttonApplyOnly.clicked.connect(self.applyonly)
        self.buttonApply.clicked.connect(self.setandapply)
        self.buttoneeprom.clicked.connect(self.savetoeeprom)
        #self.connect(self.edit[0], QtCore.SIGNAL("returnPressed(void)"),
        #             lambda : self.boxtoslider(0,0))
        #self.edit[0].returnPressed.connect(lambda : self.boxtoslider(0,0))
        #self.sld[0].valueChanged.connect(lambda : self.slidertobox(0,0))
        #self.connect(self.sld[0], QtCore.SIGNAL("sliderMoved(void)"),
        #             lambda : self.slidertobox(0,0))

    def makeboardbox(self, number):
        label = QtGui.QLabel("SiPM Board {0}:".format(number))
        g1 = QtGui.QLabel("Gain Ch {0}:       ".format((number-1)*2))
        g2 = QtGui.QLabel("Gain Ch {0}:       ".format((number-1)*2+1))
        t1 = QtGui.QLabel("Threshold Ch {0}:".format((number-1)*2))
        t2 = QtGui.QLabel("Threshold Ch {0}:".format((number-1)*2+1))

        sld1 = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        sld1.setFocusPolicy(QtCore.Qt.NoFocus)
        sld1.setMinimum(0)
        sld1.setMaximum(4095)
        sld1.setSingleStep(1)

        sld2 = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        sld2.setFocusPolicy(QtCore.Qt.NoFocus)
        sld2.setMinimum(0)
        sld2.setMaximum(4095)
        sld2.setSingleStep(1)

        sld3 = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        sld3.setFocusPolicy(QtCore.Qt.NoFocus) 
        sld3.setMinimum(0)
        sld3.setMaximum(4095)
        sld3.setSingleStep(1)

        sld4 = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        sld4.setFocusPolicy(QtCore.Qt.NoFocus)
        sld4.setMinimum(0)
        sld4.setMaximum(4095)
        sld4.setSingleStep(1)
        self.sld.append(sld1)
        self.sld.append(sld2)
        self.sld.append(sld3)
        self.sld.append(sld4)

        edit1 = QtGui.QLineEdit()
        edit1.setMaximumWidth(100)
        edit2 = QtGui.QLineEdit()
        edit2.setMaximumWidth(100)
        edit3 = QtGui.QLineEdit()
        edit3.setMaximumWidth(100)
        edit4 = QtGui.QLineEdit()
        edit4.setMaximumWidth(100)
        self.edit.append(edit1)
        self.edit.append(edit2)
        self.edit.append(edit3)
        self.edit.append(edit4)

        hbox1 = QtGui.QHBoxLayout()
        hbox1.addWidget(g1)
        hbox1.addWidget(sld1)
        hbox1.addWidget(edit1)
        hbox1.addWidget(g2)
        hbox1.addWidget(sld2)
        hbox1.addWidget(edit2)

        hbox2 = QtGui.QHBoxLayout()
        hbox2.addWidget(t1)
        hbox2.addWidget(sld3)
        hbox2.addWidget(edit3)
        hbox2.addWidget(t2)
        hbox2.addWidget(sld4)
        hbox2.addWidget(edit4)

        tframe = QtGui.QFrame()
        tframe.setFrameShape(QtGui.QFrame.HLine)
        tframe.setFrameShadow(QtGui.QFrame.Sunken)

        vbox  = QtGui.QVBoxLayout()
        vbox.addWidget(label)
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addWidget(tframe)
        vbox.setMargin(1)

        return vbox
        

#    def run_command(self):
#        cmd = str(self.le.text())
#        stdouterr = os.popen4(cmd)[1].read()
#        self.te.setText(stdouterr)

    def slidertobox(self, num, val):
        self.edit[num*4+val].setText(str(self.sld[num*4+val].sliderPosition()))
        #print num, val, num*4+val       
        #self.edit[num*4+val].setText("asd")
        
    def boxtoslider(self, num, val):
        try:
            self.s.check_value(int(self.edit[num*4+val].text()))
        except sipminterface.DACOverflow, e:
            QtGui.QMessageBox.warning(self,
                            "Warning",
                            "The entered value is too high! Defaulting to maximum.\n{0}".format(e))
        except sipminterface.DACUnderflow, e:
            QtGui.QMessageBox.warning(self,
                            "Warning",
                            "The entered value is too high! Defaulting to zero.\n{0}".format(e))

        self.sld[num*4+val].setSliderPosition(int(self.edit[num*4+val].text())) 
        #self.sld[num*4+val].setSliderPosition(2000)
    
    def readvalues(self):
        val=0
        try:
            val = self.s.readvalues()
        except serial.serialutil.SerialException, e:
            QtGui.QMessageBox.critical(self,
                            "Error",
                            "The connection to the device is lost!\n Check the connection and/or try to reset the arduino board.\n{0}".format(e))
        #print val[0], val[1]
        for i in range(self.numofboards):
            self.edit[i*4+0].setText(str(val[0][i*2+0]))
            self.edit[i*4+1].setText(str(val[0][i*2+1]))
            self.edit[i*4+2].setText(str(val[1][i*2+0]))
            self.edit[i*4+3].setText(str(val[1][i*2+1]))
            self.sld[i*4+0].setSliderPosition(val[0][i*2+0])
            self.sld[i*4+1].setSliderPosition(val[0][i*2+1])
            self.sld[i*4+2].setSliderPosition(val[1][i*2+0])
            self.sld[i*4+3].setSliderPosition(val[1][i*2+1])
        
            
    def setonly(self):
        try:
            for i in range(self.numofboards):
                self.s.setgain(i*2+0,int(self.edit[i*4+0].text()))
                self.s.setgain(i*2+1,int(self.edit[i*4+1].text()))
                self.s.setthreshold(i*2+0,int(self.edit[i*4+2].text()))
                self.s.setthreshold(i*2+1,int(self.edit[i*4+3].text()))
        except serial.serialutil.SerialException, e:
            QtGui.QMessageBox.critical(self,
                                       "Error",
                                       "The connection to the device is lost!\n Check the connection and/or try to reset the arduino board.\n{0}".format(e))


    def applyonly(self):
        try:
            self.s.applyvalues()
        except serial.serialutil.SerialException, e:
            QtGui.QMessageBox.critical(self,
                                       "Error",
                                       "The connection to the device is lost!\n Check the connection and/or try to reset the arduino board.\n{0}".format(e))


    def setandapply(self):
        try:
            self.setonly()
            self.applyonly()
        except serial.serialutil.SerialException, e:
            QtGui.QMessageBox.critical(self,
                                       "Error",
                                       "The connection to the device is lost!\n Check the connection and/or try to reset the arduino board.\n{0}".format(e))


    def savetoeeprom(self):
        reply = QtGui.QMessageBox.question(self, 'Save to EEPROM',
            "This will take 5 seconds!", QtGui.QMessageBox.Yes | 
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)
        try:
            if reply == QtGui.QMessageBox.Yes:
                self.s.savetoeeprom()
            else:
                pass
        except serial.serialutil.SerialException, e:
            QtGui.QMessageBox.critical(self,
                                       "Error",
                                       "The connection to the device is lost!\n Check the connection and/or try to reset the arduino board.\n{0}".format(e))
        
if __name__ == "__main__": 
    main()
