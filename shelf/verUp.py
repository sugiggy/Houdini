import re

def defGetRefPath(path):
    if path.startswith("`ch"):
        refPath = path.split("'")[0]
        refPathList = refPath.split('"')[1].split('/')
        refNode = hou.node("/".join(refPathList[:-1]))
        path = refNode.parm(refPathList[-1]).unexpandedString()
        
        return path

    if path.startswith("`ch"):
        defGetRefPath(path)

    else : return path

supportList = ['opengl','comp','file','alembic','rop_geometry','geometry']

for node in hou.selectedNodes():
    nodeType = node.type().name()
    #print nodeType
    
    if nodeType in supportList :
        hou.cd(node.path())

        if nodeType == 'opengl': parmName = 'picture'
        if nodeType == 'comp': parmName = 'copoutput'
        if nodeType == 'file': parmName = 'file'
        if nodeType == 'alembic':parmName = 'fileName'
        if nodeType == 'rop_geometry' or nodeType == 'geometry': parmName = 'sopoutput'
        if nodeType == 'ifd': parmName = 'vm_picture'
        
        path = node.parm(parmName).unexpandedString()
        path = defGetRefPath(path)        
        parm = node.parm(parmName)
        
        pathList = re.split(r'[._/-]+',path)
        #print pathList
        matches = [item for item in pathList if (item.startswith('v') or item.startswith('u'))and item[1:].isdigit()]
        #print matches
        
        if len(matches)>0:
            version = matches[0]
            #print version
            
            curVersion = version[1:]
            pad = len(curVersion)
            
            newVersion = version[0] + str(max(0,int(curVersion) + 1)).zfill(pad) #########here to change
            #print curVersion
            #print newVersion
            
            #print path
            newPath = path.replace(version, newVersion)
            #print 'old\n',path
            #print 'new\n',newPath
            
            parm.revertToDefaults() ## to break reference
            parm.set(newPath)
            node.setPosition(node.position()+hou.Vector2(0,0.001))
