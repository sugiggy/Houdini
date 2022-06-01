import os
from shutil import copyfile

#categories = ['lop','out','sop','top']

lopList = ['usdrender_rop','usd_rop','karma']
outList = ['alembic','comp','geometry','ifd','opengl','Redshift_Proxy_Output','Redshift_ROP','usdrender','usd','fetch']
sopList = ['rop_alembic','rop_geometry','usdexport']
topList = ['ropalembic','ropcomposite','ropgeometry','ropmantra','ropusd']

dir = os.path.dirname(__file__)
print (dir)
srcFile = dir +'/sorceFileForAll.py'  ### master file 
dir += '/scripts/'

for nodeType in lopList:
	fileName =  dir + 'lop' + '/' + nodeType +'_oncreated.py'
	copyfile(srcFile,fileName)

for nodeType in outList:
	fileName =  dir + 'out' + '/' + nodeType +'_oncreated.py'
	copyfile(srcFile,fileName)

for nodeType in sopList:
	fileName =  dir + 'sop' + '/' + nodeType +'_oncreated.py'
	copyfile(srcFile,fileName)

for nodeType in topList:
	fileName =  dir + 'top' + '/' + nodeType +'_oncreated.py'
	copyfile(srcFile,fileName)
