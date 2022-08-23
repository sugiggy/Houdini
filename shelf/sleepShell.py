import hou
out = hou.node("/out")
rop = out.createNode("shell",'sleep')
rop.moveToGoodPosition()
rop.parm('prerender').set('import time'+ '\n' +'time.sleep(60*60) #1h sleep')
rop.parm('lprerender').set('python')
rop.parm('trange').set(2)
rop.parm('f1').set(1)
rop.parm('f2').set(1)
