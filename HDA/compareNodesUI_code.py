import os
import hou
import subprocess
from subprocess import Popen

def defGetParms(node,txt):
    for p in node.parms():
        txt += p.path() + '\t'
        value = p.eval()
        if type(value) == str: value = value.replace('\n', ' ')
        txt += str(value) + '\n'  
    return txt

node = kwargs['node']

textfile  = hou.getenv("HIP")+'/nodeInfo.txt'
f = open(textfile, 'w')

txt = ''
if node.parm('children').eval()==1:
    for targetNode in hou.node(node.parm('targetnode').eval()).children():
        txt = defGetParms(targetNode,txt)
else:
    targetNode = hou.node(node.parm('targetnode').eval())
    txt = defGetParms(targetNode,txt)

f.write(txt)
f.close()

#oldFile = 'Z:/Houdini/HoudiniWorkshop/workshop7/test/test_box_old.hiplc'
oldFile = node.parm('targethipfile').eval()

py = r'$NAS/CG/pipeline/launcher_0.4.0/launcherlib/houdini/utilityScripts/compareNodes.py'
command = 'hython '+ py +' '+ oldFile +' '+ textfile 
subprocess.Popen(command.split())
