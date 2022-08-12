import hou
import os
from os import listdir
from os.path import isfile, join
import pathlib
from pathlib import Path
import datetime
import math

for cookTimeNode in hou.selectedNodes():

    nodeType = cookTimeNode.type().name()
    if nodeType == 'ifd': parmName = 'vm_picture'
    if nodeType == 'opengl': parmName = 'picture'
    if nodeType == 'comp':   parmName = 'copoutput'
    if nodeType == 'arnold':   parmName = 'ar_picture'
    if nodeType == 'Redshift_ROP': parmName = 'RS_outputFileNamePrefix'
    if nodeType == 'Redshift_Proxy_Output': parmName = 'RS_archive_file'
    if nodeType == 'usdrender_rop' : parmName = 'outputimage'
    if nodeType == 'karma' : parmName = 'picture'    
    
    if nodeType == 'geometry' or nodeType =='ropgeometry': parmName = 'sopoutput'
    if nodeType == 'file':   parmName = 'file'
    if nodeType == 'alembic' :parmName = 'fileName'
    if nodeType == 'fetch': parmName = 'ropoutput'
    if nodeType == 'usdexport': parmName = 'lopoutput'
    if nodeType == 'usdimport': parmName = 'filepath1'
    
    file_parm = cookTimeNode.parm(parmName).eval()
    dirname = os.path.dirname(file_parm)
    ext = pathlib.Path(file_parm).suffix
    files = list(Path(dirname).glob(r'*'+ext))
    files.sort(key=os.path.getmtime)
    cookTime = os.path.getmtime(files[-1])-os.path.getmtime(files[0])
    cookTime /= 60
    #cookTime += 120
    
    #print(cookTime)
    if cookTime>60 :
        hour = math.floor(int(cookTime/60))
        min = str(cookTime-hour*60)[:2]
    else : 
        hour = 0
        min = str(cookTime)[:2]
    cookTimeStr = str(hour) + 'h '  + min + 'm'
    #print(cookTimeStr)
   
    print(cookTimeNode.name() + ' : ' +cookTimeStr + '\n')
