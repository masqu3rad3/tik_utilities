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

windowName = "Flipboard"


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
            try:
                if entry.objectName() == windowName:
                    entry.close()
            except AttributeError:
                pass
        parent = getMayaMainWindow()
        super(testUI, self).__init__(parent=parent)

        self.setWindowTitle(windowName)
        self.setObjectName(windowName)
        self.resize(421, 253)
        self.buildUI()

    def buildUI(self):

        self.from_groupBox = QtWidgets.QGroupBox(self)
        self.from_groupBox.setGeometry(QtCore.QRect(10, 20, 401, 80))
        self.from_groupBox.setTitle("FROM")
        self.from_groupBox.setObjectName(("from_groupBox"))

        self.saatA_label = QtWidgets.QLabel(self.from_groupBox)
        self.saatA_label.setGeometry(QtCore.QRect(10, 20, 41, 16))
        self.saatA_label.setText(("SAAT"))
        self.saatA_label.setAlignment(QtCore.Qt.AlignCenter)
        self.saatA_label.setObjectName(("saatA_label"))

        self.ucusA_label = QtWidgets.QLabel(self.from_groupBox)
        self.ucusA_label.setGeometry(QtCore.QRect(60, 20, 51, 16))
        self.ucusA_label.setText(("UCUS"))
        self.ucusA_label.setAlignment(QtCore.Qt.AlignCenter)
        self.ucusA_label.setObjectName(("ucusA_label"))

        self.destA_label = QtWidgets.QLabel(self.from_groupBox)
        self.destA_label.setGeometry(QtCore.QRect(120, 20, 91, 16))
        self.destA_label.setText(("GIDECEGI YER"))
        self.destA_label.setAlignment(QtCore.Qt.AlignCenter)
        self.destA_label.setObjectName(("destA_label"))

        self.kapiA_label = QtWidgets.QLabel(self.from_groupBox)
        self.kapiA_label.setGeometry(QtCore.QRect(220, 20, 31, 16))
        self.kapiA_label.setText(("KAPI"))
        self.kapiA_label.setAlignment(QtCore.Qt.AlignCenter)
        self.kapiA_label.setObjectName(("kapiA_label"))

        self.aciklamaA_label = QtWidgets.QLabel(self.from_groupBox)
        self.aciklamaA_label.setGeometry(QtCore.QRect(260, 20, 121, 16))
        self.aciklamaA_label.setText(("ACIKLAMA"))
        self.aciklamaA_label.setAlignment(QtCore.Qt.AlignCenter)
        self.aciklamaA_label.setObjectName(("aciklamaA_label"))

        self.saatA_lineEdit = QtWidgets.QLineEdit(self.from_groupBox)
        self.saatA_lineEdit.setGeometry(QtCore.QRect(10, 40, 41, 20))
        self.saatA_lineEdit.setText((""))
        self.saatA_lineEdit.setPlaceholderText((""))
        self.saatA_lineEdit.setObjectName(("saatA_lineEdit"))

        self.ucusA_lineEdit = QtWidgets.QLineEdit(self.from_groupBox)
        self.ucusA_lineEdit.setGeometry(QtCore.QRect(60, 40, 51, 20))
        self.ucusA_lineEdit.setText((""))
        self.ucusA_lineEdit.setPlaceholderText((""))
        self.ucusA_lineEdit.setObjectName(("ucusA_lineEdit"))

        self.destA_lineEdit = QtWidgets.QLineEdit(self.from_groupBox)
        self.destA_lineEdit.setGeometry(QtCore.QRect(120, 40, 91, 20))
        self.destA_lineEdit.setText((""))
        self.destA_lineEdit.setPlaceholderText((""))
        self.destA_lineEdit.setObjectName(("destA_lineEdit"))

        self.kapiA_lineEdit = QtWidgets.QLineEdit(self.from_groupBox)
        self.kapiA_lineEdit.setGeometry(QtCore.QRect(220, 40, 31, 20))
        self.kapiA_lineEdit.setText((""))
        self.kapiA_lineEdit.setPlaceholderText((""))
        self.kapiA_lineEdit.setObjectName(("kapiA_lineEdit"))

        self.aciklamaA_lineEdit = QtWidgets.QLineEdit(self.from_groupBox)
        self.aciklamaA_lineEdit.setGeometry(QtCore.QRect(260, 40, 121, 20))
        self.aciklamaA_lineEdit.setText((""))
        self.aciklamaA_lineEdit.setPlaceholderText((""))
        self.aciklamaA_lineEdit.setObjectName(("aciklamaA_lineEdit"))




        self.to_groupBox = QtWidgets.QGroupBox(self)
        self.to_groupBox.setGeometry(QtCore.QRect(10, 110, 401, 80))
        self.to_groupBox.setObjectName(("to_groupBox"))
        self.to_groupBox.setTitle("TO")

        self.saatB_label = QtWidgets.QLabel(self.to_groupBox)
        self.saatB_label.setGeometry(QtCore.QRect(10, 20, 41, 16))
        self.saatB_label.setText(("SAAT"))
        self.saatB_label.setAlignment(QtCore.Qt.AlignCenter)
        self.saatB_label.setObjectName(("saatB_label"))

        self.ucusB_label = QtWidgets.QLabel(self.to_groupBox)
        self.ucusB_label.setGeometry(QtCore.QRect(60, 20, 51, 16))
        self.ucusB_label.setText(("UCUS"))
        self.ucusB_label.setAlignment(QtCore.Qt.AlignCenter)
        self.ucusB_label.setObjectName(("ucusB_label"))

        self.destB_label = QtWidgets.QLabel(self.to_groupBox)
        self.destB_label.setGeometry(QtCore.QRect(120, 20, 91, 16))
        self.destB_label.setText(("GIDECEGI YER"))
        self.destB_label.setAlignment(QtCore.Qt.AlignCenter)
        self.destB_label.setObjectName(("destB_label"))

        self.kapiB_label = QtWidgets.QLabel(self.to_groupBox)
        self.kapiB_label.setGeometry(QtCore.QRect(220, 20, 31, 16))
        self.kapiB_label.setText(("KAPI"))
        self.kapiB_label.setAlignment(QtCore.Qt.AlignCenter)
        self.kapiB_label.setObjectName(("kapiB_label"))

        self.aciklamaB_label = QtWidgets.QLabel(self.to_groupBox)
        self.aciklamaB_label.setGeometry(QtCore.QRect(260, 20, 121, 16))
        self.aciklamaB_label.setText(("ACIKLAMA"))
        self.aciklamaB_label.setAlignment(QtCore.Qt.AlignCenter)
        self.aciklamaB_label.setObjectName(("aciklamaB_label"))

        self.saatB_lineEdit = QtWidgets.QLineEdit(self.to_groupBox)
        self.saatB_lineEdit.setGeometry(QtCore.QRect(10, 40, 41, 20))
        self.saatB_lineEdit.setText((""))
        self.saatB_lineEdit.setPlaceholderText((""))
        self.saatB_lineEdit.setObjectName(("saatB_lineEdit"))

        self.ucusB_lineEdit = QtWidgets.QLineEdit(self.to_groupBox)
        self.ucusB_lineEdit.setGeometry(QtCore.QRect(60, 40, 51, 20))
        self.ucusB_lineEdit.setText((""))
        self.ucusB_lineEdit.setPlaceholderText((""))
        self.ucusB_lineEdit.setObjectName(("ucusB_lineEdit"))

        self.destB_lineEdit = QtWidgets.QLineEdit(self.to_groupBox)
        self.destB_lineEdit.setGeometry(QtCore.QRect(120, 40, 91, 20))
        self.destB_lineEdit.setText((""))
        self.destB_lineEdit.setPlaceholderText((""))
        self.destB_lineEdit.setObjectName(("destB_lineEdit"))

        self.kapiB_lineEdit = QtWidgets.QLineEdit(self.to_groupBox)
        self.kapiB_lineEdit.setGeometry(QtCore.QRect(220, 40, 31, 20))
        self.kapiB_lineEdit.setText((""))
        self.kapiB_lineEdit.setPlaceholderText((""))
        self.kapiB_lineEdit.setObjectName(("kapiB_lineEdit"))

        self.aciklamaB_lineEdit = QtWidgets.QLineEdit(self.to_groupBox)
        self.aciklamaB_lineEdit.setGeometry(QtCore.QRect(260, 40, 121, 20))
        self.aciklamaB_lineEdit.setText((""))
        self.aciklamaB_lineEdit.setPlaceholderText((""))
        self.aciklamaB_lineEdit.setObjectName(("aciklamaB_lineEdit"))

        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(180, 200, 211, 31))
        self.pushButton.setText(("GO"))
        self.pushButton.setObjectName(("pushButton"))

        self.keyoffset_spinBox = QtWidgets.QSpinBox(self)
        self.keyoffset_spinBox.setGeometry(QtCore.QRect(120, 195, 42, 20))
        self.keyoffset_spinBox.setValue(2)
        self.keyoffset_spinBox.setRange(1,100)
        self.keyoffset_spinBox.setObjectName(("keyoffset_spinBox"))

        self.keyoffset_label = QtWidgets.QLabel(self)
        self.keyoffset_label.setGeometry(QtCore.QRect(20, 195, 101, 20))
        self.keyoffset_label.setText(("Keyframe  Offset"))
        self.keyoffset_label.setAlignment(QtCore.Qt.AlignCenter)
        self.keyoffset_label.setObjectName(("keyoffset_label"))

        self.clearkeys_checkbox = QtWidgets.QCheckBox(self)
        self.clearkeys_checkbox.setGeometry(QtCore.QRect(28, 215, 80, 31))
        self.clearkeys_checkbox.setText(("Clear Keys"))
        self.clearkeys_checkbox.setChecked(True)
        self.clearkeys_checkbox.setObjectName(("Clear_Keys"))
        # self.clearkeys_checkbox.setLayoutDirection(QtCore.Qt.RightToLeft)

        self.pushButton.clicked.connect(self.onGo)

        # testUI().show()

    def onGo(self):
        # objList = pm.ls(sl=True)
        objList = pm.listRelatives(pm.ls(sl=True)[0], c=True)

        cDic = {
            "A": 0,
            "B": 1,
            "C": 2,
            "D": 3,
            "E": 4,
            "F": 5,
            "G": 6,
            "H": 7,
            "I": 8,
            "J": 9,
            "K": 10,
            "L": 11,
            "M": 12,
            "N": 13,
            "O": 14,
            "P": 15,
            "R": 16,
            "S": 17,
            "T": 18,
            "U": 19,
            "V": 20,
            "W": 21,
            "X": 22,
            "Y": 23,
            "Z": 24,
            "1": 25,
            "2": 26,
            "3": 27,
            "4": 28,
            "5": 29,
            "6": 30,
            "7": 31,
            "8": 32,
            "9": 33,
            "0": 34,
            "-": 35,
            ":": 36,
            "*": 37
        }

        satirLen = len(objList)

        saatA = (self.saatA_lineEdit.text().ljust(5,"*")).replace(" ", "*")
        ucusA = (self.ucusA_lineEdit.text().ljust(6,"*")).replace(" ", "*")
        destinationA = (self.destA_lineEdit.text().ljust(12,"*")).replace(" ", "*")
        kapiA = (self.kapiA_lineEdit.text().ljust(3, "*")).replace(" ", "*")
        aciklamaA = (self.aciklamaA_lineEdit.text().ljust(10, "*")).replace(" ", "*")

        saatB = (self.saatB_lineEdit.text().ljust(5,"*")).replace(" ", "*")
        ucusB = (self.ucusB_lineEdit.text().ljust(6,"*")).replace(" ", "*")
        destinationB = (self.destB_lineEdit.text().ljust(12,"*")).replace(" ", "*")
        kapiB = (self.kapiB_lineEdit.text().ljust(3, "*")).replace(" ", "*")
        aciklamaB = (self.aciklamaB_lineEdit.text().ljust(10, "*")).replace(" ", "*")

        fromWord = "{0}{1}{2}{3}{4}".format(saatA, ucusA, destinationA, kapiA, aciklamaA)
        toWord = "{0}{1}{2}{3}{4}".format(saatB, ucusB, destinationB, kapiB, aciklamaB)
        # fromWord = "17:15TK2020KAYSERI*****112**********"
        # toWord = "17:10TK2420VAN*********106**********"

        frameMult = self.keyoffset_spinBox.value()

        for s in range(0, satirLen):
            fromLetter = fromWord[s].upper()
            print "fromLetter", fromLetter
            fromIndex = cDic[fromLetter]

            # set the flipper to fromIndex

            toLetter = toWord[s].upper()
            print "toLetter", toLetter
            toIndex = cDic[toLetter]

            if fromIndex == toIndex:
                pass
                # do nothing

            if toIndex < fromIndex:
                compensate = fromIndex - toIndex
                print "comp", compensate
                moveValue = ((len(cDic.keys()))) - compensate

            else:
                moveValue = toIndex - fromIndex

            # pm.setAttr(testObj.Flip, moveValue)
            if self.clearkeys_checkbox.isChecked():
                pm.cutKey(objList[s])

            pm.setKeyframe(objList[s], at="Flip", v=fromIndex, t=pm.currentTime(), ott="linear")
            pm.setKeyframe(objList[s], at="Flip", v=fromIndex + moveValue, t=pm.currentTime() + (moveValue * frameMult),
                           itt="linear")

