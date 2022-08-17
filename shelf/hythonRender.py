import os
import hou
import platform
import subprocess
from subprocess import Popen

#node = kwargs['node']
L_LIB = hou.getenv("LAUNCHER_LIB")

myFile = hou.hipFile.path()
print('saved hip file')
hou.hipFile.save()

"""
if platform.system()=='Linux':
    py = '/mnt/NAS/CG/pipeline/launcher_0.4.0/launcherlib/hythonRender.py'
    if 'PYTHONHOME' in os.environ:
        del os.environ['PYTHONHOME']
    command = 'hython '+ py +' ' + myFile
    subprocess.call(['/bin/bash', '-i', '-c', command])
"""
#if platform.system()=='Windows':
py = hou.getenv("NAS")+'/CG/pipeline/launcher_0.4.0/launcherlib/hythonRender.py'
command = 'hython '+ py +' ' + myFile
subprocess.Popen(command.split())
