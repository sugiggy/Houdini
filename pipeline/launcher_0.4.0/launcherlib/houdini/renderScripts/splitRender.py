import os
import hou
import platform
import subprocess
from subprocess import Popen

#num_split = 1
myFile = hou.hipFile.path()
os.chdir(hou.getenv('HIP'))

orgNodes = hou.selectedNodes()
rops = []
if (len(orgNodes)==1):
    orgNode = orgNodes[0]
    num_split = orgNode.parm('numsplit').eval()
    startFrame = orgNode.parm('f1').eval()
    #print(startFrame)
    for i in range(num_split):
        hou.copyNodesTo(orgNodes,hou.node('/out/'))
        copiedNode = hou.selectedNodes()[0]
        
        copiedNode.parm('f1').deleteAllKeyframes()
        copiedNode.parm('f3').deleteAllKeyframes()
        
        copiedNode.parm('f1').set(startFrame+i)
        copiedNode.parm('f3').set(num_split)
        copiedNode.moveToGoodPosition()
        rops.append(copiedNode)

print('saved hip file')
hou.hipFile.save()

for rop in rops:
    ropPath = rop.path() 
    #command = "splitRender " + myFile + " " + ropPath +  " &"
    if platform.system()=='Linux':
        py = '/mnt/NAS/CG/pipeline/launcher_0.4.0/launcherlib/ropHythonRender.py'
        command = 'hython '+ py +' ' + myFile + " " + ropPath +  " &"
        if 'PYTHONHOME' in os.environ:
            del os.environ['PYTHONHOME']
        #os.system("gnome-terminal -e 'bash -c \""+command+";bash\"'")
        subprocess.call(['/bin/bash', '-i', '-c', command])
    if platform.system()=='Windows':
        py = 'Z:\\CG\pipeline\\launcher_0.4.0\\launcherlib\\ropHythonRender.py'
        command = 'hython '+ py +' ' + myFile + " " + ropPath +  " &"
        subprocess.Popen(command.split())