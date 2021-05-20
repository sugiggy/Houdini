import os
import subprocess
import platform

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

imgType = ['ifd','opengl','comp','arnold','Redshift_ROP'] 
geoType = ['geometry','file','alembic','Redshift_Proxy_Output']

for node in hou.selectedNodes():
    nodeType = node.type().name()
    #print nodeType

    if nodeType == 'ifd': parmName = 'vm_picture'
    if nodeType == 'opengl': parmName = 'picture'
    if nodeType == 'comp':   parmName = 'copoutput'
    if nodeType == 'arnold':   parmName = 'ar_picture'
    if nodeType == 'Redshift_ROP': parmName = 'RS_outputFileNamePrefix'
    if nodeType == 'Redshift_Proxy_Output': parmName = 'RS_archive_file'

    if nodeType == 'geometry': parmName = 'sopoutput'
    if nodeType == 'file':   parmName = 'file'
    if nodeType == 'alembic' :parmName = 'fileName'  
    
    try:
        path = node.parm(parmName).expression()
        #print path
    except:
        path = node.parm(parmName).eval()

    path = defGetRefPath(path)       

    if nodeType in imgType:
        # for rv
        #ext = os.path.splitext(path)[1]    
        #pad = path[-len(ext)-4:-len(ext)]
        #path = path.replace(pad,'%04d')
        #os.system("rv"+" "+path+ " &")
        #print path
        subprocess.call(['/bin/bash', '-i', '-c', "djv"+" "+path+ " &"]) # for djv , need to add alias djv in .bashrc
        

    if nodeType in geoType:
        path = os.path.dirname(path)
        #print path
        if platform.system()=='Linux': os.system("caja"+" "+path+ " &")
        if platform.system()=='Windows': os.system("explorer"+" "+ path.replace("/", "\\") + " &")
