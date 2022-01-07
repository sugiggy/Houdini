import hou
for node in hou.selectedNodes():
    depNodes = node.dependents()
    for rop in depNodes:
        path = rop.path()
        if path.startswith('/out'):
            p = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
            p.setCurrentNode(hou.node(path))
            p.homeToSelection()
