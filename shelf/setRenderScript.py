#file = '$LAUNCHER_LIB/houdini/Pre-Render_Script/keepMasterFile.py'
#node.parm('prerender').set('exec(compile(open('+ file +').read(),'+file+', "exec"))' )

pre = 'execfile("$LAUNCHER_LIB/houdini/renderScripts/PreRender.py")'
post = 'execfile("$LAUNCHER_LIB/houdini/renderScripts/PostRender.py")'

for node in hou.selectedNodes():
    orgPre = node.parm('prerender').eval()
    orgPost = node.parm('postrender').eval()
    if len(orgPre)>0:
        pre = orgPre+ '\n' + pre
    node.parm('prerender').set(pre)
    node.parm('lprerender').set('python')
    if len(orgPost)>0:
        post = orgPost + '\n' + post
    node.parm('postrender').set(post)
    node.parm('lpostrender').set('python')

