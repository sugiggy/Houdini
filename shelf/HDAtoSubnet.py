import hou

# Get the HDA node
for hda_node in hou.selectedNodes():
    #hda_node = hou.selectedNodes()[0]
    
    # Create a subnet node at the same level as the HDA node
    subnet_node = hda_node.parent().createNode("subnet", hda_node.name() + "_subnet")
    
    # Copy parameters from HDA node to subnet node
    for parm in hda_node.parms():
        # Check if the parameter already exists on the subnet node
        if subnet_node.parm(parm.name()) is None:
            # If not, create it
            template = parm.parmTemplate()
            subnet_node.addSpareParmTuple(template)
        # Now, copy the value
        subnet_node.parm(parm.name()).set(parm.eval())
    
    # Move the children of the HDA node to the subnet node
    for child in hda_node.children():
        child.copyTo(subnet_node)
        
    for i in range(len(hda_node.inputs())):
        subnet_node.setInput(i, hda_node.inputs()[i])
        

#hda_node.destroy()
