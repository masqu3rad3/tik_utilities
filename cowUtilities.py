import pymel.core as pm
import maya.mel as mel


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

windowName = "Cow_Utilities"

def getControllers(mode="phonemes"):
    """
    returns the controller list
    Args:
        mode: This is scene specific. valid modes are for cow setup: 'phonemes', 'allControllers', 'faceTweaks', 'extraControllers'

    Returns: list of controllers

    """
    # get the namespace
    selection = pm.ls(sl=True)
    # if nothing is selected, get the first namespace (other then the default "UI" amd "shared"
    if len(selection) == 0:
        namespace = ""
        nlist = pm.namespaceInfo(listOnlyNamespaces=True)
        if len(nlist) > 2: ## if there are extra namespaces other than the defaults (2)
            firstNameSpace = list(set(nlist).difference([u'UI', u'shared']))[0]
            namespace="%s:" %firstNameSpace
    else:
        namespace = selection[0].namespace()

    try:
        selectionSet = pm.PyNode(namespace+mode)
    except:
        pm.warning("Cannot get specified selection set")
        return None
    controllers = sorted(selectionSet.elements())
    return controllers

def resetControllers(selectionOnly=True):
    if not selectionOnly:
        controllers = getControllers("allControllers")
    else:
        controllers = pm.ls(sl=True)
    if not controllers:
        pm.warning("Cannot get controllers -resetControllers m")
        return

    attDict = {"tx":0,"ty":0,"tz":0,"rx":0,"ry":0,"rz":0,"sx":1,"sy":1,"sz":1,"TweakControls":1,
               "ExtraControls":1,"Control_Visibility":1, "Joints_Visibility":0, "Rig_Visibility":0,
               "FK_A_Visibility":0, "FK_B_Visibility":0, "Tweaks_Visibility":1, "Preserve_Volume":0,
               "Volume_Factor":1, "Stretchyness":1, "Curl":0, "Curl_Size":1.5, "Curl_Angle":1.6,
               "Curl_Direction":90, "Curl_Shift":0, "Twist_Angle":0, "Twist_Slide":0, "Twist_Area":1,
               "Sine_Amplitude":0, "Sine_Wavelength":1, "Sine_Dropoff":0, "Sine_Slide":0, "Sine_Area":1,
               "Sine_Direction":0, "Sine_Animate":0
               }
    for cont in controllers:
        for att in attDict.keys():
            try:
                pm.delete("%s.%s" %(cont, att), icn=True)
                pm.setAttr("%s.%s" %(cont, att), attDict[att])
            except:
                pass
    # for i in controllers:
    #     try:
    #         pm.delete(i.ty, icn=True)
    #         pm.setAttr(i.tx, 0)
    #     except RuntimeError:
    #         pass

def lipSynch(word, seperation=2, useSelectedRange=True):
    # check if any area highlighted on the timeline
    if useSelectedRange:
        aTimeSlider = mel.eval('$tmpVar=$gPlayBackSlider')
        timeRange = pm.timeControl(aTimeSlider, q=True, rangeArray=True)
        duration = timeRange[1] - timeRange[0]
        if duration < 2:
            pm.warning("No range selected, using the cursor point and default seperation value")
            # useSelectedRange = False
            startFrame = timeRange[0]
        elif len(word) > duration:
            pm.warning("Selected Range is too small for entered text, select a larger area or use 'start from cursor position' option")
            return
        else:
            ## range calculation
            startFrame = timeRange[0]
            seperation = duration/len(word)
    else:
        startFrame = pm.currentTime()



    controllers = getControllers(mode="phonemes")
    if not controllers:
        pm.warning("select only the 'cont_facial' controller")
        return
    phenomeDict = {"a": controllers[0],
                   "b": controllers[6],
                   "c": controllers[9],
                   "C": controllers[9],
                   "d": controllers[1],
                   "e": controllers[2],
                   "f": controllers[3],
                   "g": controllers[9],
                   "G": "repeat",
                   "h": controllers[0],
                   "I": controllers[0],
                   "i": controllers[9],
                   "j": controllers[4],
                   "k": controllers[9],
                   "l": controllers[5],
                   "m": controllers[6],
                   "n": controllers[1],
                   "o": controllers[7],
                   "O": controllers[7],
                   "p": controllers[6],
                   "r": controllers[3],
                   "s": controllers[8],
                   "S": controllers[4],
                   "t": controllers[8],
                   "u": controllers[7],
                   "U": controllers[7],
                   "v": controllers[3],
                   "y": controllers[9],
                   "z": controllers[8],
                   " ": "default", }

    for i in range(len(word)):

        targetFrame = startFrame + ((i + 1) * seperation)
        try:
            command = phenomeDict[word[i]]
        except KeyError:
            pm.error("letter Error")

        print command, i, targetFrame

        if command == "repeat":
            command = phenomeDict[word[i - 1]]
        if command != "default" and command != "repeat":
            # put a keyframe for the previous step if the previous letter is not the same:
            if command != phenomeDict[word[i - 1]]:
                pm.setKeyframe(command, at="tx", v=0, t=targetFrame - seperation, itt="flat", ott="flat")
            # put a keyframe for the lipsync
            pm.setKeyframe(command, at="tx", v=5, t=targetFrame, itt="flat", ott="flat")
            # put a keyframe for the next step:
            pm.setKeyframe(command, at="tx", v=0, t=targetFrame + seperation, itt="flat", ott="flat")


def getMayaMainWindow():
    """
    Gets the memory adress of the main window to connect Qt dialog to it.
    Returns:
        (long) Memory Adress
    """
    win = omui.MQtUtil_mainWindow()
    ptr = wrapInstance(long(win), QtWidgets.QMainWindow)
    return ptr


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
        self.validCharacters = ["a", "b", "c", "C", "d", "e", "f", "g", "G", "h", "i", "I", "j", "k", "l", "m", "n", "o",
                           "O", "p", "r", "s", "S", "t", "u", "U", "v", "y", "z", " "]
        self.setWindowTitle(windowName)
        self.setObjectName(windowName)
        self.resize(270, 348)
        self.buildUI()

    def buildUI(self):

        self.lipsync_groupBox = QtWidgets.QGroupBox(self)
        self.lipsync_groupBox.setGeometry(QtCore.QRect(20, 20, 231, 135))
        self.lipsync_groupBox.setTitle(("LipSync"))
        self.lipsync_groupBox.setObjectName(("lipsync_groupBox"))

        self.seperation_label = QtWidgets.QLabel(self.lipsync_groupBox)
        self.seperation_label.setGeometry(QtCore.QRect(10, 60, 61, 20))
        self.seperation_label.setText(("Seperation"))
        self.seperation_label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.seperation_label.setObjectName(("seperation_label"))

        self.seperation_spinBox = QtWidgets.QSpinBox(self.lipsync_groupBox)
        self.seperation_spinBox.setGeometry(QtCore.QRect(80, 59, 42, 22))
        self.seperation_spinBox.setMinimum(1)
        self.seperation_spinBox.setProperty("value", 2)
        self.seperation_spinBox.setObjectName(("seperation_spinBox"))

        self.liptext_lineEdit = QtWidgets.QLineEdit(self.lipsync_groupBox)
        self.liptext_lineEdit.setGeometry(QtCore.QRect(10, 29, 211, 20))
        self.liptext_lineEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.liptext_lineEdit.setPlaceholderText(("enter text for lipSync"))
        self.liptext_lineEdit.setObjectName(("liptext_lineEdit"))

        self.lipsync_pushButton = QtWidgets.QPushButton(self.lipsync_groupBox)
        self.lipsync_pushButton.setGeometry(QtCore.QRect(140, 60, 81, 21))
        self.lipsync_pushButton.setText(("LipSync"))
        self.lipsync_pushButton.setObjectName(("lipsync_pushButton"))
        self.lipsync_pushButton.setFocus()

        POSradioGrp = QtWidgets.QButtonGroup(self.lipsync_groupBox)
        self.useCursorPosition_RB= QtWidgets.QRadioButton("Start From Cursor Position", parent=self.lipsync_groupBox)
        self.useCursorPosition_RB.setGeometry(QtCore.QRect(12, 90, 231, 20))
        self.useSelectionHiglight_RB= QtWidgets.QRadioButton("Use Selection Highlight", parent=self.lipsync_groupBox)
        self.useSelectionHiglight_RB.setGeometry(QtCore.QRect(12, 110, 231, 20))

        POSradioGrp.addButton(self.useCursorPosition_RB)
        POSradioGrp.addButton(self.useSelectionHiglight_RB)
        self.useSelectionHiglight_RB.setChecked(True)

        # MPradioColumn = QtWidgets.QVBoxLayout()
        # MPradioColumn.setAlignment(QtCore.Qt.AlignLeft)
        # MPLayout.addLayout(MPradioColumn)

        # MPLayout.addWidget(self.MPLeftToRight)
        # MPLayout.addWidget(self.MPRightToLeft)


        # self.disclaimer_label = QtWidgets.QLabel(self.lipsync_groupBox)
        # self.disclaimer_label.setGeometry(QtCore.QRect(0, 90, 231, 20))
        # font = QtGui.QFont()
        # font.setItalic(True)
        # self.disclaimer_label.setFont(font)
        # self.disclaimer_label.setText(("* cursor position is the starting point"))
        # self.disclaimer_label.setTextFormat(QtCore.Qt.RichText)
        # self.disclaimer_label.setAlignment(QtCore.Qt.AlignCenter)
        # self.disclaimer_label.setObjectName(("disclaimer_label"))

        self.cont_selection_groupBox = QtWidgets.QGroupBox(self)
        self.cont_selection_groupBox.setGeometry(QtCore.QRect(20, 170, 231, 81))
        self.cont_selection_groupBox.setTitle(("Controller Selection"))
        self.cont_selection_groupBox.setObjectName(("cont_selection_groupBox"))

        self.selectphonemes_pushButton = QtWidgets.QPushButton(self.cont_selection_groupBox)
        self.selectphonemes_pushButton.setGeometry(QtCore.QRect(10, 20, 101, 21))
        self.selectphonemes_pushButton.setObjectName(("selectphonemes_pushButton"))
        self.selectphonemes_pushButton.setText(("Select Phonemes"))

        self.selectall_pushButton = QtWidgets.QPushButton(self.cont_selection_groupBox)
        self.selectall_pushButton.setGeometry(QtCore.QRect(120, 20, 101, 21))
        self.selectall_pushButton.setObjectName(("selectall_pushButton"))
        self.selectall_pushButton.setText(("Select All"))

        self.selecttweaks_pushButton = QtWidgets.QPushButton(self.cont_selection_groupBox)
        self.selecttweaks_pushButton.setGeometry(QtCore.QRect(10, 50, 101, 21))
        self.selecttweaks_pushButton.setObjectName(("selecttweaks_pushButton"))
        self.selecttweaks_pushButton.setText(("Select Tweaks"))

        self.selectextras_pushButton = QtWidgets.QPushButton(self.cont_selection_groupBox)
        self.selectextras_pushButton.setGeometry(QtCore.QRect(120, 50, 101, 21))
        self.selectextras_pushButton.setObjectName(("selectextras_pushButton"))
        self.selectextras_pushButton.setText(("Select Extras"))

        self.cont_reset_groupBox = QtWidgets.QGroupBox(self)
        self.cont_reset_groupBox.setGeometry(QtCore.QRect(20, 265, 231, 61))
        self.cont_reset_groupBox.setTitle(("Controller Reset"))
        self.cont_reset_groupBox.setObjectName(("cont_reset_groupBox"))

        self.resetselection_pushButton = QtWidgets.QPushButton(self.cont_reset_groupBox)
        self.resetselection_pushButton.setGeometry(QtCore.QRect(120, 20, 101, 21))
        self.resetselection_pushButton.setObjectName(("resetselection_pushButton"))
        self.resetselection_pushButton.setText(("Reset Selection"))

        self.resetall_pushButton = QtWidgets.QPushButton(self.cont_reset_groupBox)
        self.resetall_pushButton.setGeometry(QtCore.QRect(10, 20, 101, 21))
        self.resetall_pushButton.setObjectName(("resetall_pushButton"))
        self.resetall_pushButton.setText(("Reset All"))

        self.lipsync_pushButton.clicked.connect(self.onLipSynchPressed)
        self.liptext_lineEdit.textChanged.connect(self.checkValidity)
        self.useSelectionHiglight_RB.toggled.connect(self.onUseStateChange)
        self.useCursorPosition_RB.toggled.connect(self.onUseStateChange)
        self.selectphonemes_pushButton.clicked.connect(self.onSelectPhonemesPressed)
        self.selectall_pushButton.clicked.connect(self.onSelectAllPressed)
        self.selectextras_pushButton.clicked.connect(self.onSelectExtrasPressed)
        self.selecttweaks_pushButton.clicked.connect(self.onSelectTweaksPressed)
        self.resetall_pushButton.clicked.connect(self.onResetAllPressed)
        self.resetselection_pushButton.clicked.connect(self.onResetSelectionPressed)

    def onUseStateChange(self):
        if self.useSelectionHiglight_RB.isChecked():
            self.seperation_spinBox.setEnabled(False)
            self.seperation_label.setEnabled(False)
        else:
            self.seperation_spinBox.setEnabled(True)
            self.seperation_label.setEnabled(True)

    def onLipSynchPressed(self):
        print self.useSelectionHiglight_RB.isChecked()
        with pm.UndoChunk():
            lipSynch(self.liptext_lineEdit.text(), self.seperation_spinBox.value())
        pass
    def onSelectAllPressed(self):
        pm.select(getControllers(mode="allControllers"))
        pass
    def onSelectPhonemesPressed(self):
        pm.select(getControllers(mode="phonemes"))
        pass
    def onSelectTweaksPressed(self):
        pm.select(getControllers(mode="faceTweaks"))
        pass
    def onSelectExtrasPressed(self):
        pm.select(getControllers(mode="extraControllers"))
        pass
    def onResetAllPressed(self):

        quit_msg = "Are you sure you want to reset the rig?"
        reply = QtWidgets.QMessageBox.question(self, 'Message',
                                           quit_msg, QtWidgets.QMessageBox.Yes, QtWidgets.QMessageBox.No)

        if reply == QtWidgets.QMessageBox.Yes:
            # event.accept()
            with pm.UndoChunk():
                resetControllers(selectionOnly=False)
        else:
            pass


    def onResetSelectionPressed(self):
        with pm.UndoChunk():
            resetControllers(selectionOnly=True)
        pass

    def checkValidity(self):
        text = self.liptext_lineEdit.text()
        if text == "":
            return

        for letter in text:
            if not letter in self.validCharacters:
                self.liptext_lineEdit.setStyleSheet("background-color: red; color: black")
                self.lipsync_pushButton.setEnabled(False)
                break
            else:
                self.liptext_lineEdit.setStyleSheet("background-color: rgb(40,40,40); color: white")
                self.lipsync_pushButton.setEnabled(True)



# testUI().show()

