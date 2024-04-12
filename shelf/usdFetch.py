import hou
out = hou.node("/out")
lop = hou.node('/stage')

My_labels = ['Render Current Frame','Render Frame Range','Render Frame Range Only(Strict)']
def addparms(node):
    group = node.parmTemplateGroup()
    parmRef = hou.StringParmTemplate('ref_node','reference node',1,string_type=hou.stringParmType.NodeReference)
    parmA = hou.MenuParmTemplate('trange','Valid Frame Range',['off','normal','on'],menu_labels=My_labels,default_value=0)
    parmB = hou.FloatParmTemplate('f','Start/End/Inc',3,disable_when='{trange == off}',naming_scheme=hou.parmNamingScheme.Base1)
    parmC = hou.StringParmTemplate('ropoutput','Output File',1,string_type=hou.stringParmType.FileReference)
    parmSFPF = hou.ToggleParmTemplate('fileperframe', 'Separate File Per Frame')
    group.insertAfter('source',parmSFPF)
    group.insertAfter('source',parmC)
    group.insertAfter('source',parmB)
    group.insertAfter('source',parmA)
    group.insertAfter('source',parmRef)
    node.setParmTemplateGroup(group)
    
def createFetch(node):
    curParent = node.parent().name()
    
    usdexport = node.parent().createNode("usdexport")
    
    name = node.name()
    if name.startswith('OUT_') == True : name = name[4:]
    
    
    rop = out.createNode("fetch",name)
    rop.setColor(hou.Color(0.584,0.776,1))
    addparms(rop)
    rop.parm('f1').setExpression('$FSTART')
    rop.parm('f2').setExpression('$FEND')
    rop.parm('f3').set(1)
    rop.parm("source").set(usdexport.path()+'/lopnet_EXPORT/USD_OUT')
    rop.parm('ref_node').set(usdexport.path())
    rop.parm('fileperframe').set(0)
    
    ropOutput = '`chs("'+ rop.path() +'/ropoutput")`'
    rop.parm('ropoutput').set('$CACHE/`$OS`/v001/`$OS`.usd')
    
    
    ref = lop.createNode("reference",name)
    ref.parm("filepath1").set(ropOutput)
    
    rop.moveToGoodPosition()
    ref.moveToGoodPosition()          
          
    try:
        outNodes = node.outputs()
        for i,outNode in enumerate(outNodes):
            for j,inNode in enumerate(outNode.inputs()):
                if inNode!= None:
                    if inNode.name() == name:
                        #print j
                        outNode.setInput(j,usdexport)
    except:
        pass
    

    usdexport.parm('trange').setExpression("ch('" + rop.path() + "/trange')")
    usdexport.parm('f1').setExpression('ch("' + rop.path() + '/f1")')
    usdexport.parm('f2').setExpression('ch("' + rop.path() + '/f2")')
    usdexport.parm('f3').setExpression('ch("' + rop.path() + '/f3")')
    usdexport.parm('lopoutput').setExpression('chs("' + rop.path() + '/ropoutput")') 
    usdexport.parm('fileperframe').setExpression('ch("' + rop.path() + '/fileperframe")')
    usdexport.parm('postrender').set('opupdate()')
    
    usdexport.parm('enable_attribs').set(1)
    usdexport.parm('enable_subsetgroups').set(1)
    usdexport.parm('subsetgroups').set('*')
    
    usdexport.setInput(0,node)
    usdexport.setPosition(node.position() + hou.Vector2(0,-1))
    txt = 'create "' + rop.path()+'" , "'+ rop.path() +'"'+ ref.path()
    hou.ui.setStatusMessage(txt,severity=hou.severityType.ImportantMessage)
    
    usdimport = node.parent().createNode("usdimport")
    usdimport.parm('filepath1').setExpression('chs("' + rop.path() + '/ropoutput")') 
    usdimport.setPosition(usdexport.position() + hou.Vector2(0,-1))
    
for node in hou.selectedNodes():      
    nodeType = hou.hscript('optype -s %s' % node.path())[0][:-1]  
    if nodeType == "sop":
        createFetch(node)
        
