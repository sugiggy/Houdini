import hou
out = hou.node("/out")
parm_prefix = '_reference'

def createGeometryRop(node):
    curParent = node.parent().name()
    
    rop = out.createNode("geometry",node.name())
    rop.moveToGoodPosition()
    file = node.parent().createNode("file")


    try:
        outNodes = node.outputs()
        for i,outNode in enumerate(outNodes):
            for j,inNode in enumerate(outNode.inputs()):
                if inNode!= None:
                    if inNode.name() == node.name():
                        #print j
                        outNode.setInput(j,file)
    except:
        pass
        
    rop.parm("soppath").set(node.path())
    ropOutput = '`chs("'+ rop.path() +'/sopoutput")`'
    rop.parm('postrender').set('opupdate()')
    
    file.parm("file").set(ropOutput)
    file.parm("missingframe").set(1)
    file.setInput(0,node)
    file.setPosition(node.position() + hou.Vector2(0,-1))
    
    txt = 'create "' + rop.path()+'" and "'+ file.path() +'"'
    hou.ui.setStatusMessage(txt,severity=hou.severityType.ImportantMessage)
       
        
if len(hou.selectedNodes())>0:
    for node in hou.selectedNodes():
        nodeType = hou.hscript('optype -s %s' % node.path())[0][:-1]  
        if nodeType == "sop":
            createGeometryRop(node)
            
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
