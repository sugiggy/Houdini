import hou
offset = 0
for node in hou.selectedNodes():
    for p in node.parms():
        keys = p.keyframes()
        for k in keys:
            k.setFrame(k.frame() + offset)
        p.deleteAllKeyframes()
        p.setKeyframes(keys)
        
