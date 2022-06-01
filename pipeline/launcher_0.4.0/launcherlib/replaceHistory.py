
def DefReplaceHistory(Env):
	files =  ['/dir.history','/file.history']
	paths = ['/mnt/NAS','/Volumes/home','Z:','$NAS//']
	L_paths = ['/mnt/LOCAL','L:','$LOCAL//']

	envDir = Env['HOUDINI_USER_PREF_DIR']

	#file = '/mnt/NAS/CG/pipeline/launcher_0.4.0/launcherlib/houdini/houdini_path19.0/dir.history'

	for file in files:
		f = open(envDir + file, 'r')
		history = f.read()
		#print(read)
		for path in paths:
			history = history.replace(path,'$NAS')
		for L_path in L_paths:
			history = history.replace(L_path,'$LOCAL')
		f.close()


		f = open(envDir + file, 'w')
		f.write(history)
		f.close()
		#print(history)
