import os
import subprocess
import hou
import platform
from subprocess import Popen
dir = hou.getenv('NAS')+ '/Houdini/hip/constrain/'

py = hou.getenv('NAS')+ '/CG/pipeline/launcher_0.4.0/launcherlib/houdini/utilityScripts/hiplcToTxt.py'
for file in os.listdir(dir):
    if file.endswith(".hiplc"):
        command = 'hython '+ py +' ' + dir +' ' + file
        #print(command)
        subprocess.Popen(command.split())
print('converting hiplc files in ' + dir)
