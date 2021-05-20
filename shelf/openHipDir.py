import os
import platform
path = os.environ["HIP"]
print hou.hipFile.path()
if platform.system()=='Linux': os.system("caja"+" "+path+ " &")
if platform.system()=='Windows': os.system("explorer"+" "+ path.replace("/", "\\") + " &")
