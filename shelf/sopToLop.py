stage = hou.node("/stage")
numA = 0
parm_prefix = '_reference'

for node in hou.selectedNodes():
    curParent = node.parent().name()
    numA += 1
    
    sopImport = stage.createNode("sopimport")
    sopImport.parm("soppath").set(node.path())
    
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
        
    p = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    p.setCurrentNode(sopImport)
    p.homeToSelection()
