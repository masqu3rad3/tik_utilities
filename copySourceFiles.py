import maya.cmds as cmds
from shutil import copyfile
import os

def copySourceFiles(childDir=""):
    """
    This function copies all file sources to under the sourceImages Directory of current project and update the node connections
    :param childDir: Extra directory to be created under sourceImages
    :return:
    """
    projectPath = cmds.workspace(q=1, rd=1)
    copyPath = os.path.join(projectPath, "sourceImages", childDir)
    if not os.path.isdir(copyPath):
        os.makedirs(os.path.normpath(copyPath))

    for fileNode in cmds.ls(type="file"):

        oldPath = cmds.getAttr("%s.fileTextureName" % fileNode)
        print ('\nNode: {0}, \nPath: {1}'.format(fileNode, oldPath))

        newPath = os.path.join(copyPath, os.path.basename(oldPath))
        print "new full path: %s" %newPath

        try:
            copyfile(oldPath, newPath)
        except:
            print "File Copy Error"

        cmds.setAttr("%s.fileTextureName" %fileNode, newPath)



