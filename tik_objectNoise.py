import pymel.core as pm
import pymel.core.datatypes as dt
import random

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
    controller = pm.circle(name="cont_loc", nr=(0,1,0))[0]
    pm.parent(locator, controller)
    alignToAlter(controller, node, mode=2)

    #check if the target object has a parent
    originalParent = pm.listRelatives(node, p=True)
    if (len(originalParent) > 0):
        pm.parent(controller, originalParent[0], r=False)
    pm.parent(node, locator)

    #Create rotation noise attributes if rotate flag is set

    pm.addAttr(controller, longName="seedRND", niceName="Seed", at="long", k=True, defaultValue=12345)

    if rotate:
        pm.addAttr(controller, longName="rotationAtt", niceName="ROTATION_ATTS", at="enum", enumName="-------", k=True)
        pm.setAttr(controller.rotationAtt, l=True)
        pm.addAttr(controller, longName="rotSpeed", niceName="Overall_Rotation_Speed", at="float", defaultValue=10, k=True)
        pm.addAttr(controller, longName="xRotType", niceName="X_Rotation_Type", at="enum", enumName="Noise:Sinus:Continuous", k=True)
        pm.addAttr(controller, longName="xRotMult", niceName="X_Rotation_Multiplier", at="float", defaultValue=1, k=True)
        pm.addAttr(controller, longName="xRotMax", niceName="X_Rotation_Max", at="float", defaultValue=25, k=True)

        pm.addAttr(controller, longName="yRotType", niceName="Y_Rotation_Type", at="enum", enumName="Noise:Sinus:Continuous", k=True)
        pm.addAttr(controller, longName="yRotMult", niceName="Y_Rotation_Multiplier", at="float", defaultValue=1, k=True)
        pm.addAttr(controller, longName="yRotMax", niceName="Y_Rotation_Max", at="float", defaultValue=25, k=True)

        pm.addAttr(controller, longName="zRotType", niceName="Z_Rotation_Type", at="enum", enumName="Noise:Sinus:Continuous", k=True)
        pm.addAttr(controller, longName="zRotMult", niceName="Z_Rotation_Multiplier", at="float", defaultValue=1, k=True)
        pm.addAttr(controller, longName="zRotMax", niceName="Z_Rotation_Max", at="float", defaultValue=25, k=True)

    if translate:
        pm.addAttr(controller, longName="positionAtt", niceName="POSITION_ATTS", at="enum", enumName="-------", k=True)
        pm.setAttr(controller.positionAtt, l=True)
        pm.addAttr(controller, longName="posSpeed", niceName="Overall_Position_Speed", at="float", defaultValue=0, k=True)
        pm.addAttr(controller, longName="xPosType", niceName="X_Position_Type", at="enum", enumName="Noise:Sinus", k=True)
        pm.addAttr(controller, longName="xPosMult", niceName="X_Position_Multiplier", at="float", defaultValue=0, k=True)
        pm.addAttr(controller, longName="xPosMax", niceName="X_Position_Max", at="float", defaultValue=0, k=True)

        pm.addAttr(controller, longName="yPosType", niceName="Y_Position_Type", at="enum", enumName="Noise:Sinus", k=True)
        pm.addAttr(controller, longName="yPosMult", niceName="Y_Position_Multiplier", at="float", defaultValue=0, k=True)
        pm.addAttr(controller, longName="yPosMax", niceName="Y_Position_Max", at="float", defaultValue=0, k=True)

        pm.addAttr(controller, longName="zPosType", niceName="Z_Position_Type", at="enum", enumName="Noise:Sinus", k=True)
        pm.addAttr(controller, longName="zPosMult", niceName="Z_Position_Multiplier", at="float", defaultValue=0, k=True)
        pm.addAttr(controller, longName="zPosMax", niceName="Z_Position_Max", at="float", defaultValue=0, k=True)

        exp="""
        $seedRND= {0}.seedRND;
        seed $seedRND;
        $geoRandomX=rand(1000);;
        $geoRandomY=rand(1000);
        $geoRandomZ=rand(1000);;
        """.format(controller)

        if rotate:
            noiseExpRot = """
            $rotSpeed={0}.rotSpeed;
            $xRotType={0}.xRotType;
            $xRotMult={0}.xRotMult;
            $xRotMax={0}.xRotMax;
            $yRotType={0}.yRotType;
            $yRotMult={0}.yRotMult;
            $yRotMax={0}.yRotMax;
            $zRotType={0}.zRotType;
            $zRotMult={0}.zRotMult;
            $zRotMax={0}.zRotMax;

            if ($xRotType==0)//Noise Movement
            {{{1}.rotateX=(noise((time*$rotSpeed+$geoRandomX)*($xRotMult)))*$xRotMax;}}
            if ($xRotType==1)//Sinus Movement
            {{{1}.rotateX=(sin((time*$rotSpeed+$geoRandomX)*($xRotMult)))*$xRotMax;}}
            if ($xRotType==2)//Continuous Movement
            {{{1}.rotateX=((time*5*($rotSpeed*$xRotMult)));}}
            if ($yRotType==0)//Noise Movement
            {{{1}.rotateY=(noise((time*$rotSpeed+$geoRandomY)*($yRotMult)))*$yRotMax;}}
            if ($yRotType==1)//Sinus Movement
            {{{1}.rotateY=(sin((time*$rotSpeed+$geoRandomY)*($yRotMult)))*$yRotMax;}}
            if ($yRotType==2)//Continuous Movement
            {{{1}.rotateY=((time*5*($rotSpeed*$yRotMult)));}}
            if ($zRotType==0)//Noise Movement
            {{{1}.rotateZ=(noise((time*$rotSpeed+$geoRandomZ)*($zRotMult)))*$zRotMax;}}
            if ($zRotType==1)//Sinus Movement
            {{{1}.rotateZ=(sin((time*$rotSpeed+$geoRandomZ)*($zRotMult)))*$zRotMax;}}
            if ($zRotType==2)//Continuous Movement
            {{{1}.rotateZ=((time*5*($rotSpeed*$zRotMult)));}}
            """.format(controller, locator)

            exp += noiseExpRot

        if translate:
            noiseExpPos = """
            $posSpeed={0}.posSpeed;
            $xPosType={0}.xPosType;
            $xPosMult={0}.xPosMult;
            $xPosMax={0}.xPosMax;
            $yPosType={0}.yPosType;
            $yPosMult={0}.yPosMult;
            $yPosMax={0}.yPosMax;
            $zPosType={0}.zPosType;
            $zPosMult={0}.zPosMult;
            $zPosMax= {0}.zPosMax;
            
            if ($xPosType==0)//Noise Movement
            {{{1}.translateX=(noise((time*$posSpeed+$geoRandomX)*($xPosMult)))*$xPosMax;}}
            if ($xPosType==1)//Sinus Movement
            {{{1}.translateX=(sin((time*$posSpeed+$geoRandomX)*($xPosMult)))*$xPosMax;}}
            if ($yPosType==0)//Noise Movement
            {{{1}.translateY=(noise((time*$posSpeed+$geoRandomY)*($yPosMult)))*$yPosMax;}}
            if ($yPosType==1)//Sinus Movement
            {{{1}.translateY=(sin((time*$posSpeed+$geoRandomY)*($yPosMult)))*$yPosMax;}}
            if ($zPosType==0)//Noise Movement
            {{{1}.translateZ=(noise((time*$posSpeed+$geoRandomZ)*($zPosMult)))*$zPosMax;}}
            if ($zPosType==1)//Sinus Movement
            {{{1}.translateZ=(sin((time*$posSpeed+$geoRandomZ)*($zPosMult)))*$zPosMax;}}
            """.format(controller, locator)

            exp += noiseExpPos

        pm.expression(string=exp, name="%s_noiseExp" %node)

