#!/usr/bin/env python
# -*- coding: utf-8 -*-

fpsDictionary = {25: 5644800,
                 24: 250}

import os, sys
import pyseq
import subprocess

import maya.cmds as cmds

fileFilter = "*.bhclassic;;*.hclassic;;*.bgeo"

selectedPath = cmds.fileDialog2(fileFilter=fileFilter, fm=1, dialogStyle=2)

if not selectedPath:
    raise Exception ("No File Selected")
else:
    selectedPath = selectedPath[0]

fileLocation = os.path.dirname(os.path.abspath(__file__))
exe = os.path.join(fileLocation, "bin", "windows_x86_64", "partconv.exe")

selectedDir, selectedFile = os.path.split(selectedPath)
# particleDir = os.path.join(fileLocation, "tornado_cachev2")
# convertedDir = os.path.join(fileLocation, "testConvert")

projectPath = cmds.workspace(q=1, rd=1)
particleDir = os.path.join(projectPath, "particles")
sceneFilePath = cmds.file(q=True, sn=True)
if sceneFilePath == "":
    raise Exception ("Scene Must be saved")
basename = os.path.splitext(os.path.basename(sceneFilePath))[0]
print basename

convertedDir= os.path.join(particleDir, basename)
if not os.path.isdir(convertedDir):
    os.makedirs(convertedDir)

# get All Sequences in the selected folder
seqList = pyseq.get_sequences(selectedDir)

# find the sequence of selected file

for x in seqList:
    if x.contains(selectedFile):
        theSeq = x
        break

print theSeq



## Create particle node
# cmds.particle(n=)
#
# def convertToPDC(source, fps=25):
#     """Converts the given pyseq item into pdc"""
#     multip = fpsDictionary[fps]
#     digit = int(source.digits[0])
#     if digit < 381:
#         pdcDigit = digit*multip
#     else:
#         pdcDigit = (-2144298496-multip)+((digit-380)*multip)
#     base = source.parts[0]
#     targetName = "{0}{1}.pdc".format(base, pdcDigit)
#     targetName = "{0}{1}.pdc".format("particleShape1.", pdcDigit)
#     targetPath = os.path.join(convertedDir, targetName)
#     subprocess.check_call([exe, source, targetPath], shell=True)
#     print targetPath
#
#
# seqList = pyseq.get_sequences(particleDir)
# for seq in seqList:
#     for item in seq:
#         print item.name
#         convertToPDC(item)

