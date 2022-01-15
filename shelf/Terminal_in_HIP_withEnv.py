import os
import platform
import subprocess
os.chdir(hou.getenv('HIP'))
#os.system("pwd")
if platform.system()=='Linux':
    if 'PYTHONHOME' in os.environ:
        del os.environ['PYTHONHOME']
    os.system("gnome-terminal")
    
if platform.system()=='Windows': subprocess.Popen('cmd')


#import subprocess
#subprocess.Popen(['/bin/bash', '-c', 'pwd &'])
#print subprocess.check_output("pwd &", shell=True)
