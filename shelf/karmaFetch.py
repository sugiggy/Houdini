import hou
out = hou.node("/out")
lop = hou.node('/stage')

My_labels = ['Render Current Frame','Render Frame Range','Render Frame Range Only(Strict)']
def addparms(node):
    group = node.parmTemplateGroup()
    parmA = hou.MenuParmTemplate('trange','Valid Frame Range',['off','normal','on'],menu_labels=My_labels,default_value=0)
    parmB = hou.FloatParmTemplate('f','Start/End/Inc',3,disable_when='{trange == off}',naming_scheme=hou.parmNamingScheme.Base1)
    parmC = hou.StringParmTemplate('ropoutput','Output File',1,string_type=hou.stringParmType.FileReference)

    group.insertAfter('source',parmC)
    group.insertAfter('source',parmB)
    group.insertAfter('source',parmA)
    node.setParmTemplateGroup(group)
    
def createFetch(node):
        curParent = node.parent().name()
                
        rop = out.createNode("fetch","karma_"+node.name())
        rop.setColor(hou.Color(0.976,0.78,0.263))
        addparms(rop)
        rop.parm('f1').setExpression('$FSTART')
        rop.parm('f2').setExpression('$FEND')
        rop.parm('f3').set(1)
        rop.parm("source").set(node.path())
                
        ropOutput = '`chs("'+ rop.path() +'/ropoutput")`'
        rop.parm('ropoutput').set('$HIP/render/$OS.$F4.exr')
                
        rop.moveToGoodPosition()
        
        node.parm('trange').setExpression("ch('" + rop.path() + "/trange')")
        node.parm('f1').setExpression('ch("' + rop.path() + '/f1")')
        node.parm('f2').setExpression('ch("' + rop.path() + '/f2")')
        node.parm('f3').setExpression('ch("' + rop.path() + '/f3")')
        node.parm('outputimage').setExpression('chs("' + rop.path() + '/ropoutput")') 
        node.parm('postrender').set('opupdate()')
        
        txt = 'create "' + rop.path()
        hou.ui.setStatusMessage(txt,severity=hou.severityType.ImportantMessage)
        

for node in hou.selectedNodes():
    nodeType = hou.hscript('optype -s %s' % node.path())[0][:-1]  
    if nodeType == "out": createFetch(node)
