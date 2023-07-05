import hou
import os

dir = hou.getenv('NAS')+ '/Houdini/hip/constrain/'
txtDir = dir + "txtFiles/"

for file in os.listdir(txtDir):
    if file.endswith(".txt"):
        exec(open(txtDir + file).read())
        name = file[:-4]
        #print(txtDir + name)
        fileName = txtDir + name + '.hip'
        #print(fileName)
        if not os.path.exists(fileName): hou.hipFile.save(file_name= fileName)
