#####################################################################################################################
## Tik Camera Overscan - Python Script
## Title: TIK Camera Overscan
## AUTHOR:	Arda Kutlu
## e-mail: ardakutlu@gmail.com
## Web: http://www.ardakutlu.com
## VERSION:1.0(Initial)
## CREATION DATE: 27.09.2017
## LAST MODIFIED DATE: 27.09.2017
##
## DESCRIPTION: A simple tool to overscan the camera render area. Works with vray phsical Camera as well
## INSTALL:
## Copy tik_cameraOverScan.py to user/maya/scripts folder
## Run these commands in python tab (or put them in a shelf:
## import tik_cameraOverscan
## tik_cameraOverscan.cameraOverscan().show()

#####################################################################################################################

import pymel.core as pm

import Qt
from Qt import QtWidgets, QtCore, QtGui
from maya import OpenMayaUI as omui

if Qt.__binding__ == "PySide":
    from shiboken import wrapInstance
    from Qt.QtCore import Signal
elif Qt.__binding__.startswith('PyQt'):
    from sip import wrapinstance as wrapInstance
    from Qt.Core import pyqtSignal as Signal
else:
    from shiboken2 import wrapInstance
    from Qt.QtCore import Signal

windowName = "Tik_OverScan"

def getMayaMainWindow():
    """
    Gets the memory adress of the main window to connect Qt dialog to it.
    Returns:
        (long) Memory Adress
    """
    win = omui.MQtUtil_mainWindow()
    ptr = wrapInstance(long(win), QtWidgets.QMainWindow)
    return ptr


class cameraOverscan(QtWidgets.QDialog):


    def __init__(self):
        for entry in QtWidgets.QApplication.allWidgets():
            try:
                if entry.objectName() == windowName:
                    entry.close()
            except (AttributeError, TypeError):
                pass
        parent = getMayaMainWindow()
        super(cameraOverscan, self).__init__(parent=parent)

        self.cameraList = []
        self.cameraNames = []
        self.setWindowTitle(windowName)
        self.setObjectName(windowName)
        self.buildUI()

    def buildUI(self):
        layout = QtWidgets.QVBoxLayout(self)

        self.cameraDropDown = QtWidgets.QComboBox()

        layout.addWidget(self.cameraDropDown)

        self.getSceneCameras()
        self.cameraDropDown.addItems(self.cameraNames)

        self.multiplierLb = QtWidgets.QLabel("Multiply Value")
        layout.addWidget(self.multiplierLb)

        self.multiplierSp = QtWidgets.QDoubleSpinBox()
        self.multiplierSp.setValue(1.0)
        layout.addWidget(self.multiplierSp)

        self.overScanBtn = QtWidgets.QPushButton("OverSiker")
        layout.addWidget(self.overScanBtn)
        # print self.cameraDropDown.currentIndex()
        self.overScanBtn.clicked.connect(self.calcOverscan)

        pass
        # layout = QtWidgets.QVBoxLayout(self)

    def getSceneCameras(self):

        self.cameraList = pm.ls(type="camera")
        self.cameraNames = []
        for c in self.cameraList:
            self.cameraNames.append(c.getParent().name())


    def calcOverscan(self):
        camera = self.cameraList[self.cameraDropDown.currentIndex()]
        mult = self.multiplierSp.value()
        print "mult", mult

        # selection = pm.ls(sl=True)
        # if len(selection) < 1:
        #     pm.error("nothing selected")
        #     return

        rEngine = pm.getAttr("defaultRenderGlobals.currentRenderer")
        print "render Engine", rEngine
        if rEngine == "vray":
            originalWidth = pm.getAttr("vraySettings.width")
            originalHeight = pm.getAttr("vraySettings.height")

        else:
            originalWidth = pm.getAttr("defaultResolution.width")
            originalHeight = pm.getAttr("defaultResolution.height")

        print "originalWidth: ", originalWidth
        print "originalHeight: ", originalHeight
        # camera = pm.ls(sl=True)[0]

        originalApertureWidth = camera.horizontalFilmAperture.get()
        originalApertureHeight = camera.verticalFilmAperture.get()

        newWidth = originalWidth * mult
        newHeight = originalHeight * mult
        overscanWidth = newWidth / originalWidth
        overscanHeight = newHeight / originalHeight
        newApertureWidth = originalApertureWidth * overscanWidth
        newApertureHeight = originalApertureHeight * overscanHeight

        camera.horizontalFilmAperture.set(newApertureWidth)
        camera.verticalFilmAperture.set(newApertureHeight)

        if rEngine == "vray":
            pm.setAttr("vraySettings.width", newWidth)
            pm.setAttr("vraySettings.height", newHeight)

        else:
            pm.setAttr("defaultResolution.width", newWidth)
            pm.setAttr("defaultResolution.height", newHeight)

