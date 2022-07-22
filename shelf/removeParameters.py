import hou

for node in hou.selectedNodes():

    
    group = node.parmTemplateGroup()
    parms = group.entries()
    #print(parms)
    #p = group.find('ref')
    for p in parms:
        group.remove(p)
    node.setParmTemplateGroup( group )
