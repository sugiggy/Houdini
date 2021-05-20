import hou
out = hou.node("/out")

def createNodes():
    for node in hou.selectedNodes():
        curParent = node.parent().name()
        
        rop = out.createNode("Redshift_Proxy_Output",node.name())
        rop.moveToGoodPosition()
        file = node.parent().createNode("redshift_packedProxySOP")
        file.setPosition(node.position() + hou.Vector2(0,-1))

        try:
            outNode = node.outputs()[0]
            outNode.setInput(0,file)
        except:
            print 'no output'
        
        rop.parm("RS_archive_sopPath").set(node.path())
        ropOutput = '`chs("'+ rop.path() +'/RS_archive_file")`'
        file.parm("RS_proxy_file").set(ropOutput)
        file.parm("prevMode").set(1)
        
        txt = 'create "' + rop.path()+'" and "'+ file.path() +'"'
        hou.ui.setStatusMessage(txt,severity=hou.severityType.ImportantMessage)
        

if len(hou.selectedNodes())>0:
    node = hou.selectedNodes()[0]      
    nodeType = hou.hscript('optype -s %s' % node.path())[0][:-1]  
    if nodeType == "sop":
        txt = "Create 'Redshift Proxy ROP' and import it ?"
        #if hou.ui.displayMessage(txt, buttons=('OK','Cancel',)) == 0 : 
        createNodes()
