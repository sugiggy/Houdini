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

    group.insertAfter('source',parmC)
    group.insertAfter('source',parmB)
    group.insertAfter('source',parmA)
    group.insertAfter('source',parmRef)
    node.setParmTemplateGroup(group)
    
def createKarma(node):
        curParent = node.parent().name()
        
        karma = node.parent().createNode("karma")
        
        rop = out.createNode("fetch",karma.name())
        addparms(rop)
        rop.parm('f1').setExpression('$FSTART')
        rop.parm('f2').setExpression('$FEND')
        rop.parm('f3').set(1)
        rop.parm("source").set(karma.path()+'/rop_usdrender')
        rop.parm('ref_node').set(karma.path())
        
        ropOutput = '`chs("'+ rop.path() +'/ropoutput")`'
        rop.parm('ropoutput').set('$HIP/render/$OS.$F4.exr')
                
        rop.moveToGoodPosition()
          

        karma.parm('trange').setExpression("ch('" + rop.path() + "/trange')")
        karma.parm('f1').setExpression('ch("' + rop.path() + '/f1")')
        karma.parm('f2').setExpression('ch("' + rop.path() + '/f2")')
        karma.parm('f3').setExpression('ch("' + rop.path() + '/f3")')
        karma.parm('picture').setExpression('chs("' + rop.path() + '/ropoutput")') 
        karma.parm('postrender').set('opupdate()')
        
        karma.setInput(0,node)
        karma.setPosition(node.position() + hou.Vector2(0,-1))
        
        txt = 'create "' + rop.path()
        hou.ui.setStatusMessage(txt,severity=hou.severityType.ImportantMessage)
        

for node in hou.selectedNodes():
    nodeType = hou.hscript('optype -s %s' % node.path())[0][:-1]  
    if nodeType == "lop": createKarma(node)
