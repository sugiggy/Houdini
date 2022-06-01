##how to use
##open Houdini Terminal
##Type 'hython splitRender.py hipfile rop'
import sys
import hou
import os


argvs = sys.argv

myFile = argvs[1]
print ("Open File(s).."+str(myFile))
hou.hipFile.load(myFile)

print("start.." + argvs[2])
rop = hou.node(argvs[2])
rop.parm('execute').pressButton()
hou.hipFile.clear()
