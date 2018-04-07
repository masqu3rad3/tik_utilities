import pymel.core as pm



def objectNoise(node):
    targetcoordinate = pm.getAttr(node.center)
    locator = pm.spaceLocator(name="Loc")
    controller = pm.circle(name="cont_loc")
    pm.parent(locator, controller)

