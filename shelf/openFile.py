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

imgType = ['ifd','opengl','comp','arnold','Redshift_ROP','usdrender_rop','karma'] 
geoType = ['geometry','file','alembic','Redshift_Proxy_Output','ropgeometry','fetch']

for node in hou.selectedNodes():
    nodeType = node.type().name()
    #print(nodeType)

    if nodeType == 'ifd': parmName = 'vm_picture'
    if nodeType == 'opengl': parmName = 'picture'
    if nodeType == 'comp':   parmName = 'copoutput'
    if nodeType == 'arnold':   parmName = 'ar_picture'
    if nodeType == 'Redshift_ROP': parmName = 'RS_outputFileNamePrefix'
    if nodeType == 'Redshift_Proxy_Output': parmName = 'RS_archive_file'
    if nodeType == 'usdrender_rop' : parmName = 'outputimage'
    if nodeType == 'karma' : parmName = 'picture'    
    
    if nodeType == 'geometry' or nodeType =='ropgeometry': parmName = 'sopoutput'
    if nodeType == 'file':   parmName = 'file'
    if nodeType == 'alembic' :parmName = 'fileName'
    if nodeType == 'fetch': parmName = 'ropoutput'
    
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
        #print(path)
        
        # mplay
        if platform.system()=='Windows':
            ext = os.path.splitext(path)[1]    
            pad = path[-len(ext)-4:-len(ext)]
            path = path.replace(pad,'*')
            #print(path)
            os.system("start mplay"+" "+path+ " &")
        
        if platform.system()=='Linux':subprocess.call(['/bin/bash', '-i', '-c', "djv"+" "+path+ " &"]) # for djv , need to add alias djv in .bashrc
        #if platform.system()=='Linux':subprocess.call(['/bin/bash', '-i', '-c', "mplay"+" "+path+ " &"]) # for djv , need to add alias djv in .bashrc
        '''
        if platform.system()=='Windows':
            djv = r'"C:\Program Files\djv-1.1.0-Windows-64\bin\djv_view.exe"'
            #djv = r'"D:\Program Files\DJV2\bin\djv.exe"'
            cmd = "start " + djv+" "+ path.replace("/", "\\") + " &"
            os.system(cmd)
        '''
    if nodeType in geoType:
        path = os.path.dirname(path)
        #print(path)
        #print(platform.system())
        if platform.system()=='Linux': os.system("nemo"+" "+path+ " &")
        if platform.system()=='Windows': os.system("explorer"+" "+ path.replace("/", "\\") + " &")
