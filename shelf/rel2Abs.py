import hou
def defGetRefParmPath(path):
    if path.startswith("`ch") or path.startswith("ch"):
        refPath = path.split("'")[0]
        refPathList = refPath.split('"')[1].split('/')
        refNode = hou.node("/".join(refPathList[:-1]))
        path = refNode.parm(refPathList[-1]).path()
        return path
        if path.startswith("`ch") or path.startswith("ch"):
            defGetRefParmPath(path)
            
    else: return path
    
for node in hou.selectedNodes():
    cd = hou.cd(node.path())
    #print cd
    for p in node.parms():
        try:
            try:
                oldValue = p.expression()
            except:
                oldValue = p.unexpandedString()
        except:oldValue = p.eval()
        #oldValue = p.unexpandedString()
        if type(oldValue) is not int and type(oldValue) is not float :
            try:
                if (oldValue.startswith("ch") or oldValue.startswith("`ch")) and "../" in oldValue :
                    absPath = defGetRefParmPath(oldValue)
                    start = oldValue.find('"')+1
                    end = oldValue.find('"',start+1)
                    newValue =  oldValue[0:start] + absPath + oldValue[end:]
                    
                    if oldValue.startswith("ch"):
                        p.deleteAllKeyframes()
                        p.setExpression(newValue)
                    else:
                        p.revertToDefaults()
                        p.set(newValue)
            except:
                pass
                
