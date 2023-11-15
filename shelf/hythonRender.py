import os
import subprocess
import hou
import platform
from subprocess import Popen

hou.hipFile.save()
myFile = hou.hipFile.path()
os.chdir(hou.getenv('HIP'))

hou.hipFile.save()
print('hip file saved')

"""
if platform.system()=='Linux':
    py = '/mnt/NAS/CG/pipeline/launcher_0.4.0/launcherlib/hythonRender.py'
    command = 'hython '+ py +' ' + myFile
    if 'PYTHONHOME' in os.environ:
        del os.environ['PYTHONHOME']
    subprocess.call(['/bin/bash', '-i', '-c', command])
"""

#if platform.system()=='Windows':
py = hou.getenv('NAS')+'/CG/pipeline/launcher_0.4.0/launcherlib/hythonRender.py'
myCommand = 'hython '+ py +' ' + myFile
#print(myCommand)

if platform.system()=='Windows': 
    subprocess.Popen(myCommand.split())
    
if platform.system()=='Linux':
    command = "x-terminal-emulator -e " + myCommand 
    subprocess.run(command, shell=True)
