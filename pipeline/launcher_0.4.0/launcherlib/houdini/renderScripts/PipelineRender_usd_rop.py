node = kwargs['node']
hou.node(node.path()+'/usd1').parm('pipelineRender').pressButton()
p = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
p.setCurrentNode(node) 
#p.homeToSelection()