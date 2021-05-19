obj = hou.node("/obj")
num = 0

for node in hou.selectedNodes():
    curParent = node.parent().name()
    num += 1
    
    geoNode = obj.createNode("geo",node.name(),run_init_scripts=True)
    objMerge = geoNode.createNode("object_merge")
    
    objMerge.parm("xformtype").set(1)
    #objMerge.parm("objpath1").set("../../" + curParent + "/" + node.name())
    objMerge.parm("objpath1").set(node.path())
    
    geoNode.setPosition(node.parent().position() + hou.Vector2(0,-num))
    
    
    p = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    p.setCurrentNode(geoNode)
    p.homeToSelection()
