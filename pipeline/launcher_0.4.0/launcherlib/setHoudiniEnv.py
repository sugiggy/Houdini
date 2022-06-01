import os
import platform
from . import manageOS
import socket


lib_path = os.path.dirname(__file__) # /mnt/NAS/CG/pipeline/launcher_0.4.0/launcherlib
print(lib_path)

def setHoudiniEnv(Env,appPath,ver):
	
	verlist = ver.split('.')

	HOME_DIR = manageOS.getHOME_DIR()
	
	print(HOME_DIR)

	if platform.system()=='Linux':  
	    Env['HFS'] = appPath +'/hfs'+ ver

	if platform.system()=='Darwin':
	    Env['HFS'] = appPath + '/Houdini'+ ver +'/Frameworks/Houdini.framework/Versions/Current/Resources'

	if platform.system()=='Windows': 
	 	Env['HFS'] = appPath +'/Houdini '+ver
	 	#print Env['HFS']
	 	#Env['HFS'] = "C:\Program Files\Side Effects Software\Houdini 18.5.563"
	print(Env['HFS'])

	Env['HB'] = '%s/bin' % Env['HFS']

	Env['H'] = Env['HFS']
	Env['HD'] = '%s/demo' % Env['H']
	Env['HH'] = '%s/houdini' % Env['H']
	Env['HHC'] = '%s/config' % Env['HH']
	if int(verlist[0]) > 18:
		Env['HHP'] ='%s/python3.7libs' % Env['HH']
	else: Env['HHP'] ='%s/python2.7libs' % Env['HH']
	Env['HT'] = '%s/toolkit' % Env['H']


	if platform.system()!='Windows': 
		Env['PATH'] = '%s:%s' % (Env['HB'],os.environ['PATH'])
	else:
		Env['PATH'] = '%s;%s' % (Env['HB'],os.environ['PATH'])
	 
	Env['HOUDINI_MAJOR_RELEASE'] = verlist[0]
	Env['HOUDINI_MINOR_RELEASE'] = verlist[1]
	Env['HOUDINI_BUILD_VERSION'] = verlist[2]
	Env['HOUDINI_VERSION'] = '%s.%s.%s' % (Env['HOUDINI_MAJOR_RELEASE'], Env['HOUDINI_MINOR_RELEASE'],Env['HOUDINI_BUILD_VERSION'])
	 
	Env['HIH'] = '%s/houdini%s.%s' % (HOME_DIR, Env['HOUDINI_MAJOR_RELEASE'],Env['HOUDINI_MINOR_RELEASE'])
	Env['HIS'] = Env['HH']

	#Env['NASJOB']='%s/job' % Env['NAS']
	
	h_path = lib_path +'/houdini/houdini_path'+Env['HOUDINI_MAJOR_RELEASE']+'.'+Env['HOUDINI_MINOR_RELEASE'] ## onCreateScript
	#print(h_path)
	if platform.system()!='Windows':
		Env['HOUDINI_PATH']= h_path +':&'
		#print Env['HOUDINI_PATH']
	else:
		Env['HOUDINI_PATH']= h_path +';&'
	print(Env['HOUDINI_PATH'])

##### sharing tools for 		
	## hconfig -ap  in terminal show how to add Env
	Env['HOUDINI_USER_PREF_DIR'] = Env['NAS']+'/Houdini/env/houdini'+ ver[:4]

	print(Env['HOUDINI_USER_PREF_DIR'])
	#if platform.system()!='Windows':
	#	Env['HOUDINI_TOOLBAR_PATH']='$NAS/Houdini/env/houdini'+ ver[:4] +'/toolbar:@/^'
	#else:
		#Env['HOUDINI_TOOLBAR_PATH']='$NAS/Houdini/env/houdini'+ ver[:4] +'/toolbar;@/^'
	#print Env['HOUDINI_TOOLBAR_PATH']

	if platform.system()=='Linux':
		#Env['PYTHONIOENCODING']='utf-8'
		if int(verlist[0]) > 18:
			Env['PXR_PLUGINPATH_NAME'] = '/usr/redshift/redshift4solaris/19.0.589'
		else:
			Env['PXR_PLUGINPATH_NAME'] = '/usr/redshift/redshift4solaris/18.5.759'
		
		Env['REDSHIFT_CACHEPATH'] = '/mnt/CACHE/TMP/redshift'
		print(Env['PXR_PLUGINPATH_NAME'])
		if socket.gethostname().startswith('Threadripper'):
			Env['HOUDINI_TEMP_DIR']='/mnt/CACHE/TMP'
			
	if platform.system()=='Windows':
		if socket.gethostname().startswith('threadripper'):
			Env['HOUDINI_TEMP_DIR']='Y:\\TMP'
			Env['PATH'] = "C:\\ProgramData\\Redshift\\bin;"+Env['PATH']
			
		if int(verlist[0]) > 18:
			Env['HOUDINI_PATH'] = h_path + ';&' + "C:\\ProgramData\\Redshift\\Plugins\\Houdini\\19.0.589;&"
			Env['PXR_PLUGINPATH_NAME'] = "C:\\ProgramData\\Redshift\\Plugins\\Solaris\\19.0.589"
			print('redshift_windows')
		'''	
		else:
			Env['PXR_PLUGINPATH_NAME'] = 'C:\\ProgramData\\Redshift\\Plugins\\Solaris\\18.5.759'
		'''
	#Env['OTL']=('%s/Houdini/otls/houdini'+Env['HOUDINI_MAJOR_RELEASE']+'.'+Env['HOUDINI_MINOR_RELEASE']) % Env['NAS']
	#Env['HOUDINI_OTLSCAN_PATH']='$HIH/otls:$HIH/otls/wip:$QOTL/base:$QOTL/future:$QOTL/experimental:@/otls:$OTL'

	return Env

