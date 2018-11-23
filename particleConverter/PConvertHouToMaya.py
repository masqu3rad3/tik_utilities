#!/usr/bin/env python
# -*- coding: utf-8 -*-

fpsDictionary = {25: 5644800,
                 24: 250}

import os, sys
import pyseq
import subprocess



fileLocation = os.path.dirname(os.path.abspath(__file__))

exe = os.path.join(fileLocation, "bin", "windows_x86_64", "partconv.exe")

particleDir = os.path.join(fileLocation, "tornado_cachev2")
convertedDir = os.path.join(fileLocation, "testConvert")
if not os.path.isdir(convertedDir):
    os.makedirs(convertedDir)

def convertToPDC(source, fps=25):
    """Converts the given pyseq item into pdc"""
    multip = fpsDictionary[fps]
    digit = int(source.digits[0])
    if digit < 381:
        pdcDigit = digit*multip
    else:
        pdcDigit = (-2144298496-multip)+((digit-380)*multip)
    base = source.parts[0]
    targetName = "{0}{1}.pdc".format(base, pdcDigit)
    targetName = "{0}{1}.pdc".format("particleShape1.", pdcDigit)
    targetPath = os.path.join(convertedDir, targetName)
    subprocess.check_call([exe, source, targetPath], shell=True)
    print targetPath


seqList = pyseq.get_sequences(particleDir)
for seq in seqList:
    for item in seq:
        print item.name
        convertToPDC(item)

