import os
from . import manageOS

USER = manageOS.getUSER()

# folder name
JOS_DIR_NAME = 'job'
SEQS_DIR_NAME = 'seq'
ASSET_DIR_NAME = 'asset'

EDIT_DIR_NAME = 'edit'
IMAGE_DIR_NAME = 'image'
 
'/job/batb/vault/bake/film/pb055/pb055_0100/Tea01/primary_fx_Tea_main_render_ldn.batb.asset.1141951/v006/fbkseq_seed0/bake.#.fbk'

app_dirs = ['houdini','nuke','max','maya','photoshop']

asset_ctgs = ['anim','camera','character','crowd','environment','fx','light','prop','set','veicle']

image_ctgs = ['render','comp','playblast','delivery']

app_dic = {
'houdini' : ['cache','hip','images','render','scripts','tmp'],
'nuke' : ['scripts','render'],
'max' : ['cache','scenes','images','render','scripts','tmp'],
'maya' : ['cache','scenes','images','render','scripts','tmp'],
'photoshop' : ['psd','obj','scripts'],
}

null = '-'

def makeDirIfNotExist(path):
	if not os.path.exists(path):
		#print path
		os.makedirs(path)

def makeAssetWorkDir(shot_path,appName):
	path_list = shot_path.split(os.sep)
	if not null in path_list:
		shot_asset_dir = os.path.join(shot_path,ASSET_DIR_NAME)
		if not os.path.exists(shot_asset_dir):
			print('making shot asset directories in '+ shot_asset_dir)
			for aCtg in asset_ctgs:
				path = os.path.join(shot_asset_dir,aCtg)
				#print path
				os.makedirs(path)

		user_work_dir = os.path.join(shot_path,'work',USER)
		user_app_dir = os.path.join(user_work_dir,appName)
		if not os.path.exists(user_app_dir):
			print('making work directories in '+ user_work_dir + '/' +appName)
			for appSubDir in app_dic[appName]:
				path = os.path.join(user_work_dir,appName,appSubDir)
				#print path
				os.makedirs(path)

#makeAssetWorkDir('/Volumes/home/job/PrologueImpact/seq/ip000/ip000_0080','maya')





 	    