obj = hou.node("/obj")
numA = 0
parm_prefix = '_reference'

for node in hou.selectedNodes():
    curParent = node.parent().name()
    numA += 1
    
    geoNode = obj.createNode("geo",node.name(),run_init_scripts=True)
    objMerge = geoNode.createNode("object_merge")
    
    objMerge.parm("xformtype").set(1)
    #objMerge.parm("objpath1").set("../../" + curParent + "/" + node.name())
    objMerge.parm("objpath1").set(node.path())
    
    
    #################
    group = node.parmTemplateGroup()
    
    ## remove parms
    parms = group.entries()
    for p in parms:
        if p.name().startswith(parm_prefix): group.remove(p)
    
    ## get refs
    node.setParmTemplateGroup( group )
    
    depNodes = node.dependents()
    num = 0
    for depNode in depNodes:
        parmName = parm_prefix+str(num)
        num += 1
        
        parm = hou.StringParmTemplate(parmName, "",1,string_type=hou.stringParmType.NodeReference)
        path = depNode.path()
        node.addSpareParmTuple(parm)
        node.parm(parmName).set(path)
    ####################
    
    geoNode.setPosition(node.parent().position() + hou.Vector2(0,-num))
    p = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    p.setCurrentNode(geoNode)
    p.homeToSelection()
