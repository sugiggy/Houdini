import hou
from datetime import datetime

#node = hou.pwd()
node = hou.selectedNodes()[0]
#node = kwargs['node']
startStr = hou.getenv('RenderStartTime')

logfile = hou.getenv('RenderLog')
log = open(logfile, "w")
text = 'Start time: '+ startStr[:-7] +'\n'

#2021-05-14 11:29:33.777000 year need to be 'Y' not 'y'
startTime = datetime.strptime(startStr,'%Y-%m-%d %H:%M:%S.%f')
endTime = datetime.now()
endText = 'End time: ' + str(endTime)[:-7]
text += endText +'\n'
workingTime = endTime - startTime
workingText = "Working time: " + str(workingTime)[:-7]
text += workingText+'\n'


if node.type().name() != 'fetch': 
	range = node.parm('trange').eval()
	startFrame = node.parm('f1').eval()
	endFrame = node.parm('f2').eval()
else:
	parent = hou.node(node.parm('source').eval())
	range = parent.parm('trange').eval()
	startFrame = parent.parm('f1').eval()
	endFrame = parent.parm('f2').eval()


if range!=0:
	frameRange = endFrame-startFrame+1
else:
	frameRange = 1
	
averageTime = workingTime.total_seconds()/60/ frameRange	
averageText = 'Average time: ' + str(averageTime)+' min'
text += str(int(frameRange))+' frames'+'\n'
text += averageText+'\n'

print(endText)
print(workingText)
print(averageText)
print(node.name() + ' Node ended!' +'\n')

log.write(text)
log.close()
hou.unsetenv('RenderStartTime')
hou.unsetenv('RenderLog')