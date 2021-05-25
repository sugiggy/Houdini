import hou
for node in hou.selectedNodes():
    bbox = node.geometry().boundingBox()
    center = bbox.center()
    size = bbox.sizevec()
    bbox = node.parent().createNode("box",node.name()+"_bbox",run_init_scripts=True)
    bbox.setPosition(node.position() + hou.Vector2(0,-1))
    bbox.parm('sizex').set(size[0])
    bbox.parm('sizey').set(size[1])
    bbox.parm('sizez').set(size[2])
    bbox.parm('tx').set(center[0])
    bbox.parm('ty').set(center[1])
    bbox.parm('tz').set(center[2])
