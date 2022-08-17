import sys
import hou
import os
import time

argvs = sys.argv


oldFile = argvs[1]
textfile = argvs[2]

hou.hipFile.load(oldFile)


with open(textfile) as file:
    cur_txt = [s.strip() for s in file.readlines()]

newNodes = []
for i in range(len(cur_txt)):
    try:
        path_value = cur_txt[i].split('\t')
        path = path_value[0]
        nodePath = os.path.dirname(path)
        node = hou.node(nodePath)

        if nodePath not in newNodes and node==None : newNodes.append(nodePath)
    
        oldValue = hou.parm(path).eval()
        if type(oldValue) == str: oldValue = oldValue.replace('\n', ' ')
        curValue = path_value[1]
        if str(oldValue) != curValue :
            print(path)
            print('old Value: ' + str(oldValue) + ' current Value: ' + curValue + '\n')
    except: pass
print('new Node(s): ', newNodes)
os.system("pause")
