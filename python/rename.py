import os
import glob
path = '/home/sugiggy/NAS/Houdini/HoudiniWorkshop/workshop7/week3/render/LightingRBD/Solaris/Lighting/v006/*.exr'

flist = glob.glob(path)

for file in flist:
  print(file)
  new = file.replace('Lighting.','Lighting_')
  os.rename(file,new)
  print(new)
