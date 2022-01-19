import hou
import os

#username = getpass.getuser()

#dir = '/mnt/LOCAL/TMP/'
#print dir
dir = hou.getenv("HOUDINI_TEMP_DIR")+"/"
print dir
files = []
for file in os.listdir(dir):
    if file.endswith(".hiplc"):
        files.append(dir+file)
newest = max(files,key=os.path.getctime)
#print newest

hou.setUpdateMode(hou.updateMode.Manual)
hou.hipFile.load(newest)
