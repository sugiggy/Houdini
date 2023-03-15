import sys
import toolutils

outputitem = None
inputindex = -1
inputitem = None
outputindex = -1

num_args = 1
h_extra_args = ''
pane = toolutils.activePane(kwargs)
if not isinstance(pane, hou.NetworkEditor):
    pane = hou.ui.paneTabOfType(hou.paneTabType.NetworkEditor)
    if pane is None:
       hou.ui.displayMessage(
               'Cannot create node: cannot find any network pane')
       sys.exit(0)
else: # We're creating this tool from the TAB menu inside a network editor
    pane_node = pane.pwd()
    if "outputnodename" in kwargs and "inputindex" in kwargs:
        outputitem = pane_node.item(kwargs["outputnodename"])
        inputindex = kwargs["inputindex"]
        h_extra_args += 'set arg4 = "' + kwargs["outputnodename"] + '"\n'
        h_extra_args += 'set arg5 = "' + str(inputindex) + '"\n'
        num_args = 6
    if "inputnodename" in kwargs and "outputindex" in kwargs:
        inputitem = pane_node.item(kwargs["inputnodename"])
        outputindex = kwargs["outputindex"]
        h_extra_args += 'set arg6 = "' + kwargs["inputnodename"] + '"\n'
        h_extra_args += 'set arg9 = "' + str(outputindex) + '"\n'
        num_args = 9
    if "autoplace" in kwargs:
        autoplace = kwargs["autoplace"]
    else:
        autoplace = False
    # If shift-clicked we want to auto append to the current
    # node
    if "shiftclick" in kwargs and kwargs["shiftclick"]:
        if inputitem is None:
            inputitem = pane.currentNode()
            outputindex = 0
    if "nodepositionx" in kwargs and             "nodepositiony" in kwargs:
        try:
            pos = [ float( kwargs["nodepositionx"] ),
                    float( kwargs["nodepositiony"] )]
        except:
            pos = None
    else:
        pos = None

    if not autoplace and not pane.listMode():
        if pos is not None:
            pass
        elif outputitem is None:
            pos = pane.selectPosition(inputitem, outputindex, None, -1)
        else:
            pos = pane.selectPosition(inputitem, outputindex,
                                      outputitem, inputindex)

    if pos is not None:
        if "node_bbox" in kwargs:
            size = kwargs["node_bbox"]
            pos[0] -= size[0] / 2
            pos[1] -= size[1] / 2
        else:
            pos[0] -= 0.573625
            pos[1] -= 0.220625
        h_extra_args += 'set arg2 = "' + str(pos[0]) + '"\n'
        h_extra_args += 'set arg3 = "' + str(pos[1]) + '"\n'
h_extra_args += 'set argc = "' + str(num_args) + '"\n'

pane_node = pane.pwd()
child_type = pane_node.childTypeCategory().nodeTypes()

if 'subnet' not in child_type:
   hou.ui.displayMessage(
           'Cannot create node: incompatible pane network type')
   sys.exit(0)

# First clear the node selection
pane_node.setSelected(False, True)

h_path = pane_node.path()
h_preamble = 'set arg1 = "' + h_path + '"\n'
h_cmd = r'''
if ($argc < 2 || "$arg2" == "") then
   set arg2 = 0
endif
if ($argc < 3 || "$arg3" == "") then
   set arg3 = 0
endif
# Automatically generated script
# $arg1 - the path to add this node
# $arg2 - x position of the tile
# $arg3 - y position of the tile
# $arg4 - input node to wire to
# $arg5 - which input to wire to
# $arg6 - output node to wire to
# $arg7 - the type of this node
# $arg8 - the node is an indirect input
# $arg9 - index of output from $arg6

\set noalias = 1
set saved_path = `execute("oppwf")`
opcf $arg1

# Node $_obj_parameterPrint (Object/subnet)
set _obj_parameterPrint = `run("opadd -e -n -v subnet parameterPrint")`
oplocate -x `$arg2 + 0` -y `$arg3 + 0` $_obj_parameterPrint
opspareds '    group {         name    "stdswitcher3"         label   "Transform"         invisibletab          parm {             name    "xOrd"             baseparm             label   "Transform Order"             joinnext             export  none         }         parm {             name    "rOrd"             baseparm             label   "Rotate Order"             nolabel             export  none         }         parm {             name    "t"             baseparm             label   "Translate"             export  none         }         parm {             name    "r"             baseparm             label   "Rotate"             export  none         }         parm {             name    "s"             baseparm             label   "Scale"             export  none         }         parm {             name    "p"             baseparm             label   "Pivot Translate"             export  none         }         parm {             name    "pr"             baseparm             label   "Pivot Rotate"             export  none         }         parm {             name    "scale"             baseparm             label   "Uniform Scale"             export  none         }         parm {             name    "pre_xform"             baseparm             label   "Modify Pre-Transform"             export  none         }         parm {             name    "keeppos"             baseparm             label   "Keep Position When Parenting"             export  none         }         parm {             name    "childcomp"             baseparm             label   "Child Compensation"             export  none         }         parm {             name    "constraints_on"             baseparm             label   "Enable Constraints"             export  none         }         parm {             name    "constraints_path"             baseparm             label   "Constraints"             export  none         }         parm {             name    "lookatpath"             baseparm             label   "Look At"             invisible             export  none         }         parm {             name    "lookupobjpath"             baseparm             label   "Look Up Object"             invisible             export  none         }         parm {             name    "lookup"             baseparm             label   "Look At Up Vector"             invisible             export  none         }         parm {             name    "pathobjpath"             baseparm             label   "Path Object"             invisible             export  none         }         parm {             name    "roll"             baseparm             label   "Roll"             invisible             export  none         }         parm {             name    "pos"             baseparm             label   "Position"             invisible             export  none         }         parm {             name    "uparmtype"             baseparm             label   "Parameterization"             invisible             export  none         }         parm {             name    "pathorient"             baseparm             label   "Orient Along Path"             invisible             export  none         }         parm {             name    "up"             baseparm             label   "Orient Up Vector"             invisible             export  none         }         parm {             name    "bank"             baseparm             label   "Auto-Bank factor"             invisible             export  none         }     }      group {         name    "stdswitcher3_1"         label   "Subnet"         invisibletab          parm {             name    "label1"             baseparm             label   "Input #1 Label"             export  all         }         parm {             name    "label2"             baseparm             label   "Input #2 Label"             export  all         }         parm {             name    "label3"             baseparm             label   "Input #3 Label"             export  all         }         parm {             name    "label4"             baseparm             label   "Input #4 Label"             export  all         }         parm {             name    "tdisplay"             baseparm             label   "Display"             joinnext             export  all         }         parm {             name    "display"             baseparm             label   "Display"             export  all         }         parm {             name    "outputobj"             baseparm             label   "Output Transform"             export  all         }         parm {             name    "visibleobjects"             baseparm             label   "Visible Children"             export  none         }         parm {             name    "picking"             baseparm             label   "Viewport Selecting Enabled"             export  none         }         parm {             name    "pickscript"             baseparm             label   "Select Script"             export  none         }         parm {             name    "caching"             baseparm             label   "Cache Object Transform"             export  none         }         parm {             name    "use_dcolor"             baseparm             label   "Set Wireframe Color"             invisible             export  none         }         parm {             name    "dcolor"             baseparm             label   "Wireframe Color"             invisible             export  none         }     }      parm {         name    "camera"         label   "Camera"         type    oppath         default { "" }         parmtag { "opfilter" "!!OBJ/CAMERA!!" }         parmtag { "oprelative" "." }         parmtag { "script_callback_language" "python" }     }     parm {         name    "targetnode"         label   "Target Node"         type    oppath         default { "" }         parmtag { "oprelative" "." }         parmtag { "script_callback_language" "python" }     }     parm {         name    "getaddparms"         label   "Get/Add Parameters"         type    button         joinnext         default { "0" }         parmtag { "script_callback" "exec(kwargs[\'node\'].parm(\'code\').eval())" }         parmtag { "script_callback_language" "python" }     }     parm {         name    "clear"         label   "Clear"         type    button         default { "0" }         parmtag { "script_callback" "exec(kwargs[\'node\'].parm(\'code1\').eval())" }         parmtag { "script_callback_language" "python" }     }     groupcollapsible {         name    "python"         label   "Python"          parm {             name    "code"             label   "Code"             type    string             default { "" }             parmtag { "editor" "1" }             parmtag { "editorlang" "python" }             parmtag { "script_callback_language" "python" }         }         parm {             name    "code1"             label   "Code1"             type    string             default { "" }             parmtag { "editor" "1" }             parmtag { "editorlang" "python" }             parmtag { "script_callback_language" "python" }         }     }  ' $_obj_parameterPrint
opset -S on $_obj_parameterPrint
opparm -V 19.5.332 $_obj_parameterPrint camera ( /obj/cam1 ) targetnode ( /obj/flip_sim/popdrag1 ) python ( 1 ) code ( 'import hou\n\ncommonParms = [\'timescale\',\'substep\',\'minimumsubstep\',\'substeps\']\npyroParms = [\'divsize\',\'veldivscale\',\'dissipation\',\'tempdiffusion\',\'tempcooling\',\'buoyancylift\',\'disturbance\',\'disturbance_blocksize\',\'turbulence\',\'turbulence_swirlsize\',\'turbulence_pulselength\',\'shredding\',\'div_amount\',\'viscosity\']\nflipParms = [\'particlesep\',\'radiusscale\',\'gridscale\',\'veltransfer\',\'surfacetension\',\'default_viscosity\',\'doreseeding\']\n\nnode = kwargs[\'node\']\ncamera = hou.node(node.parm(\'camera\').eval())\ntry:\n    group = camera.parmTemplateGroup()\n    folder = hou.FolderParmTemplate(\'openGL_view\', \'OpenGL View\')\n    parm = hou.StringParmTemplate(\'vcomment\', "",1)\n    parm.setTags({"editor": "1"})\n    folder.addParmTemplate(parm)\n    group.append(folder)\n    camera.setParmTemplateGroup(group)\n    comment = \'\'\nexcept: comment = camera.parm(\'vcomment\').unexpandedString();\n\n#node = hou.selectedNodes()[0]\ntargetNode = hou.node(node.parm(\'targetnode\').eval())\nparms = targetNode.parms()\n\nif targetNode.type().name().startswith(\'pyro\') or targetNode.type().name().startswith(\'smoke\') or targetNode.type().name().startswith(\'flip\'):\n    for p in parms:\n        if p.name() in commonParms or p.name() in pyroParms or p.name() in flipParms  :\n            if type(p.eval()) != str :\n                comment += p.description() +\' : \'+ \'\\`substr(chs("\' + p.path() + \'"),0,6) \\`\' +\'\\n\'\n            else:\n                comment += p.description() +\' : \'+ \'\\`(chs("\' + p.path() + \'")) \\`\' +\'\\n\'\nelse: \n    for p in parms:\n        if \'group\' not in p.name() and \'folder\' not in p.name():\n            if type(p.eval()) != str :\n                comment += p.description() +\' : \'+ \'\\`substr(chs("\' + p.path() + \'"),0,6) \\`\' +\'\\n\'\n            else:\n                comment += p.description() +\' : \'+ \'\\`(chs("\' + p.path() + \'")) \\`\' +\'\\n\'\n\ncamera.parm(\'vcomment\').set(comment)' ) code1 ( 'node = kwargs[\'node\']\ncamera = hou.node(node.parm(\'camera\').eval())\ntry: camera.parm(\'vcomment\').set(\'\')\nexcept: pass' )
chautoscope $_obj_parameterPrint +tx +ty +tz +rx +ry +rz +sx +sy +sz
opset -d on -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -x off $_obj_parameterPrint
opexprlanguage -s hscript $_obj_parameterPrint
opuserdata -n '___Version___' -v '19.5.332' $_obj_parameterPrint
opset -p on $_obj_parameterPrint

opcf $arg1

set oidx = 0
if ($argc >= 9 && "$arg9" != "") then
    set oidx = $arg9
endif

if ($argc >= 5 && "$arg4" != "") then
    set output = $_obj_parameterPrint
    opwire -n $output -$arg5 $arg4
endif
if ($argc >= 6 && "$arg6" != "") then
    set input = $_obj_parameterPrint
    if ($arg8) then
        opwire -n -i $arg6 -0 $input
    else
        opwire -n -o $oidx $arg6 -0 $input
    endif
endif
opcf $saved_path
'''
hou.hscript(h_preamble + h_extra_args + h_cmd)
