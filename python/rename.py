import os
import glob
path = '//vdisk/AAA/vdb/*.vdb'

flist = glob.glob(path)

for file in flist:
  print file
  new = file.replace('u003','u004')
  os.rename(file.new)
  print new
