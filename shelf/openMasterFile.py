import os
import subprocess
import hou

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


imgType = ['ifd','opengl','comp','arnold'] 
geoType = ['geometry','file','alembic']

for node in hou.selectedNodes():
    nodeType = node.type().name()
    #print nodeType

    if nodeType == 'ifd': parmName = 'vm_picture'
    if nodeType == 'opengl': parmName = 'picture'
    if nodeType == 'comp':   parmName = 'copoutput'
    if nodeType == 'arnold':   parmName = 'ar_picture'    

    if nodeType == 'geometry': parmName = 'sopoutput'
    if nodeType == 'file':   parmName = 'file'
    if nodeType == 'alembic' :parmName = 'fileName'  
    
    path = node.parm(parmName).eval()
    #try:
        #path = node.parm(parmName).expression()
        #print path
    #except:
        #path = node.parm(parmName).eval()

    path = defGetRefPath(path)       
    dir = os.path.dirname(path)
    list = list(os.path.split(dir))
    list[-1] = 'master_scene'
    new_dir = list[0] + '/' + list[1]
    master_file =''
    for file in os.listdir(new_dir):
        if file.endswith('.hip'):
            master_file = os.path.join(new_dir,file)
    hou.hipFile.load(master_file)          
