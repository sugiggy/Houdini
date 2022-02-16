import hou
num_copy = 3

orgNodes = hou.selectedNodes()
if (len(orgNodes)==1):
    orgNode = orgNodes[0]
    startFrame = orgNode.parm('f1').eval()
    #print(startFrame)
    for i in range(num_copy):
        hou.copyNodesTo(orgNodes,hou.node('/out/'))
        copiedNode = hou.selectedNodes()[0]
        copiedNode.parm('f1').deleteAllKeyframes()
        copiedNode.parm('f3').deleteAllKeyframes()
        
        copiedNode.parm('f1').set(startFrame+i)
        copiedNode.parm('f3').set(num_copy)
        copiedNode.moveToGoodPosition()
