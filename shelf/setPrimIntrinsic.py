import hou
nodes = hou.selectedNodes()
setInTrans = "setprimintrinsic(0,'pointinstancetransform',@ptnum,1);"
for node in nodes:
    if node.type().name()=='attribwrangle':
        ext_code = node.parm('snippet').eval()
        node.parm('snippet').set(ext_code + '\n' + setInTrans)
