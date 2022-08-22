##how to use
##open Houdini Terminal
##Type 'hython renderPython.py hipfile'
import sys
import hou
import os
from datetime import datetime

argvs = sys.argv

notRunTypes = ["shell"]
L_LIB = hou.getenv("LAUNCHER_LIB")

for i in range(1,len(argvs)):
    myFile = argvs[i]
    print ("Open File(s).."+str(i)+" of "+str(len(argvs)-1)+" "+str(myFile))
    hou.hipFile.load(myFile)
    ROPs =  hou.node("/out").children()
    
### making list and render order
    RenderROPs = []
    for R in ROPs:
        nameAndDpenNum = []
        if (R.type().name()) not in notRunTypes and R.isBypassed()==False:
            nameAndDpenNum.append(R)
            nameAndDpenNum.append(R.name())
            nameAndDpenNum.append(len(R.inputDependencies()))
            if R.isBypassed() == False:
                RenderROPs.append(nameAndDpenNum)
        #print len(R.inputs())
        #hou.hscript("render -V "+R.name()) 

    SortedRenderROPs = sorted(RenderROPs, key=lambda aaa: aaa[2])
    #print SortedRenderROPs
    hou.hipFile.clear()
    
### render each rop
    for Ren in SortedRenderROPs:
        hou.hipFile.load(myFile)

        ROPs =  hou.node("/out").children()
        NodeName = Ren[1]

        for Rop in ROPs:
            if Rop.name() == NodeName:
                Rop.bypass(0)
                #frameText = Rop.render(ignore_inputs=True,verbose=False)
                #print Rop
                Rop.setSelected(True, clear_all_selected=True)
                Rop.setCurrent(True, clear_all_selected=True)
                if Rop.type().name()!='shell' and Rop.type().name()!='subnet' :  ## subnet should change once I made printCookTime HDA
                    exec(open(L_LIB+"/houdini/renderScripts/PreRender.py").read())
                #Rop.render(ignore_inputs=True)

                ##Bypass all rops except Current Rop
                for node in ROPs:
                    if node.name() != NodeName: node.bypass(1)

                Rop.parm('execute').pressButton()

                if Rop.type().name()!='shell' and Rop.type().name()!='subnet' :  ## subnet should change once I made printCookTime HDA
                    exec(open(L_LIB+"/houdini/renderScripts/PostRender.py").read())

        #frameText = hou.hscript("render -s -V "+RenName)
		#tmp = os.popen("ls").read()
    hou.hipFile.clear()
