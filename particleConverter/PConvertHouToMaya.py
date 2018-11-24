#!/usr/bin/env python
# -*- coding: utf-8 -*-

fpsDictionary = {25: 5644800,
                 24: 250}

import os, sys
import pyseq
import subprocess

import maya.cmds as cmds

class ParticleImporter(object):
    def __init__(self):
        super(ParticleImporter, self).__init__()

        self.fileFilter = "*.bhclassic;;*.hclassic;;*.bgeo"
        self.initPaths()

    def initPaths(self):
        self.selectedPath = cmds.fileDialog2(fileFilter=self.fileFilter, fm=1, dialogStyle=2)
        if not self.selectedPath:
            msg = "No File Selected"
            self.exception(title="SElection Error", msg=msg)
            raise Exception(msg)
        else:
            self.selectedPath = self.selectedPath[0]

        self.fileLocation = os.path.dirname(os.path.abspath(__file__))
        self.exe = os.path.join(self.fileLocation, "bin", "windows_x86_64", "partconv.exe")
        self.selectedDir, self.selectedFile = os.path.split(self.selectedPath)

        self.projectPath = cmds.workspace(q=1, rd=1)
        self.particleDir = os.path.join(self.projectPath, "particles")
        self.sceneFilePath = cmds.file(q=True, sn=True)
        if self.sceneFilePath == "":
            msg = "Scene Must be saved"
            self.exception(title="System Error", msg=msg)
            raise Exception(msg)
        self.basename = os.path.splitext(os.path.basename(self.sceneFilePath))[0]
        # print self.basename

        self.convertedDir = os.path.join(self.particleDir, self.basename)
        if not os.path.isdir(self.convertedDir):
            os.makedirs(self.convertedDir)

    def uniqueName(self, name):
        baseName = name
        idcounter = 0
        while cmds.objExists(name):
            name = "%s%s" % (baseName, str(idcounter + 1))
            idcounter = idcounter + 1
        return name

    def convertToPDC(self, source, customName=None, fps=25):
        """Converts the given pyseq item into pdc"""
        multip = fpsDictionary[fps]
        digit = int(source.digits[0])
        if digit < 381:
            pdcDigit = digit*multip
        else:
            pdcDigit = (-2144298496-multip)+((digit-380)*multip)
        base = source.parts[0]

        if not customName:
            customName = "particleShape1."

        # targetName = "{0}{1}.pdc".format(base, pdcDigit)
        targetName = "{0}{1}.pdc".format(customName, pdcDigit)
        targetPath = os.path.normpath(os.path.join(self.convertedDir, targetName))

        # print self.exe, source, targetPath
        subprocess.Popen([self.exe, source.path, targetPath], shell=True)
        # print targetPath

    def run(self):
        seqList = pyseq.get_sequences(self.selectedDir)
        theSeq =self._findItem(self.selectedFile, seqList)
        if not theSeq:
            self.exception(title="File Error", msg="Cannot get the sequence list. Make sure the sequence numbers have enough padding")
            return
        for x in seqList:
            if x.contains(self.selectedFile):
                theSeq = x
                break

        particleObjName = self.uniqueName("particle1")
        cmds.particle(n=particleObjName)
        particleCacheName = "%s." %(cmds.listRelatives(particleObjName, shapes=True)[0])

        for item in theSeq:
            # print item.name
            self.convertToPDC(item, customName=particleCacheName)
        # seqList = pyseq.get_sequences(self.particleDir)
        # for seq in seqList:
        #     for item in seq:
                # print item.name


    def _findItem(self, itemPath, seqlist):
        for x in seqlist:
            if x.contains(itemPath):
                return x

    def _exception(self, title, msg):
        """Overriden Function"""
        cmds.confirmDialog(title=title, message=msg, button=['Ok'])











# particleDir = os.path.join(fileLocation, "tornado_cachev2")
# convertedDir = os.path.join(fileLocation, "testConvert")





# get All Sequences in the selected folder


# find the sequence of selected file



# print theSeq.head()



## Create particle node
# particleObjName =  uniqueName("particle")
# cmds.particle(n=particleObjName)
#

#
#
# seqList = pyseq.get_sequences(particleDir)
# for seq in seqList:
#     for item in seq:
#         print item.name
#         convertToPDC(item)

