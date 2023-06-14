import hou
RopType = ['usd','alembic','cs_meshCache','geometry','CS::csCache::001']
for node in hou.selectedNodes():
    if node.type().name() in RopType:
        node.parm('cs_new_version').pressButton()
        print(node.name() + ' v' + str(node.parm('cs_user_version').eval()))
    if node.type().name() == 'fetch':
        path = node.parm('source').eval()
        sourceNode = hou.node(path).parent().parent()
        sourceNode.parm('cs_new_version').pressButton()
        print(sourceNode.name() + ' v' + str(sourceNode.parm('cs_user_version').eval()))
