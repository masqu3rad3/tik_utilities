#!/usr/bin/env python

import pymel.core as pm
import pymel.core.datatypes as dt
import random
import os


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

windowName = "Kelebek Path Helper"

def getMayaMainWindow():
    """
    Gets the memory adress of the main window to connect Qt dialog to it.
    Returns:
        (long) Memory Adress
    """
    win = omui.MQtUtil_mainWindow()
    ptr = wrapInstance(long(win), QtWidgets.QMainWindow)
    return ptr

class KelebekHelper(object):
    def __init__(self):
        super(KelebekHelper, self).__init__()
        self.infinityDict = {"Constant":0, "Linear":1, "Cycle":3, "Cycle with Offset":4, "Oscillate":5}
        self.seperation = 1
        self.randomRadiusX = 5
        self.randomRadiusY = 5
        self.randomRadiusZ = 5
        self.postInfinity = "Linear"
        self.preInfinity = "Linear"
        self.follow = True
        self.parametriclength = True
        self.count = 20
        self.scale = 1.0
        self.referencePath = "M:\\Projects\\Kelebek_logoKelebekler_DEPO_191003\\scenes\\Rig\\Kelebek_Loop\\Kelebek_Loop_Rig_forReference.mb"
        self.proxyPath = "M:\\Projects\\Kelebek_logoKelebekler_DEPO_191003\\_TRANSFER\\OBJ\\kelebekProxy.obj"
        self.flightController = "cont_diamond"
        self.masterController = "cont_Master"
        self.placementController = "cont_Placement"
        self.previewObjects = []
        self.previewCurve=None
        self.randomseed = 1234
        pass

    def previewModeOn(self):
        self.previewObjects = []
        if not self.previewCurve:
            try:
                curveTransform = pm.ls(sl=True)[0]
                self.previewCurve = curveTransform
            except IndexError:
                pm.displayWarning("Nothing selected. Select the path curve")
                return
        else:
            curveTransform = self.previewCurve
        curveShape = curveTransform.getShape()
        if (pm.nodeType(curveShape) != "nurbsCurve"):
            pm.displayWarning("Selection must be a nurbs curve.")

        if not pm.objExists("kelebekPrx"):
            pm.importFile(self.proxyPath)
        proxy = pm.PyNode("kelebekPrx")
        pm.setAttr(proxy.v, 0)
        # self.previewObjects.append(proxy)

        if not pm.attributeQuery("drive", node=curveTransform, exists=True):
            pm.addAttr(curveTransform, shortName="drive", longName="drive", defaultValue=0, at="float", k=True)

        # get namespace
        refFileBasename = os.path.split(self.referencePath)[1]
        namespace = os.path.splitext(refFileBasename)[0]

        for i in range(self.count):
            # ref = pm.polyCone()[0]
            ref = pm.duplicate(proxy)[0]
            pm.setAttr(ref.v, 1)
            refGrp = pm.group(ref)

            # ----------------------------

            locator = pm.spaceLocator(name="tmp_%s" % (i))
            r = pm.pathAnimation(locator,
                                 stu=i*self.seperation,
                                 etu=self.count + i*self.seperation,
                                 follow=self.follow,
                                 fractionMode=self.parametriclength, c=curveTransform,
                                 upAxis="Y",
                                 followAxis="Z",
                                 inverseFront=True,
                                 )


            rRel = pm.listConnections(r, t="animCurveTL")[0]
            pm.setAttr(rRel.postInfinity, self.infinityDict[self.postInfinity])
            pm.setAttr(rRel.preInfinity, self.infinityDict[self.preInfinity])
            pm.keyTangent(rRel, itt='linear', ott='linear')
            pm.connectAttr("%s.%s" % (curveTransform, "drive"), rRel.input)

            # ------------------
            # positioning
            # ------------------
            self.alignTo(refGrp, locator, mode=2)
            pm.parentConstraint(locator, refGrp, mo=True)
            random.seed(i+self.randomseed)
            pm.setAttr(ref.tx, (random.random()-0.5) * self.randomRadiusX)
            pm.setAttr(ref.ty, (random.random()-0.5) * self.randomRadiusY)
            pm.setAttr(ref.tz, (random.random()-0.5) * self.randomRadiusZ)
            pm.setAttr(ref.sx, self.scale)
            pm.setAttr(ref.sy, self.scale)
            pm.setAttr(ref.sz, self.scale)
            # pm.parent(controller, locator)
            self.previewObjects.append(refGrp)
            self.previewObjects.append(locator)

    def previewModeOff(self):
        pm.delete(self.previewObjects)
        self.previewObjects=[]

    def attachToPath(self):

        try:curveTransform = pm.ls(sl=True)[0]
        except IndexError:
            pm.displayWarning("Nothing selected. Select the path curve")
            return
        curveShape = curveTransform.getShape()
        if (pm.nodeType(curveShape) != "nurbsCurve"):
            pm.displayWarning("Selection must be a nurbs curve.")

        if not pm.attributeQuery("drive", node=curveTransform, exists=True):
            pm.addAttr(curveTransform, shortName="drive", longName="drive", defaultValue=0, at="float", k=True)

        # get namespace
        refFileBasename = os.path.split(self.referencePath)[1]
        namespace = os.path.splitext(refFileBasename)[0]

        for i in range(self.count):
            n = (pm.createReference(self.referencePath, namespace=namespace))
            masterController = pm.PyNode("{0}:{1}".format(n.fullNamespace, self.masterController))
            flightController = pm.PyNode("{0}:{1}".format(n.fullNamespace, self.flightController))
            placementController = pm.PyNode("{0}:{1}".format(n.fullNamespace, self.placementController))
            # print controller

            # ---------------------------
            # Keyframe the loop animation
            # ---------------------------

            # get first and last frames of the timeslider range

            # key the loop animation
            pm.setAttr(flightController.timeOffset, 1000*random.random())
            # ----------------------------

            locator = pm.spaceLocator(name="loc_%s_%s" % (n.fullNamespace, i))
            r = pm.pathAnimation(locator,
                                 stu=i*self.seperation,
                                 etu=self.count + i*self.seperation,
                                 follow=self.follow,
                                 fractionMode=self.parametriclength, c=curveTransform,
                                 upAxis="Y",
                                 followAxis="Z",
                                 inverseFront=True,
                                 )


            rRel = pm.listConnections(r, t="animCurveTL")[0]
            pm.setAttr(rRel.postInfinity, self.infinityDict[self.postInfinity])
            pm.setAttr(rRel.preInfinity, self.infinityDict[self.preInfinity])
            pm.keyTangent(rRel, itt='linear', ott='linear')
            pm.connectAttr("%s.%s" % (curveTransform, "drive"), rRel.input)

            # ------------------
            # positioning
            # ------------------
            self.alignTo(masterController, locator, mode=2)
            pm.parentConstraint(locator, masterController, mo=False)
            random.seed(i+self.randomseed)
            pm.setAttr(placementController.tx, (random.random()-0.5) * self.randomRadiusX)
            pm.setAttr(placementController.ty, (random.random()-0.5) * self.randomRadiusY)
            pm.setAttr(placementController.tz, (random.random()-0.5) * self.randomRadiusZ)

            pm.setAttr(placementController.sx, self.scale)
            pm.setAttr(placementController.sy, self.scale)
            pm.setAttr(placementController.sz, self.scale)

            if (int(i) % 2) > 0:
                colorValue = random.randrange(1, 7)
            else:
                colorValue = 0
            pm.setAttr(placementController.color, colorValue)
            # pm.parent(controller, locator)

    def alignTo(self, sourceObj=None, targetObj=None, mode=0, sl=False, o=(0, 0, 0)):
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

    def moveKeys(self, value):
        selection = pm.ls(sl=True)
        for x in selection:
            namespace = x.namespace()
            masterController = pm.PyNode("{0}:{1}".format(namespace, self.masterController))
            mPath = self._getMotionPath(masterController)  # parent node of the controller is connected to motion path
            pm.keyframe(mPath, r=True, tc=value)
            # if x.name().endswith(self.placementController):
            #     mPath = self._getMotionPath(x.getParent()) # parent node of the controller is connected to motion path
            #     pm.keyframe(mPath, r=True, tc=value)

    def speedChange(self, value):
        selection = pm.ls(sl=True)
        for x in selection:
            namespace = x.namespace()
            masterController = pm.PyNode("{0}:{1}".format(namespace, self.masterController))
            mPath = self._getMotionPath(masterController)  # parent node of the controller is connected to motion path
            pm.keyframe(mPath, r=True, index=0, vc=value*-1)
            pm.keyframe(mPath, r=True, index=1, vc=value)
            # if x.name().endswith(self.placementController):
            #     mPath = self._getMotionPath(x.getParent()) # parent node of the controller is connected to motion path
            #     pm.keyframe(mPath, r=True, index=0, vc=value*-1)
            #     pm.keyframe(mPath, r=True, index=1, vc=value)

    def _getMotionPath(self, node):
        for x in pm.listHistory(node):
            if (pm.nodeType(x)) == "motionPath":
                return x
        return None

    def selectMotionPath(self):
        selection = pm.ls(sl=True)
        # mList = [self._getMotionPath(x.getParent()) for x in selection]
        mList=[]
        for x in selection:
            namespace = x.namespace()
            masterController = pm.PyNode("{0}:{1}".format(namespace, self.masterController))
            mList.append(self._getMotionPath(masterController))
        pm.select(mList)

    def selectAllDiamonds(self):
        pm.select("*:%s" %self.flightController)

    def selectAllPlacements(self):
        pm.select("*:%s" % self.placementController)



class MainUI(QtWidgets.QDialog):
    def __init__(self):
        for entry in QtWidgets.QApplication.allWidgets():
            try:
                if entry.objectName() == windowName:
                    entry.close()
            except (AttributeError, TypeError):
                pass
        parent = getMayaMainWindow()
        super(MainUI, self).__init__(parent=parent)

        #initialize logic class
        self.kelebekHelper = KelebekHelper()

        #variables
        self.lastPosition = 0
        self.lastSpeed = 0

        self.setWindowTitle(windowName)
        self.setObjectName(windowName)
        self.resize(230, 565)
        self.buildUI()

    def buildUI(self):
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(0, -1, -1, -1)
        self.verticalLayout = QtWidgets.QVBoxLayout()

        self.label = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setText("Position")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout.addWidget(self.label)

        self.position_dial = QtWidgets.QDial(self)
        self.position_dial.setMaximum(99)
        self.position_dial.setPageStep(1)
        self.position_dial.setTracking(True)
        self.position_dial.setInvertedAppearance(False)
        self.position_dial.setInvertedControls(False)
        self.position_dial.setWrapping(True)
        self.position_dial.setNotchesVisible(False)
        self.verticalLayout.addWidget(self.position_dial)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setFont(font)
        self.label_2.setText("Speed")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.verticalLayout_2.addWidget(self.label_2)

        self.speed_dial = QtWidgets.QDial(self)
        self.speed_dial.setMaximum(99)
        self.speed_dial.setPageStep(1)
        self.speed_dial.setTracking(True)
        self.speed_dial.setInvertedAppearance(False)
        self.speed_dial.setInvertedControls(False)
        self.speed_dial.setWrapping(True)
        self.speed_dial.setNotchesVisible(False)
        self.verticalLayout_2.addWidget(self.speed_dial)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.multiplier_dSpn = QtWidgets.QDoubleSpinBox(self)
        self.multiplier_dSpn.setValue(1.0)
        self.verticalLayout_3.addWidget(self.multiplier_dSpn)

        self.selectMotionPath_pb = QtWidgets.QPushButton(self)
        self.selectMotionPath_pb.setText("Select Motion Path(s)")
        self.verticalLayout_3.addWidget(self.selectMotionPath_pb)

        self.selectAllDiamonds_pb = QtWidgets.QPushButton(self)
        self.selectAllDiamonds_pb.setText("Select All Diamonds")
        self.verticalLayout_3.addWidget(self.selectAllDiamonds_pb)

        self.selectAllPlacements_pb = QtWidgets.QPushButton(self)
        self.selectAllPlacements_pb.setText("Select All Placements")
        self.verticalLayout_3.addWidget(self.selectAllPlacements_pb)

        self.line = QtWidgets.QFrame(self)
        self.line.setLineWidth(5)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.verticalLayout_3.addWidget(self.line)

        self.groupBox = QtWidgets.QGroupBox(self)

        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.groupBox)
        self.formLayout = QtWidgets.QFormLayout()

        self.count_lb = QtWidgets.QLabel(self.groupBox, text="Count:")
        self.count_spn = QtWidgets.QSpinBox(self.groupBox, minimum=1, maximum=999)
        self.count_spn.setMaximumSize(QtCore.QSize(100, 16777215))
        self.count_spn.setProperty("value", 20)
        self.formLayout.addRow(self.count_lb, self.count_spn)

        self.scale_lb = QtWidgets.QLabel(self.groupBox, text="Scale:")
        self.scale_dSpn = QtWidgets.QDoubleSpinBox(self.groupBox, minimum=0.0, maximum=999.9)
        self.scale_dSpn.setMaximumSize(QtCore.QSize(100, 16777215))
        self.scale_dSpn.setProperty("value", 1)
        self.formLayout.addRow(self.scale_lb, self.scale_dSpn)

        self.seperation_lb = QtWidgets.QLabel(self.groupBox, text="Seperation:")
        self.seperation_dSpn = QtWidgets.QDoubleSpinBox(self.groupBox, minimum=0.0, maximum=999.9)
        self.seperation_dSpn.setMaximumSize(QtCore.QSize(100, 16777215))
        self.seperation_dSpn.setValue(1.0)
        self.formLayout.addRow(self.seperation_lb, self.seperation_dSpn)

        self.randX_lb = QtWidgets.QLabel(self.groupBox, text="Random Position X:")
        self.randX_dSpn = QtWidgets.QDoubleSpinBox(self.groupBox, minimum=0.0, maximum=9999.9)
        self.randX_dSpn.setMaximumSize(QtCore.QSize(100, 16777215))
        self.randX_dSpn.setValue(5.0)
        self.formLayout.addRow(self.randX_lb, self.randX_dSpn)

        self.randY_lb = QtWidgets.QLabel(self.groupBox, text="Random Position Y:")
        self.randY_dSpn = QtWidgets.QDoubleSpinBox(self.groupBox, minimum=0.0, maximum=9999.9)
        self.randY_dSpn.setMaximumSize(QtCore.QSize(100, 16777215))
        self.randY_dSpn.setValue(5.0)
        self.formLayout.addRow(self.randY_lb, self.randY_dSpn)

        self.randZ_lb = QtWidgets.QLabel(self.groupBox, text="Random Position Z:")
        self.randZ_dSpn = QtWidgets.QDoubleSpinBox(self.groupBox, minimum=0.0, maximum=9999.9)
        self.randZ_dSpn.setMaximumSize(QtCore.QSize(100, 16777215))
        self.randZ_dSpn.setValue(5.0)
        self.formLayout.addRow(self.randZ_lb, self.randZ_dSpn)

        self.randomseed_lb = QtWidgets.QLabel(self.groupBox, text="Random Seed:")
        self.randomseed_spn = QtWidgets.QSpinBox(self.groupBox, minimum=1, maximum=999999)
        self.randomseed_spn.setMaximumSize(QtCore.QSize(100, 16777215))
        self.randomseed_spn.setProperty("value", 1234)
        self.formLayout.addRow(self.randomseed_lb, self.randomseed_spn)


        self.verticalLayout_4.addLayout(self.formLayout)

        self.attachToPath_pb = QtWidgets.QPushButton(self.groupBox, text="Attach to path")
        self.verticalLayout_4.addWidget(self.attachToPath_pb)
        self.verticalLayout_3.addWidget(self.groupBox)


        self.preview_pb = QtWidgets.QPushButton(self.groupBox, text="Preview")
        self.preview_pb.setCheckable(True)
        self.verticalLayout_4.addWidget(self.preview_pb)
        self.verticalLayout_3.addWidget(self.groupBox)

        # self.attach_pb = QtWidgets.QPushButton(self)
        # self.attach_pb.setText("")

        self.position_dial.valueChanged.connect(self.onSlidePosition)
        self.speed_dial.valueChanged.connect(self.onSlideSpeed)
        self.attachToPath_pb.clicked.connect(self.onAttachToPath)
        self.selectMotionPath_pb.clicked.connect(self.kelebekHelper.selectMotionPath)
        self.preview_pb.clicked.connect(self.onPreview)

        self.selectAllDiamonds_pb.clicked.connect(self.kelebekHelper.selectAllDiamonds)
        self.selectAllPlacements_pb.clicked.connect(self.kelebekHelper.selectAllPlacements)

        self.count_spn.valueChanged.connect(self.onPreview)
        self.scale_dSpn.valueChanged.connect(self.onPreview)
        self.seperation_dSpn.valueChanged.connect(self.onPreview)
        self.randX_dSpn.valueChanged.connect(self.onPreview)
        self.randY_dSpn.valueChanged.connect(self.onPreview)
        self.randZ_dSpn.valueChanged.connect(self.onPreview)
        self.randomseed_spn.valueChanged.connect(self.onPreview)


        # layout = QtWidgets.QVBoxLayout(self)

    def onPreview(self):
        self.kelebekHelper.previewModeOff()
        if self.preview_pb.isChecked():
            self.refreshProperties()
            self.kelebekHelper.previewModeOn()
        # else:
        #     self.kelebekHelper.previewModeOff()


    def onSlidePosition(self):
        currentPosition = self.position_dial.value()
        mult = self.multiplier_dSpn.value()
        val=0
        if self.lastPosition > currentPosition and currentPosition != 0:
            val = mult

        if self.lastPosition < currentPosition and currentPosition != 99:
            val = -mult

        self.kelebekHelper.moveKeys(val*0.01)
        self.lastPosition = self.position_dial.value()

    def onSlideSpeed(self):
        currentPosition = self.speed_dial.value()
        mult = self.multiplier_dSpn.value()
        val = 0
        if self.lastSpeed > currentPosition and currentPosition != 0:
            val = -mult

        if self.lastSpeed < currentPosition and currentPosition != 99:
            val = mult

        self.kelebekHelper.speedChange(val * 0.01)
        self.lastSpeed = self.speed_dial.value()

    def refreshProperties(self):
        self.kelebekHelper.count = self.count_spn.value()
        self.kelebekHelper.scale = self.scale_dSpn.value()
        self.kelebekHelper.seperation = self.seperation_dSpn.value()
        self.kelebekHelper.randomRadiusX = self.randX_dSpn.value()
        self.kelebekHelper.randomRadiusY = self.randY_dSpn.value()
        self.kelebekHelper.randomRadiusZ = self.randZ_dSpn.value()
        self.kelebekHelper.randomseed = self.randomseed_spn.value()

    def onAttachToPath(self):
        # self.kelebekHelper.count = self.count_spn.value()
        # self.kelebekHelper.seperation = self.seperation_dSpn.value()
        # self.kelebekHelper.randomRadiusX = self.randX_dSpn.value()
        # self.kelebekHelper.randomRadiusY = self.randY_dSpn.value()
        # self.kelebekHelper.randomRadiusZ = self.randZ_dSpn.value()
        self.refreshProperties()
        self.kelebekHelper.attachToPath()

    def closeEvent(self, event):
        # do stuff
        self.kelebekHelper.previewModeOff()

# testUI().show()





