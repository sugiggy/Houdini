import platform
import os
from os.path import expanduser
import subprocess
import socket
OSTYPE = platform.system()

def getUSER():
	if OSTYPE != 'Windows': return os.environ.get('USER')
	else : return os.environ.get('USERNAME')

def getHOME_DIR():
	if OSTYPE =='Windows':
		return os.path.join(expanduser("~"),'Documents')
	else:
		return expanduser("~")

if OSTYPE == 'Windows': os.environ["USER"] = getUSER()

### Set Global Envrionment

def setGlobalEnv():
	Env = os.environ.copy()
	if platform.system()=='Linux':  
	    Env['NAS']= '/mnt/NAS'
	    Env['CACHE']= '/mnt/CACHE/Houdini'
	    Env['OCIO'] = Env['NAS']+'/CG/pipeline/ocio/aces_1.2/config.ocio'
			
	if platform.system()=='Darwin':
	    Env['NAS'] = '/Volumes/data'
	    Env['CACHE']= '/Volumes/cache/Houdini'
	    Env['LOCAL'] = '/Users/sugiggy/pipeline/ocio/aces_1.0.3/config.ocio"'
	    
	if platform.system()=='Windows': 
	 	Env['NAS'] = 'Z:'
	 	Env['CACHE']= 'Y:/Houdini'
	 	Env['OCIO'] = Env['NAS']+'/CG/pipeline/ocio/aces_1.2/config.ocio'

	Env['LAUNCHER_LIB'] = os.path.dirname(os.path.realpath(__file__))
	#if platform.system()!='Windows': 
	#	Env['PATH'] = '%s:%s' % (Env['LAUNCHER_LIB'],os.environ['PATH'])
	#else:
	#	Env['PATH'] = '%s;%s' % (Env['LAUNCHER_LIB'],os.environ['PATH'])
	#print Env['PATH']	
	 	
	print('set environment varialbe as ' + '$NAS' +' =',Env['NAS'])
	print('set environment varialbe as ' + '$CACHE' +' =',Env['CACHE'])
	print('set environment varialbe as ' + '$LAUNCHER_LIB' +' =',Env['LAUNCHER_LIB'])
	print("\n")

	#print Env
	return Env
	
'''
def subprocess_cmd(command,envSetting):
    process = subprocess.Popen(command,stdout=subprocess.PIPE, shell=True, env=envSetting)
    proc_stdout = process.communicate()[0].strip()
    print proc_stdout
'''

'''
def launchHoudini(envSetting):
	if OSTYPE =='Darwin':
		subprocess_cmd('cd /Library/Frameworks/Houdini.framework/Versions/15.0.323/Resources; source ./houdini_setup;cd - ; hindie &',aEnv)
	if OSTYPE =='Windows':
		import houdini15
		#subprocess_cmd('C:\\Program Files\\Side Effects Software\\Houdini 15.0.362\\bin\\hindie.exe',aEnv)
'''
#launchHoudini(aEnv)