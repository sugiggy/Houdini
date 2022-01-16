stage = hou.node("/stage")
num = 0

for node in hou.selectedNodes():
    curParent = node.parent().name()
    num += 1
    
    sopImport = stage.createNode("sopimport")
    sopImport.parm("soppath").set(node.path())
        
    p = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    p.setCurrentNode(sopImport)
    #p.homeToSelection()
