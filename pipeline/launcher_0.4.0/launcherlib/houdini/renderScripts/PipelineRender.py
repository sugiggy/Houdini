#node = hou.pwd()
node = kwargs['node']

L_LIB = hou.getenv("LAUNCHER_LIB")

type =  hou.hscript('optype -s %s' % node.path())[0] [:-1]
if type == 'out':
    depenNodes = node.inputDependencies()
else:
    depenNodes = ""    
#print(depenNodes)

if len(depenNodes)>0 :
    for renTuple in depenNodes:
        if renTuple[0].type().name()!='shell' :
            renTuple[0].setSelected(True, clear_all_selected=True)
            renTuple[0].setCurrent(True, clear_all_selected=True)
            exec(open(L_LIB+"/houdini/renderScripts/PreRender.py").read())
            #renTuple[0].render(ignore_inputs=True)
            renTuple[0].parm('execute').pressButton()
            exec(open(L_LIB+"/houdini/renderScripts/PostRender.py").read())
else:
    if node.type().name() !='shell' :
        node.setCurrent(True, clear_all_selected=True)
        exec(open(L_LIB+"/houdini/renderScripts/PreRender.py").read())
        #if node.type().name() == 'usdexport' or node.type().name() == 'usd' or node.type().name() == 'karma':
        #    node.parm('execute').pressButton()
        #else:
        #node.render(ignore_inputs=True)
        node.parm('execute').pressButton()
        exec(open(L_LIB+"/houdini/renderScripts/PostRender.py").read())
