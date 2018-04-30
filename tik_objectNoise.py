import pymel.core as pm
import pymel.core.datatypes as dt

def alignToAlter(node1, node2, mode=0, o=(0,0,0)):
    """
    Aligns the first node to the second.
    Args:
        node1: Node to be aligned.
        node2: Target Node.
        mode: Specifies the alignment Mode. Valid Values: 0=position only, 1=Rotation Only, 2=Position and Rotation
        o: Offset Value. Default: (0,0,0)

    Returns:None

    """
    if type(node1) == str:
        node1 = pm.PyNode(node1)

    if type(node2) == str:
        node2 = pm.PyNode(node2)

    if mode==0:
        ##Position Only
        tempPocon = pm.pointConstraint(node2, node1, mo=False)
        pm.delete(tempPocon)
        # targetLoc = node2.getRotatePivot(space="world")
        # pm.move(node1, targetLoc, a=True, ws=True)

    elif mode==1:
        ##Rotation Only
        if node2.type() == "joint":
            tempOri = pm.orientConstraint(node2, node1, o=o, mo=False)
            pm.delete(tempOri)
        else:
            targetRot = node2.getRotation()
            pm.rotate(node1, targetRot, a=True, ws=True)

    elif mode==2:
        ##Position and Rotation
        tempPacon = pm.parentConstraint(node2, node1, mo=False)
        pm.delete(tempPacon)


def objectNoise(node, translate=True, rotate=True):

    # Create noise locator and master controller
    locator = pm.spaceLocator(name="Loc")
    controller = pm.circle(name="cont_loc")[0]
    pm.parent(locator, controller)
    alignToAlter(controller, node, mode=2)

    #check if the target object has a parent
    originalParent = pm.listRelatives(node, p=True)
    if (len(originalParent) > 0):
        pm.parent(controller, originalParent[0], r=False)
    pm.parent(node, locator)

    #Create rotation noise attributes if rotate flag is set

    if rotate:
        pm.addAttr(controller, shortName="rotSpeed", longName="Overall_Rotation_Speed", at="float", defaultValue=10, k=True)
        pm.addAttr(controller, shortName="xRotType", longName="X_Rotation_Type", at="enum", enumName="Noise:Sinus:Continuous", k=True)
        pm.addAttr(controller, shortName="xRotMult", longName="X_Rotation_Multiplier", at="float", defaultValue=1, k=True)
        pm.addAttr(controller, shortName="xRotMax", longName="X_Rotation_Max", at="float", defaultValue=25, k=True)

        pm.addAttr(controller, shortName="yRotType", longName="Y_Rotation_Type", at="enum", enumName="Noise:Sinus:Continuous", k=True)
        pm.addAttr(controller, shortName="yRotMult", longName="Y_Rotation_Multiplier", at="float", defaultValue=1, k=True)
        pm.addAttr(controller, shortName="yRotMax", longName="Y_Rotation_Max", at="float", defaultValue=25, k=True)

        pm.addAttr(controller, shortName="zRotType", longName="Z_Rotation_Type", at="enum", enumName="Noise:Sinus:Continuous", k=True)
        pm.addAttr(controller, shortName="zRotMult", longName="Z_Rotation_Multiplier", at="float", defaultValue=1, k=True)
        pm.addAttr(controller, shortName="zRotMax", longName="Z_Rotation_Max", at="float", defaultValue=25, k=True)