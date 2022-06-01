import hou
import os
from datetime import datetime
import sys

#node = hou.selectedNodes()[0] ## select node in ROP
def getNodeSaveDir(node):
	nodeType = node.type().name()
	#print nodeType
	if nodeType != 'fetch':
	##ROPs
		if nodeType == 'geometry': parmName = 'sopoutput'
		if nodeType == 'ifd': parmName = 'vm_picture'
		if nodeType == 'opengl': parmName = 'picture'
		if nodeType == 'comp':   parmName = 'copoutput'
		if nodeType == 'arnold':   parmName = 'ar_picture'
		if nodeType == 'alembic' : parmName = 'filename'
		if nodeType == 'Redshift_Proxy_Output': parmName = 'RS_archive_file'
		if nodeType == 'Redshift_ROP': parmName = 'RS_outputFileNamePrefix'
		if nodeType == 'usdrender' : parmName = 'outputimage'
		if nodeType == 'usd_rop' : parmName = 'lopoutput'
		##LOPs
		if nodeType == 'usdrender_rop' : parmName = 'outputimage'
		if nodeType == 'usd' : parmName = 'lopoutput'
		if nodeType == 'karma' or nodeType == 'karmarenderproperties' : parmName = 'picture'
		if nodeType == 'rop_usdrender' : parmName = 'outputimage'
		##TOPs
		if nodeType == 'ropmantra' : parmName = 'vm_picture'
		if nodeType == 'ropcomposite' : parmName = 'copoutput'
		if nodeType == 'ropgeometry' : parmName = 'sopoutput'
		if nodeType == 'ropalembic' : parmName = 'filename'
		if nodeType == 'ropusd' : parmName = 'lopoutput'
		##SOPs
		if nodeType == 'usdexport' : parmName = 'lopoutput'
		if nodeType == 'rop_geometry' : parmName = 'sopoutput'
		

		'''
		if nodeType =='karma':
			filePath = hou.node(node.path()+'/karmarenderproperties').parm(parmName).eval()
		else: filePath = node.parm(parmName).eval()
		'''	
		filePath = node.parm(parmName).eval()
		#filePath = hou.hipFile.name()
		#filePath = '/mnt/NAS/Houdini/python/geo/test.bgeo.sc'

		dirPath = os.path.dirname(filePath)
		#print dirPath
		return dirPath

def getParentSaveDir(node):
	print(node.type().name())
	if node.type().name()=='fetch':	
		path = node.parm('source').eval()
		node = hou.node(path) 
		if node.parent().type().name() == 'karma':
			node = node.parent()

	if node.type().name()=='usdrender_rop' and node.parent().type().name() == 'karma':
		node = node.parent()
	
	dirPath = getNodeSaveDir(node)
	return dirPath


#node = hou.pwd()
#node = kwargs['node']
node = hou.selectedNodes()[0]

orgName = hou.hipFile.path()
baseName = hou.hipFile.basename()

## keep master file
#print(node.type().name())
if node.type().name()=='fetch' or node.type().name()=='usdrender_rop':
	dir = getParentSaveDir(node)
else: dir = getNodeSaveDir(node)
#print(dir)

if os.path.exists(dir)==False: os.makedirs(dir)


hou.hipFile.save(dir+'/'+node.name()+'_'+baseName,False)
hou.hipFile.setName(orgName)

startTime = datetime.now()
startStr = str(startTime)
print(node.name() + ' Node started!')

if node.type().name() != 'fetch': 
	range = node.parm('trange').eval()
	startFrame = node.parm('f1').eval()
	endFrame = node.parm('f2').eval()
else:
	parent = hou.node(node.parm('source').eval())
	range = parent.parm('trange').eval()
	startFrame = parent.parm('f1').eval()
	endFrame = parent.parm('f2').eval()

if range!=0:
	print(str(int(startFrame)) + ' - ' + str(int(endFrame))+' frame')
else: '1 frame'

print('Start time: ' + startStr)
hou.hscript("set -g RenderStartTime={}".format(startStr))

logfile = dir+"/log_"+node.name()+'_'+ str(startTime.date())+' '+str(startTime.time())[:-10].replace(":", "_") +".txt"
#print logfile
hou.hscript("set -g RenderLog={}".format(logfile))

#print(range)