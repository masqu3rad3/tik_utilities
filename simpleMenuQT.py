
import pymel.core as pm

import Qt
from Qt import QtWidgets, QtCore, QtGui
from maya import OpenMayaUI as omui

import math
if Qt.__binding__ == "PySide":
    from shiboken import wrapInstance
    from Qt.QtCore import Signal
elif Qt.__binding__.startswith('PyQt'):
    from sip import wrapinstance as wrapInstance
    from Qt.Core import pyqtSignal as Signal
else:
    from shiboken2 import wrapInstance
    from Qt.QtCore import Signal

windowName = "TestUI"

def getMayaMainWindow():
    """
    Gets the memory adress of the main window to connect Qt dialog to it.
    Returns:
        (long) Memory Adress
    """
    win = omui.MQtUtil_mainWindow()
    ptr = wrapInstance(long(win), QtWidgets.QMainWindow)
    return ptr

class testUI(QtWidgets.QDialog):
    def __init__(self):
        for entry in QtWidgets.QApplication.allWidgets():
            if entry.objectName() == windowName:
                entry.close()
        parent = getMayaMainWindow()
        super(testUI, self).__init__(parent=parent)
        
        self.setWindowTitle(windowName)
        self.setObjectName(windowName)
        self.buildUI()
    
    def buildUI(self):

        ## This is the main layout
        layout = QtWidgets.QVBoxLayout(self)

        #   ___       _
        #  / __> ___ <_>._ _  ___
        #  \__ \| . \| || ' |/ ._>
        #  <___/|  _/|_||_|_|\___.
        #       |_|

        spineLabel = QtWidgets.QLabel("Spine Section",minimumSize=(QtCore.QSize(20,18)),parent=self)
        spineLabel.setFont(QtGui.QFont("Arial", weight=QtGui.QFont.Bold))
        spineLabel.setAlignment(QtCore.Qt.AlignCenter)
        spineLabel.setFrameStyle(QtWidgets.QFrame.Panel)
        spineDefine = QtWidgets.QPushButton("Define", minimumSize=(QtCore.QSize(80,50)), parent=self)
        spineCreate = QtWidgets.QPushButton("Create", minimumSize=(QtCore.QSize(80,50)), parent=self)
        spineSegLb = QtWidgets.QLabel("Segments")
        spineSegInt = QtWidgets.QSpinBox()

        spineLayout = QtWidgets.QVBoxLayout()
        layout.addLayout(spineLayout)
        spineLayout.addWidget(spineLabel)

        spineButtonLayout = QtWidgets.QHBoxLayout()
        spineButtonLayout.addWidget(spineDefine)
        spineButtonLayout.addWidget(spineCreate)
        spineLayout.addLayout(spineButtonLayout)

        spineSegLayout = QtWidgets.QVBoxLayout()
        spineSegLayout.addWidget(spineSegLb)
        spineSegLayout.addWidget(spineSegInt)
        spineButtonLayout.addLayout(spineSegLayout)

        #   ___
        #  | . | _ _ ._ _ _
        #  |   || '_>| ' ' |
        #  |_|_||_|  |_|_|_|
        #

        ## These are the all Widgets in the Dialog
        armLabel = QtWidgets.QLabel("Arm Section",minimumSize=(QtCore.QSize(20,18)),parent=self)
        armLabel.setFont(QtGui.QFont("Arial", weight=QtGui.QFont.Bold))
        armLabel.setAlignment(QtCore.Qt.AlignCenter)
        armLabel.setFrameStyle(QtWidgets.QFrame.Panel)
        armDefine = QtWidgets.QPushButton("Define", minimumSize=(QtCore.QSize(80,50)), parent=self)
        armCreate = QtWidgets.QPushButton("Create", minimumSize=(QtCore.QSize(80,50)), parent=self)

        radioGrpArm = QtWidgets.QButtonGroup(layout)
        armSideLeft = QtWidgets.QRadioButton("Left",parent=self)
        armSideRight = QtWidgets.QRadioButton("Right",parent=self)
        armSideBoth = QtWidgets.QRadioButton("Both", parent=self)
        radioGrpArm.addButton(armSideLeft)
        radioGrpArm.addButton(armSideRight)
        armSideLeft.setChecked(True)

        ## These are the layouts
        # fingerWidget = QtWidgets.QWidget()
        armLayout = QtWidgets.QVBoxLayout()
        layout.addLayout(armLayout)
        armLayout.addWidget(armLabel)

        ## Create FingerLayout
        armButtonLayout = QtWidgets.QHBoxLayout()
        ## Buttons
        armButtonLayout.addWidget(armDefine)
        armButtonLayout.addWidget(armCreate)
        ## put Buttons layout under fingerLayout
        armLayout.addLayout(armButtonLayout)
        ## layout for Radio Buttons
        armRadioLayout = QtWidgets.QHBoxLayout()
        ## Radio Buttons
        armRadioLayout.addWidget(armSideLeft)
        armRadioLayout.addWidget(armSideRight)
        ## put it under (next to) the buttons layout
        armButtonLayout.addLayout(armRadioLayout)



        #   ___  _
        #  | __><_>._ _  ___  ___  _ _
        #  | _> | || ' |/ . |/ ._>| '_>
        #  |_|  |_||_|_|\_. |\___.|_|
        #               <___'

        ## These are the all Widgets in the Dialog
        fingerLabel = QtWidgets.QLabel("Finger Section",minimumSize=(QtCore.QSize(20,18)),parent=self)
        fingerLabel.setFont(QtGui.QFont("Arial", weight=QtGui.QFont.Bold))
        fingerLabel.setAlignment(QtCore.Qt.AlignCenter)
        fingerLabel.setFrameStyle(QtWidgets.QFrame.Panel)
        fingerDefine = QtWidgets.QPushButton("Define", minimumSize=(QtCore.QSize(80,50)), parent=self)
        fingerCreate = QtWidgets.QPushButton("Create", minimumSize=(QtCore.QSize(80,50)), parent=self)

        radioGrpFinger = QtWidgets.QButtonGroup(layout)
        fingerSideLeft = QtWidgets.QRadioButton("Left",parent=self)
        fingerSideRight = QtWidgets.QRadioButton("Right",parent=self)
        radioGrpFinger.addButton(fingerSideLeft)
        radioGrpFinger.addButton(fingerSideRight)
        fingerSideLeft.setChecked(True)

        fingerIsThumbChk = QtWidgets.QCheckBox("Thumb", parent=self)

        ## These are the layouts
        fingerLayout = QtWidgets.QVBoxLayout()
        layout.addLayout(fingerLayout)
        fingerLayout.addWidget(fingerLabel)

        ## Create FingerLayout
        fingerButtonLayout = QtWidgets.QHBoxLayout()
        ## Buttons
        fingerButtonLayout.addWidget(fingerDefine)
        fingerButtonLayout.addWidget(fingerCreate)
        ## put Buttons layout under fingerLayout
        fingerLayout.addLayout(fingerButtonLayout)
        ## layout for Radio Buttons
        fingerRadioLayout = QtWidgets.QVBoxLayout()
        ## Radio Buttons
        fingerRadioLayout.addWidget(fingerSideLeft)
        fingerRadioLayout.addWidget(fingerSideRight)
        ## put it under (next to) the buttons layout
        fingerButtonLayout.addLayout(fingerRadioLayout)

        fingerButtonLayout.addWidget(fingerIsThumbChk)



        #   _
        #  | |   ___  ___
        #  | |_ / ._>/ . |
        #  |___|\___.\_. |
        #            <___'

        ## These are the all Widgets in the Dialog
        legLabel = QtWidgets.QLabel("Leg Section",minimumSize=(QtCore.QSize(20,18)),parent=self)
        legLabel.setFont(QtGui.QFont("Arial", weight=QtGui.QFont.Bold))
        legLabel.setAlignment(QtCore.Qt.AlignCenter)
        legLabel.setFrameStyle(QtWidgets.QFrame.Panel)
        legDefine = QtWidgets.QPushButton("Define", minimumSize=(QtCore.QSize(80,50)), parent=self)
        legCreate = QtWidgets.QPushButton("Create", minimumSize=(QtCore.QSize(80,50)), parent=self)

        radioGrpLeg = QtWidgets.QButtonGroup(layout)
        legSideLeft = QtWidgets.QRadioButton("Left",parent=self)
        legSideRight = QtWidgets.QRadioButton("Right",parent=self)
        radioGrpLeg.addButton(legSideLeft)
        radioGrpLeg.addButton(legSideRight)
        legSideLeft.setChecked(True)

        ## These are the layouts
        # fingerWidget = QtWidgets.QWidget()
        legLayout = QtWidgets.QVBoxLayout()
        layout.addLayout(legLayout)
        legLayout.addWidget(legLabel)

        ## Create FingerLayout
        legButtonLayout = QtWidgets.QHBoxLayout()
        ## Buttons
        legButtonLayout.addWidget(legDefine)
        legButtonLayout.addWidget(legCreate)
        ## put Buttons layout under fingerLayout
        legLayout.addLayout(legButtonLayout)
        ## layout for Radio Buttons
        legRadioLayout = QtWidgets.QVBoxLayout()
        ## Radio Buttons
        legRadioLayout.addWidget(legSideLeft)
        legRadioLayout.addWidget(legSideRight)
        ## put it under (next to) the buttons layout
        legButtonLayout.addLayout(legRadioLayout)






        #   ___      _  _
        #  |_ _|___ <_>| |
        #   | |<_> || || |
        #   |_|<___||_||_|
        #



        #   _ _            _     _    _ _              _
        #  | \ | ___  ___ | |__ < >  | | | ___  ___  _| |
        #  |   |/ ._>/ | '| / / /.\/ |   |/ ._><_> |/ . |
        #  |_\_|\___.\_|_.|_\_\ \_/\ |_|_|\___.<___|\___|
        #


        # searchLabel = QtWidgets.QLabel("Seach Filter: ")
        # layout.addWidget(searchLabel)
        # searchNameField = QtWidgets.QLineEdit()
        # # self.searchNameField.textEdited.connect( <NEED TO CALL A FUNCTION> )
        # layout.addWidget(searchNameField)
        # defFingerBtn.clicked.connect(self.setColor)

    def testPop(self):
        exportWindow, ok = QtWidgets.QInputDialog.getItem(self, 'Text Input Dialog',
                                                          'SAVE BEFORE PROCEED\n\nANY UNSAVED WORK WILL BE LOST\n\nEnter Asset Name:')
        if ok:
            print "popped"

    def setColor(self):
        color = QtWidgets.QColorDialog.getColor(QtCore.Qt.green, self)
        if color.isValid():
            print(color.name())
            print(QtGui.QPalette(color))
            print color

    def wheelEvent(self, event):
        # print event.delta()
        t =(math.pow(1.2, event.delta() / 120.0))
        if event.modifiers() == QtCore.Qt.ControlModifier:
            print t


# testUI().show()
        
