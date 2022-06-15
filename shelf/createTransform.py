import hou
for node in hou.selectedNodes():
    trans = node.geometry().boundingBox()
    center = trans.center()
    trans = node.parent().createNode("xform")
    trans.setPosition(node.position() + hou.Vector2(0,-1))
    trans.parm('tx').set(center[0])
    trans.parm('ty').set(center[1])
    trans.parm('tz').set(center[2])
    trans.parm('px').setExpression('$CEX')
    trans.parm('py').setExpression('$CEY')
    trans.parm('pz').setExpression('$CEZ')
