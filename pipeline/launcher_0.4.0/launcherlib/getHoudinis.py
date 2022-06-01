import os
import platform
#import socket

def getHoudiniDirs(path):
  try :
    list = next(os.walk(path))[1]
    list.sort()
    return list
  except:
    print(path, 'does not exist')
    return ['']


def getHoudinis(): ## Houdini install directory
	if platform.system()=='Linux': 
		appPath = '/opt' 
	if platform.system()=='Darwin':
		#appPath = '/Library/Frameworks/Houdini.framework/Versions'
		appPath = '/Applications/Houdini'
		#['14.0.444', '15.0.291', '15.0.323', '15.0.378', 'Current']
	if platform.system()=='Windows': 
		appPath = 'C:\Program Files\Side Effects Software'

	dirs = getHoudiniDirs(appPath)

	versions = [d[-8:] for d in dirs if d[-8:].startswith(('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'))]
	print(versions)
	
	return appPath,versions

#appPath,ver = getHoudinis()

#print(appPath)
#print(ver)