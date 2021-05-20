import hou
nodes = hou.node('/').allSubChildren()

preRender = 'execfile("$LAUNCHER_LIB/houdini/renderScripts/PreRender.py")'
postRender = 'execfile("$LAUNCHER_LIB/houdini/renderScripts/PostRender.py")'
for node in nodes:
    try:
        orgPre = node.parm('prerender').unexpandedString()
        #print org
        cleaned_orgPre = orgPre.replace(preRender,'')
        node.parm('prerender').set(cleaned_orgPre)
        #node.parm('lprerender').set('hscript')
        
        orgPost = node.parm('postrender').unexpandedString()
        cleaned_orgPost = orgPost.replace(postRender,'')
        node.parm('postrender').set(cleaned_orgPost)
        #node.parm('postrender').set('hscript')
        #print node.type().name()
    except Exception:
        pass
