node = kwargs['node']

# ノードが持つparmTemplateGroup()（箱）を取得
group = node.parmTemplateGroup()

parm = hou.ButtonParmTemplate("pipelineRender", "Pipeline Render")
parm.setScriptCallback('exec(open(hou.getenv("LAUNCHER_LIB")+"/houdini/renderScripts/PipelineRender.py").read())')
parm.setScriptCallbackLanguage(hou.scriptLanguage.Python)

group.insertBefore('execute',parm) #insert before execute button
#group.addParmTemplate(parm) # add to end

node.setParmTemplateGroup(group)
#print 'added Pipeline Render Button'




