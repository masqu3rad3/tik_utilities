#####################################################################################################################
## Tik Path Motion - Python Script
## Title: TIK Path Motion
## AUTHOR:	Arda Kutlu
## e-mail: ardakutlu@gmail.com
## Web: http://www.ardakutlu.com
## VERSION:1.0(Initial)
## CREATION DATE: 05.04.2018
## LAST MODIFIED DATE: 05.04.2018
##
## DESCRIPTION: A utility tool to attach multiple objects to a path with equal distance.
## INSTALL:
## Copy tik_cameraOverScan.py to user/maya/scripts folder
## Run these commands in python tab (or put them in a shelf:
## import tik_pathMotion
## tik_pathMotion.pathMotion().show()
## Known Issues:
    # Undo is not working due to a bug with python wrapping of path animation command
## TODO: Right now the objects are distributed with the selection order. Random distribution will be added

#####################################################################################################################

import pymel.core as pm
import pymel.core.datatypes as dt

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

def alignTo(sourceObj=None, targetObj=None, mode=0, sl=False, o=(0, 0, 0)):
    offset = dt.Vector(o)
    if sl == True:
        selection = pm.ls(sl=True)
        if not len(selection) == 2:
            pm.error("select exactly 2 objects")
            return
        sourceObj = selection[0]
        targetObj = selection[1]
    if not sourceObj or not targetObj:
        pm.error("No source and/or target object defined")
        return
    if mode == 0:
        targetTranslation = pm.xform(targetObj, query=True, worldSpace=True, translation=True)
        pm.xform(sourceObj, worldSpace=True, translation=targetTranslation)
    if mode == 1:
        targetRotation = pm.xform(targetObj, query=True, worldSpace=True, rotation=True)
        pm.xform(sourceObj, worldSpace=True, rotation=targetRotation + offset)
    if mode == 2:
        targetMatrix = pm.xform(targetObj, query=True, worldSpace=True, matrix=True)
        pm.xform(sourceObj, worldSpace=True, matrix=targetMatrix)

def getMayaMainWindow():
    """
    Gets the memory adress of the main window to connect Qt dialog to it.
    Returns:
        (long) Memory Adress
    """
    win = omui.MQtUtil_mainWindow()
    ptr = wrapInstance(long(win), QtWidgets.QMainWindow)
    return ptr


class PathMotion(QtWidgets.QDialog):


    def __init__(self):
        for entry in QtWidgets.QApplication.allWidgets():
            if entry.objectName() == "pathmotion_Dialog":
                entry.close()
        parent = getMayaMainWindow()
        super(PathMotion, self).__init__(parent=parent)

        self.setObjectName(("pathmotion_Dialog"))
        self.resize(337, 363)
        self.setWindowTitle(("PathMotion"))
        self.buildUI()

        self.nametemplate = None
        self.masterController = None
        self.controllerAttribute = "driver"
        self.objectList = []
        self.pathCurveList = []
        self.count = 10
        self.preInfinity = 0
        self.postInfinity = 0


    def buildUI(self):

        self.infinityList = ["Constant", "Linear", "Cycle", "Cycle with Offset", "Oscillate"]
        self.infinityDict = {"Constant":0, "Linear":1, "Cycle":3, "Cycle with Offset":4, "Oscillate":5}

        self.mastercontroller_lineEdit = QtWidgets.QLineEdit(self)
        self.mastercontroller_lineEdit.setGeometry(QtCore.QRect(120, 50, 141, 21))
        self.mastercontroller_lineEdit.setToolTip(("If none defined, one will be created automatically"))
        self.mastercontroller_lineEdit.setText((""))
        self.mastercontroller_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.mastercontroller_lineEdit.setReadOnly(True)
        self.mastercontroller_lineEdit.setPlaceholderText(("Define a master controller"))
        self.mastercontroller_lineEdit.setObjectName(("mastercontroller_lineEdit"))

        self.mastercontroller_pushButton = QtWidgets.QPushButton(self)
        self.mastercontroller_pushButton.setGeometry(QtCore.QRect(270, 50, 41, 21))
        self.mastercontroller_pushButton.setToolTip(("If none defined, one will be created automatically"))
        self.mastercontroller_pushButton.setText(("< Get"))
        self.mastercontroller_pushButton.setObjectName(("mastercontroller_pushButton"))
        self.mastercontroller_pushButton.setFocus()

        self.mastercontroller_label = QtWidgets.QLabel(self)
        self.mastercontroller_label.setGeometry(QtCore.QRect(20, 50, 91, 21))
        self.mastercontroller_label.setText(("Master Controller:"))
        self.mastercontroller_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.mastercontroller_label.setObjectName(("mastercontroller_label"))

        self.objects_label = QtWidgets.QLabel(self)
        self.objects_label.setGeometry(QtCore.QRect(20, 110, 91, 19))
        self.objects_label.setText(("Object(s):"))
        self.objects_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.objects_label.setObjectName(("objects_label"))

        self.objects_lineEdit = QtWidgets.QLineEdit(self)
        self.objects_lineEdit.setGeometry(QtCore.QRect(120, 110, 141, 19))
        self.objects_lineEdit.setToolTip(("If none, only locators will be placed along the curve"))
        self.objects_lineEdit.setText((""))
        self.objects_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.objects_lineEdit.setReadOnly(True)
        self.objects_lineEdit.setPlaceholderText(("Define object(s)"))
        self.objects_lineEdit.setObjectName(("objects_lineEdit"))

        self.objects_pushButton = QtWidgets.QPushButton(self)
        self.objects_pushButton.setGeometry(QtCore.QRect(270, 110, 41, 19))
        self.objects_pushButton.setToolTip(("If none, only locators will be placed along the curve"))
        self.objects_pushButton.setText(("< Get"))
        self.objects_pushButton.setObjectName(("objects_pushButton"))

        self.pathcurve_label = QtWidgets.QLabel(self)
        self.pathcurve_label.setGeometry(QtCore.QRect(20, 140, 91, 19))
        self.pathcurve_label.setText(("Path Curve(s):"))
        self.pathcurve_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.pathcurve_label.setObjectName(("pathcurve_label"))

        self.pathcurve_lineEdit = QtWidgets.QLineEdit(self)
        self.pathcurve_lineEdit.setGeometry(QtCore.QRect(120, 140, 141, 19))
        self.pathcurve_lineEdit.setToolTip(("at least one curve is required"))
        self.pathcurve_lineEdit.setText((""))
        self.pathcurve_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.pathcurve_lineEdit.setReadOnly(True)
        self.pathcurve_lineEdit.setPlaceholderText(("Define path curve(s)"))
        self.pathcurve_lineEdit.setObjectName(("pathcurve_lineEdit"))

        self.pathcurve_pushButton = QtWidgets.QPushButton(self)
        self.pathcurve_pushButton.setGeometry(QtCore.QRect(270, 140, 41, 19))
        self.pathcurve_pushButton.setToolTip(("at least one curve is required"))
        self.pathcurve_pushButton.setText(("< Get"))
        self.pathcurve_pushButton.setObjectName(("pathcurve_pushButton"))

        self.count_spinBox = QtWidgets.QSpinBox(self)
        self.count_spinBox.setGeometry(QtCore.QRect(120, 170, 51, 20))
        self.count_spinBox.setMinimum(1)
        self.count_spinBox.setMaximum(9999)
        self.count_spinBox.setProperty("value", 10)
        self.count_spinBox.setObjectName(("count_spinBox"))

        self.count_label = QtWidgets.QLabel(self)
        self.count_label.setGeometry(QtCore.QRect(20, 170, 90, 19))
        self.count_label.setText(("Count:"))
        self.count_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.count_label.setObjectName(("count_label"))

        self.preinfinity_label = QtWidgets.QLabel(self)
        self.preinfinity_label.setGeometry(QtCore.QRect(20, 200, 90, 19))
        self.preinfinity_label.setText(("Pre-Infinity:"))
        self.preinfinity_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.preinfinity_label.setObjectName(("preinfinity_label"))

        self.postinfinity_label = QtWidgets.QLabel(self)
        self.postinfinity_label.setGeometry(QtCore.QRect(20, 230, 90, 19))
        self.postinfinity_label.setText(("Post-Infinity:"))
        self.postinfinity_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.postinfinity_label.setObjectName(("postinfinity_label"))

        self.preinfinity_comboBox = QtWidgets.QComboBox(self)
        self.preinfinity_comboBox.setGeometry(QtCore.QRect(120, 200, 111, 20))
        self.preinfinity_comboBox.setObjectName(("preinfinity_comboBox"))
        self.preinfinity_comboBox.addItems(self.infinityList)

        self.postinfinity_comboBox = QtWidgets.QComboBox(self)
        self.postinfinity_comboBox.setGeometry(QtCore.QRect(120, 230, 111, 20))
        self.postinfinity_comboBox.setObjectName(("postinfinity_comboBox"))
        self.postinfinity_comboBox.addItems(self.infinityList)
        self.postinfinity_comboBox.setCurrentIndex(2)

        self.nametemplate_label = QtWidgets.QLabel(self)
        self.nametemplate_label.setGeometry(QtCore.QRect(20, 20, 91, 21))
        self.nametemplate_label.setText(("Name Template:"))
        self.nametemplate_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.nametemplate_label.setObjectName(("nametemplate_label"))

        self.nametemplate_lineEdit = QtWidgets.QLineEdit(self)
        self.nametemplate_lineEdit.setGeometry(QtCore.QRect(120, 20, 141, 21))
        self.nametemplate_lineEdit.setToolTip(("If none defined, default namings will be used"))
        self.nametemplate_lineEdit.setText((""))
        self.nametemplate_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.nametemplate_lineEdit.setReadOnly(False)
        self.nametemplate_lineEdit.setPlaceholderText(("Define a unique name"))
        self.nametemplate_lineEdit.setObjectName(("nametemplate_lineEdit"))

        self.controllerattr_label = QtWidgets.QLabel(self)
        self.controllerattr_label.setGeometry(QtCore.QRect(20, 80, 91, 21))
        self.controllerattr_label.setText(("Controller Attr:"))
        self.controllerattr_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.controllerattr_label.setObjectName(("controllerattr_label"))

        self.controllerattr_lineEdit = QtWidgets.QLineEdit(self)
        self.controllerattr_lineEdit.setGeometry(QtCore.QRect(120, 80, 141, 21))
        self.controllerattr_lineEdit.setToolTip(("If not specified a custom attribute named \"driver\" will be used"))
        self.controllerattr_lineEdit.setText((""))
        self.controllerattr_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.controllerattr_lineEdit.setReadOnly(False)
        self.controllerattr_lineEdit.setPlaceholderText(("Name for custom Attirubte"))
        self.controllerattr_lineEdit.setObjectName(("controllerattr_lineEdit"))

        self.parametriclength_checkBox = QtWidgets.QCheckBox("Parametric Length", self)
        self.parametriclength_checkBox.setGeometry(QtCore.QRect(120, 260, 111, 20))
        self.parametriclength_checkBox.setChecked(True)

        self.follow_checkBox = QtWidgets.QCheckBox("Follow", self)
        self.follow_checkBox.setGeometry(QtCore.QRect(120, 280, 111, 20))
        self.follow_checkBox.setChecked(True)

        self.create_pushButton = QtWidgets.QPushButton(self)
        self.create_pushButton.setGeometry(QtCore.QRect(30, 310, 281, 31))
        self.create_pushButton.setText(("Create Path Objects"))
        self.create_pushButton.setObjectName(("create_pushButton"))

        self.create_pushButton.clicked.connect(self.createPathMotion)
        self.mastercontroller_pushButton.clicked.connect(self.onGetMasterController)
        self.objects_pushButton.clicked.connect(self.onGetObjects)
        self.pathcurve_pushButton.clicked.connect(self.onGetPathCurve)

        # QtCore.QMetaObject.connectSlotsByName(pathmotion_Dialog)

    def onGetMasterController(self):
        sel = pm.ls(sl=True)
        if len(sel) > 1:
            self.infoPop(textTitle="Selection Error", textHeader="Select a single object as master controller")
            return
        elif len(sel) == 0:
            self.masterController = None
            self.mastercontroller_lineEdit.setText("")
            return
        else:
            self.masterController = sel[0]
            self.mastercontroller_lineEdit.setText(sel[0].name())

    def onGetObjects(self):
        sel = pm.ls(sl=True)
        if len(sel) == 0:
            self.objectList = []
            self.objects_lineEdit.setText("")
            return
        elif len(sel) > 1:
            self.objectList = sel
            self.objects_lineEdit.setText("%s Objects" %(len(self.objectList)))
            return
        else:
            self.objectList = sel
            self.objects_lineEdit.setText(self.objectList[0].name())

    def onGetPathCurve(self):
        sel = pm.ls(sl=True)
        # sanity check
        for i in sel:
            if not pm.objectType(i.getShape()) == "nurbsCurve":
                self.infoPop(textTitle="Selection Error", textHeader="One or more objects are not nurbs curve")
                return
        if len(sel) == 0:
            self.pathCurveList = []
            self.pathcurve_lineEdit.setText("")
            return
        elif len(sel) > 1:
            self.pathCurveList = sel
            self.pathcurve_lineEdit.setText("%s Objects" %(len(self.pathCurveList)))
            return
        else:
            self.pathCurveList = sel
            self.pathcurve_lineEdit.setText(self.pathCurveList[0].name())

    def createPathMotion(self):

        ## initialization process:
        self.nametemplate = self.nametemplate_lineEdit.text()
        if not self.masterController:
            self.masterController = pm.circle(name="cont_%s" %self.nametemplate, ch=0)[0]
        if not self.controllerattr_lineEdit.text() == "":
            self.controllerAttribute = self.controllerattr_lineEdit.text()
        else:
            self.controllerAttribute = "driver"

        self.count = self.count_spinBox.value()
        self.preInfinity = self.infinityDict[self.preinfinity_comboBox.currentText()]
        self.postInfinity = self.infinityDict[self.postinfinity_comboBox.currentText()]

        print self.controllerAttribute
        ## add the attribute if it is not already present
        if not pm.attributeQuery(self.controllerAttribute, node=self.masterController, exists=True):
            pm.addAttr(self.masterController, shortName=self.controllerAttribute, longName=self.controllerAttribute, defaultValue=0,
                       at="float", k=True)

        for path in self.pathCurveList:

            for iter in range(0, self.count ):
                locator = pm.spaceLocator(name="%s_%s" % (self.nametemplate, iter))
                r = pm.pathAnimation(locator, stu=iter, etu=self.count + iter, follow=self.follow_checkBox.isChecked(), fractionMode=self.parametriclength_checkBox.isChecked(), c=path)
                rRel = pm.listConnections(r, t="animCurveTL")[0]
                pm.setAttr(rRel.postInfinity, self.postInfinity)
                pm.setAttr(rRel.preInfinity, self.preInfinity)
                pm.keyTangent(rRel, itt='linear', ott='linear')
                pm.connectAttr("%s.%s" % (self.masterController, self.controllerAttribute), rRel.input)
                dupObjIndex = iter % (len(self.objectList))
                dup = pm.duplicate(self.objectList[dupObjIndex])
                alignTo(dup, locator, mode=2)
                pm.parent(dup, locator)


    def infoPop(self, textTitle="info", textHeader="", textInfo="", type="I"):
        self.msg = QtWidgets.QMessageBox(parent=self)
        if type == "I":
            self.msg.setIcon(QtWidgets.QMessageBox.Information)
        if type == "C":
            self.msg.setIcon(QtWidgets.QMessageBox.Critical)

        self.msg.setText(textHeader)
        self.msg.setInformativeText(textInfo)
        self.msg.setWindowTitle(textTitle)
        self.msg.setStandardButtons(QtWidgets.QMessageBox.Ok)
        self.msg.show()