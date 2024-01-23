import hou

commonParms = ['timescale','substep','minimumsubstep','substeps']
pyroParms = ['divsize','veldivscale','dissipation','tempdiffusion','tempcooling','buoyancylift','disturbance','disturbance_blocksize','turbulence','turbulence_swirlsize','turbulence_pulselength','shredding','div_amount','viscosity']
flipParms = ['particlesep','gridscale','veltransfer','surfacetension','default_viscosity','doreseeding']

node = kwargs['node']
camera = hou.node(node.parm('camera').eval())
targetNode = hou.node(node.parm('targetnode').eval())

try:
    group = camera.parmTemplateGroup()
    folder = hou.FolderParmTemplate('openGL_view', 'OpenGL View')
    parm = hou.StringParmTemplate('vcomment', "",1)
    parm.setTags({"editor": "1"})
    folder.addParmTemplate(parm)
    group.append(folder)
    camera.setParmTemplateGroup(group)
except: pass

comment = camera.parm('vcomment').unexpandedString();

#node = hou.selectedNodes()[0]

parms = targetNode.parms()
for p in parms:
    if 'folder' not in p.name():
        if targetNode.type().name().startswith('pyro') or targetNode.type().name().startswith('smoke') or targetNode.type().name().startswith('flip'):
            if p.name() in commonParms or p.name() in pyroParms or p.name() in flipParms  :
                comment += p.description() +' : '+ '`substr(chs("' + p.path() + '"),0,6) `' +'\n'
        else: comment += p.description() +' : '+ '`substr(chs("' + p.path() + '"),0,6) `' +'\n'
        
camera.parm('vcomment').set(comment)
