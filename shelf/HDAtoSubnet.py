import hou

def copy_parameters(source_node, target_node):
    source_ptg = source_node.parmTemplateGroup()
    target_ptg = target_node.parmTemplateGroup()

    for folder in source_ptg.entries():
        if target_ptg.find(folder.name()) is None:
            target_ptg.append(folder)

    target_node.setParmTemplateGroup(target_ptg)

    for parm in source_node.parms():
        parm_name = parm.name()

        if target_node.parm(parm_name) is not None:
            target_node.parm(parm_name).set(parm.eval())

for node in hou.selectedNodes():
    hda_node = node
    subnet_node = hda_node.parent().createNode("subnet", hda_node.name() + "_subnet")
    
    copy_parameters(hda_node, subnet_node)

    hou.copyNodesTo(hda_node.children(),subnet_node)
    #hou.copyNodesToClipboard(hda_node.children())
    #hou.pasteNodesFromClipboard(subnet_node)
    
    for i in range(len(hda_node.inputs())):
        subnet_node.setInput(i, hda_node.inputs()[i])
