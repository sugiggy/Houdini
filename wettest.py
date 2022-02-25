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

if 'geo' not in child_type:
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

# Node $_obj_work (Object/geo)
set _obj_work = `run("opadd -e -n -v geo work")`
oplocate -x `$arg2 + 0` -y `$arg3 + 0` $_obj_work
opspareds '    group {         name    "stdswitcher4"         label   "Transform"          parm {             name    "xOrd"             baseparm             label   "Transform Order"             joinnext             export  none         }         parm {             name    "rOrd"             baseparm             label   "Rotate Order"             nolabel             export  none         }         parm {             name    "t"             baseparm             label   "Translate"             export  all         }         parm {             name    "r"             baseparm             label   "Rotate"             export  all         }         parm {             name    "s"             baseparm             label   "Scale"             export  none         }         parm {             name    "p"             baseparm             label   "Pivot Translate"             export  none         }         parm {             name    "pr"             baseparm             label   "Pivot Rotate"             export  none         }         parm {             name    "scale"             baseparm             label   "Uniform Scale"             export  none         }         parm {             name    "pre_xform"             baseparm             label   "Modify Pre-Transform"             export  none         }         parm {             name    "keeppos"             baseparm             label   "Keep Position When Parenting"             export  none         }         parm {             name    "childcomp"             baseparm             label   "Child Compensation"             export  none         }         parm {             name    "constraints_on"             baseparm             label   "Enable Constraints"             export  none         }         parm {             name    "constraints_path"             baseparm             label   "Constraints"             export  none         }         parm {             name    "lookatpath"             baseparm             label   "Look At"             invisible             export  none         }         parm {             name    "lookupobjpath"             baseparm             label   "Look Up Object"             invisible             export  none         }         parm {             name    "lookup"             baseparm             label   "Look At Up Vector"             invisible             export  none         }         parm {             name    "pathobjpath"             baseparm             label   "Path Object"             invisible             export  none         }         parm {             name    "roll"             baseparm             label   "Roll"             invisible             export  none         }         parm {             name    "pos"             baseparm             label   "Position"             invisible             export  none         }         parm {             name    "uparmtype"             baseparm             label   "Parameterization"             invisible             export  none         }         parm {             name    "pathorient"             baseparm             label   "Orient Along Path"             invisible             export  none         }         parm {             name    "up"             baseparm             label   "Orient Up Vector"             invisible             export  none         }         parm {             name    "bank"             baseparm             label   "Auto-Bank factor"             invisible             export  none         }     }      group {         name    "stdswitcher4_1"         label   "Render"          parm {             name    "shop_materialpath"             baseparm             label   "Material"             export  none         }         parm {             name    "shop_materialopts"             baseparm             label   "Options"             invisible             export  none         }         parm {             name    "tdisplay"             baseparm             label   "Display"             joinnext             export  none         }         parm {             name    "display"             baseparm             label   "Display"             export  none         }         parm {             name    "viewportlod"             label   "Display As"             type    ordinal             default { "full" }             help    "Choose how the object\'s geometry should be rendered in the viewport"             menu {                 "full"      "Full Geometry"                 "points"    "Point Cloud"                 "box"       "Bounding Box"                 "centroid"  "Centroid"                 "hidden"    "Hidden"                 "subd"      "Subdivision Surface / Curves"             }             parmtag { "spare_category" "Render" }         }         parm {             name    "vm_rendervisibility"             label   "Render Visibility"             type    string             default { "*" }             menureplace {                 "*"                             "Visible to all"                 "primary"                       "Visible only to primary rays"                 "primary|shadow"                "Visible only to primary and shadow rays"                 "-primary"                      "Invisible to primary rays (Phantom)"                 "-diffuse"                      "Invisible to diffuse rays"                 "-diffuse&-reflect&-refract"    "Invisible to secondary rays"                 ""                              "Invisible (Unrenderable)"             }             parmtag { "mantra_class" "object" }             parmtag { "mantra_name" "rendervisibility" }             parmtag { "spare_category" "Render" }         }         parm {             name    "vm_rendersubd"             label   "Render Polygons As Subdivision (Mantra)"             type    toggle             default { "0" }             parmtag { "mantra_class" "object" }             parmtag { "mantra_name" "rendersubd" }             parmtag { "spare_category" "Geometry" }         }         parm {             name    "vm_subdstyle"             label   "Subdivision Style"             type    string             default { "mantra_catclark" }             hidewhen "{ vm_rendersubd == 0 }"             menu {                 "mantra_catclark"   "Mantra Catmull-Clark"                 "osd_catclark"      "OpenSubdiv Catmull-Clark"             }             parmtag { "mantra_class" "object" }             parmtag { "mantra_name" "subdstyle" }             parmtag { "spare_category" "Geometry" }         }         parm {             name    "vm_subdgroup"             label   "Subdivision Group"             type    string             default { "" }             hidewhen "{ vm_rendersubd == 0 }"             parmtag { "mantra_class" "object" }             parmtag { "mantra_name" "subdgroup" }             parmtag { "spare_category" "Geometry" }         }         parm {             name    "vm_osd_quality"             label   "Open Subdiv Quality"             type    float             default { "1" }             hidewhen "{ vm_rendersubd == 0 vm_subdstyle != osd_catclark }"             range   { 0 10 }             parmtag { "mantra_class" "object" }             parmtag { "mantra_name" "osd_quality" }             parmtag { "spare_category" "Geometry" }         }         parm {             name    "vm_osd_vtxinterp"             label   "OSD Vtx Interp"             type    integer             default { "2" }             hidewhen "{ vm_rendersubd == 0 vm_subdstyle != osd_catclark }"             menu {                 "0" "No vertex interpolation"                 "1" "Edges only"                 "2" "Edges and Corners"             }             range   { 0 10 }             parmtag { "mantra_class" "object" }             parmtag { "mantra_name" "osd_vtxinterp" }             parmtag { "spare_category" "Geometry" }         }         parm {             name    "vm_osd_fvarinterp"             label   "OSD FVar Interp"             type    integer             default { "4" }             hidewhen "{ vm_rendersubd == 0 vm_subdstyle != osd_catclark }"             menu {                 "0" "Smooth everywhere"                 "1" "Sharpen corners only"                 "2" "Sharpen edges and corners"                 "3" "Sharpen edges and propagated corners"                 "4" "Sharpen all boundaries"                 "5" "Bilinear interpolation"             }             range   { 0 10 }             parmtag { "mantra_class" "object" }             parmtag { "mantra_name" "osd_fvarinterp" }             parmtag { "spare_category" "Geometry" }         }         group {             name    "folder0"             label   "Shading"              parm {                 name    "categories"                 label   "Categories"                 type    string                 default { "" }                 help    "A list of tags which can be used to select the object"                 parmtag { "spare_category" "Shading" }             }             parm {                 name    "reflectmask"                 label   "Reflection Mask"                 type    oplist                 default { "*" }                 help    "Objects that will be reflected on this object."                 parmtag { "opexpand" "1" }                 parmtag { "opfilter" "!!OBJ/GEOMETRY!!" }                 parmtag { "oprelative" "/obj" }                 parmtag { "spare_category" "Shading" }             }             parm {                 name    "refractmask"                 label   "Refraction Mask"                 type    oplist                 default { "*" }                 help    "Objects that will be refracted on this object."                 parmtag { "opexpand" "1" }                 parmtag { "opfilter" "!!OBJ/GEOMETRY!!" }                 parmtag { "oprelative" "/obj" }                 parmtag { "spare_category" "Shading" }             }             parm {                 name    "lightmask"                 label   "Light Mask"                 type    oplist                 default { "*" }                 help    "Lights that illuminate this object."                 parmtag { "opexpand" "1" }                 parmtag { "opfilter" "!!OBJ/LIGHT!!" }                 parmtag { "oprelative" "/obj" }                 parmtag { "spare_category" "Shading" }             }             parm {                 name    "lightcategories"                 label   "Light Selection"                 type    string                 default { "*" }                 parmtag { "spare_category" "Shading" }             }             parm {                 name    "vm_lpetag"                 label   "LPE Tag"                 type    string                 default { "" }                 parmtag { "mantra_class" "object" }                 parmtag { "mantra_name" "lpetag" }                 parmtag { "spare_category" "Shading" }             }             parm {                 name    "vm_volumefilter"                 label   "Volume Filter"                 type    string                 default { "box" }                 menu {                     "box"       "Box Filter"                     "gaussian"  "Gaussian"                     "bartlett"  "Bartlett (triangle)"                     "catrom"    "Catmull-Rom"                     "hanning"   "Hanning"                     "blackman"  "Blackman"                     "sinc"      "Sinc (sharpening)"                 }                 parmtag { "mantra_class" "object" }                 parmtag { "mantra_name" "filter" }                 parmtag { "spare_category" "Shading" }             }             parm {                 name    "vm_volumefilterwidth"                 label   "Volume Filter Width"                 type    float                 default { "1" }                 range   { 0.001 5 }                 parmtag { "mantra_class" "object" }                 parmtag { "mantra_name" "filterwidth" }                 parmtag { "spare_category" "Shading" }             }             parm {                 name    "vm_matte"                 label   "Matte shading"                 type    toggle                 default { "0" }                 parmtag { "mantra_class" "object" }                 parmtag { "mantra_name" "matte" }                 parmtag { "spare_category" "Shading" }             }             parm {                 name    "vm_rayshade"                 label   "Raytrace Shading"                 type    toggle                 default { "0" }                 parmtag { "mantra_class" "object" }                 parmtag { "mantra_name" "rayshade" }                 parmtag { "spare_category" "Shading" }             }         }          group {             name    "folder0_1"             label   "Sampling"              parm {                 name    "geo_velocityblur"                 label   "Geometry Velocity Blur"                 type    ordinal                 default { "off" }                 disablewhen "{ allowmotionblur == 0 }"                 menu {                     "off"       "No Velocity Blur"                     "on"        "Velocity Blur"                     "accelblur" "Acceleration Blur"                 }             }             parm {                 name    "geo_accelattribute"                 label   "Acceleration Attribute"                 type    string                 default { "accel" }                 hidewhen "{ geo_velocityblur != accelblur }"                 parmtag { "spare_category" "Sampling" }             }         }          group {             name    "folder0_2"             label   "Dicing"              parm {                 name    "vm_shadingquality"                 label   "Shading Quality"                 type    float                 default { "1" }                 range   { 0 10 }                 parmtag { "mantra_class" "object" }                 parmtag { "mantra_name" "shadingquality" }                 parmtag { "spare_category" "Dicing" }             }             parm {                 name    "vm_flatness"                 label   "Dicing Flatness"                 type    float                 default { "0.05" }                 range   { 0 1 }                 parmtag { "mantra_class" "object" }                 parmtag { "mantra_name" "flatness" }                 parmtag { "spare_category" "Dicing" }             }             parm {                 name    "vm_raypredice"                 label   "Ray Predicing"                 type    integer                 default { "0" }                 menu {                     "0" "Disable Predicing"                     "1" "Full Predicing"                     "2" "Precompute Bounds"                 }                 range   { 0 10 }                 parmtag { "mantra_class" "object" }                 parmtag { "mantra_name" "raypredice" }                 parmtag { "spare_category" "Dicing" }             }             parm {                 name    "vm_curvesurface"                 label   "Shade Curves As Surfaces"                 type    toggle                 default { "0" }                 parmtag { "mantra_class" "object" }                 parmtag { "mantra_name" "curvesurface" }                 parmtag { "spare_category" "Dicing" }             }         }          group {             name    "folder0_3"             label   "Geometry"              parm {                 name    "vm_rmbackface"                 label   "Backface Removal"                 type    toggle                 default { "0" }                 parmtag { "mantra_class" "object" }                 parmtag { "mantra_name" "rmbackface" }                 parmtag { "spare_category" "Geometry" }             }             parm {                 name    "shop_geometrypath"                 label   "Procedural Shader"                 type    oppath                 default { "" }                 parmtag { "opfilter" "!!SHOP/GEOMETRY!!" }                 parmtag { "oprelative" "." }                 parmtag { "spare_category" "Geometry" }             }             parm {                 name    "vm_forcegeometry"                 label   "Force Procedural Geometry Output"                 type    toggle                 default { "1" }                 parmtag { "spare_category" "Geometry" }             }             parm {                 name    "vm_rendersubdcurves"                 label   "Render Polygon Curves As Subdivision (Mantra)"                 type    toggle                 default { "0" }                 parmtag { "mantra_class" "object" }                 parmtag { "mantra_name" "rendersubdcurves" }                 parmtag { "spare_category" "Geometry" }             }             parm {                 name    "vm_renderpoints"                 label   "Render As Points (Mantra)"                 type    integer                 default { "2" }                 menu {                     "0" "No Point Rendering"                     "1" "Render Only Points"                     "2" "Render Unconnected Points"                 }                 range   { 0 10 }                 parmtag { "mantra_class" "object" }                 parmtag { "mantra_name" "renderpoints" }                 parmtag { "spare_category" "Geometry" }             }             parm {                 name    "vm_renderpointsas"                 label   "Render Points As (Mantra)"                 type    integer                 default { "0" }                 disablewhen "{ vm_renderpoints == 0 }"                 menu {                     "0" "Spheres"                     "1" "Circles"                 }                 range   { 0 10 }                 parmtag { "mantra_class" "object" }                 parmtag { "mantra_name" "renderpointsas" }                 parmtag { "spare_category" "Geometry" }             }             parm {                 name    "vm_usenforpoints"                 label   "Use N For Point Rendering"                 type    toggle                 default { "0" }                 disablewhen "{ vm_renderpoints == 0 }"                 parmtag { "mantra_class" "object" }                 parmtag { "mantra_name" "usenforpoints" }                 parmtag { "spare_category" "Geometry" }             }             parm {                 name    "vm_pointscale"                 label   "Point Scale"                 type    float                 default { "1" }                 disablewhen "{ vm_renderpoints == 0 }"                 range   { 0! 10 }                 parmtag { "mantra_class" "object" }                 parmtag { "mantra_name" "pointscale" }                 parmtag { "spare_category" "Geometry" }             }             parm {                 name    "vm_pscalediameter"                 label   "Treat Point Scale as Diameter Instead of Radius"                 type    toggle                 default { "0" }                 parmtag { "mantra_class" "object" }                 parmtag { "mantra_name" "pscalediameter" }                 parmtag { "spare_category" "Geometry" }             }             parm {                 name    "vm_metavolume"                 label   "Metaballs as Volume"                 type    toggle                 default { "0" }                 parmtag { "mantra_class" "object" }                 parmtag { "mantra_name" "metavolume" }                 parmtag { "spare_category" "Geometry" }             }             parm {                 name    "vm_coving"                 label   "Coving"                 type    integer                 default { "1" }                 menu {                     "0" "Disable Coving"                     "1" "Coving for displacement/sub-d"                     "2" "Coving for all primitives"                 }                 range   { 0 10 }                 parmtag { "mantra_class" "object" }                 parmtag { "mantra_name" "coving" }                 parmtag { "spare_category" "Geometry" }             }             parm {                 name    "vm_materialoverride"                 label   "Material Override"                 type    string                 default { "compact" }                 menu {                     "none"      "Disabled"                     "full"      "Evaluate for Each Primitve/Point"                     "compact"   "Evaluate Once"                 }                 parmtag { "spare_category" "Geometry" }             }             parm {                 name    "vm_overridedetail"                 label   "Ignore Geometry Attribute Shaders"                 type    toggle                 default { "0" }                 parmtag { "mantra_class" "object" }                 parmtag { "mantra_name" "overridedetail" }                 parmtag { "spare_category" "Geometry" }             }             parm {                 name    "vm_procuseroottransform"                 label   "Proc Use Root Transform"                 type    toggle                 default { "1" }                 parmtag { "mantra_class" "object" }                 parmtag { "mantra_name" "procuseroottransform" }                 parmtag { "spare_category" "Geometry" }             }         }      }      group {         name    "stdswitcher4_2"         label   "Arnold"          parm {             name    "shop_propertiespath"             label   "Default Properties"             type    oppath             default { "" }             help    "Specifies a Property SHOP that is used to resolve rendering parameter values. At render time, this SHOP (if given) is used to resolve rendering parameter values first, before looking for then on the objects being rendered."             range   { 0 1 }             parmtag { "opfilter" "!!SHOP/PROPERTIES!!" }             parmtag { "oprelative" "." }             parmtag { "spare_category" "Shaders" }         }         parm {             name    "ar_user_options"             label   "User Options"             type    string             joinnext             default { "" }             help    "This string is passed to AiNodeSetAttributes() ont the Arnold node. It can contain any number of parameter/value pairs separated by whitespace (spaces, tabs, newlines) as found in .ass files."             disablewhen "{ ar_user_options_enable == 0 }"         }         parm {             name    "ar_user_options_enable"             label   "Enable"             type    toggle             default { "0" }             help    "Overrides the value of any parameter of the Arnold node."         }         group {             name    "folder_subdivision"             label   "Subdivision"              parm {                 name    "ar_subdiv_type"                 label   "Type"                 type    string                 default { "none" }                 help    "Subdivision algorithm. None ignores any subdivision and renders the mesh as it is. Linear subdivision puts vertices in the middle of each face. The Catmull-Clark algorithm is used to create smooth surfaces by recursive subdivision surface modeling. The resulting surface will always consist of a mesh of quadrilateral faces."                 menu {                     "none"      "None"                     "catclark"  "Catmull-Clark"                     "linear"    "Linear"                 }                 range   { 0 1 }                 parmtag { "spare_category" "Subdivision" }             }             parm {                 name    "ar_subdiv_iterations"                 label   "Iterations"                 type    integer                 default { "1" }                 help    "The number of iterations / levels of subdivision. With Catmull-Clark subdivision, increasing the number of iterations produces a smoother mesh."                 disablewhen "{ ar_subdiv_type == none }"                 range   { 1! 10 }                 parmtag { "spare_category" "Subdivision" }             }             parm {                 name    "ar_subdiv_adaptive_metric"                 label   "Adaptive Metric"                 type    string                 joinnext                 default { "auto" }                 help    "The adaptive subdivision criterion. Auto subdiv will choose between the EDGELENGTH mode and the FLATNESS depending on the displacement property of the polymesh. This means that if there is a displacement it will use the EDGELENGTH algorithm. If there is not displacement (or it is ignored in the global options) it will use FLATNESS."                 disablewhen "{ ar_subdiv_type == none }"                 menu {                     "auto"          "Auto"                     "edge_length"   "Edge Length"                     "flatness"      "Flatness"                 }                 parmtag { "spare_category" "Subdivision" }             }             parm {                 name    "ar_subdiv_adaptive_error"                 label   "     Error"                 type    float                 default { "0" }                 help    "The \\"adaptive error\\" refers to the acceptable tessellation error as seen from the camera. If there\'s no displacement, then the error represents the distance from the subdivided mesh to the \\"true\\" or \\"limit\\" surface -- sort of a \\"flatness\\" heuristic. The smaller the error, the closer to the limit surface a mesh will be and the less inter-frame popping when the subdivision level jumps. If displacement is enabled, then the error represents the final size of the subdivided quads. A value of 0 disables adaptive subdivision."                 disablewhen "{ ar_subdiv_type == none }"                 range   { 0! 10 }                 parmtag { "spare_category" "Subdivision" }             }             parm {                 name    "ar_subdiv_adaptive_space"                 label   "Adaptive Space"                 type    string                 default { "raster" }                 help    "The space in which the adaptive metric is evaluated."                 disablewhen "{ ar_subdiv_type == none }"                 menu {                     "raster"    "Raster"                     "object"    "Object"                 }                 parmtag { "spare_category" "Subdivision" }             }             parm {                 name    "ar_subdiv_uv_smoothing"                 label   "UV Smoothing"                 type    string                 joinnext                 default { "pin_corners" }                 help    "UV smoothing algorithm."                 disablewhen "{ ar_subdiv_type == none }"                 menu {                     "pin_corners"   "Pin Corners"                     "pin_borders"   "Pin Borders"                     "linear"        "Linear"                     "smooth"        "Smooth"                 }                 range   { 0 1 }                 parmtag { "spare_category" "Subdivision" }             }             parm {                 name    "ar_subdiv_smooth_derivs"                 label   "Smooth Derivatives"                 type    toggle                 default { "0" }                 help    "This option makes it possible to remove the faceted appearance from anisotropic speculars. The object must have a valid UV map for this option to work and only works if you apply at least one subdivision level to the geometry."                 disablewhen "{ ar_subdiv_type == none }"                 range   { 0 1 }                 parmtag { "spare_category" "Subdivision" }             }             parm {                 name    "ar_merge_vertex_indices"                 label   "Merge Vertex Indices"                 type    toggle                 default { "1" }                 help    "Enable merging of the indices and data of coincident and identical vertex attribute values (UVs, normals, vertex user data). This allows the proper interpolation of vertex attributes when subdividing, and yields more compact render scenes in memory and on disk, at the cost of a slower export."                 range   { 0 1 }                 parmtag { "spare_category" "Subdivision" }             }             parm {                 name    "ar_subdiv_frustum_ignore"                 label   "Ignore Frustum Culling"                 type    toggle                 default { "0" }                 help    "Subdivision surfaces outside the view or dicing camera frustum will not be subdivided. This can be turned on globally by enabling subdiv_frustum_culling on the ROP and can be turned off for specific meshes by setting subdiv_frustum_ignore true."                 disablewhen "{ ar_subdiv_type == none }"                 parmtag { "spare_category" "Subdivision" }             }         }          group {             name    "folder_subdivision_1"             label   "Displacement"              parm {                 name    "ar_disp_height"                 label   "Height"                 type    float                 default { "1" }                 range   { 0 10 }                 parmtag { "spare_category" "Displacement" }             }             parm {                 name    "ar_disp_zero_value"                 label   "Zero Value"                 type    float                 default { "0" }                 range   { 0 1 }                 parmtag { "spare_category" "Displacement" }             }             parm {                 name    "ar_disp_padding"                 label   "Bounds Padding"                 type    float                 default { "0" }                 range   { 0 10 }                 parmtag { "spare_category" "Displacement" }             }             parm {                 name    "ar_disp_autobump"                 label   "Autobump"                 type    toggle                 default { "0" }                 range   { 0 1 }                 parmtag { "spare_category" "Displacement" }             }             groupcollapsible {                 name    "folder_autobump"                 label   "Autobump Visibility"                  parm {                     name    "ar_autobump_visibility_camera"                     label   "Camera"                     type    toggle                     default { "1" }                     help    "Toggle autobump for camera rays (i.e. primary or view rays)."                     disablewhen "{ ar_disp_autobump == 0 }"                     range   { 0 1 }                     parmtag { "spare_category" "Displacement" }                 }                 parm {                     name    "ar_autobump_visibility_shadow"                     label   "Shadow"                     type    toggle                     default { "0" }                     help    "Toggle autobump for shadow rays fired in the direct lighting calculations."                     disablewhen "{ ar_disp_autobump == 0 }"                     range   { 0 1 }                     parmtag { "spare_category" "Displacement" }                 }                 parm {                     name    "ar_autobump_visibility_diffuse_transmit"                     label   "Diffuse Transmission"                     type    toggle                     default { "0" }                     help    "Toggle autobump for indirect diffuse transmission rays."                     disablewhen "{ ar_disp_autobump == 0 }"                     range   { 0 1 }                     parmtag { "spare_category" "Displacement" }                 }                 parm {                     name    "ar_autobump_visibility_specular_transmit"                     label   "Specular Transmission"                     type    toggle                     default { "0" }                     help    "Toggle autobump for indirect specular transmission rays."                     disablewhen "{ ar_disp_autobump == 0 }"                     range   { 0 1 }                     parmtag { "spare_category" "Displacement" }                 }                 parm {                     name    "ar_autobump_visibility_diffuse_reflect"                     label   "Diffuse Reflection"                     type    toggle                     default { "0" }                     help    "Toggle autobump for indirect diffuse reflection rays."                     disablewhen "{ ar_disp_autobump == 0 }"                     range   { 0 1 }                     parmtag { "spare_category" "Displacement" }                 }                 parm {                     name    "ar_autobump_visibility_specular_reflect"                     label   "Specular Reflection"                     type    toggle                     default { "0" }                     help    "Toggle autobump for indirect specular reflection rays."                     disablewhen "{ ar_disp_autobump == 0 }"                     range   { 0 1 }                     parmtag { "spare_category" "Displacement" }                 }                 parm {                     name    "ar_autobump_visibility_volume"                     label   "Volume Scattering"                     type    toggle                     default { "0" }                     help    "Toggle autobump for indirect volume scattering rays."                     disablewhen "{ ar_disp_autobump == 0 }"                     range   { 0 1 }                     parmtag { "spare_category" "Displacement" }                 }             }          }          group {             name    "folder_subdivision_2"             label   "Shapes"              parm {                 name    "ar_min_pixel_width"                 label   "Minimum Pixel Width"                 type    float                 default { "0" }                 help    "If this value is non-zero, points or curves with a small on-screen width will be automatically enlarged so that they are at least the specified size in pixels. The enlargement fraction is then used in the hair shader to adjust the opacity so that the visible thickness of the hair remains the same. For a given number of AA samples, this makes it a lot easier to antialias fine hair, at the expense of render time (because of the additional transparency/depth complexity). Good values are in the range 0.2 to 0.7. Values closer to 0 are faster to render but need more AA samples. So if your scene already uses very high AA settings, you should use a low value like 0.1. For best results, you may need to increase the auto-transparency depth, and/or lower the auto-transparency threshold, but watch the effect on render times. Note that this parameter currently works with the ribbon mode only."                 range   { 0 10 }                 parmtag { "spare_category" "Curves" }             }             parm {                 name    "ar_radius"                 label   "Default Radius"                 type    float                 default { "0.05" }                 help    "Sets the default rendered radius of points or thickness of curves. This property can be overridden per point with the \\"ar_radius\\", \\"pscale\\" or \\"width\\" (curves only) attributes."                 range   { 0 10 }                 parmtag { "units" "m1" }             }             group {                 name    "folder_points"                 label   "Points"                  parm {                     name    "ar_mode"                     label   "Mode"                     type    ordinal                     default { "sphere" }                     help    "Rendering mode for points or particles. Can be spheres, or camera-facing disks or quads."                     menu {                         "disk"      "Disk"                         "sphere"    "Sphere"                         "quad"      "Quad"                     }                     range   { 0 1 }                 }                 parm {                     name    "ar_point_scale"                     label   "Point Scale"                     type    float                     default { "1" }                     help    "A global scale factor applied to points."                     range   { 0! 10 }                 }                 parm {                     name    "ar_aspect"                     label   "Aspect"                     type    log                     default { "1" }                     help    "The aspect ratio for quads. This property can be overrriden per point by setting the \\"ar_aspect\\" or \\"spritescale\\" attributes on the geometry."                     disablewhen "{ ar_mode != quad }"                     range   { 0.1 10 }                 }                 parm {                     name    "ar_rotation"                     label   "Rotation"                     type    angle                     default { "0" }                     help    "The rotation angle in degrees for quads. This property can be overrriden per point by setting the \\"ar_rotation\\" or the \\"spriterot\\" attributes on the geometry."                     disablewhen "{ ar_mode != quad }"                     range   { -180 180 }                 }             }              group {                 name    "folder_points_1"                 label   "Curves"                  parm {                     name    "ar_curves_basis"                     label   "Basis"                     type    string                     default { "auto" }                     help    "The curves basis to interpret the knots of the input curves or open polygons. When set to \\"Automatic\\", the basis will attempt to match the closest equivalent in Arnold, ie. linear for open polygons, Bezier for Bezier curves and B-spline for NURBS."                     menu {                         "bezier"        "Bezier"                         "b-spline"      "B-Spline"                         "catmull-rom"   "Catmull-Rom"                         "linear"        "Linear"                         "auto"          "Automatic"                     }                     range   { 0 1 }                     parmtag { "spare_category" "Curves" }                 }                 parm {                     name    "ar_curves_mode"                     label   "Mode"                     type    string                     default { "ribbon" }                     help    "- Ribbon: This mode is recommended for fine geometry such as realistic hair, fur or fields of grass. These curves are rendered as camera-facing flat ribbons. For secondary and shadow rays, they face the incoming ray direction. This mode doesn\'t look so good for very wide hairs or dramatic zoom-ins because of the flat appearance. This mode works best with a proper hair shader (perhaps based on a Kay-Kajiya or Marschner specular model).\\\\n\\\\n- Thick: This mode resembles spaghetti. It has a circular cross section, and a normal vector that varies across the width of the hair. Thick hairs look great when zoomed in, and are specially useful for effects work, but their varying normals make them more difficult to antialias when they are small. You can use any shader with this rendering mode, including lambert, phong, etc.\\\\n\\\\n- Oriented: This mode is similar to the ribbons mode, but you can set the ribbon orientation for each knot with an \\"ar_orientations\\" vector attribute representing the direction of the normal of the ribbon. This mode can be useful to render grass strands for example."                     menu {                         "ribbon"    "Ribbon"                         "thick"     "Thick"                         "oriented"  "Oriented      "                     }                     range   { 0 1 }                     parmtag { "spare_category" "Curves" }                 }             }              group {                 name    "folder_points_2"                 label   "Volumes"                  parm {                     name    "ar_step_size"                     label   "Volume Step Size"                     type    float                     default { "0" }                     help    "When ar_step_size is set to a value other than zero, then points rendered as spheres, particles and polymeshes will be rendered as volumes."                     range   { 0 1 }                 }                 parm {                     name    "ar_volume_padding"                     label   "Volume Padding"                     type    float                     default { "0" }                     help    "When rendering particles or polymeshes as volumes (when ar_step_size is non-zero), ar_volume_padding will provide extra the volume padding specified for displacement requirements"                     disablewhen "{ ar_step_size == 0 }"                     range   { 0 10 }                 }                 parm {                     name    "label_volume"                     label   "Label"                     type    label                     nolabel                     default { "" }                 }                 parm {                     name    "label_volume2"                     label   "Label"                     type    label                     nolabel                     default { "Points and polymeshes are rendered as volumes if Step Size > 0" }                 }             }              group {                 name    "folder_points_3"                 label   " VDB "                  parm {                     name    "ar_vdb_file_enable"                     label   "Export VDB File"                     type    toggle                     nolabel                     joinnext                     default { "0" }                     help    "Export the VDB primitives as a VDB file and reference the file in the Arnold volume."                     range   { 0 1 }                 }                 parm {                     name    "ar_vdb_file"                     label   "Save to File"                     type    file                     default { "$HIP/`pythonexprs(\\"hou.pwd().path()[1:].replace(\'/\', \'_\')\\")`.$F4.vdb" }                     help    "The OpenVDB file name that the VDB primitves will be written to, and that will be referenced by the Arnold volume instead of attaching the volume data."                     disablewhen "{ ar_vdb_file_enable == 0 }"                     range   { 0 1 }                     parmtag { "filechooser_pattern" "*.vdb" }                 }                 parm {                     name    "ar_grids"                     label   "Export Grids"                     type    string                     default { "*" }                     help    "The VDB grids to export and make available in the volume shading context."                     menutoggle {                         [ "import htoa.properties" ]                         [ "return htoa.properties.vdbGridMenu()" ]                         language python                     }                     range   { 0 1 }                     parmtag { "script_callback" "__import__(\'htoa\').properties.vdbAutoStepSizeCallback()" }                     parmtag { "script_callback_language" "python" }                 }                 parm {                     name    "ar_velocity_grids"                     label   "Velocity Grids"                     type    string                     default { "*" }                     help    "Select 1 vector or 3 float grids representing velocity for motion blur."                     menutoggle {                         [ "import htoa.properties" ]                         [ "return htoa.properties.vdbGridMenu()" ]                         language python                     }                     range   { 0 1 }                 }                 parm {                     name    "ar_velocity_scale"                     label   "Velocity Scale"                     type    log                     default { "1" }                     help    "Scale the velocities by this factor."                     disablewhen "{ ar_velocity_grids == \\"\\" }"                     range   { 0.1 10 }                 }                 parm {                     name    "ar_velocity_threshold"                     label   "Velocity Threshold"                     type    log                     default { "0.001" }                     help    "Controls filtering of noisy velocities. The default value 0.001 should have little to no visual impact, setting it to zero disables filtering entirely."                     disablewhen "{ ar_velocity_grids == \\"\\" }"                     range   { 0! 1! }                 }                 parm {                     name    "ar_padding"                     label   "Bounds Padding"                     type    float                     default { "0" }                     help    "Extra padding for the volume bounds"                     range   { 0 10 }                 }                 parm {                     name    "ar_step_size_type"                     label   "Volume Step"                     type    ordinal                     joinnext                     default { "0" }                     help    "When set to auto, the step size is automatically determined by the volume plugin, yielding the minimum voxel size."                     menu {                         "auto"      "Automatic       "                         "custom"    "Custom"                     }                     range   { 0 1 }                     parmtag { "script_callback" "__import__(\'htoa\').properties.vdbAutoStepSizeCallback()" }                     parmtag { "script_callback_language" "python" }                 }                 parm {                     name    "ar_vdb_step_size"                     label   "      Step Size"                     type    float                     default { "0.02" }                     help    "The ray marching step size. When the step type is auto, this indicates the computed step size, the minimum voxel size."                     disablewhen "{ ar_step_size_type == auto }"                     range   { 0! 10 }                 }                 parm {                     name    "ar_step_scale"                     label   "Step Scale"                     type    log                     default { "1" }                     help    "Multiply the step size by this factor, including when it\'s automatically detected."                     range   { 0.1! 10 }                 }                 parm {                     name    "ar_compress"                     label   "Compress"                     type    toggle                     invisible                     default { "1" }                     help    "Optimize voxel storage to reduce memory usage."                     range   { 0 1 }                 }             }              group {                 name    "folder_points_4"                 label   "Tessellation"                  parm {                     name    "ar_tessellation_enable"                     label   "Tessellate Primitives"                     type    toggle                     default { "1" }                     help    "Tessellate Houdini primitives such as NURBS, Bezier meshes, circles, tubes or spheres prior to sending to Arnold."                     disablewhen "{ ar_tessellation_use_rop == 1 }"                     range   { 0 1 }                     parmtag { "spare_category" "Tessellation" }                 }                 parm {                     name    "ar_tessellation_style"                     label   "Tessellation Style"                     type    string                     invisible                     default { "lod" }                     help    "Specifies the conversion style for the geometry. The default is\\"Level of Detail\\". Can be one of the following:\\\\n- Level of Detail: Tessellate geometry using the level of detail settings.\\\\n- Divisions: Tessellate geometry based on the number of divisions settings."                     disablewhen "{ ar_tessellation_enable == 0 }"                     menu {                         "lod"   "Level of Detail"                         "div"   "Divisions"                     }                     range   { 0 1 }                     parmtag { "spare_category" "Tessellation" }                 }                 parm {                     name    "ar_tessellation_ulod"                     label   "U Level of Detail"                     type    float                     default { "1" }                     help    "Specifies the level of detail for U subdivisions of the surface being converted. Applicable only when conversion method is set to Level of Detail. Defaults to 1.0."                     disablewhen "{ ar_tessellation_enable == 0 }"                     hidewhen "{ ar_tessellation_style != lod }"                     range   { 0! 10 }                     parmtag { "spare_category" "Tessellation" }                 }                 parm {                     name    "ar_tessellation_vlod"                     label   "V Level of Detail"                     type    float                     default { "1" }                     help    "Specifies the level of detail for V subdivisions of the surface being converted. Applicable only when conversion method is set to Level of Detail. Defaults to 1.0."                     disablewhen "{ ar_tessellation_enable == 0 }"                     hidewhen "{ ar_tessellation_style != lod }"                     range   { 0! 10 }                     parmtag { "spare_category" "Tessellation" }                 }                 parm {                     name    "ar_tessellation_trimlod"                     label   "Trim Level of Detail"                     type    float                     default { "1" }                     help    "Specifies the level of detail for trim curves of the surface being converted. Applicable only when conversion method is set to Level of Detail. Defaults to 1.0."                     disablewhen "{ ar_tessellation_enable == 0 }"                     hidewhen "{ ar_tessellation_style != lod }"                     range   { 0! 10 }                     parmtag { "spare_category" "Tessellation" }                 }             }              group {                 name    "folder_points_5"                 label   "Procedurals"                  parm {                     name    "ar_operator_graph_enable"                     label   "Enable Operator Graph"                     type    toggle                     nolabel                     joinnext                     default { "1" }                     help    "Enables the operator graph on procedurals in this OBJ node."                     range   { 0 1 }                 }                 parm {                     name    "ar_operator_graph"                     label   "Operator Graph"                     type    oppath                     default { "" }                     help    "Specify an operator ROP graph to connect to procedurals created by this OBJ node."                     disablewhen "{ ar_operator_graph_enable == 0 }"                     parmtag { "opfilter" "!!ROP!!" }                     parmtag { "oprelative" "." }                 }             }          }          group {             name    "folder_subdivision_3"             label   "Attributes"              parm {                 name    "ar_toon_id"                 label   "Toon ID Group"                 type    string                 default { "" }                 help    "Objects in the same toon ID group will be rendered with the same silhouette, if the user_id attribute is set on the toon shader"             }             parm {                 name    "ar_attributes_detail"                 label   "Detail Attributes"                 type    string                 default { "*" }                 help    "The list of details attributes to be exported as user data for Arnold. As user data is costly in memory, nothing is exported by default. If this field contains a wildcard character (*), all available attributes will be exported."                 menutoggle {                     [ "__import__(\'htoa\').properties.detailAttributeMenu()" ]                     language python                 }                 range   { 0 1 }                 parmtag { "spare_category" "Attributes" }             }             parm {                 name    "ar_attributes_primitive"                 label   "Primitive Attributes"                 type    string                 default { "*" }                 help    "The list of primitive attributes to be exported as user data for Arnold. As user data is costly in memory, nothing is exported by default. If this field contains a wildcard character (*), all available attributes will be exported."                 menutoggle {                     [ "__import__(\'htoa\').properties.primitiveAttributeMenu()" ]                     language python                 }                 range   { 0 1 }                 parmtag { "spare_category" "Attributes" }             }             parm {                 name    "ar_attributes_point"                 label   "Point Attributes"                 type    string                 default { "*" }                 help    "The list of point attributes to be exported as user data for Arnold. As user data is costly in memory, nothing is exported by default. If this field contains a wildcard character (*), all available attributes will be exported."                 menutoggle {                     [ "__import__(\'htoa\').properties.pointAttributeMenu()" ]                     language python                 }                 range   { 0 1 }                 parmtag { "spare_category" "Attributes" }             }             parm {                 name    "ar_attributes_vertex"                 label   "Vertex Attributes"                 type    string                 default { "*" }                 help    "The list of vertex attributes to be exported as user data for Arnold. As user data is costly in memory, nothing is exported by default. If this field contains a wildcard character (*), all available attributes will be exported."                 menutoggle {                     [ "__import__(\'htoa\').properties.vertexAttributeMenu()" ]                     language python                 }                 range   { 0 1 }                 parmtag { "spare_category" "Attributes" }             }         }          group {             name    "folder_subdivision_4"             label   "Motion Blur"              parm {                 name    "ar_transform_type"                 label   "Transform Type"                 type    ordinal                 default { "2" }                 help    "The type of motion for the transformation of the object, as a hint for the matrix interpolation for transformation motion blur."                 menu {                     "linear"                "Linear"                     "rotate_about_origin"   "Rotate About Origin"                     "rotate_about_center"   "Rotate About Center"                 }                 range   { 0 2 }                 parmtag { "spare_category" "Motion Blur" }             }             parm {                 name    "ar_mb_xform_keys_override"                 label   "Transform Keys Override"                 type    toggle                 nolabel                 joinnext                 default { "0" }                 help    "Override the ROP settings for Transform Keys."                 range   { 0 1 }                 parmtag { "spare_category" "Motion Blur" }             }             parm {                 name    "ar_mb_xform_keys"                 label   "Transform Keys"                 type    integer                 default { "2" }                 help    "Number of motion keys for matrix transformation. Transformation motion blur is calculated based on a linear interpolation of an object transform matrix, between successive motion keys. Increasing this value will add extra steps, which can improve the blurred result, especially for rotating objects. The default is 2, which results in straight lines of blur between shutter start and shutter end."                 disablewhen "{ ar_mb_xform_keys_override == 0 }"                 range   { 1! 20 }                 parmtag { "spare_category" "Motion Blur" }             }             parm {                 name    "ar_mb_dform_keys_override"                 label   "Deform Keys Override"                 type    toggle                 nolabel                 joinnext                 default { "0" }                 help    "Override the ROP settings for Transform Keys."                 range   { 0 1 }                 parmtag { "spare_category" "Motion Blur" }             }             parm {                 name    "ar_mb_dform_keys"                 label   "Deform Keys"                 type    integer                 default { "2" }                 help    "Number of motion keys for object points. Just like with transformation motion keys, increasing this value allows curved motion paths to be rendered more accurately, at the expense of using more memory."                 disablewhen "{ ar_mb_dform_keys_override == 0 } { ar_mb_velocity_enable == 1 ar_mb_acceleration_enable != 1 }"                 range   { 1! 20 }                 parmtag { "spare_category" "Motion Blur" }             }             parm {                 name    "ar_mb_velocity_enable"                 label   "Velocity Blur Enable"                 type    toggle                 nolabel                 joinnext                 default { "0" }                 help    "Deformation blur will be computed from the \\"v\\" point attribute."                 range   { 0 1 }                 parmtag { "spare_category" "Motion Blur" }             }             parm {                 name    "ar_mb_velocity_attribute"                 label   "Velocity Blur"                 type    string                 default { "v" }                 help    "The velocity point attribute to use for velocity blur. The Houdini convention is \'v\'."                 disablewhen "{ ar_mb_velocity_enable == 0 }"                 menureplace {                     [ "geometry = hou.pwd().renderNode().geometry()" ]                     [ "if not geometry:" ]                     [ "    return []" ]                     [ "menu_items = []" ]                     [ "for attr in geometry.pointAttribs():" ]                     [ "    if not attr.name() in (\'P\', \'Pw\'):" ]                     [ "        menu_items += [attr.name(), \'%s\\\\t  %s[%i]\' % (attr.name(), attr.dataType().name().lower(), attr.size())]" ]                     [ "return menu_items" ]                     language python                 }                 range   { 0 1 }             }             parm {                 name    "ar_mb_acceleration_enable"                 label   "Acceleration Blur Enable"                 type    toggle                 nolabel                 joinnext                 default { "0" }                 disablewhen "{ ar_mb_velocity_enable == 0 }"                 range   { 0 1 }             }             parm {                 name    "ar_mb_acceleration_attribute"                 label   "Acceleration Blur"                 type    string                 default { "force" }                 help    "The acceleration point attribute to use for acceleration blur. The Houdini convention is \'force\' or \'accel\'. If you use use \'force\' ensure you divide by the mass."                 disablewhen "{ ar_mb_velocity_enable == 0 } { ar_mb_acceleration_enable == 0 }"                 menureplace {                     [ "geometry = hou.pwd().renderNode().geometry()" ]                     [ "if not geometry:" ]                     [ "    return []" ]                     [ "menu_items = []" ]                     [ "for attr in geometry.pointAttribs():" ]                     [ "    if not attr.name() in (\'P\', \'Pw\'):" ]                     [ "        menu_items += [attr.name(), \'%s\\\\t  %s[%i]\' % (attr.name(), attr.dataType().name().lower(), attr.size())]" ]                     [ "return menu_items" ]                     language python                 }                 range   { 0 1 }             }         }          group {             name    "folder_subdivision_5"             label   "Visibility"              parm {                 name    "ar_visibility_camera"                 label   "Visible to Camera Rays"                 type    toggle                 default { "1" }                 help    "Toggle object visibility for camera rays (i.e. primary or view rays)."                 range   { 0 1 }                 parmtag { "spare_category" "Visibility" }             }             parm {                 name    "ar_visibility_shadow"                 label   "Visible to Shadow Rays"                 type    toggle                 default { "1" }                 help    "Toggle object visibility for shadow rays fired in the direct lighting calculations."                 range   { 0 1 }                 parmtag { "spare_category" "Visibility" }             }             parm {                 name    "ar_visibility_diffuse_transmit"                 label   "Visible to Diffuse Transmission Rays"                 type    toggle                 default { "1" }                 help    "Toggle object visibility for indirect diffuse transmission rays."                 range   { 0 1 }                 parmtag { "spare_category" "Visibility" }             }             parm {                 name    "ar_visibility_specular_transmit"                 label   "Visible to Specular Transmission Rays"                 type    toggle                 default { "1" }                 help    "Toggle object visibility for indirect specular transmission rays."                 range   { 0 1 }                 parmtag { "spare_category" "Visibility" }             }             parm {                 name    "ar_visibility_diffuse_reflect"                 label   "Visible to Diffuse Reflection Rays"                 type    toggle                 default { "1" }                 help    "Toggle object visibility for indirect diffuse reflection rays."                 range   { 0 1 }                 parmtag { "spare_category" "Visibility" }             }             parm {                 name    "ar_visibility_specular_reflect"                 label   "Visible to Specular Reflection Rays"                 type    toggle                 default { "1" }                 help    "Toggle object visibility for indirect specular reflection rays."                 range   { 0 1 }                 parmtag { "spare_category" "Visibility" }             }             parm {                 name    "ar_visibility_volume"                 label   "Visible to Volume Scattering Rays"                 type    toggle                 default { "1" }                 help    "Toggle object visibility for indirect volume scattering rays."                 range   { 0 1 }                 parmtag { "spare_category" "Visibility" }             }             parm {                 name    "ar_receive_shadows"                 label   "Receive Shadows"                 type    toggle                 default { "1" }                 help    "Enable/disable received shadows over the object."                 range   { 0 1 }                 parmtag { "spare_category" "Visibility" }             }             parm {                 name    "ar_self_shadows"                 label   "Self Shadows"                 type    toggle                 default { "1" }                 help    "Enable/disable self-shadowing over the object."                 disablewhen "{ ar_receive_shadows == 0 }"                 range   { 0 1 }                 parmtag { "spare_category" "Visibility" }             }             parm {                 name    "ar_opaque"                 label   "Opaque"                 type    toggle                 default { "1" }                 help    "By default, Arnold will assume that objects are opaque, which lets the renderer take certain shortcuts and optimizations for maximum ray tracing speed. When this option is unchecked, the object is assumed as \\"possibly transparent\\", and Arnold will perform extra computations to support transparency and transparent shadows, according to the shader\'s opacity settings."                 range   { 0 1 }                 parmtag { "spare_category" "Visibility" }             }             parm {                 name    "ar_matte"                 label   "Matte"                 type    toggle                 default { "0" }                 help    "Output black and zero alpha for camera rays to create a holdout."                 range   { 0 1 }                 parmtag { "spare_category" "Visibility" }             }             parm {                 name    "ar_skip"                 label   "Skip"                 type    toggle                 default { "0" }                 help    "Do not output this object regardless of it being forced or not."                 range   { 0 1 }                 parmtag { "spare_category" "Visibility" }             }             parm {                 name    "ar_use_light_group"                 label   "Use Light Group"                 type    toggle                 invisible                 nolabel                 joinnext                 default { "0" }                 range   { 0 1 }             }             parm {                 name    "ar_light_group"                 label   "Light Group"                 type    oplist                 invisible                 default { "" }                 disablewhen "{ ar_use_light_group == 0 }"                 range   { 0 1 }                 parmtag { "opfilter" "!!OBJ/LIGHT!!" }                 parmtag { "oprelative" "/" }             }             parm {                 name    "ar_use_shadow_group"                 label   "Use Shadow Group"                 type    toggle                 invisible                 nolabel                 joinnext                 default { "0" }                 range   { 0 1 }             }             parm {                 name    "ar_shadow_group"                 label   "Shadow Group"                 type    oplist                 invisible                 default { "" }                 disablewhen "{ ar_use_shadow_group == 0 }"                 range   { 0 1 }                 parmtag { "opfilter" "!!OBJ/LIGHT!!" }                 parmtag { "oprelative" "/" }             }             parm {                 name    "ar_trace_sets"                 label   "Trace Sets"                 type    string                 default { "" }                 menutoggle {                     [ "__import__(\'htoa.properties\').properties.tracesetMenu()" ]                     language python                 }                 range   { 0 1 }             }             parm {                 name    "ar_sss_setname"                 label   "SSS Set"                 type    string                 default { "" }                 help    "Use this parameter to tag multiple objects as belonging to the same SSS set so that illumination will blur across object boundaries. A common use case might be blurring between teeth and gum geometry. This feature is only available when using raytraced SSS."                 menureplace {                     [ "__import__(\'htoa.properties\').properties.sssMenu()" ]                     language python                 }                 range   { 0 1 }             }         }          group {             name    "folder_subdivision_6"             label   "Normals"              parm {                 name    "ar_smoothing"                 label   "Smoothing"                 type    toggle                 default { "1" }                 help    "Smooth/Flat normals."                 range   { 0 1 }                 parmtag { "spare_category" "Render" }             }             parm {                 name    "ar_invert_normals"                 label   "Invert Normals"                 type    toggle                 default { "0" }                 help    "Invert normals"                 range   { 0 1 }                 parmtag { "spare_category" "Render" }             }             parm {                 name    "ar_sidedness_camera"                 label   "Double-sided for Camera Rays"                 type    toggle                 default { "1" }                 help    "Toggle object double-sidedness for camera rays (i.e. primary or view rays)."                 range   { 0 1 }                 parmtag { "spare_category" "Sidedness" }             }             parm {                 name    "ar_sidedness_shadow"                 label   "Double-sided for Shadow Rays"                 type    toggle                 default { "1" }                 help    "Toggle object double-sidedness for shadow rays fired in the direct lighting calculations."                 range   { 0 1 }                 parmtag { "spare_category" "Sidedness" }             }             parm {                 name    "ar_sidedness_diffuse_transmit"                 label   "Double-sided for Diffuse Transmission Rays"                 type    toggle                 default { "1" }                 help    "Toggle object double-sidedness for indirect diffuse transmission rays."                 range   { 0 1 }                 parmtag { "spare_category" "Sidedness" }             }             parm {                 name    "ar_sidedness_specular_transmit"                 label   "Double-sided for Specular Transmission Rays"                 type    toggle                 default { "1" }                 help    "Toggle object double-sidedness for indirect specular transmission rays."                 range   { 0 1 }                 parmtag { "spare_category" "Sidedness" }             }             parm {                 name    "ar_sidedness_diffuse_reflect"                 label   "Double-sided for Diffuse Reflection Rays"                 type    toggle                 default { "1" }                 help    "Toggle object double-sidedness for indirect diffuse reflection rays."                 range   { 0 1 }                 parmtag { "spare_category" "Sidedness" }             }             parm {                 name    "ar_sidedness_specular_reflect"                 label   "Double-sided for Specular Reflection Rays"                 type    toggle                 default { "1" }                 help    "Toggle object double-sidedness for indirect specular reflection rays."                 range   { 0 1 }                 parmtag { "spare_category" "Sidedness" }             }             parm {                 name    "ar_sidedness_volume"                 label   "Double-sided for Volume Scattering Rays"                 type    toggle                 default { "1" }                 help    "Toggle object double-sidedness for indirect volume scattering rays."                 range   { 0 1 }                 parmtag { "spare_category" "Sidedness" }             }         }      }      group {         name    "stdswitcher4_3"         label   "Misc"          parm {             name    "use_dcolor"             baseparm             label   "Set Wireframe Color"             export  none         }         parm {             name    "dcolor"             baseparm             label   "Wireframe Color"             export  none         }         parm {             name    "picking"             baseparm             label   "Viewport Selecting Enabled"             export  none         }         parm {             name    "pickscript"             baseparm             label   "Select Script"             export  none         }         parm {             name    "caching"             baseparm             label   "Cache Object Transform"             export  none         }         parm {             name    "vport_shadeopen"             baseparm             label   "Shade Open Curves In Viewport"             export  none         }         parm {             name    "vport_displayassubdiv"             baseparm             label   "Display as Subdivision in Viewport"             invisible             export  none         }         parm {             name    "vport_onionskin"             baseparm             label   "Onion Skinning"             export  none         }     }  ' $_obj_work
chblockbegin
chadd -t 0 0 $_obj_work ar_point_scale
chkey -t 0 -v 0 -V 0 -m 0 -M 0 -a 0 -A 0 -F 'ch("vm_pointscale")' $_obj_work/ar_point_scale
chadd -t 0 0 $_obj_work ar_mb_velocity_enable
chkey -t 0 -v 0 -V 0 -m 0 -M 0 -a 0 -A 0 -F 'ch("geo_velocityblur")' $_obj_work/ar_mb_velocity_enable
chadd -t 0 0 $_obj_work ar_matte
chkey -t 0 -v 0 -V 0 -m 0 -M 0 -a 0 -A 0 -F 'ch("vm_matte")' $_obj_work/ar_matte
chblockend
opset -S on $_obj_work
chautoscope $_obj_work +tx +ty +tz +rx +ry +rz +sx +sy +sz
opcolor -c 0.76499998569488525 1 0.57599997520446777 $_obj_work
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F off -c on -e on -b off -x off $_obj_work
opexprlanguage -s hscript $_obj_work
opuserdata -n '___Version___' -v '18.5.532' $_obj_work
opcf $_obj_work

# Node $_obj_work_set_noise (Sop/attribwrangle)
set _obj_work_set_noise = `run("opadd -e -n -v attribwrangle set_noise")`
oplocate -x `$arg2 + -4.3284303200077519` -y `$arg3 + 6.9898744573200391` $_obj_work_set_noise
opspareds '    group {         name    "folder1"         label   "Code"          parm {             name    "group"             baseparm             label   "Group"             export  none             bindselector points "Modify Points"                 "Select the points to affect and press Enter to complete."                 0 1 0xffffffff 0 grouptype 0         }         parm {             name    "grouptype"             baseparm             label   "Group Type"             export  none         }         parm {             name    "class"             baseparm             label   "Run Over"             export  none         }         parm {             name    "vex_numcount"             baseparm             label   "Number Count"             export  none         }         parm {             name    "vex_threadjobsize"             baseparm             label   "Thread Job Size"             export  none         }         parm {             name    "snippet"             baseparm             label   "VEXpression"             export  all         }         parm {             name    "exportlist"             baseparm             label   "Attributes to Create"             export  none         }         parm {             name    "vex_strict"             baseparm             label   "Enforce Prototypes"             export  none         }     }      group {         name    "folder1_1"         label   "Bindings"          parm {             name    "autobind"             baseparm             label   "Autobind by Name"             export  none         }         multiparm {             name    "bindings"             label    "Number of Bindings"             baseparm             default 0             parmtag { "autoscope" "0000000000000000" }             parmtag { "multistartoffset" "1" }              parm {                 name    "bindname#"                 baseparm                 label   "Attribute Name"                 export  none             }             parm {                 name    "bindparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "groupautobind"             baseparm             label   "Autobind Groups by Name"             export  none         }         multiparm {             name    "groupbindings"             label    "Group Bindings"             baseparm             default 0             parmtag { "autoscope" "0000000000000000" }             parmtag { "multistartoffset" "1" }              parm {                 name    "bindgroupname#"                 baseparm                 label   "Group Name"                 export  none             }             parm {                 name    "bindgroupparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "vex_cwdpath"             baseparm             label   "Evaluation Node Path"             export  none         }         parm {             name    "vex_outputmask"             baseparm             label   "Export Parameters"             export  none         }         parm {             name    "vex_updatenmls"             baseparm             label   "Update Normals If Displaced"             export  none         }         parm {             name    "vex_matchattrib"             baseparm             label   "Attribute to Match"             export  none         }         parm {             name    "vex_inplace"             baseparm             label   "Compute Results In Place"             export  none         }         parm {             name    "vex_selectiongroup"             baseparm             label   "Output Selection Group"             export  none         }         parm {             name    "vex_precision"             baseparm             label   "VEX Precision"             export  none         }     }      parm {         name    "fre"         label   "Fre"         type    float         default { "0" }         range   { 0 1 }     } ' $_obj_work_set_noise
opparm $_obj_work_set_noise  bindings ( 0 ) groupbindings ( 0 )
opparm $_obj_work_set_noise snippet ( '@noise = onoise(@P*chf(\'fre\'));\n//@Cd = @noise;' ) fre ( 100 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_set_noise
opexprlanguage -s hscript $_obj_work_set_noise
opuserdata -n '___Version___' -v '' $_obj_work_set_noise

# Node $_obj_work_deform (Sop/attribwrangle)
set _obj_work_deform = `run("opadd -e -n -v attribwrangle deform")`
oplocate -x `$arg2 + -0.30672132000775176` -y `$arg3 + 7.7560344573200393` $_obj_work_deform
opparm $_obj_work_deform  bindings ( 0 ) groupbindings ( 0 )
opparm $_obj_work_deform snippet ( '@P = point(1,\'P\',@ptnum);' )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_deform
opexprlanguage -s hscript $_obj_work_deform
opuserdata -n '___Version___' -v '' $_obj_work_deform

# Node $_obj_work_popnet (Sop/dopnet)
set _obj_work_popnet = `run("opadd -e -n -v dopnet popnet")`
oplocate -x `$arg2 + -3.9970261057843279` -y `$arg3 + 1.4394928303782089` $_obj_work_popnet
opspareds '    parm {         name    "isplayer"         baseparm         label   "Dopnet is Player"         joinnext         export  none     }     parm {         name    "playfilesname"         baseparm         label   "Playback Simulation"         export  none     }     group {         name    "stdswitcher4"         label   "Object Merge"          multiparm {             name    "numobj"             label    "Number of Objects"             baseparm             default 1              parm {                 name    "enable#"                 baseparm                 label   "Enable"                 export  none             }             parm {                 name    "objname#"                 baseparm                 label   "Object"                 export  none             }             parm {                 name    "dataname#"                 baseparm                 label   "Data"                 export  none             }         }      }      group {         name    "stdswitcher4_1"         label   "Simulation"          parm {             name    "minimumsubsteps"             label   "Min Substeps"             type    integer             default { "1" }             range   { 0 10 }             parmtag { "autoscope" "0000000000000000" }         }         parm {             name    "resimulate"             baseparm             label   "Reset Simulation"             nolabel             export  none         }         parm {             name    "initialstate"             baseparm             label   "Initial State"             export  none         }         parm {             name    "timestep"             baseparm             label   "Timestep"             export  none         }         parm {             name    "substep"             baseparm             label   "Substeps"             export  none         }         parm {             name    "timeoffset"             baseparm             label   "Offset Time"             export  none         }         parm {             name    "startframe"             baseparm             label   "Start Frame"             export  none         }         parm {             name    "timescale"             baseparm             label   "Scale Time"             export  none         }         parm {             name    "maxfeedback"             baseparm             label   "Max Feedback Loops"             export  none         }         parm {             name    "autoresim"             baseparm             label   "Enable Automatic Resimulation"             export  none         }         parm {             name    "datahints"             baseparm             label   "Provide Data Hints"             export  none         }         parm {             name    "interpolate"             baseparm             label   "Interpolate Display Data"             export  none         }     }      group {         name    "stdswitcher4_2"         label   "Cache"          parm {             name    "cacheenabled"             baseparm             label   "Cache Simulation"             export  none         }         parm {             name    "compresssims"             baseparm             label   "Compress .sim Files"             export  none         }         parm {             name    "cachetodisk"             baseparm             label   "Allow Caching To Disk"             export  none         }         parm {             name    "cachetodisknoninteractive"             baseparm             label   "Cache to Disk in Non-Interactive Sessions"             export  none         }         parm {             name    "cachesubsteps"             baseparm             label   "Cache Substep Data"             export  none         }         parm {             name    "cachemaxsize"             baseparm             label   "Cache Memory (MB)"             export  none         }         parm {             name    "timeless"             baseparm             label   "Timeless (No History)"             export  none         }         parm {             name    "explicitcache"             baseparm             label   "Save Checkpoints"             export  none         }         parm {             name    "explicitcachename"             baseparm             label   "Checkpoint File"             export  none         }         parm {             name    "explicitcachensteps"             baseparm             label   "Checkpoint Trail Length"             export  none         }         parm {             name    "explicitcachecheckpointspacing"             baseparm             label   "Checkpoint Interval"             export  none         }     }  ' $_obj_work_popnet
opparm $_obj_work_popnet  numobj ( 1 )
chblockbegin
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet timestep
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("timescale")/(ch("substep")*$FPS)' $_obj_work_popnet/timestep
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet timeoffset
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F '(ch("startframe")-1)/$FPS' $_obj_work_popnet/timeoffset
chblockend
opparm -V 18.5.532 $_obj_work_popnet stdswitcher ( 1 1 1 ) startframe ( 950 ) explicitcachename ( '//vdisk/SUM/rnd/wetness/fx/work_msugimura/temp/Sim/checkpoints_20220112154910/local/$OS.$SF.sim' ) objname1 ( pop* ) stdswitcher4 ( 1 1 1 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_popnet
opexprlanguage -s hscript $_obj_work_popnet
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_popnet
opuserdata -n 'base_path_dir' -v '//vdisk/SUM/rnd/wetness/fx/work_msugimura/temp/Sim/checkpoints_20220112154910' $_obj_work_popnet
opcf $_obj_work_popnet

# Node $_obj_work_popnet_popsolver (Dop/popsolver::2.0)
set _obj_work_popnet_popsolver = `run("opadd -e -n -v popsolver::2.0 popsolver")`
oplocate -x `$arg2 + 0.10595400000000001` -y `$arg3 + -0.19964699999999999` $_obj_work_popnet_popsolver
chblockbegin
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet_popsolver minimumsubsteps
chkey -t 41.666666666666664 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../minimumsubsteps")' $_obj_work_popnet_popsolver/minimumsubsteps
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet_popsolver substeps
chkey -t 41.666666666666664 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("minimumsubsteps")' $_obj_work_popnet_popsolver/substeps
chblockend
opset -d on -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_popnet_popsolver
opexprlanguage -s hscript $_obj_work_popnet_popsolver
opuserdata -n '___Version___' -v '' $_obj_work_popnet_popsolver
opuserdata -n '___toolcount___' -v '1' $_obj_work_popnet_popsolver
opuserdata -n '___toolid___' -v 'dynamics_poplocation' $_obj_work_popnet_popsolver

# Node $_obj_work_popnet_source_first_input (Dop/popsource::2.0)
set _obj_work_popnet_source_first_input = `run("opadd -e -n -v popsource::2.0 source_first_input")`
oplocate -x `$arg2 + 1.2601599999999999` -y `$arg3 + 5.3437799999999998` $_obj_work_popnet_source_first_input
opparm $_obj_work_popnet_source_first_input folder0 ( 1 1 1 1 1 ) emittype ( allpoint ) usecontextgeo ( first )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_popnet_source_first_input
opexprlanguage -s hscript $_obj_work_popnet_source_first_input
opuserdata -n '___Version___' -v '' $_obj_work_popnet_source_first_input
opuserdata -n '___toolcount___' -v '2' $_obj_work_popnet_source_first_input
opuserdata -n '___toolid___' -v 'dynamics_popsource' $_obj_work_popnet_source_first_input

# Node $_obj_work_popnet_popforce1 (Dop/popforce)
set _obj_work_popnet_popforce1 = `run("opadd -e -n -v popforce popforce1")`
oplocate -x `$arg2 + 1.2601599999999999` -y `$arg3 + 4.0455100000000002` $_obj_work_popnet_popforce1
chblockbegin
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet_popforce1 forcey
chkey -t 41.666666666666664 -v -9.8000000000000007 -m 0 -a 0 -A 0 -T a  -F -9.8 $_obj_work_popnet_popforce1/forcey
chblockend
opparm $_obj_work_popnet_popforce1 force ( 0 forcey 0 ) uselocalforce ( on ) localforceexpression ( '// Randomize Magnitude\n// Assign to a float to force rand to scalar.\n// 0.5 and 1.0 are the min and max scales\nfloat amt = rand(@id);\nforce *= fit01(pow(amt,3) , 0.25, 1.0);\n\n' ) swirlsize ( 0.10000000000000001 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_popnet_popforce1
opexprlanguage -s hscript $_obj_work_popnet_popforce1
opuserdata -n '___Version___' -v '' $_obj_work_popnet_popforce1
opuserdata -n '___toolcount___' -v '2' $_obj_work_popnet_popforce1
opuserdata -n '___toolid___' -v 'dynamics_popforce' $_obj_work_popnet_popforce1

# Node $_obj_work_popnet_minpos (Dop/popwrangle)
set _obj_work_popnet_minpos = `run("opadd -e -n -v popwrangle minpos")`
oplocate -x `$arg2 + 0.55691299999999999` -y `$arg3 + 1.3983699999999999` $_obj_work_popnet_minpos
opparm $_obj_work_popnet_minpos  bindings ( 0 ) bindfield_num ( 0 ) groupbindings ( 0 )
opparm $_obj_work_popnet_minpos snippet ( '@P = minpos(2,@P);\n' ) bindinputmenu3 ( third )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_popnet_minpos
opexprlanguage -s hscript $_obj_work_popnet_minpos
opuserdata -n '___Version___' -v '' $_obj_work_popnet_minpos

# Node $_obj_work_popnet_SDF (Dop/popwrangle)
set _obj_work_popnet_SDF = `run("opadd -e -n -v popwrangle SDF")`
oplocate -x `$arg2 + 3.3323700000000001` -y `$arg3 + 2.6400000000000001` $_obj_work_popnet_SDF
opparm $_obj_work_popnet_SDF  bindings ( 0 ) bindfield_num ( 0 ) groupbindings ( 0 )
opparm $_obj_work_popnet_SDF folder1 ( 2 2 2 2 ) snippet ( 'float vs = volumesample(3,0,@P);\nvector vg = normalize(volumegradient(3,0,@P));\n@P -= vg*vs;  ' ) bindinputmenu3 ( third ) bindinputmenu4 ( fourth )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_popnet_SDF
opexprlanguage -s hscript $_obj_work_popnet_SDF
opuserdata -n '___Version___' -v '' $_obj_work_popnet_SDF

# Node $_obj_work_popnet_get_v_N (Dop/popvop)
set _obj_work_popnet_get_v_N = `run("opadd -e -n -v popvop get_v_N")`
oplocate -x `$arg2 + 0.55646300000000004` -y `$arg3 + 2.641` $_obj_work_popnet_get_v_N
opspareds '    parm {         name    "activate"         baseparm         label   "Activation"         export  none     }     parm {         name    "usegroup"         baseparm         label   "Group"         joinnext         export  none     }     parm {         name    "partgroup"         baseparm         label   "Group"         export  none     }     group {         name    "stdswitcher5"         label   "Vex Setup"          parm {             name    "vexsrc"             baseparm             label   "Vex Source"             export  all         }         parm {             name    "vexshoppath"             baseparm             label   "Shop Path"             export  all         }         parm {             name    "vexscript"             baseparm             label   "Script"             export  none         }         parm {             name    "vexclear"             baseparm             label   "Re-load VEX Functions"             export  none         }         parm {             name    "vop_compiler"             baseparm             label   "Compiler"             export  none         }         parm {             name    "vop_forcecompile"             baseparm             label   "Force Compile"             export  none         }         parm {             name    "vex_cwdpath"             baseparm             label   "Evaluation Node Path"             export  none         }         parm {             name    "vex_outputmask"             baseparm             label   "Export Parameters"             export  none         }         parm {             name    "vex_multithread"             baseparm             label   "Enable Multithreading"             export  none         }     }      group {         name    "stdswitcher5_1"         label   "Data Bindings"          parm {             name    "bindgeo"             baseparm             label   "Geometry"             export  none         }         parm {             name    "autobind"             baseparm             label   "Autobind by Name"             export  none         }         multiparm {             name    "bindings"             label    "Attribute Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "binddata#"                 baseparm                 label   "Attribute Name"                 export  none             }             parm {                 name    "bindparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          multiparm {             name    "bindfield_num"             label    "Field Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindfield_data#"                 baseparm                 label   "Field Name"                 export  none             }             parm {                 name    "bindfield_parm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "groupautobind"             baseparm             label   "Autobind Groups by Name"             export  none         }         multiparm {             name    "groupbindings"             label    "Group Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindgroupname#"                 baseparm                 label   "Group Name"                 export  none             }             parm {                 name    "bindgroupparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "vex_updatenmls"             baseparm             label   "Update Normals If Displaced"             export  none         }         parm {             name    "vex_precision"             baseparm             label   "VEX Precision"             export  none         }     }      group {         name    "stdswitcher5_2"         label   "Inputs"          parm {             name    "bindinputmenu1"             baseparm             label   "Input 1"             export  none         }         parm {             name    "bindgeoinput1"             baseparm             label   "SOP Path"             export  none         }         parm {             name    "binddopinput1"             baseparm             label   "DOP Data"             export  none         }         parm {             name    "bindinputmenu2"             baseparm             label   "Input 2"             export  none         }         parm {             name    "bindgeoinput2"             baseparm             label   "SOP Path"             export  none         }         parm {             name    "binddopinput2"             baseparm             label   "DOP Data"             export  none         }         parm {             name    "bindinputmenu3"             baseparm             label   "Input 3"             export  none         }         parm {             name    "bindgeoinput3"             baseparm             label   "SOP Path"             export  none         }         parm {             name    "binddopinput3"             baseparm             label   "DOP Data"             export  none         }         parm {             name    "bindinputmenu4"             baseparm             label   "Input 4"             export  none         }         parm {             name    "bindgeoinput4"             baseparm             label   "SOP Path"             export  none         }         parm {             name    "binddopinput4"             baseparm             label   "DOP Data"             export  none         }     }      group {         name    "stdswitcher5_3"         label   "Solver"          parm {             name    "usetimestep"             baseparm             label   "Use Timestep"             export  none         }         parm {             name    "timescale"             baseparm             label   "Time Scale"             export  none         }         parm {             name    "addaffectors"             baseparm             label   "Make Objects Mutual Affectors"             export  none         }         parm {             name    "group"             baseparm             label   "Group"             export  none         }         parm {             name    "dataname"             baseparm             label   "Data Name"             export  none         }         parm {             name    "uniquedataname"             baseparm             label   "Unique Data Name"             export  none         }         parm {             name    "solverperobject"             baseparm             label   "Solver Per Object"             export  none         }     }      parm {         name    "ptnum"         label   "Point Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "vtxnum"         label   "Vertex Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "primnum"         label   "Primitive Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "id"         label   "Id"         type    integer         invisible         default { "-1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numpt"         label   "Number of Points"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numvtx"         label   "Number of Vertices"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numprim"         label   "Number of Prims"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Time"         label   "Time"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "TimeInc"         label   "Time Inc"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Frame"         label   "Frame"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "life"         label   "Life"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "age"         label   "Age"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput2"         label   "Second Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput3"         label   "Third Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput4"         label   "Fourth Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput1"         label   "First Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "uv"         label   "UV"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "P"         label   "P"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "v"         label   "Velocity"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "force"         label   "Force"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Cd"         label   "Cd"         type    float         invisible         size    3         default { "1" "1" "1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "N"         label   "N"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     } ' $_obj_work_popnet_get_v_N
opparm $_obj_work_popnet_get_v_N  bindings ( 0 ) bindfield_num ( 0 ) groupbindings ( 0 )
opparm -V 18.5.532 $_obj_work_popnet_get_v_N stdswitcher ( 2 2 2 2 ) bindinputmenu3 ( third )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_popnet_get_v_N
opexprlanguage -s hscript $_obj_work_popnet_get_v_N
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_popnet_get_v_N
opcf $_obj_work_popnet_get_v_N

# Node $_obj_work_popnet_get_v_N_geometryvopglobal1 (Vop/geometryvopglobal::2.0)
set _obj_work_popnet_get_v_N_geometryvopglobal1 = `run("opadd -e -n -v geometryvopglobal::2.0 geometryvopglobal1")`
oplocate -x `$arg2 + 0.59860000000000002` -y `$arg3 + 2.2050700000000001` $_obj_work_popnet_get_v_N_geometryvopglobal1
opset -d on -r on -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_work_popnet_get_v_N_geometryvopglobal1
opexprlanguage -s hscript $_obj_work_popnet_get_v_N_geometryvopglobal1
opuserdata -n '___Version___' -v '' $_obj_work_popnet_get_v_N_geometryvopglobal1

# Node $_obj_work_popnet_get_v_N_geometryvopoutput1 (Vop/geometryvopoutput)
set _obj_work_popnet_get_v_N_geometryvopoutput1 = `run("opadd -e -n -v geometryvopoutput geometryvopoutput1")`
oplocate -x `$arg2 + 8.2213899999999995` -y `$arg3 + 3.6876699999999998` $_obj_work_popnet_get_v_N_geometryvopoutput1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_work_popnet_get_v_N_geometryvopoutput1
opexprlanguage -s hscript $_obj_work_popnet_get_v_N_geometryvopoutput1
opuserdata -n '___Version___' -v '' $_obj_work_popnet_get_v_N_geometryvopoutput1

# Node $_obj_work_popnet_get_v_N_pcopen1 (Vop/pcopen)
set _obj_work_popnet_get_v_N_pcopen1 = `run("opadd -e -n -v pcopen pcopen1")`
oplocate -x `$arg2 + 3.1665700000000001` -y `$arg3 + 1.23007` $_obj_work_popnet_get_v_N_pcopen1
opparm $_obj_work_popnet_get_v_N_pcopen1 radius ( 0.050000000000000003 ) maxpoints ( 5 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_work_popnet_get_v_N_pcopen1
opexprlanguage -s hscript $_obj_work_popnet_get_v_N_pcopen1
opuserdata -n '___Version___' -v '' $_obj_work_popnet_get_v_N_pcopen1

# Node $_obj_work_popnet_get_v_N_pcfilter1 (Vop/pcfilter)
set _obj_work_popnet_get_v_N_pcfilter1 = `run("opadd -e -n -v pcfilter pcfilter1")`
oplocate -x `$arg2 + 5.6310599999999997` -y `$arg3 + 2.0600700000000001` $_obj_work_popnet_get_v_N_pcfilter1
opparm $_obj_work_popnet_get_v_N_pcfilter1 channel ( v )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_work_popnet_get_v_N_pcfilter1
opexprlanguage -s hscript $_obj_work_popnet_get_v_N_pcfilter1
opuserdata -n '___Version___' -v '' $_obj_work_popnet_get_v_N_pcfilter1

# Node $_obj_work_popnet_get_v_N_pcfilter2 (Vop/pcfilter)
set _obj_work_popnet_get_v_N_pcfilter2 = `run("opadd -e -n -v pcfilter pcfilter2")`
oplocate -x `$arg2 + 5.6310599999999997` -y `$arg3 + 0.70506800000000003` $_obj_work_popnet_get_v_N_pcfilter2
opparm $_obj_work_popnet_get_v_N_pcfilter2 channel ( N )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_work_popnet_get_v_N_pcfilter2
opexprlanguage -s hscript $_obj_work_popnet_get_v_N_pcfilter2
opuserdata -n '___Version___' -v '' $_obj_work_popnet_get_v_N_pcfilter2
opcf ..
opcf ..

# Node $_obj_work_collisionsource1 (Sop/collisionsource::2.0)
set _obj_work_collisionsource1 = `run("opadd -e -n -v collisionsource::2.0 collisionsource1")`
oplocate -x `$arg2 + 3.2707062491696561` -y `$arg3 + 7.1177865625346559` $_obj_work_collisionsource1
opparm $_obj_work_collisionsource1 folder3 ( 1 1 ) voxelsize ( 0.0040000000000000001 ) bandwidth ( 8 )
opset -d on -r on -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_collisionsource1
opexprlanguage -s hscript $_obj_work_collisionsource1
opuserdata -n '___Version___' -v '' $_obj_work_collisionsource1
opuserdata -n '___toolcount___' -v '4' $_obj_work_collisionsource1
opuserdata -n '___toolid___' -v 'dop_deformingobject' $_obj_work_collisionsource1

# Node $_obj_work_pscale (Sop/attribwrangle)
set _obj_work_pscale = `run("opadd -e -n -v attribwrangle pscale")`
oplocate -x `$arg2 + -0.040925299999999998` -y `$arg3 + -13.893800000000001` $_obj_work_pscale
opspareds '    group {         name    "folder1"         label   "Code"          parm {             name    "group"             baseparm             label   "Group"             export  none             bindselector points "Modify Points"                 "Select the points to affect and press Enter to complete."                 0 1 0xffffffff 0 grouptype 0         }         parm {             name    "grouptype"             baseparm             label   "Group Type"             export  none         }         parm {             name    "class"             baseparm             label   "Run Over"             export  none         }         parm {             name    "vex_numcount"             baseparm             label   "Number Count"             export  none         }         parm {             name    "vex_threadjobsize"             baseparm             label   "Thread Job Size"             export  none         }         parm {             name    "snippet"             baseparm             label   "VEXpression"             export  all         }         parm {             name    "exportlist"             baseparm             label   "Attributes to Create"             export  none         }         parm {             name    "vex_strict"             baseparm             label   "Enforce Prototypes"             export  none         }     }      group {         name    "folder1_1"         label   "Bindings"          parm {             name    "autobind"             baseparm             label   "Autobind by Name"             export  none         }         multiparm {             name    "bindings"             label    "Number of Bindings"             baseparm             default 0             parmtag { "autoscope" "0000000000000000" }             parmtag { "multistartoffset" "1" }              parm {                 name    "bindname#"                 baseparm                 label   "Attribute Name"                 export  none             }             parm {                 name    "bindparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "groupautobind"             baseparm             label   "Autobind Groups by Name"             export  none         }         multiparm {             name    "groupbindings"             label    "Group Bindings"             baseparm             default 0             parmtag { "autoscope" "0000000000000000" }             parmtag { "multistartoffset" "1" }              parm {                 name    "bindgroupname#"                 baseparm                 label   "Group Name"                 export  none             }             parm {                 name    "bindgroupparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "vex_cwdpath"             baseparm             label   "Evaluation Node Path"             export  none         }         parm {             name    "vex_outputmask"             baseparm             label   "Export Parameters"             export  none         }         parm {             name    "vex_updatenmls"             baseparm             label   "Update Normals If Displaced"             export  none         }         parm {             name    "vex_matchattrib"             baseparm             label   "Attribute to Match"             export  none         }         parm {             name    "vex_inplace"             baseparm             label   "Compute Results In Place"             export  none         }         parm {             name    "vex_selectiongroup"             baseparm             label   "Output Selection Group"             export  none         }         parm {             name    "vex_precision"             baseparm             label   "VEX Precision"             export  none         }     }      parm {         name    "pscale"         label   "Pscale"         type    ramp_flt         default { "2" }         range   { 1! 10 }     }     parm {         name    "pscale_max"         label   "Pscale Max"         type    float         default { "0" }         range   { 0 1 }     } ' $_obj_work_pscale
opparm $_obj_work_pscale  bindings ( 0 ) groupbindings ( 0 ) pscale ( 9 )
opparm $_obj_work_pscale snippet ( '\nfloat nAge = @age/@life;\n@pscale = chf(\'pscale_max\') * chramp(\'pscale\',nAge);\n' ) pscale ( 9 ) pscale1value ( 0.98958331346511841 ) pscale_max ( 0.0040000000000000001 ) pscale3pos ( 0.020618556067347527 ) pscale3value ( 0.59375 ) pscale4pos ( 0.073310427367687225 ) pscale4value ( 0.97916668653488159 ) pscale5pos ( 0.12371134012937546 ) pscale5value ( 1 ) pscale6pos ( 0.21191294491291046 ) pscale6value ( 0.9375 ) pscale7pos ( 0.65406644344329834 ) pscale7value ( 0.1927083283662796 ) pscale8pos ( 0.81099659204483032 ) pscale8value ( 0.046875 ) pscale9pos ( 0.99541807174682617 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_pscale
opexprlanguage -s hscript $_obj_work_pscale
opuserdata -n '___Version___' -v '' $_obj_work_pscale

# Node $_obj_work_popnet_trail (Sop/dopnet)
set _obj_work_popnet_trail = `run("opadd -e -n -v dopnet popnet_trail")`
oplocate -x `$arg2 + 0.270096` -y `$arg3 + -9.8928200000000004` $_obj_work_popnet_trail
opspareds '    parm {         name    "isplayer"         baseparm         label   "Dopnet is Player"         joinnext         export  none     }     parm {         name    "playfilesname"         baseparm         label   "Playback Simulation"         export  none     }     group {         name    "stdswitcher4"         label   "Object Merge"          multiparm {             name    "numobj"             label    "Number of Objects"             baseparm             default 1              parm {                 name    "enable#"                 baseparm                 label   "Enable"                 export  none             }             parm {                 name    "objname#"                 baseparm                 label   "Object"                 export  none             }             parm {                 name    "dataname#"                 baseparm                 label   "Data"                 export  none             }         }      }      group {         name    "stdswitcher4_1"         label   "Simulation"          parm {             name    "minimumsubsteps"             label   "Min Substeps"             type    integer             default { "1" }             range   { 0 10 }             parmtag { "autoscope" "0000000000000000" }         }         parm {             name    "resimulate"             baseparm             label   "Reset Simulation"             nolabel             export  none         }         parm {             name    "initialstate"             baseparm             label   "Initial State"             export  none         }         parm {             name    "timestep"             baseparm             label   "Timestep"             export  none         }         parm {             name    "substep"             baseparm             label   "Substeps"             export  none         }         parm {             name    "timeoffset"             baseparm             label   "Offset Time"             export  none         }         parm {             name    "startframe"             baseparm             label   "Start Frame"             export  none         }         parm {             name    "timescale"             baseparm             label   "Scale Time"             export  none         }         parm {             name    "maxfeedback"             baseparm             label   "Max Feedback Loops"             export  none         }         parm {             name    "autoresim"             baseparm             label   "Enable Automatic Resimulation"             export  none         }         parm {             name    "datahints"             baseparm             label   "Provide Data Hints"             export  none         }         parm {             name    "interpolate"             baseparm             label   "Interpolate Display Data"             export  none         }     }      group {         name    "stdswitcher4_2"         label   "Cache"          parm {             name    "cacheenabled"             baseparm             label   "Cache Simulation"             export  none         }         parm {             name    "compresssims"             baseparm             label   "Compress .sim Files"             export  none         }         parm {             name    "cachetodisk"             baseparm             label   "Allow Caching To Disk"             export  none         }         parm {             name    "cachetodisknoninteractive"             baseparm             label   "Cache to Disk in Non-Interactive Sessions"             export  none         }         parm {             name    "cachesubsteps"             baseparm             label   "Cache Substep Data"             export  none         }         parm {             name    "cachemaxsize"             baseparm             label   "Cache Memory (MB)"             export  none         }         parm {             name    "timeless"             baseparm             label   "Timeless (No History)"             export  none         }         parm {             name    "explicitcache"             baseparm             label   "Save Checkpoints"             export  none         }         parm {             name    "explicitcachename"             baseparm             label   "Checkpoint File"             export  none         }         parm {             name    "explicitcachensteps"             baseparm             label   "Checkpoint Trail Length"             export  none         }         parm {             name    "explicitcachecheckpointspacing"             baseparm             label   "Checkpoint Interval"             export  none         }     }  ' $_obj_work_popnet_trail
opparm $_obj_work_popnet_trail  numobj ( 1 )
chblockbegin
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet_trail timestep
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("timescale")/(ch("substep")*$FPS)' $_obj_work_popnet_trail/timestep
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet_trail timeoffset
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F '(ch("startframe")-1)/$FPS' $_obj_work_popnet_trail/timeoffset
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet_trail startframe
chkey -t 41.666666666666664 -v 1001 -m 0 -a 0 -A 0 -T a  -F 'ch("../popnet/startframe")' $_obj_work_popnet_trail/startframe
chblockend
opparm -V 18.5.532 $_obj_work_popnet_trail stdswitcher ( 1 1 1 ) substep ( 2 ) startframe ( startframe ) explicitcachename ( '//vdisk/SUM/rnd/wetness/fx/work_msugimura/temp/Sim/checkpoints_20220112154910/local/$OS.$SF.sim' ) objname1 ( pop* ) stdswitcher4 ( 1 1 1 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_popnet_trail
opexprlanguage -s hscript $_obj_work_popnet_trail
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_popnet_trail
opuserdata -n 'base_path_dir' -v '//vdisk/SUM/rnd/wetness/fx/work_msugimura/temp/Sim/checkpoints_20220112154910' $_obj_work_popnet_trail
opcf $_obj_work_popnet_trail

# Node $_obj_work_popnet_trail_popsolver (Dop/popsolver::2.0)
set _obj_work_popnet_trail_popsolver = `run("opadd -e -n -v popsolver::2.0 popsolver")`
oplocate -x `$arg2 + 0.27025100000000002` -y `$arg3 + 0.0152027` $_obj_work_popnet_trail_popsolver
chblockbegin
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet_trail_popsolver minimumsubsteps
chkey -t 41.666666666666664 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../minimumsubsteps")' $_obj_work_popnet_trail_popsolver/minimumsubsteps
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet_trail_popsolver substeps
chkey -t 41.666666666666664 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("minimumsubsteps")' $_obj_work_popnet_trail_popsolver/substeps
chblockend
opset -d on -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_popnet_trail_popsolver
opexprlanguage -s hscript $_obj_work_popnet_trail_popsolver
opuserdata -n '___Version___' -v '' $_obj_work_popnet_trail_popsolver
opuserdata -n '___toolcount___' -v '1' $_obj_work_popnet_trail_popsolver
opuserdata -n '___toolid___' -v 'dynamics_poplocation' $_obj_work_popnet_trail_popsolver

# Node $_obj_work_popnet_trail_source_first_input (Dop/popsource::2.0)
set _obj_work_popnet_trail_source_first_input = `run("opadd -e -n -v popsource::2.0 source_first_input")`
oplocate -x `$arg2 + 1.0942499999999999` -y `$arg3 + 5.1668399999999997` $_obj_work_popnet_trail_source_first_input
opparm $_obj_work_popnet_trail_source_first_input folder0 ( 1 1 1 1 1 ) emittype ( allpoint ) usecontextgeo ( first ) life ( 2.5 ) lifevar ( 0.5 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_popnet_trail_source_first_input
opexprlanguage -s hscript $_obj_work_popnet_trail_source_first_input
opuserdata -n '___Version___' -v '' $_obj_work_popnet_trail_source_first_input
opuserdata -n '___toolcount___' -v '2' $_obj_work_popnet_trail_source_first_input
opuserdata -n '___toolid___' -v 'dynamics_popsource' $_obj_work_popnet_trail_source_first_input

# Node $_obj_work_popnet_trail_popvop1 (Dop/popvop)
set _obj_work_popnet_trail_popvop1 = `run("opadd -e -n -v popvop popvop1")`
oplocate -x `$arg2 + 1.0908` -y `$arg3 + 2.80342` $_obj_work_popnet_trail_popvop1
opspareds '    parm {         name    "activate"         baseparm         label   "Activation"         export  none     }     parm {         name    "usegroup"         baseparm         label   "Group"         joinnext         export  none     }     parm {         name    "partgroup"         baseparm         label   "Group"         export  none     }     group {         name    "stdswitcher5"         label   "Vex Setup"          parm {             name    "vexsrc"             baseparm             label   "Vex Source"             export  all         }         parm {             name    "vexshoppath"             baseparm             label   "Shop Path"             export  all         }         parm {             name    "vexscript"             baseparm             label   "Script"             export  none         }         parm {             name    "vexclear"             baseparm             label   "Re-load VEX Functions"             export  none         }         parm {             name    "vop_compiler"             baseparm             label   "Compiler"             export  none         }         parm {             name    "vop_forcecompile"             baseparm             label   "Force Compile"             export  none         }         parm {             name    "vex_cwdpath"             baseparm             label   "Evaluation Node Path"             export  none         }         parm {             name    "vex_outputmask"             baseparm             label   "Export Parameters"             export  none         }         parm {             name    "vex_multithread"             baseparm             label   "Enable Multithreading"             export  none         }     }      group {         name    "stdswitcher5_1"         label   "Data Bindings"          parm {             name    "bindgeo"             baseparm             label   "Geometry"             export  none         }         parm {             name    "autobind"             baseparm             label   "Autobind by Name"             export  none         }         multiparm {             name    "bindings"             label    "Attribute Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "binddata#"                 baseparm                 label   "Attribute Name"                 export  none             }             parm {                 name    "bindparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          multiparm {             name    "bindfield_num"             label    "Field Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindfield_data#"                 baseparm                 label   "Field Name"                 export  none             }             parm {                 name    "bindfield_parm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "groupautobind"             baseparm             label   "Autobind Groups by Name"             export  none         }         multiparm {             name    "groupbindings"             label    "Group Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindgroupname#"                 baseparm                 label   "Group Name"                 export  none             }             parm {                 name    "bindgroupparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "vex_updatenmls"             baseparm             label   "Update Normals If Displaced"             export  none         }         parm {             name    "vex_precision"             baseparm             label   "VEX Precision"             export  none         }     }      group {         name    "stdswitcher5_2"         label   "Inputs"          parm {             name    "bindinputmenu1"             baseparm             label   "Input 1"             export  none         }         parm {             name    "bindgeoinput1"             baseparm             label   "SOP Path"             export  none         }         parm {             name    "binddopinput1"             baseparm             label   "DOP Data"             export  none         }         parm {             name    "bindinputmenu2"             baseparm             label   "Input 2"             export  none         }         parm {             name    "bindgeoinput2"             baseparm             label   "SOP Path"             export  none         }         parm {             name    "binddopinput2"             baseparm             label   "DOP Data"             export  none         }         parm {             name    "bindinputmenu3"             baseparm             label   "Input 3"             export  none         }         parm {             name    "bindgeoinput3"             baseparm             label   "SOP Path"             export  none         }         parm {             name    "binddopinput3"             baseparm             label   "DOP Data"             export  none         }         parm {             name    "bindinputmenu4"             baseparm             label   "Input 4"             export  none         }         parm {             name    "bindgeoinput4"             baseparm             label   "SOP Path"             export  none         }         parm {             name    "binddopinput4"             baseparm             label   "DOP Data"             export  none         }     }      group {         name    "stdswitcher5_3"         label   "Solver"          parm {             name    "usetimestep"             baseparm             label   "Use Timestep"             export  none         }         parm {             name    "timescale"             baseparm             label   "Time Scale"             export  none         }         parm {             name    "addaffectors"             baseparm             label   "Make Objects Mutual Affectors"             export  none         }         parm {             name    "group"             baseparm             label   "Group"             export  none         }         parm {             name    "dataname"             baseparm             label   "Data Name"             export  none         }         parm {             name    "uniquedataname"             baseparm             label   "Unique Data Name"             export  none         }         parm {             name    "solverperobject"             baseparm             label   "Solver Per Object"             export  none         }     }      parm {         name    "ptnum"         label   "Point Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "vtxnum"         label   "Vertex Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "primnum"         label   "Primitive Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "id"         label   "Id"         type    integer         invisible         default { "-1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numpt"         label   "Number of Points"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numvtx"         label   "Number of Vertices"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numprim"         label   "Number of Prims"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Time"         label   "Time"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "TimeInc"         label   "Time Inc"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Frame"         label   "Frame"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "life"         label   "Life"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "age"         label   "Age"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput2"         label   "Second Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput3"         label   "Third Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput4"         label   "Fourth Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput1"         label   "First Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "uv"         label   "UV"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "P"         label   "P"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "v"         label   "Velocity"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "force"         label   "Force"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Cd"         label   "Cd"         type    float         invisible         size    3         default { "1" "1" "1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "N"         label   "N"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     } ' $_obj_work_popnet_trail_popvop1
opparm $_obj_work_popnet_trail_popvop1  bindings ( 0 ) bindfield_num ( 0 ) groupbindings ( 0 )
opparm -V 18.5.532 $_obj_work_popnet_trail_popvop1 stdswitcher ( 2 2 2 2 ) bindinputmenu3 ( third ) stdswitcher5 ( 2 2 2 2 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_popnet_trail_popvop1
opexprlanguage -s hscript $_obj_work_popnet_trail_popvop1
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_popnet_trail_popvop1
opcf $_obj_work_popnet_trail_popvop1

# Node $_obj_work_popnet_trail_popvop1_geometryvopglobal1 (Vop/geometryvopglobal::2.0)
set _obj_work_popnet_trail_popvop1_geometryvopglobal1 = `run("opadd -e -n -v geometryvopglobal::2.0 geometryvopglobal1")`
oplocate -x `$arg2 + 1.9057900000000001` -y `$arg3 + 1.97631` $_obj_work_popnet_trail_popvop1_geometryvopglobal1
opset -d on -r on -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_work_popnet_trail_popvop1_geometryvopglobal1
opexprlanguage -s hscript $_obj_work_popnet_trail_popvop1_geometryvopglobal1
opuserdata -n '___Version___' -v '' $_obj_work_popnet_trail_popvop1_geometryvopglobal1

# Node $_obj_work_popnet_trail_popvop1_geometryvopoutput1 (Vop/geometryvopoutput)
set _obj_work_popnet_trail_popvop1_geometryvopoutput1 = `run("opadd -e -n -v geometryvopoutput geometryvopoutput1")`
oplocate -x `$arg2 + 6.64696` -y `$arg3 + 3.67056` $_obj_work_popnet_trail_popvop1_geometryvopoutput1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_work_popnet_trail_popvop1_geometryvopoutput1
opexprlanguage -s hscript $_obj_work_popnet_trail_popvop1_geometryvopoutput1
opuserdata -n '___Version___' -v '' $_obj_work_popnet_trail_popvop1_geometryvopoutput1

# Node $_obj_work_popnet_trail_popvop1_primuv1 (Vop/primuv)
set _obj_work_popnet_trail_popvop1_primuv1 = `run("opadd -e -n -v primuv primuv1")`
oplocate -x `$arg2 + 4.6505599999999996` -y `$arg3 + 1.37151` $_obj_work_popnet_trail_popvop1_primuv1
opparm $_obj_work_popnet_trail_popvop1_primuv1 attrib ( P )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_work_popnet_trail_popvop1_primuv1
opexprlanguage -s hscript $_obj_work_popnet_trail_popvop1_primuv1
opuserdata -n '___Version___' -v '' $_obj_work_popnet_trail_popvop1_primuv1

# Node $_obj_work_popnet_trail_popvop1_bind1 (Vop/bind)
set _obj_work_popnet_trail_popvop1_bind1 = `run("opadd -e -n -v bind bind1")`
oplocate -x `$arg2 + 2.27311` -y `$arg3 + 4.8306899999999997` $_obj_work_popnet_trail_popvop1_bind1
opparm -V 18.5.532 $_obj_work_popnet_trail_popvop1_bind1 parmname ( hitprim ) parmtype ( int ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_work_popnet_trail_popvop1_bind1
opexprlanguage -s hscript $_obj_work_popnet_trail_popvop1_bind1
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_popnet_trail_popvop1_bind1

# Node $_obj_work_popnet_trail_popvop1_bind2 (Vop/bind)
set _obj_work_popnet_trail_popvop1_bind2 = `run("opadd -e -n -v bind bind2")`
oplocate -x `$arg2 + 2.2404299999999999` -y `$arg3 + 3.4747400000000002` $_obj_work_popnet_trail_popvop1_bind2
opparm -V 18.5.532 $_obj_work_popnet_trail_popvop1_bind2 parmname ( hitprimuv ) parmtype ( vector ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_work_popnet_trail_popvop1_bind2
opexprlanguage -s hscript $_obj_work_popnet_trail_popvop1_bind2
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_popnet_trail_popvop1_bind2
opcf ..
opcf ..

# Node $_obj_work_clean2 (Sop/clean)
set _obj_work_clean2 = `run("opadd -e -n -v clean clean2")`
oplocate -x `$arg2 + -1.3862000000000001` -y `$arg3 + -7.3351199999999999` $_obj_work_clean2
opparm $_obj_work_clean2 deldegengeo ( off ) delunusedpts ( off ) dodelattribs ( on ) delattribs ( '* ^id' ) delnans ( off )
chautoscope $_obj_work_clean2 +delete_small
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_clean2
opexprlanguage -s hscript $_obj_work_clean2
opuserdata -n '___Version___' -v '' $_obj_work_clean2

# Node $_obj_work_particlefluidsurface1 (Sop/particlefluidsurface::2.0)
set _obj_work_particlefluidsurface1 = `run("opadd -e -n -v particlefluidsurface::2.0 particlefluidsurface1")`
oplocate -x `$arg2 + -1.3201499999999999` -y `$arg3 + -19.712399999999999` $_obj_work_particlefluidsurface1
opparm $_obj_work_particlefluidsurface1  velvisramp ( 3 ) vorticityvisramp ( 3 ) maskvisramp ( 5 )
chblockbegin
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_particlefluidsurface1 doerode
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("dodilate")' $_obj_work_particlefluidsurface1/doerode
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_particlefluidsurface1 erodeoffset
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("dilateoffset")' $_obj_work_particlefluidsurface1/erodeoffset
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_particlefluidsurface1 erodemask
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("dilatemask")' $_obj_work_particlefluidsurface1/erodemask
chblockend
opparm $_obj_work_particlefluidsurface1 particlesep ( 0.001 ) velvisramp1c ( 0 0 0.89999997615814209 ) velvisramp2pos ( 0.50579148530960083 ) velvisramp2c ( 0 0.90000000000000002 0.90000000000000002 ) velvisramp3pos ( 1 ) velvisramp3c ( 1 1 1 ) vorticityvisramp1c ( 0 0 0.89999997615814209 ) vorticityvisramp2pos ( 0.5 ) vorticityvisramp2c ( 0 0.89999997615814209 0.89999997615814209 ) vorticityvisramp3pos ( 1 ) vorticityvisramp3c ( 1 1 1 ) maskvisramp1c ( 0.20000000000000001 0 1 ) maskvisramp2pos ( 0.25 ) maskvisramp2c ( 0 0.84999999999999998 1 ) maskvisramp3pos ( 0.5 ) maskvisramp3c ( 0 1 0.10000000149011612 ) maskvisramp4pos ( 0.75 ) maskvisramp4c ( 0.94999999999999996 1 0 ) maskvisramp5pos ( 1 ) maskvisramp5c ( 1 0 0 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_particlefluidsurface1
opexprlanguage -s hscript $_obj_work_particlefluidsurface1
opuserdata -n '___Version___' -v '' $_obj_work_particlefluidsurface1
opuserdata -n '___toolcount___' -v '1' $_obj_work_particlefluidsurface1
opuserdata -n '___toolid___' -v 'dynamics_flipbox' $_obj_work_particlefluidsurface1

# Node $_obj_work_clean3 (Sop/clean)
set _obj_work_clean3 = `run("opadd -e -n -v clean clean3")`
oplocate -x `$arg2 + 0.59681200000000001` -y `$arg3 + -17.3232` $_obj_work_clean3
opparm $_obj_work_clean3 deldegengeo ( off ) delunusedpts ( off ) dodelattribs ( on ) delattribs ( '* ^pscale ^v' ) delnans ( off )
chautoscope $_obj_work_clean3 +delete_small
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_clean3
opexprlanguage -s hscript $_obj_work_clean3
opuserdata -n '___Version___' -v '' $_obj_work_clean3

# Node $_obj_work_clean4 (Sop/clean)
set _obj_work_clean4 = `run("opadd -e -n -v clean clean4")`
oplocate -x `$arg2 + -3.7434303200077519` -y `$arg3 + -0.6228855426799611` $_obj_work_clean4
opparm $_obj_work_clean4 deldegengeo ( off ) delunusedpts ( off ) dodelattribs ( on ) delattribs ( '* ^id ^v ^N ^life ^age' ) dodelgroups ( on ) delnans ( off )
chautoscope $_obj_work_clean4 +delete_small
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_clean4
opexprlanguage -s hscript $_obj_work_clean4
opuserdata -n '___Version___' -v '' $_obj_work_clean4

# Node $_obj_work_remove_by_dot (Sop/attribwrangle)
set _obj_work_remove_by_dot = `run("opadd -e -n -v attribwrangle remove_by_dot")`
oplocate -x `$arg2 + -7.1245632342602443` -y `$arg3 + -6.7968790288209204` $_obj_work_remove_by_dot
opparm $_obj_work_remove_by_dot  bindings ( 0 ) groupbindings ( 0 )
opparm $_obj_work_remove_by_dot snippet ( 'float dot = dot(v@N, {0,-1,0});\n\nif (pow( rand(@id*1.33) , 0.5)  > dot ) removepoint(0,@ptnum);' )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_remove_by_dot
opexprlanguage -s hscript $_obj_work_remove_by_dot
opuserdata -n '___Version___' -v '' $_obj_work_remove_by_dot

# Node $_obj_work_remove_random (Sop/attribwrangle)
set _obj_work_remove_random = `run("opadd -e -n -v attribwrangle remove_random")`
oplocate -x `$arg2 + -7.3177999965336173` -y `$arg3 + -7.935245154306755` $_obj_work_remove_random
opspareds '    group {         name    "folder1"         label   "Code"          parm {             name    "group"             baseparm             label   "Group"             export  none             bindselector points "Modify Points"                 "Select the points to affect and press Enter to complete."                 0 1 0xffffffff 0 grouptype 0         }         parm {             name    "grouptype"             baseparm             label   "Group Type"             export  none         }         parm {             name    "class"             baseparm             label   "Run Over"             export  none         }         parm {             name    "vex_numcount"             baseparm             label   "Number Count"             export  none         }         parm {             name    "vex_threadjobsize"             baseparm             label   "Thread Job Size"             export  none         }         parm {             name    "snippet"             baseparm             label   "VEXpression"             export  all         }         parm {             name    "exportlist"             baseparm             label   "Attributes to Create"             export  none         }         parm {             name    "vex_strict"             baseparm             label   "Enforce Prototypes"             export  none         }     }      group {         name    "folder1_1"         label   "Bindings"          parm {             name    "autobind"             baseparm             label   "Autobind by Name"             export  none         }         multiparm {             name    "bindings"             label    "Number of Bindings"             baseparm             default 0             parmtag { "autoscope" "0000000000000000" }             parmtag { "multistartoffset" "1" }              parm {                 name    "bindname#"                 baseparm                 label   "Attribute Name"                 export  none             }             parm {                 name    "bindparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "groupautobind"             baseparm             label   "Autobind Groups by Name"             export  none         }         multiparm {             name    "groupbindings"             label    "Group Bindings"             baseparm             default 0             parmtag { "autoscope" "0000000000000000" }             parmtag { "multistartoffset" "1" }              parm {                 name    "bindgroupname#"                 baseparm                 label   "Group Name"                 export  none             }             parm {                 name    "bindgroupparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "vex_cwdpath"             baseparm             label   "Evaluation Node Path"             export  none         }         parm {             name    "vex_outputmask"             baseparm             label   "Export Parameters"             export  none         }         parm {             name    "vex_updatenmls"             baseparm             label   "Update Normals If Displaced"             export  none         }         parm {             name    "vex_matchattrib"             baseparm             label   "Attribute to Match"             export  none         }         parm {             name    "vex_inplace"             baseparm             label   "Compute Results In Place"             export  none         }         parm {             name    "vex_selectiongroup"             baseparm             label   "Output Selection Group"             export  none         }         parm {             name    "vex_precision"             baseparm             label   "VEX Precision"             export  none         }     }      parm {         name    "seed"         label   "Seed"         type    float         default { "0" }         range   { 0 1 }     }     parm {         name    "amount"         label   "Amount"         type    float         default { "0" }         range   { 0 1 }     } ' $_obj_work_remove_random
opparm $_obj_work_remove_random  bindings ( 0 ) groupbindings ( 0 )
chblockbegin
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_remove_random seed
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F '$F' $_obj_work_remove_random/seed
chblockend
opparm $_obj_work_remove_random snippet ( 'if (rand(@id*1.313+chf(\'seed\')) < chf(\'amount\') || @age> 5 ) removepoint(0,@ptnum);' ) seed ( seed ) amount ( 0.95999999999999996 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_remove_random
opexprlanguage -s hscript $_obj_work_remove_random
opuserdata -n '___Version___' -v '' $_obj_work_remove_random

# Node $_obj_work_popnet_droplet (Sop/dopnet)
set _obj_work_popnet_droplet = `run("opadd -e -n -v dopnet popnet_droplet")`
oplocate -x `$arg2 + -5.8408199999999999` -y `$arg3 + -14.398300000000001` $_obj_work_popnet_droplet
opspareds '    parm {         name    "isplayer"         baseparm         label   "Dopnet is Player"         joinnext         export  none     }     parm {         name    "playfilesname"         baseparm         label   "Playback Simulation"         export  none     }     group {         name    "stdswitcher4"         label   "Object Merge"          multiparm {             name    "numobj"             label    "Number of Objects"             baseparm             default 1              parm {                 name    "enable#"                 baseparm                 label   "Enable"                 export  none             }             parm {                 name    "objname#"                 baseparm                 label   "Object"                 export  none             }             parm {                 name    "dataname#"                 baseparm                 label   "Data"                 export  none             }         }      }      group {         name    "stdswitcher4_1"         label   "Simulation"          parm {             name    "minimumsubsteps"             label   "Min Substeps"             type    integer             default { "1" }             range   { 0 10 }             parmtag { "autoscope" "0000000000000000" }         }         parm {             name    "resimulate"             baseparm             label   "Reset Simulation"             nolabel             export  none         }         parm {             name    "initialstate"             baseparm             label   "Initial State"             export  none         }         parm {             name    "timestep"             baseparm             label   "Timestep"             export  none         }         parm {             name    "substep"             baseparm             label   "Substeps"             export  none         }         parm {             name    "timeoffset"             baseparm             label   "Offset Time"             export  none         }         parm {             name    "startframe"             baseparm             label   "Start Frame"             export  none         }         parm {             name    "timescale"             baseparm             label   "Scale Time"             export  none         }         parm {             name    "maxfeedback"             baseparm             label   "Max Feedback Loops"             export  none         }         parm {             name    "autoresim"             baseparm             label   "Enable Automatic Resimulation"             export  none         }         parm {             name    "datahints"             baseparm             label   "Provide Data Hints"             export  none         }         parm {             name    "interpolate"             baseparm             label   "Interpolate Display Data"             export  none         }     }      group {         name    "stdswitcher4_2"         label   "Cache"          parm {             name    "cacheenabled"             baseparm             label   "Cache Simulation"             export  none         }         parm {             name    "compresssims"             baseparm             label   "Compress .sim Files"             export  none         }         parm {             name    "cachetodisk"             baseparm             label   "Allow Caching To Disk"             export  none         }         parm {             name    "cachetodisknoninteractive"             baseparm             label   "Cache to Disk in Non-Interactive Sessions"             export  none         }         parm {             name    "cachesubsteps"             baseparm             label   "Cache Substep Data"             export  none         }         parm {             name    "cachemaxsize"             baseparm             label   "Cache Memory (MB)"             export  none         }         parm {             name    "timeless"             baseparm             label   "Timeless (No History)"             export  none         }         parm {             name    "explicitcache"             baseparm             label   "Save Checkpoints"             export  none         }         parm {             name    "explicitcachename"             baseparm             label   "Checkpoint File"             export  none         }         parm {             name    "explicitcachensteps"             baseparm             label   "Checkpoint Trail Length"             export  none         }         parm {             name    "explicitcachecheckpointspacing"             baseparm             label   "Checkpoint Interval"             export  none         }     }  ' $_obj_work_popnet_droplet
opparm $_obj_work_popnet_droplet  numobj ( 1 )
chblockbegin
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet_droplet timestep
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("timescale")/(ch("substep")*$FPS)' $_obj_work_popnet_droplet/timestep
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet_droplet timeoffset
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F '(ch("startframe")-1)/$FPS' $_obj_work_popnet_droplet/timeoffset
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet_droplet startframe
chkey -t 41.666666666666664 -v 1001 -m 0 -a 0 -A 0 -T a  -F 'ch("../popnet/startframe")' $_obj_work_popnet_droplet/startframe
chblockend
opparm -V 18.5.532 $_obj_work_popnet_droplet stdswitcher ( 1 1 1 ) substep ( 2 ) startframe ( startframe ) explicitcachename ( '//vdisk/SUM/rnd/wetness/fx/work_msugimura/temp/Sim/checkpoints_20220112154910/local/$OS.$SF.sim' ) objname1 ( pop* ) stdswitcher4 ( 1 1 1 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_popnet_droplet
opexprlanguage -s hscript $_obj_work_popnet_droplet
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_popnet_droplet
opuserdata -n 'base_path_dir' -v '//vdisk/SUM/rnd/wetness/fx/work_msugimura/temp/Sim/checkpoints_20220112154910' $_obj_work_popnet_droplet
opcf $_obj_work_popnet_droplet

# Node $_obj_work_popnet_droplet_popsolver (Dop/popsolver::2.0)
set _obj_work_popnet_droplet_popsolver = `run("opadd -e -n -v popsolver::2.0 popsolver")`
oplocate -x `$arg2 + 0.22115099999999999` -y `$arg3 + 0.034413699999999998` $_obj_work_popnet_droplet_popsolver
chblockbegin
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet_droplet_popsolver minimumsubsteps
chkey -t 41.666666666666664 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../minimumsubsteps")' $_obj_work_popnet_droplet_popsolver/minimumsubsteps
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet_droplet_popsolver substeps
chkey -t 41.666666666666664 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("minimumsubsteps")' $_obj_work_popnet_droplet_popsolver/substeps
chblockend
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_popnet_droplet_popsolver
opexprlanguage -s hscript $_obj_work_popnet_droplet_popsolver
opuserdata -n '___Version___' -v '' $_obj_work_popnet_droplet_popsolver
opuserdata -n '___toolcount___' -v '1' $_obj_work_popnet_droplet_popsolver
opuserdata -n '___toolid___' -v 'dynamics_poplocation' $_obj_work_popnet_droplet_popsolver

# Node $_obj_work_popnet_droplet_source_first_input (Dop/popsource::2.0)
set _obj_work_popnet_droplet_source_first_input = `run("opadd -e -n -v popsource::2.0 source_first_input")`
oplocate -x `$arg2 + 1.12114` -y `$arg3 + 4.8352000000000004` $_obj_work_popnet_droplet_source_first_input
opparm $_obj_work_popnet_droplet_source_first_input emittype ( allpoint ) usecontextgeo ( first )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_popnet_droplet_source_first_input
opexprlanguage -s hscript $_obj_work_popnet_droplet_source_first_input
opuserdata -n '___Version___' -v '' $_obj_work_popnet_droplet_source_first_input
opuserdata -n '___toolcount___' -v '2' $_obj_work_popnet_droplet_source_first_input
opuserdata -n '___toolid___' -v 'dynamics_popsource' $_obj_work_popnet_droplet_source_first_input

# Node $_obj_work_popnet_droplet_popforce1 (Dop/popforce)
set _obj_work_popnet_droplet_popforce1 = `run("opadd -e -n -v popforce popforce1")`
oplocate -x `$arg2 + 1.12114` -y `$arg3 + 2.1122100000000001` $_obj_work_popnet_droplet_popforce1
opparm $_obj_work_popnet_droplet_popforce1 force ( 0 -7 0 ) uselocalforce ( on ) localforceexpression ( 'force *= fit01(@weight, 0.85, 1);\n\n' ) swirlsize ( 0.10000000000000001 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_popnet_droplet_popforce1
opexprlanguage -s hscript $_obj_work_popnet_droplet_popforce1
opuserdata -n '___Version___' -v '' $_obj_work_popnet_droplet_popforce1
opuserdata -n '___toolcount___' -v '2' $_obj_work_popnet_droplet_popforce1
opuserdata -n '___toolid___' -v 'dynamics_popforce' $_obj_work_popnet_droplet_popforce1

# Node $_obj_work_popnet_droplet_groundplane1 (Dop/groundplane)
set _obj_work_popnet_droplet_groundplane1 = `run("opadd -e -n -v groundplane groundplane1")`
oplocate -x `$arg2 + -2.6676199999999999` -y `$arg3 + -1.4009799999999999` $_obj_work_popnet_droplet_groundplane1
opparm $_obj_work_popnet_droplet_groundplane1 std_switcher_0 ( 1 1 ) friction ( 0.59999999999999998 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_popnet_droplet_groundplane1
opexprlanguage -s hscript $_obj_work_popnet_droplet_groundplane1
opuserdata -n '___Version___' -v '' $_obj_work_popnet_droplet_groundplane1
opuserdata -n '___toolcount___' -v '1' $_obj_work_popnet_droplet_groundplane1
opuserdata -n '___toolid___' -v 'dop_groundplane' $_obj_work_popnet_droplet_groundplane1

# Node $_obj_work_popnet_droplet_popfluid1 (Dop/popfluid)
set _obj_work_popnet_droplet_popfluid1 = `run("opadd -e -n -v popfluid popfluid1")`
oplocate -x `$arg2 + 3.03077` -y `$arg3 + 4.8129` $_obj_work_popnet_droplet_popfluid1
opparm $_obj_work_popnet_droplet_popfluid1 particleseparation ( 0.02 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_popnet_droplet_popfluid1
opexprlanguage -s hscript $_obj_work_popnet_droplet_popfluid1
opuserdata -n '___Version___' -v '' $_obj_work_popnet_droplet_popfluid1

# Node $_obj_work_popnet_droplet_set_bounce (Dop/popwrangle)
set _obj_work_popnet_droplet_set_bounce = `run("opadd -e -n -v popwrangle set_bounce")`
oplocate -x `$arg2 + 1.1181399999999999` -y `$arg3 + 1.2355100000000001` $_obj_work_popnet_droplet_set_bounce
opparm $_obj_work_popnet_droplet_set_bounce  bindings ( 0 ) bindfield_num ( 0 ) groupbindings ( 0 )
opparm $_obj_work_popnet_droplet_set_bounce snippet ( '@bounce = fit01(rand(@id*1.12),0,0.1);' )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_popnet_droplet_set_bounce
opexprlanguage -s hscript $_obj_work_popnet_droplet_set_bounce
opuserdata -n '___Version___' -v '' $_obj_work_popnet_droplet_set_bounce
opcf ..

# Node $_obj_work_clean5 (Sop/clean)
set _obj_work_clean5 = `run("opadd -e -n -v clean clean5")`
oplocate -x `$arg2 + -6.6588322684871164` -y `$arg3 + -12.509777433818856` $_obj_work_clean5
opparm $_obj_work_clean5 deldegengeo ( off ) delunusedpts ( off ) dodelattribs ( on ) delattribs ( 'id age life N' ) delnans ( off )
chautoscope $_obj_work_clean5 +delete_small
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_clean5
opexprlanguage -s hscript $_obj_work_clean5
opuserdata -n '___Version___' -v '' $_obj_work_clean5

# Node $_obj_work_pointjitter1 (Sop/pointjitter)
set _obj_work_pointjitter1 = `run("opadd -e -n -v pointjitter pointjitter1")`
oplocate -x `$arg2 + -7.3148` -y `$arg3 + -10.0158` $_obj_work_pointjitter1
opparm $_obj_work_pointjitter1 scale ( 0.001 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_pointjitter1
opexprlanguage -s hscript $_obj_work_pointjitter1
opuserdata -n '___Version___' -v '' $_obj_work_pointjitter1

# Node $_obj_work_pscale_by_weight (Sop/attribwrangle)
set _obj_work_pscale_by_weight = `run("opadd -e -n -v attribwrangle pscale_by_weight")`
oplocate -x `$arg2 + -5.84382` -y `$arg3 + -19.0473` $_obj_work_pscale_by_weight
opspareds '    group {         name    "folder1"         label   "Code"          parm {             name    "group"             baseparm             label   "Group"             export  none             bindselector points "Modify Points"                 "Select the points to affect and press Enter to complete."                 0 1 0xffffffff 0 grouptype 0         }         parm {             name    "grouptype"             baseparm             label   "Group Type"             export  none         }         parm {             name    "class"             baseparm             label   "Run Over"             export  none         }         parm {             name    "vex_numcount"             baseparm             label   "Number Count"             export  none         }         parm {             name    "vex_threadjobsize"             baseparm             label   "Thread Job Size"             export  none         }         parm {             name    "snippet"             baseparm             label   "VEXpression"             export  all         }         parm {             name    "exportlist"             baseparm             label   "Attributes to Create"             export  none         }         parm {             name    "vex_strict"             baseparm             label   "Enforce Prototypes"             export  none         }     }      group {         name    "folder1_1"         label   "Bindings"          parm {             name    "autobind"             baseparm             label   "Autobind by Name"             export  none         }         multiparm {             name    "bindings"             label    "Number of Bindings"             baseparm             default 0             parmtag { "autoscope" "0000000000000000" }             parmtag { "multistartoffset" "1" }              parm {                 name    "bindname#"                 baseparm                 label   "Attribute Name"                 export  none             }             parm {                 name    "bindparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "groupautobind"             baseparm             label   "Autobind Groups by Name"             export  none         }         multiparm {             name    "groupbindings"             label    "Group Bindings"             baseparm             default 0             parmtag { "autoscope" "0000000000000000" }             parmtag { "multistartoffset" "1" }              parm {                 name    "bindgroupname#"                 baseparm                 label   "Group Name"                 export  none             }             parm {                 name    "bindgroupparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "vex_cwdpath"             baseparm             label   "Evaluation Node Path"             export  none         }         parm {             name    "vex_outputmask"             baseparm             label   "Export Parameters"             export  none         }         parm {             name    "vex_updatenmls"             baseparm             label   "Update Normals If Displaced"             export  none         }         parm {             name    "vex_matchattrib"             baseparm             label   "Attribute to Match"             export  none         }         parm {             name    "vex_inplace"             baseparm             label   "Compute Results In Place"             export  none         }         parm {             name    "vex_selectiongroup"             baseparm             label   "Output Selection Group"             export  none         }         parm {             name    "vex_precision"             baseparm             label   "VEX Precision"             export  none         }     }      parm {         name    "pscale"         label   "Pscale"         type    ramp_flt         default { "2" }         range   { 1! 10 }     } ' $_obj_work_pscale_by_weight
opparm $_obj_work_pscale_by_weight  bindings ( 0 ) groupbindings ( 0 ) pscale ( 9 )
opparm $_obj_work_pscale_by_weight snippet ( '@pscale = 0.0025 * @weight* 1;\nif (@weight<0.25) @pscale += rand(@id*1.31) * 0.001;' ) pscale ( 9 ) pscale1value ( 0.98958331346511841 ) pscale3pos ( 0.020618556067347527 ) pscale3value ( 0.59375 ) pscale4pos ( 0.073310427367687225 ) pscale4value ( 0.97916668653488159 ) pscale5pos ( 0.12371134012937546 ) pscale5value ( 1 ) pscale6pos ( 0.21191294491291046 ) pscale6value ( 0.9375 ) pscale7pos ( 0.65406644344329834 ) pscale7value ( 0.1927083283662796 ) pscale8pos ( 0.81099659204483032 ) pscale8value ( 0.046875 ) pscale9pos ( 0.99541807174682617 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_pscale_by_weight
opexprlanguage -s hscript $_obj_work_pscale_by_weight
opuserdata -n '___Version___' -v '' $_obj_work_pscale_by_weight

# Node $_obj_work_set_weight (Sop/attribwrangle)
set _obj_work_set_weight = `run("opadd -e -n -v attribwrangle set_weight")`
oplocate -x `$arg2 + -7.3178000000000001` -y `$arg3 + -11.0991` $_obj_work_set_weight
opparm $_obj_work_set_weight  bindings ( 0 ) groupbindings ( 0 )
opparm $_obj_work_set_weight snippet ( '@weight = fit01(pow(rand(@ptnum*1.33+@Frame) , 2 ) ,0.15,1);\nv@v.y *= fit(@weight,0.15,1,0,0.2);' )
opcolor -c 0.47499999403953552 0.81199997663497925 0.20399999618530273 $_obj_work_set_weight
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F off -c on -e on -b off $_obj_work_set_weight
opexprlanguage -s hscript $_obj_work_set_weight
opuserdata -n '___Version___' -v '' $_obj_work_set_weight

# Node $_obj_work_color5 (Sop/color)
set _obj_work_color5 = `run("opadd -e -n -v color color5")`
oplocate -x `$arg2 + 5.8410099999999998` -y `$arg3 + -17.0839` $_obj_work_color5
opparm $_obj_work_color5  ramp ( 2 )
opparm $_obj_work_color5 color ( 0 0 0 ) ramp2pos ( 1 ) ramp2c ( 1 1 1 )
opcolor -c 0.3059999942779541 0.3059999942779541 0.3059999942779541 $_obj_work_color5
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F off -c on -e on -b off $_obj_work_color5
opexprlanguage -s hscript $_obj_work_color5
opuserdata -n '___Version___' -v '' $_obj_work_color5
opuserdata -n '___toolcount___' -v '2' $_obj_work_color5
opuserdata -n '___toolid___' -v 'sop_color' $_obj_work_color5

# Node $_obj_work_pointvop1 (Sop/attribvop)
set _obj_work_pointvop1 = `run("opadd -e -n -v attribvop pointvop1")`
oplocate -x `$arg2 + 5.49336` -y `$arg3 + -19.603100000000001` $_obj_work_pointvop1
opspareds '    parm {         name    "bindgroup"         baseparm         label   "Group"         export  none         bindselector uvselect "Modify Points"             "Select the points to affect and press Enter to complete."             0 1 0xffffffff 0 bindgrouptype 0     }     parm {         name    "bindgrouptype"         baseparm         label   "Group Type"         export  none     }     parm {         name    "bindclass"         baseparm         label   "Run Over"         export  none     }     parm {         name    "vex_numcount"         baseparm         label   "Number Count"         export  none     }     parm {         name    "vex_threadjobsize"         baseparm         label   "Thread Job Size"         export  none     }     group {         name    "stdswitcher3"         label   "Vex Setup"          parm {             name    "vexsrc"             baseparm             label   "Vex Source"             export  all         }         parm {             name    "shoppath"             baseparm             label   "Shop Path"             export  all         }         parm {             name    "script"             baseparm             label   "Script"             export  all         }         parm {             name    "clear"             baseparm             label   "Re-load VEX Functions"             export  all         }         parm {             name    "vop_compiler"             baseparm             label   "Compiler"             export  none         }         parm {             name    "vop_forcecompile"             baseparm             label   "Force Compile"             export  none         }         parm {             name    "vex_cwdpath"             baseparm             label   "Evaluation Node Path"             export  none         }         parm {             name    "vex_outputmask"             baseparm             label   "Export Parameters"             export  none         }         parm {             name    "vex_multithread"             baseparm             label   "Enable Multithreading"             export  none         }     }      group {         name    "stdswitcher3_1"         label   "Attribute Bindings"          parm {             name    "vex_precision"             baseparm             label   "VEX Precision"             export  none         }         parm {             name    "autobind"             baseparm             label   "Autobind by Name"             export  none         }         multiparm {             name    "bindings"             label    "Number of Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindname#"                 baseparm                 label   "Attribute Name"                 export  none             }             parm {                 name    "bindparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "groupautobind"             baseparm             label   "Autobind Groups by Name"             export  none         }         multiparm {             name    "groupbindings"             label    "Group Bindings"             baseparm             default 0             parmtag { "multistartoffset" "1" }              parm {                 name    "bindgroupname#"                 baseparm                 label   "Group Name"                 export  none             }             parm {                 name    "bindgroupparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "vex_updatenmls"             baseparm             label   "Update Normals If Displaced"             export  none         }         parm {             name    "vex_matchattrib"             baseparm             label   "Attribute to Match"             export  none         }         parm {             name    "vex_inplace"             baseparm             label   "Compute Results In Place"             export  none         }         parm {             name    "vex_selectiongroup"             baseparm             label   "Output Selection Group"             export  none         }     }      parm {         name    "ptnum"         label   "Point Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "vtxnum"         label   "Vertex Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "primnum"         label   "Primitive Number"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "id"         label   "Id"         type    integer         invisible         default { "-1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numpt"         label   "Number of Points"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numvtx"         label   "Number of Vertices"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "numprim"         label   "Number of Prims"         type    integer         invisible         default { "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Time"         label   "Time"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "TimeInc"         label   "Time Inc"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Frame"         label   "Frame"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "life"         label   "Life"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "age"         label   "Age"         type    float         invisible         default { "0" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput2"         label   "Second Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput3"         label   "Third Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput4"         label   "Fourth Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "OpInput1"         label   "First Input"         type    string         invisible         default { "" }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "uv"         label   "UV"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "P"         label   "P"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "v"         label   "Velocity"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "force"         label   "Force"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "Cd"         label   "Cd"         type    float         invisible         size    3         default { "1" "1" "1" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "N"         label   "N"         type    float         invisible         size    3         default { "0" "0" "0" }         range   { 0 10 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     }     parm {         name    "srcmax"         label   "Maximum Value In Source Range"         type    float         default { "1" }         range   { 0 1 }         parmtag { "parmvop" "1" }         parmtag { "shaderparmcontexts" "cvex" }     } ' $_obj_work_pointvop1
opparm $_obj_work_pointvop1  bindings ( 0 ) groupbindings ( 0 )
chblockbegin
chadd -t 39.541666666666664 39.541666666666664 $_obj_work_pointvop1 srcmax
chkey -t 39.541666666666664 -v 1 -m 0 -a 0 -A 0 -T a  -F 'ch("../pscale/pscale_max")' $_obj_work_pointvop1/srcmax
chblockend
opparm -V 18.5.532 $_obj_work_pointvop1 srcmax ( srcmax )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_pointvop1
opexprlanguage -s hscript $_obj_work_pointvop1
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_pointvop1
opcf $_obj_work_pointvop1

# Node $_obj_work_pointvop1_geometryvopglobal1 (Vop/geometryvopglobal::2.0)
set _obj_work_pointvop1_geometryvopglobal1 = `run("opadd -e -n -v geometryvopglobal::2.0 geometryvopglobal1")`
oplocate -x `$arg2 + 0.79467900000000002` -y `$arg3 + 2.5482100000000001` $_obj_work_pointvop1_geometryvopglobal1
opset -d on -r on -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_work_pointvop1_geometryvopglobal1
opexprlanguage -s hscript $_obj_work_pointvop1_geometryvopglobal1
opuserdata -n '___Version___' -v '' $_obj_work_pointvop1_geometryvopglobal1

# Node $_obj_work_pointvop1_geometryvopoutput1 (Vop/geometryvopoutput)
set _obj_work_pointvop1_geometryvopoutput1 = `run("opadd -e -n -v geometryvopoutput geometryvopoutput1")`
oplocate -x `$arg2 + 12.567` -y `$arg3 + 3.47715` $_obj_work_pointvop1_geometryvopoutput1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_work_pointvop1_geometryvopoutput1
opexprlanguage -s hscript $_obj_work_pointvop1_geometryvopoutput1
opuserdata -n '___Version___' -v '' $_obj_work_pointvop1_geometryvopoutput1

# Node $_obj_work_pointvop1_pcopen1 (Vop/pcopen)
set _obj_work_pointvop1_pcopen1 = `run("opadd -e -n -v pcopen pcopen1")`
oplocate -x `$arg2 + 3.53912` -y `$arg3 + 0.76856599999999997` $_obj_work_pointvop1_pcopen1
opparm $_obj_work_pointvop1_pcopen1 radius ( 0.002 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_work_pointvop1_pcopen1
opexprlanguage -s hscript $_obj_work_pointvop1_pcopen1
opuserdata -n '___Version___' -v '' $_obj_work_pointvop1_pcopen1

# Node $_obj_work_pointvop1_Cd (Vop/pcfilter)
set _obj_work_pointvop1_Cd = `run("opadd -e -n -v pcfilter Cd")`
oplocate -x `$arg2 + 5.5384700000000002` -y `$arg3 + 1.59857` $_obj_work_pointvop1_Cd
opparm $_obj_work_pointvop1_Cd channel ( Cd )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_work_pointvop1_Cd
opexprlanguage -s hscript $_obj_work_pointvop1_Cd
opuserdata -n '___Version___' -v '' $_obj_work_pointvop1_Cd

# Node $_obj_work_pointvop1_pscale (Vop/pcfilter)
set _obj_work_pointvop1_pscale = `run("opadd -e -n -v pcfilter pscale")`
oplocate -x `$arg2 + 5.5384700000000002` -y `$arg3 + 0.082820599999999994` $_obj_work_pointvop1_pscale
opparm $_obj_work_pointvop1_pscale signature ( f ) channel ( pscale )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_work_pointvop1_pscale
opexprlanguage -s hscript $_obj_work_pointvop1_pscale
opuserdata -n '___Version___' -v '' $_obj_work_pointvop1_pscale

# Node $_obj_work_pointvop1_fit1 (Vop/fit)
set _obj_work_pointvop1_fit1 = `run("opadd -e -n -v fit fit1")`
oplocate -x `$arg2 + 7.9870200000000002` -y `$arg3 + 0.082820599999999994` $_obj_work_pointvop1_fit1
opparm $_obj_work_pointvop1_fit1 destmin ( 0.10000000000000001 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_work_pointvop1_fit1
opexprlanguage -s hscript $_obj_work_pointvop1_fit1
opuserdata -n '___Version___' -v '' $_obj_work_pointvop1_fit1

# Node $_obj_work_pointvop1_srcmax (Vop/parameter)
set _obj_work_pointvop1_srcmax = `run("opadd -e -n -v parameter srcmax")`
oplocate -x `$arg2 + 5.8458399999999999` -y `$arg3 + 0.482821` $_obj_work_pointvop1_srcmax
opparm -V 18.5.532 $_obj_work_pointvop1_srcmax parmname ( srcmax ) parmlabel ( 'Maximum Value In Source Range' ) floatdef ( 1 ) exportcontext ( cvex )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e off -b off -L off -M off -H on -E off $_obj_work_pointvop1_srcmax
opexprlanguage -s hscript $_obj_work_pointvop1_srcmax
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_pointvop1_srcmax

# Node $_obj_work_pointvop1_multiply1 (Vop/multiply)
set _obj_work_pointvop1_multiply1 = `run("opadd -e -n -v multiply multiply1")`
oplocate -x `$arg2 + 10.3611` -y `$arg3 + 1.74857` $_obj_work_pointvop1_multiply1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off -L off -M off -H on -E off $_obj_work_pointvop1_multiply1
opexprlanguage -s hscript $_obj_work_pointvop1_multiply1
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_pointvop1_multiply1
opcf ..

# Node $_obj_work_attribblur1 (Sop/attribblur)
set _obj_work_attribblur1 = `run("opadd -e -n -v attribblur attribblur1")`
oplocate -x `$arg2 + 5.49681` -y `$arg3 + -20.5504` $_obj_work_attribblur1
opparm -V 1.0 $_obj_work_attribblur1 attributes ( Cd )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_attribblur1
opexprlanguage -s hscript $_obj_work_attribblur1
opuserdata -n '___Version___' -v '1.0' $_obj_work_attribblur1

# Node $_obj_work_attribrandomize1 (Sop/attribrandomize)
set _obj_work_attribrandomize1 = `run("opadd -e -n -v attribrandomize attribrandomize1")`
oplocate -x `$arg2 + -7.64595` -y `$arg3 + -21.4207` $_obj_work_attribrandomize1
opparm $_obj_work_attribrandomize1  ramp ( 3 ) values ( 4 )
opparm $_obj_work_attribrandomize1 name ( orient ) folder0 ( 1 1 ) distribution ( uniformorient ) dimensions ( 4 ) seed ( 2219 ) useseedattrib ( on ) ramp2pos ( 0.5 ) ramp2value ( 0.5 ) ramp3pos ( 1 ) ramp3value ( 1 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_attribrandomize1
opexprlanguage -s hscript $_obj_work_attribrandomize1
opuserdata -n '___Version___' -v '' $_obj_work_attribrandomize1

# Node $_obj_work_attribnoise1 (Sop/attribnoise::2.0)
set _obj_work_attribnoise1 = `run("opadd -e -n -v attribnoise::2.0 attribnoise1")`
oplocate -x `$arg2 + -10.4628` -y `$arg3 + -20.406700000000001` $_obj_work_attribnoise1
opparm $_obj_work_attribnoise1  remapramp ( 2 )
opparm $_obj_work_attribnoise1 attribs ( P ) remapramp2pos ( 1 ) remapramp2value ( 1 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_attribnoise1
opexprlanguage -s hscript $_obj_work_attribnoise1
opuserdata -n '___Version___' -v '' $_obj_work_attribnoise1

# Node $_obj_work_clean6 (Sop/clean)
set _obj_work_clean6 = `run("opadd -e -n -v clean clean6")`
oplocate -x `$arg2 + -1.3201499999999999` -y `$arg3 + -24.650400000000001` $_obj_work_clean6
opparm $_obj_work_clean6 deldegengeo ( off ) delunusedpts ( off ) dodelattribs ( on ) delattribs ( '* ^v ^N' ) dodelgroups ( on ) delnans ( off )
chautoscope $_obj_work_clean6 +delete_small
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_clean6
opexprlanguage -s hscript $_obj_work_clean6
opuserdata -n '___Version___' -v '' $_obj_work_clean6

# Node $_obj_work_pscale2 (Sop/attribwrangle)
set _obj_work_pscale2 = `run("opadd -e -n -v attribwrangle pscale2")`
oplocate -x `$arg2 + -15.341900000000001` -y `$arg3 + -22.146999999999998` $_obj_work_pscale2
opspareds '    group {         name    "folder1"         label   "Code"          parm {             name    "group"             baseparm             label   "Group"             export  none             bindselector points "Modify Points"                 "Select the points to affect and press Enter to complete."                 0 1 0xffffffff 0 grouptype 0         }         parm {             name    "grouptype"             baseparm             label   "Group Type"             export  none         }         parm {             name    "class"             baseparm             label   "Run Over"             export  none         }         parm {             name    "vex_numcount"             baseparm             label   "Number Count"             export  none         }         parm {             name    "vex_threadjobsize"             baseparm             label   "Thread Job Size"             export  none         }         parm {             name    "snippet"             baseparm             label   "VEXpression"             export  all         }         parm {             name    "exportlist"             baseparm             label   "Attributes to Create"             export  none         }         parm {             name    "vex_strict"             baseparm             label   "Enforce Prototypes"             export  none         }     }      group {         name    "folder1_1"         label   "Bindings"          parm {             name    "autobind"             baseparm             label   "Autobind by Name"             export  none         }         multiparm {             name    "bindings"             label    "Number of Bindings"             baseparm             default 0             parmtag { "autoscope" "0000000000000000" }             parmtag { "multistartoffset" "1" }              parm {                 name    "bindname#"                 baseparm                 label   "Attribute Name"                 export  none             }             parm {                 name    "bindparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "groupautobind"             baseparm             label   "Autobind Groups by Name"             export  none         }         multiparm {             name    "groupbindings"             label    "Group Bindings"             baseparm             default 0             parmtag { "autoscope" "0000000000000000" }             parmtag { "multistartoffset" "1" }              parm {                 name    "bindgroupname#"                 baseparm                 label   "Group Name"                 export  none             }             parm {                 name    "bindgroupparm#"                 baseparm                 label   "VEX Parameter"                 export  none             }         }          parm {             name    "vex_cwdpath"             baseparm             label   "Evaluation Node Path"             export  none         }         parm {             name    "vex_outputmask"             baseparm             label   "Export Parameters"             export  none         }         parm {             name    "vex_updatenmls"             baseparm             label   "Update Normals If Displaced"             export  none         }         parm {             name    "vex_matchattrib"             baseparm             label   "Attribute to Match"             export  none         }         parm {             name    "vex_inplace"             baseparm             label   "Compute Results In Place"             export  none         }         parm {             name    "vex_selectiongroup"             baseparm             label   "Output Selection Group"             export  none         }         parm {             name    "vex_precision"             baseparm             label   "VEX Precision"             export  none         }     }      parm {         name    "pscale"         label   "Pscale"         type    ramp_flt         default { "2" }         range   { 1! 10 }     } ' $_obj_work_pscale2
opparm $_obj_work_pscale2  bindings ( 0 ) groupbindings ( 0 ) pscale ( 9 )
opparm $_obj_work_pscale2 snippet ( '@pscale = pow(rand(@ptnum*1.31),2) * 0.004;' ) pscale ( 9 ) pscale1value ( 0.98958331346511841 ) pscale3pos ( 0.020618556067347527 ) pscale3value ( 0.59375 ) pscale4pos ( 0.073310427367687225 ) pscale4value ( 0.97916668653488159 ) pscale5pos ( 0.12371134012937546 ) pscale5value ( 1 ) pscale6pos ( 0.21191294491291046 ) pscale6value ( 0.9375 ) pscale7pos ( 0.65406644344329834 ) pscale7value ( 0.1927083283662796 ) pscale8pos ( 0.81099659204483032 ) pscale8value ( 0.046875 ) pscale9pos ( 0.99541807174682617 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_pscale2
opexprlanguage -s hscript $_obj_work_pscale2
opuserdata -n '___Version___' -v '' $_obj_work_pscale2

# Node $_obj_work_attribrandomize2 (Sop/attribrandomize)
set _obj_work_attribrandomize2 = `run("opadd -e -n -v attribrandomize attribrandomize2")`
oplocate -x `$arg2 + -15.3424` -y `$arg3 + -23.336400000000001` $_obj_work_attribrandomize2
opparm $_obj_work_attribrandomize2  ramp ( 3 ) values ( 4 )
opparm $_obj_work_attribrandomize2 name ( orient ) folder0 ( 1 1 ) distribution ( uniformorient ) dimensions ( 4 ) seed ( 2219 ) ramp2pos ( 0.5 ) ramp2value ( 0.5 ) ramp3pos ( 1 ) ramp3value ( 1 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_attribrandomize2
opexprlanguage -s hscript $_obj_work_attribrandomize2
opuserdata -n '___Version___' -v '' $_obj_work_attribrandomize2

# Node $_obj_work_clean7 (Sop/clean)
set _obj_work_clean7 = `run("opadd -e -n -v clean clean7")`
oplocate -x `$arg2 + -14.3002` -y `$arg3 + -25.192699999999999` $_obj_work_clean7
opparm $_obj_work_clean7 deldegengeo ( off ) delunusedpts ( off ) dodelattribs ( on ) delattribs ( source* ) dodelgroups ( on ) delnans ( off )
chautoscope $_obj_work_clean7 +delete_small
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_clean7
opexprlanguage -s hscript $_obj_work_clean7
opuserdata -n '___Version___' -v '' $_obj_work_clean7
opcf ..
opcf $_obj_work

# Node $_obj_work_file1 (Sop/file)
set _obj_work_file1 = `run("opadd -e -n -v file file1")`
oplocate -x `$arg2 + -4.676615142912512` -y `$arg3 + 10.213255428737536` $_obj_work_file1
chblockbegin
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_file1 index
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F '$FF-ch("f1")' $_obj_work_file1/index
chblockend
opparm -V 18.5.532 $_obj_work_file1 file ( '`chs("/out/tmp_baseMesh/sopoutput")`' ) missingframe ( empty )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_file1
opexprlanguage -s hscript $_obj_work_file1
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_file1
opuserdata -n '___toolcount___' -v '1' $_obj_work_file1
opuserdata -n '___toolid___' -v 'geoRopFIle' $_obj_work_file1

# Node $_obj_work_file2 (Sop/file)
set _obj_work_file2 = `run("opadd -e -n -v file file2")`
oplocate -x `$arg2 + 0.25611767999224822` -y `$arg3 + 10.33874445732004` $_obj_work_file2
chblockbegin
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_file2 index
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F '$FF-ch("f1")' $_obj_work_file2/index
chblockend
opparm -V 18.5.532 $_obj_work_file2 file ( '`chs("/out/tmp_animation/sopoutput")`' ) missingframe ( empty )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_file2
opexprlanguage -s hscript $_obj_work_file2
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_file2
opuserdata -n '___toolcount___' -v '2' $_obj_work_file2
opuserdata -n '___toolid___' -v 'geoRopFIle' $_obj_work_file2
# Node $_obj_work_scatter1 (Sop/scatter::2.0)
set _obj_work_scatter1 = `run("opadd -e -n -v scatter::2.0 scatter1")`
oplocate -x `$arg2 + -4.3254303200077517` -y `$arg3 + 5.8442044573200391` $_obj_work_scatter1
chblockbegin
chadd -t 39.541666666666664 43.708333333333336 $_obj_work_scatter1 npts
chkey -t 39.541666666666664 -v 15 -m 0 -a 0.33333333333333331 -A 1.3888888888888904 -T a  -o mM  -F 'bezier()' $_obj_work_scatter1/npts
chkey -t 43.708333333333336 -v 2 -m 0 -a 1.3888888888888904 -A 0.33333333333333331 -T a  -o mM  -F 'bezier()' $_obj_work_scatter1/npts
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_scatter1 seed
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F '$FF' $_obj_work_scatter1/seed
chblockend
opparm -V 18.5.532 $_obj_work_scatter1 usedensityattrib ( on ) densityattrib ( noise ) npts ( npts ) seed ( seed ) relaxpoints ( off ) useprimnumattrib ( on ) useprimuvwattrib ( on )
chautoscope $_obj_work_scatter1 +npts
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_scatter1
opexprlanguage -s hscript $_obj_work_scatter1
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_scatter1

# Node $_obj_work_attribinterpolate1 (Sop/attribinterpolate)
set _obj_work_attribinterpolate1 = `run("opadd -e -n -v attribinterpolate attribinterpolate1")`
oplocate -x `$arg2 + -2.6516803200077517` -y `$arg3 + 4.8053944573200393` $_obj_work_attribinterpolate1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_attribinterpolate1
opexprlanguage -s hscript $_obj_work_attribinterpolate1
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_attribinterpolate1
opcf $_obj_work_popnet

# Node $_obj_work_popnet_output (Dop/output)
set _obj_work_popnet_output = `run("opadd -e -n -v output output")`
oplocate -x `$arg2 + 0.0035220300000000002` -y `$arg3 + -2.4269799999999999` $_obj_work_popnet_output
chblockbegin
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet_output f1
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F '$FSTART' $_obj_work_popnet_output/f1
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet_output f2
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F '$FEND' $_obj_work_popnet_output/f2
chblockend
opparm $_obj_work_popnet_output
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_popnet_output
opexprlanguage -s hscript $_obj_work_popnet_output
opuserdata -n '___Version___' -v '' $_obj_work_popnet_output

# Node $_obj_work_popnet_popobject (Dop/popobject)
set _obj_work_popnet_popobject = `run("opadd -e -n -v popobject popobject")`
oplocate -x `$arg2 + -1.48254` -y `$arg3 + 2.64255` $_obj_work_popnet_popobject
chblockbegin
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet_popobject createframe
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch(opcreator(".")+"/startframe")' $_obj_work_popnet_popobject/createframe
chblockend
opparm $_obj_work_popnet_popobject friction ( 1 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_popnet_popobject
opexprlanguage -s hscript $_obj_work_popnet_popobject
opuserdata -n '___Version___' -v '' $_obj_work_popnet_popobject
opuserdata -n '___toolcount___' -v '2' $_obj_work_popnet_popobject
opuserdata -n '___toolid___' -v 'dynamics_poplocation' $_obj_work_popnet_popobject

# Node $_obj_work_popnet_wire_pops_into_here (Dop/merge)
set _obj_work_popnet_wire_pops_into_here = `run("opadd -e -n -v merge wire_pops_into_here")`
oplocate -x `$arg2 + 3.8472499999999998` -y `$arg3 + 4.2613399999999997` $_obj_work_popnet_wire_pops_into_here
chblockbegin
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet_wire_pops_into_here activation
chkey -t 41.666666666666664 -v 1 -m 0 -a 0 -A 0 -T a  -F 'constant()' $_obj_work_popnet_wire_pops_into_here/activation
chblockend
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_popnet_wire_pops_into_here
opexprlanguage -s hscript $_obj_work_popnet_wire_pops_into_here
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_popnet_wire_pops_into_here

# Node $_obj_work_popnet_staticobject1 (Dop/staticobject)
set _obj_work_popnet_staticobject1 = `run("opadd -e -n -v staticobject staticobject1")`
oplocate -x `$arg2 + -2.3125` -y `$arg3 + 0.65727100000000005` $_obj_work_popnet_staticobject1
chblockbegin
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet_staticobject1 createframe
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch(opcreator(".")+"/startframe")' $_obj_work_popnet_staticobject1/createframe
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet_staticobject1 bullet_shrink_amount
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("bullet_collision_margin")' $_obj_work_popnet_staticobject1/bullet_shrink_amount
chblockend
opparm -V 4 $_obj_work_popnet_staticobject1 soppath ( '`opinputpath(\'..\',2)' ) animategeo ( on ) rbd_solver ( 1 1 1 ) collisiondetection ( volume ) proxyvolume ( '`opinputpath(\'..\',3)' )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b on $_obj_work_popnet_staticobject1
opexprlanguage -s hscript $_obj_work_popnet_staticobject1
opuserdata -n '___Version___' -v '4' $_obj_work_popnet_staticobject1
opuserdata -n '___toolcount___' -v '16' $_obj_work_popnet_staticobject1
opuserdata -n '___toolid___' -v 'dop_staticobject' $_obj_work_popnet_staticobject1

# Node $_obj_work_popnet_merge1 (Dop/merge)
set _obj_work_popnet_merge1 = `run("opadd -e -n -v merge merge1")`
oplocate -x `$arg2 + -0.124265` -y `$arg3 + -1.3993800000000001` $_obj_work_popnet_merge1
chblockbegin
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet_merge1 activation
chkey -t 41.666666666666664 -v 1 -m 0 -a 0 -A 0 -T a  -F 'constant()' $_obj_work_popnet_merge1/activation
chblockend
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_popnet_merge1
opexprlanguage -s hscript $_obj_work_popnet_merge1
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_popnet_merge1
opcf $_obj_work_popnet_get_v_N
oporder -e geometryvopglobal1 geometryvopoutput1 pcopen1 pcfilter1 pcfilter2 
opcf ..
oporder -e output popsolver popobject wire_pops_into_here source_first_input staticobject1 merge1 popforce1 minpos SDF get_v_N 
opcf ..

# Node $_obj_work_vdb (Sop/null)
set _obj_work_vdb = `run("opadd -e -n -v null vdb")`
oplocate -x `$arg2 + 3.4376562491696561` -y `$arg3 + 5.8561405625346552` $_obj_work_vdb
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_vdb
opexprlanguage -s hscript $_obj_work_vdb
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_vdb

# Node $_obj_work_trail1 (Sop/trail)
set _obj_work_trail1 = `run("opadd -e -n -v trail trail1")`
oplocate -x `$arg2 + -0.30372132000775176` -y `$arg3 + 4.631388457320039` $_obj_work_trail1
opparm -V 18.5.532 $_obj_work_trail1 result ( velocity ) inc ( 0.5 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_trail1
opexprlanguage -s hscript $_obj_work_trail1
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_trail1
opcf $_obj_work_popnet_trail

# Node $_obj_work_popnet_trail_output (Dop/output)
set _obj_work_popnet_trail_output = `run("opadd -e -n -v output output")`
oplocate -x `$arg2 + 0.0035220300000000002` -y `$arg3 + -2.4269799999999999` $_obj_work_popnet_trail_output
chblockbegin
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet_trail_output f1
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F '$FSTART' $_obj_work_popnet_trail_output/f1
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet_trail_output f2
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F '$FEND' $_obj_work_popnet_trail_output/f2
chblockend
opparm $_obj_work_popnet_trail_output
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_popnet_trail_output
opexprlanguage -s hscript $_obj_work_popnet_trail_output
opuserdata -n '___Version___' -v '' $_obj_work_popnet_trail_output

# Node $_obj_work_popnet_trail_popobject (Dop/popobject)
set _obj_work_popnet_trail_popobject = `run("opadd -e -n -v popobject popobject")`
oplocate -x `$arg2 + -1.48254` -y `$arg3 + 2.64255` $_obj_work_popnet_trail_popobject
chblockbegin
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet_trail_popobject createframe
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch(opcreator(".")+"/startframe")' $_obj_work_popnet_trail_popobject/createframe
chblockend
opparm $_obj_work_popnet_trail_popobject friction ( 1 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_popnet_trail_popobject
opexprlanguage -s hscript $_obj_work_popnet_trail_popobject
opuserdata -n '___Version___' -v '' $_obj_work_popnet_trail_popobject
opuserdata -n '___toolcount___' -v '2' $_obj_work_popnet_trail_popobject
opuserdata -n '___toolid___' -v 'dynamics_poplocation' $_obj_work_popnet_trail_popobject

# Node $_obj_work_popnet_trail_staticobject1 (Dop/staticobject)
set _obj_work_popnet_trail_staticobject1 = `run("opadd -e -n -v staticobject staticobject1")`
oplocate -x `$arg2 + -2.3125` -y `$arg3 + 0.65727100000000005` $_obj_work_popnet_trail_staticobject1
chblockbegin
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet_trail_staticobject1 createframe
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch(opcreator(".")+"/startframe")' $_obj_work_popnet_trail_staticobject1/createframe
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet_trail_staticobject1 bullet_shrink_amount
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("bullet_collision_margin")' $_obj_work_popnet_trail_staticobject1/bullet_shrink_amount
chblockend
opparm -V 4 $_obj_work_popnet_trail_staticobject1 soppath ( '`opinputpath(\'..\',2)' ) animategeo ( on ) rbd_solver ( 1 1 1 ) collisiondetection ( volume ) proxyvolume ( '`opinputpath(\'..\',3)' )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b on $_obj_work_popnet_trail_staticobject1
opexprlanguage -s hscript $_obj_work_popnet_trail_staticobject1
opuserdata -n '___Version___' -v '4' $_obj_work_popnet_trail_staticobject1
opuserdata -n '___toolcount___' -v '16' $_obj_work_popnet_trail_staticobject1
opuserdata -n '___toolid___' -v 'dop_staticobject' $_obj_work_popnet_trail_staticobject1

# Node $_obj_work_popnet_trail_merge1 (Dop/merge)
set _obj_work_popnet_trail_merge1 = `run("opadd -e -n -v merge merge1")`
oplocate -x `$arg2 + -0.124265` -y `$arg3 + -1.3993800000000001` $_obj_work_popnet_trail_merge1
chblockbegin
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet_trail_merge1 activation
chkey -t 41.666666666666664 -v 1 -m 0 -a 0 -A 0 -T a  -F 'constant()' $_obj_work_popnet_trail_merge1/activation
chblockend
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_popnet_trail_merge1
opexprlanguage -s hscript $_obj_work_popnet_trail_merge1
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_popnet_trail_merge1
opcf $_obj_work_popnet_trail_popvop1
oporder -e geometryvopglobal1 geometryvopoutput1 primuv1 bind1 bind2 
opcf ..
oporder -e output popsolver popobject source_first_input staticobject1 merge1 popvop1 
opcf ..

# Node $_obj_work_ray1 (Sop/ray)
set _obj_work_ray1 = `run("opadd -e -n -v ray ray1")`
oplocate -x `$arg2 + -0.72531199999999996` -y `$arg3 + -8.9419500000000003` $_obj_work_ray1
chblockbegin
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_ray1 dirx
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F @N.x $_obj_work_ray1/dirx
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_ray1 diry
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F @N.y $_obj_work_ray1/diry
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_ray1 dirz
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F @N.z $_obj_work_ray1/dirz
chblockend
opparm -V 18.5.532 $_obj_work_ray1 method ( minimum ) useprimnumattrib ( on ) useprimuvwattrib ( on )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_ray1
opexprlanguage -s hscript $_obj_work_ray1
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_ray1

# Node $_obj_work_pid (Sop/attribute)
set _obj_work_pid = `run("opadd -e -n -v attribute pid")`
oplocate -x `$arg2 + -1.3896500000000001` -y `$arg3 + -8.0896699999999999` $_obj_work_pid
opparm $_obj_work_pid  ptrenames ( 5 ) vtxrenames ( 5 ) primrenames ( 5 ) detailrenames ( 5 ) rmanconversions ( 5 )
opparm -V 18.5.532 $_obj_work_pid frompt0 ( id ) topt0 ( pid )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_pid
opexprlanguage -s hscript $_obj_work_pid
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_pid

# Node $_obj_work_add2 (Sop/add)
set _obj_work_add2 = `run("opadd -e -n -v add add2")`
oplocate -x `$arg2 + -0.037925300000000002` -y `$arg3 + -14.7212` $_obj_work_add2
opparm $_obj_work_add2  points ( 1 ) prims ( 1 )
opparm -V 18.5.532 $_obj_work_add2 stdswitcher ( 1 1 1 ) switcher ( 1 1 ) add ( attribute ) attrname ( pid )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_add2
opexprlanguage -s hscript $_obj_work_add2
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_add2

# Node $_obj_work_resample1 (Sop/resample)
set _obj_work_resample1 = `run("opadd -e -n -v resample resample1")`
oplocate -x `$arg2 + -0.037925300000000002` -y `$arg3 + -15.4712` $_obj_work_resample1
opparm -V 18.5.532 $_obj_work_resample1 edge ( on ) length ( 0.002 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_resample1
opexprlanguage -s hscript $_obj_work_resample1
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_resample1

# Node $_obj_work_ray2 (Sop/ray)
set _obj_work_ray2 = `run("opadd -e -n -v ray ray2")`
oplocate -x `$arg2 + 1.7739799999999999` -y `$arg3 + -16.321200000000001` $_obj_work_ray2
chblockbegin
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_ray2 dirx
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F @N.x $_obj_work_ray2/dirx
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_ray2 diry
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F @N.y $_obj_work_ray2/diry
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_ray2 dirz
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F @N.z $_obj_work_ray2/dirz
chblockend
opparm -V 18.5.532 $_obj_work_ray2 method ( minimum ) useprimnumattrib ( on ) useprimuvwattrib ( on )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_ray2
opexprlanguage -s hscript $_obj_work_ray2
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_ray2

# Node $_obj_work_add3 (Sop/add)
set _obj_work_add3 = `run("opadd -e -n -v add add3")`
oplocate -x `$arg2 + 0.59681200000000001` -y `$arg3 + -18.221900000000002` $_obj_work_add3
opparm $_obj_work_add3  points ( 1 ) prims ( 1 )
opparm -V 18.5.532 $_obj_work_add3 keep ( on )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_add3
opexprlanguage -s hscript $_obj_work_add3
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_add3

# Node $_obj_work_OUT_BaseSim (Sop/null)
set _obj_work_OUT_BaseSim = `run("opadd -e -n -v null OUT_BaseSim")`
oplocate -x `$arg2 + -3.5815000000000001` -y `$arg3 + -5.42685` $_obj_work_OUT_BaseSim
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_OUT_BaseSim
opexprlanguage -s hscript $_obj_work_OUT_BaseSim
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_OUT_BaseSim

# Node $_obj_work_file3 (Sop/file)
set _obj_work_file3 = `run("opadd -e -n -v file file3")`
oplocate -x `$arg2 + -3.5815000000000001` -y `$arg3 + -6.6095499999999996` $_obj_work_file3
chblockbegin
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_file3 index
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F '$FF-ch("f1")' $_obj_work_file3/index
chblockend
opparm -V 18.5.532 $_obj_work_file3 file ( '`chs("/out/tmp_BaseSim/sopoutput")`' ) missingframe ( empty )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_file3
opexprlanguage -s hscript $_obj_work_file3
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_file3
opuserdata -n '___toolcount___' -v '5' $_obj_work_file3
opuserdata -n '___toolid___' -v 'geoRopFIle' $_obj_work_file3

# Node $_obj_work_normal2 (Sop/normal)
set _obj_work_normal2 = `run("opadd -e -n -v normal normal2")`
oplocate -x `$arg2 + -0.30372132000775176` -y `$arg3 + 5.6187744573200398` $_obj_work_normal2
opparm -V 18.5.532 $_obj_work_normal2 type ( typepoint )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_normal2
opexprlanguage -s hscript $_obj_work_normal2
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_normal2
opcf $_obj_work_popnet_droplet

# Node $_obj_work_popnet_droplet_output (Dop/output)
set _obj_work_popnet_droplet_output = `run("opadd -e -n -v output output")`
oplocate -x `$arg2 + -0.123115` -y `$arg3 + -4.0783100000000001` $_obj_work_popnet_droplet_output
chblockbegin
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet_droplet_output f1
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F '$FSTART' $_obj_work_popnet_droplet_output/f1
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet_droplet_output f2
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F '$FEND' $_obj_work_popnet_droplet_output/f2
chblockend
opparm $_obj_work_popnet_droplet_output
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_popnet_droplet_output
opexprlanguage -s hscript $_obj_work_popnet_droplet_output
opuserdata -n '___Version___' -v '' $_obj_work_popnet_droplet_output

# Node $_obj_work_popnet_droplet_popobject (Dop/popobject)
set _obj_work_popnet_droplet_popobject = `run("opadd -e -n -v popobject popobject")`
oplocate -x `$arg2 + -1.48254` -y `$arg3 + 2.64255` $_obj_work_popnet_droplet_popobject
chblockbegin
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet_droplet_popobject createframe
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch(opcreator(".")+"/startframe")' $_obj_work_popnet_droplet_popobject/createframe
chblockend
opparm $_obj_work_popnet_droplet_popobject folder0 ( 2 2 2 ) bounce ( 0.10000000000000001 ) friction ( 0.29999999999999999 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_popnet_droplet_popobject
opexprlanguage -s hscript $_obj_work_popnet_droplet_popobject
opuserdata -n '___Version___' -v '' $_obj_work_popnet_droplet_popobject
opuserdata -n '___toolcount___' -v '2' $_obj_work_popnet_droplet_popobject
opuserdata -n '___toolid___' -v 'dynamics_poplocation' $_obj_work_popnet_droplet_popobject

# Node $_obj_work_popnet_droplet_wire_pops_into_here (Dop/merge)
set _obj_work_popnet_droplet_wire_pops_into_here = `run("opadd -e -n -v merge wire_pops_into_here")`
oplocate -x `$arg2 + 2.0425800000000001` -y `$arg3 + 3.27556` $_obj_work_popnet_droplet_wire_pops_into_here
chblockbegin
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet_droplet_wire_pops_into_here activation
chkey -t 41.666666666666664 -v 1 -m 0 -a 0 -A 0 -T a  -F 'constant()' $_obj_work_popnet_droplet_wire_pops_into_here/activation
chblockend
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_popnet_droplet_wire_pops_into_here
opexprlanguage -s hscript $_obj_work_popnet_droplet_wire_pops_into_here
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_popnet_droplet_wire_pops_into_here

# Node $_obj_work_popnet_droplet_staticobject1 (Dop/staticobject)
set _obj_work_popnet_droplet_staticobject1 = `run("opadd -e -n -v staticobject staticobject1")`
oplocate -x `$arg2 + -2.6663700000000001` -y `$arg3 + 0.60671799999999998` $_obj_work_popnet_droplet_staticobject1
chblockbegin
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet_droplet_staticobject1 createframe
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch(opcreator(".")+"/startframe")' $_obj_work_popnet_droplet_staticobject1/createframe
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet_droplet_staticobject1 bullet_shrink_amount
chkey -t 41.666666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F 'ch("bullet_collision_margin")' $_obj_work_popnet_droplet_staticobject1/bullet_shrink_amount
chblockend
opparm -V 4 $_obj_work_popnet_droplet_staticobject1 soppath ( '`opinputpath(\'..\',2)' ) animategeo ( on ) std_switcher_0_2_1 ( 1 1 ) bounce ( 0 ) friction ( 0.90000000000000002 ) collisiondetection ( volume ) mode ( volume ) proxyvolume ( '`opinputpath(\'..\',3)' )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_popnet_droplet_staticobject1
opexprlanguage -s hscript $_obj_work_popnet_droplet_staticobject1
opuserdata -n '___Version___' -v '4' $_obj_work_popnet_droplet_staticobject1
opuserdata -n '___toolcount___' -v '16' $_obj_work_popnet_droplet_staticobject1
opuserdata -n '___toolid___' -v 'dop_staticobject' $_obj_work_popnet_droplet_staticobject1

# Node $_obj_work_popnet_droplet_merge1 (Dop/merge)
set _obj_work_popnet_droplet_merge1 = `run("opadd -e -n -v merge merge1")`
oplocate -x `$arg2 + -0.124265` -y `$arg3 + -1.59731` $_obj_work_popnet_droplet_merge1
chblockbegin
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet_droplet_merge1 activation
chkey -t 41.666666666666664 -v 1 -m 0 -a 0 -A 0 -T a  -F 'constant()' $_obj_work_popnet_droplet_merge1/activation
chblockend
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_popnet_droplet_merge1
opexprlanguage -s hscript $_obj_work_popnet_droplet_merge1
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_popnet_droplet_merge1

# Node $_obj_work_popnet_droplet_merge2 (Dop/merge)
set _obj_work_popnet_droplet_merge2 = `run("opadd -e -n -v merge merge2")`
oplocate -x `$arg2 + -0.124265` -y `$arg3 + -2.93005` $_obj_work_popnet_droplet_merge2
chblockbegin
chadd -t 41.666666666666664 41.666666666666664 $_obj_work_popnet_droplet_merge2 activation
chkey -t 41.666666666666664 -v 1 -m 0 -a 0 -A 0 -T a  -F 'constant()' $_obj_work_popnet_droplet_merge2/activation
chblockend
opset -d on -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_popnet_droplet_merge2
opexprlanguage -s hscript $_obj_work_popnet_droplet_merge2
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_popnet_droplet_merge2
oporder -e output popsolver popobject wire_pops_into_here source_first_input staticobject1 merge1 popforce1 groundplane1 merge2 popfluid1 set_bounce 
opcf ..

# Node $_obj_work_copy1 (Sop/copyxform)
set _obj_work_copy1 = `run("opadd -e -n -v copyxform copy1")`
oplocate -x `$arg2 + -7.3148` -y `$arg3 + -9.1227699999999992` $_obj_work_copy1
opparm -V 18.5.532 $_obj_work_copy1 ncy ( 10 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_copy1
opexprlanguage -s hscript $_obj_work_copy1
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_copy1

# Node $_obj_work_copytopoints1 (Sop/copytopoints::2.0)
set _obj_work_copytopoints1 = `run("opadd -e -n -v copytopoints::2.0 copytopoints1")`
oplocate -x `$arg2 + -7.9090600000000002` -y `$arg3 + -23.0916` $_obj_work_copytopoints1
opparm $_obj_work_copytopoints1  targetattribs ( 3 )
opparm -V 18.5.532 $_obj_work_copytopoints1 targetattribs ( 3 ) applyattribs1 ( *,^v,^Alpha,^N,^up,^pscale,^scale,^orient,^rot,^pivot,^trans,^transform ) applymethod2 ( mult ) applyattribs2 ( Alpha ) applymethod3 ( add ) applyattribs3 ( v )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_copytopoints1
opexprlanguage -s hscript $_obj_work_copytopoints1
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_copytopoints1

# Node $_obj_work_sphere2 (Sop/sphere)
set _obj_work_sphere2 = `run("opadd -e -n -v sphere sphere2")`
oplocate -x `$arg2 + -10.4628` -y `$arg3 + -19.527899999999999` $_obj_work_sphere2
opparm -V 18.5.532 $_obj_work_sphere2 type ( poly ) freq ( 1 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_sphere2
opexprlanguage -s hscript $_obj_work_sphere2
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_sphere2

# Node $_obj_work_csSimClean1 (LIB::Sop/csSimClean::004)
set _obj_work_csSimClean1 = `run("opadd -e -n -v LIB::csSimClean::004 csSimClean1")`
oplocate -x `$arg2 + 0.270096` -y `$arg3 + -10.6746` $_obj_work_csSimClean1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_csSimClean1
opexprlanguage -s hscript $_obj_work_csSimClean1
opuserdata -n '___Version___' -v '' $_obj_work_csSimClean1

# Node $_obj_work_OUT_trail (Sop/null)
set _obj_work_OUT_trail = `run("opadd -e -n -v null OUT_trail")`
oplocate -x `$arg2 + -0.037925300000000002` -y `$arg3 + -11.726000000000001` $_obj_work_OUT_trail
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_OUT_trail
opexprlanguage -s hscript $_obj_work_OUT_trail
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_OUT_trail

# Node $_obj_work_file4 (Sop/file)
set _obj_work_file4 = `run("opadd -e -n -v file file4")`
oplocate -x `$arg2 + -0.037925300000000002` -y `$arg3 + -12.726000000000001` $_obj_work_file4
chblockbegin
chadd -t 38.291666666666664 38.291666666666664 $_obj_work_file4 index
chkey -t 38.291666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F '$FF-ch("f1")' $_obj_work_file4/index
chblockend
opparm -V 18.5.532 $_obj_work_file4 file ( '`chs("/out/tmp_trail/sopoutput")`' ) missingframe ( empty )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_file4
opexprlanguage -s hscript $_obj_work_file4
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_file4
opuserdata -n '___toolcount___' -v '9' $_obj_work_file4
opuserdata -n '___toolid___' -v 'geoRopFIle' $_obj_work_file4

# Node $_obj_work_csSimClean2 (LIB::Sop/csSimClean::004)
set _obj_work_csSimClean2 = `run("opadd -e -n -v LIB::csSimClean::004 csSimClean2")`
oplocate -x `$arg2 + -5.8408199999999999` -y `$arg3 + -15.6416` $_obj_work_csSimClean2
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_csSimClean2
opexprlanguage -s hscript $_obj_work_csSimClean2
opuserdata -n '___Version___' -v '' $_obj_work_csSimClean2

# Node $_obj_work_OUT_droplet (Sop/null)
set _obj_work_OUT_droplet = `run("opadd -e -n -v null OUT_droplet")`
oplocate -x `$arg2 + -6.0471700000000004` -y `$arg3 + -16.744299999999999` $_obj_work_OUT_droplet
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_OUT_droplet
opexprlanguage -s hscript $_obj_work_OUT_droplet
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_OUT_droplet

# Node $_obj_work_file5 (Sop/file)
set _obj_work_file5 = `run("opadd -e -n -v file file5")`
oplocate -x `$arg2 + -6.0471700000000004` -y `$arg3 + -17.744299999999999` $_obj_work_file5
chblockbegin
chadd -t 38.291666666666664 38.291666666666664 $_obj_work_file5 index
chkey -t 38.291666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F '$FF-ch("f1")' $_obj_work_file5/index
chblockend
opparm -V 18.5.532 $_obj_work_file5 file ( '`chs("/out/tmp_droplet/sopoutput")`' ) missingframe ( empty )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_file5
opexprlanguage -s hscript $_obj_work_file5
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_file5
opuserdata -n '___toolcount___' -v '11' $_obj_work_file5
opuserdata -n '___toolid___' -v 'geoRopFIle' $_obj_work_file5

# Node $_obj_work_OUT_trail_mesh (Sop/null)
set _obj_work_OUT_trail_mesh = `run("opadd -e -n -v null OUT_trail_mesh")`
oplocate -x `$arg2 + -1.3201499999999999` -y `$arg3 + -20.710599999999999` $_obj_work_OUT_trail_mesh
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_OUT_trail_mesh
opexprlanguage -s hscript $_obj_work_OUT_trail_mesh
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_OUT_trail_mesh

# Node $_obj_work_file6 (Sop/file)
set _obj_work_file6 = `run("opadd -e -n -v file file6")`
oplocate -x `$arg2 + -1.3201499999999999` -y `$arg3 + -21.710599999999999` $_obj_work_file6
chblockbegin
chadd -t 38.291666666666664 38.291666666666664 $_obj_work_file6 index
chkey -t 38.291666666666664 -v 0 -m 0 -a 0 -A 0 -T a  -F '$FF-ch("f1")' $_obj_work_file6/index
chblockend
opparm -V 18.5.532 $_obj_work_file6 file ( '`chs("/out/tmp_trail_mesh/sopoutput")`' ) missingframe ( empty )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_file6
opexprlanguage -s hscript $_obj_work_file6
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_file6
opuserdata -n '___toolcount___' -v '13' $_obj_work_file6
opuserdata -n '___toolid___' -v 'geoRopFIle' $_obj_work_file6

# Node $_obj_work_convert1 (Sop/convert)
set _obj_work_convert1 = `run("opadd -e -n -v convert convert1")`
oplocate -x `$arg2 + -1.3213999999999999` -y `$arg3 + -22.647300000000001` $_obj_work_convert1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_convert1
opexprlanguage -s hscript $_obj_work_convert1
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_convert1

# Node $_obj_work_subdivide3 (Sop/subdivide)
set _obj_work_subdivide3 = `run("opadd -e -n -v subdivide subdivide3")`
oplocate -x `$arg2 + 5.8410099999999998` -y `$arg3 + -15.8721` $_obj_work_subdivide3
opparm -V 18.5.532 $_obj_work_subdivide3 iterations ( 2 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_subdivide3
opexprlanguage -s hscript $_obj_work_subdivide3
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_subdivide3
opcf $_obj_work_pointvop1
oporder -e geometryvopglobal1 geometryvopoutput1 pcopen1 Cd pscale fit1 srcmax multiply1 
opcf ..

# Node $_obj_work_OUT_wetmask (Sop/null)
set _obj_work_OUT_wetmask = `run("opadd -e -n -v null OUT_wetmask")`
oplocate -x `$arg2 + 5.6564699999999997` -y `$arg3 + -26.614899999999999` $_obj_work_OUT_wetmask
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_OUT_wetmask
opexprlanguage -s hscript $_obj_work_OUT_wetmask
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_OUT_wetmask

# Node $_obj_work_MayaScale1 (Sop/xform)
set _obj_work_MayaScale1 = `run("opadd -e -n -v xform MayaScale1")`
oplocate -x `$arg2 + 5.6564699999999997` -y `$arg3 + -25.291699999999999` $_obj_work_MayaScale1
opparm -V 18.5.532 $_obj_work_MayaScale1 scale ( 10 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_MayaScale1
opexprlanguage -s hscript $_obj_work_MayaScale1
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_MayaScale1

# Node $_obj_work_attribute1 (Sop/attribute)
set _obj_work_attribute1 = `run("opadd -e -n -v attribute attribute1")`
oplocate -x `$arg2 + 5.6530199999999997` -y `$arg3 + -23.380700000000001` $_obj_work_attribute1
opparm $_obj_work_attribute1  ptrenames ( 5 ) vtxrenames ( 5 ) primrenames ( 5 ) detailrenames ( 5 ) rmanconversions ( 5 )
opparm -V 18.5.532 $_obj_work_attribute1 frompt0 ( Cd ) topt0 ( cs_Cd )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_attribute1
opexprlanguage -s hscript $_obj_work_attribute1
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_attribute1

# Node $_obj_work_matchsize1 (Sop/matchsize)
set _obj_work_matchsize1 = `run("opadd -e -n -v matchsize matchsize1")`
oplocate -x `$arg2 + -10.4628` -y `$arg3 + -21.4207` $_obj_work_matchsize1
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_matchsize1
opexprlanguage -s hscript $_obj_work_matchsize1
opuserdata -n '___Version___' -v '' $_obj_work_matchsize1

# Node $_obj_work_normal3 (Sop/normal)
set _obj_work_normal3 = `run("opadd -e -n -v normal normal3")`
oplocate -x `$arg2 + -10.4628` -y `$arg3 + -22.146000000000001` $_obj_work_normal3
opparm -V 18.5.532 $_obj_work_normal3 cuspangle ( 180 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_normal3
opexprlanguage -s hscript $_obj_work_normal3
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_normal3

# Node $_obj_work_normal4 (Sop/normal)
set _obj_work_normal4 = `run("opadd -e -n -v normal normal4")`
oplocate -x `$arg2 + -1.3201499999999999` -y `$arg3 + -23.650400000000001` $_obj_work_normal4
opparm -V 18.5.532 $_obj_work_normal4 cuspangle ( 180 )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_normal4
opexprlanguage -s hscript $_obj_work_normal4
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_normal4

# Node $_obj_work_scatter3 (Sop/scatter::2.0)
set _obj_work_scatter3 = `run("opadd -e -n -v scatter::2.0 scatter3")`
oplocate -x `$arg2 + -15.338900000000001` -y `$arg3 + -21.000800000000002` $_obj_work_scatter3
opparm -V 18.5.532 $_obj_work_scatter3 npts ( 100000 ) relaxpoints ( off ) useprimnumattrib ( on ) useprimuvwattrib ( on )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_scatter3
opexprlanguage -s hscript $_obj_work_scatter3
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_scatter3

# Node $_obj_work_attribinterpolate2 (Sop/attribinterpolate)
set _obj_work_attribinterpolate2 = `run("opadd -e -n -v attribinterpolate attribinterpolate2")`
oplocate -x `$arg2 + -13.737299999999999` -y `$arg3 + -24.169499999999999` $_obj_work_attribinterpolate2
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_attribinterpolate2
opexprlanguage -s hscript $_obj_work_attribinterpolate2
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_attribinterpolate2

# Node $_obj_work_copytopoints2 (Sop/copytopoints::2.0)
set _obj_work_copytopoints2 = `run("opadd -e -n -v copytopoints::2.0 copytopoints2")`
oplocate -x `$arg2 + -13.7339` -y `$arg3 + -26.711600000000001` $_obj_work_copytopoints2
opparm $_obj_work_copytopoints2  targetattribs ( 4 )
opparm -V 18.5.532 $_obj_work_copytopoints2 targetattribs ( 4 ) applyattribs1 ( '*,^uv, ^v,^Alpha,^N,^up,^pscale,^scale,^orient,^rot,^pivot,^trans,^transform' ) applymethod2 ( mult ) applyattribs2 ( Alpha ) applymethod3 ( add ) applyattribs3 ( v ) applyto4 ( verts ) applyattribs4 ( uv* )
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_copytopoints2
opexprlanguage -s hscript $_obj_work_copytopoints2
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_copytopoints2

# Node $_obj_work_OUT_droplet_fix (Sop/null)
set _obj_work_OUT_droplet_fix = `run("opadd -e -n -v null OUT_droplet_fix")`
oplocate -x `$arg2 + -13.722200000000001` -y `$arg3 + -31.5823` $_obj_work_OUT_droplet_fix
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_OUT_droplet_fix
opexprlanguage -s hscript $_obj_work_OUT_droplet_fix
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_OUT_droplet_fix

# Node $_obj_work_OUT_droplet_trail (Sop/null)
set _obj_work_OUT_droplet_trail = `run("opadd -e -n -v null OUT_droplet_trail")`
oplocate -x `$arg2 + -0.95015684208584639` -y `$arg3 + -30.966989249112451` $_obj_work_OUT_droplet_trail
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_OUT_droplet_trail
opexprlanguage -s hscript $_obj_work_OUT_droplet_trail
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_OUT_droplet_trail

# Node $_obj_work_OUT_droplet_fall (Sop/null)
set _obj_work_OUT_droplet_fall = `run("opadd -e -n -v null OUT_droplet_fall")`
oplocate -x `$arg2 + -7.3148` -y `$arg3 + -31.286820435059241` $_obj_work_OUT_droplet_fall
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_OUT_droplet_fall
opexprlanguage -s hscript $_obj_work_OUT_droplet_fall
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_OUT_droplet_fall

# Node $_obj_work_LOWMesh (Sop/null)
set _obj_work_LOWMesh = `run("opadd -e -n -v null LOWMesh")`
oplocate -x `$arg2 + 3.1674105033169155` -y `$arg3 + 9.9109276969574545` $_obj_work_LOWMesh
opset -d off -r off -h off -f off -y off -t off -l off -s off -u off -F on -c on -e on -b off $_obj_work_LOWMesh
opexprlanguage -s hscript $_obj_work_LOWMesh
opuserdata -n '___Version___' -v '18.5.532' $_obj_work_LOWMesh
oporder -e set_noise file1 file2 deform scatter1 attribinterpolate1 popnet collisionsource1 pscale vdb trail1 popnet_trail clean2 ray1 pid add2 resample1 ray2 particlefluidsurface1 clean3 add3 OUT_BaseSim file3 clean4 remove_by_dot normal2 remove_random popnet_droplet clean5 copy1 pointjitter1 pscale_by_weight copytopoints1 sphere2 set_weight csSimClean1 OUT_trail file4 csSimClean2 OUT_droplet file5 OUT_trail_mesh file6 convert1 subdivide3 color5 pointvop1 attribblur1 OUT_wetmask MayaScale1 attribute1 attribrandomize1 attribnoise1 matchsize1 normal3 clean6 normal4 scatter3 pscale2 attribinterpolate2 attribrandomize2 copytopoints2 OUT_droplet_fix clean7 OUT_droplet_trail OUT_droplet_fall LOWMesh 
opcf ..
opset -p on $_obj_work

opcf $arg1
opcf $_obj_work
opwire -n $_obj_work_file1 -0 $_obj_work_set_noise
opwire -n $_obj_work_file1 -0 $_obj_work_deform
opwire -n $_obj_work_file2 -1 $_obj_work_deform
opwire -n $_obj_work_set_noise -0 $_obj_work_scatter1
opwire -n $_obj_work_scatter1 -0 $_obj_work_attribinterpolate1
opwire -n $_obj_work_deform -1 $_obj_work_attribinterpolate1
opwire -n $_obj_work_attribinterpolate1 -0 $_obj_work_popnet
opwire -n $_obj_work_trail1 -2 $_obj_work_popnet
opcf $_obj_work_popnet
opwire -n $_obj_work_popnet_merge1 -0 $_obj_work_popnet_output
opwire -n $_obj_work_popnet_popobject -0 $_obj_work_popnet_popsolver
opwire -n $_obj_work_popnet_minpos -2 $_obj_work_popnet_popsolver
opwire -n $_obj_work_popnet_source_first_input -0 $_obj_work_popnet_wire_pops_into_here
opwire -n $_obj_work_popnet_staticobject1 -0 $_obj_work_popnet_merge1
opwire -n $_obj_work_popnet_popsolver -1 $_obj_work_popnet_merge1
opwire -n $_obj_work_popnet_source_first_input -0 $_obj_work_popnet_popforce1
opwire -n $_obj_work_popnet_get_v_N -0 $_obj_work_popnet_minpos
opwire -n $_obj_work_popnet_popforce1 -0 $_obj_work_popnet_SDF
opwire -n $_obj_work_popnet_popforce1 -0 $_obj_work_popnet_get_v_N
opcf $_obj_work_popnet_get_v_N
opwire -n $_obj_work_popnet_get_v_N_pcfilter1 -1 $_obj_work_popnet_get_v_N_geometryvopoutput1
opwire -n $_obj_work_popnet_get_v_N_pcfilter2 -4 $_obj_work_popnet_get_v_N_geometryvopoutput1
opwire -n -o 20 $_obj_work_popnet_get_v_N_geometryvopglobal1 -0 $_obj_work_popnet_get_v_N_pcopen1
opwire -n $_obj_work_popnet_get_v_N_geometryvopglobal1 -2 $_obj_work_popnet_get_v_N_pcopen1
opwire -n $_obj_work_popnet_get_v_N_pcopen1 -0 $_obj_work_popnet_get_v_N_pcfilter1
opwire -n $_obj_work_popnet_get_v_N_pcopen1 -0 $_obj_work_popnet_get_v_N_pcfilter2
opcf ..
opcf ..
opwire -n $_obj_work_LOWMesh -0 $_obj_work_collisionsource1
opwire -n $_obj_work_file4 -0 $_obj_work_pscale
opwire -n -o 1 $_obj_work_collisionsource1 -0 $_obj_work_vdb
opwire -n $_obj_work_normal2 -0 $_obj_work_trail1
opwire -n $_obj_work_ray1 -0 $_obj_work_popnet_trail
opwire -n $_obj_work_trail1 -2 $_obj_work_popnet_trail
opcf $_obj_work_popnet_trail
opwire -n $_obj_work_popnet_trail_merge1 -0 $_obj_work_popnet_trail_output
opwire -n $_obj_work_popnet_trail_popobject -0 $_obj_work_popnet_trail_popsolver
opwire -n $_obj_work_popnet_trail_popvop1 -2 $_obj_work_popnet_trail_popsolver
opwire -n $_obj_work_popnet_trail_staticobject1 -0 $_obj_work_popnet_trail_merge1
opwire -n $_obj_work_popnet_trail_popsolver -1 $_obj_work_popnet_trail_merge1
opwire -n $_obj_work_popnet_trail_source_first_input -0 $_obj_work_popnet_trail_popvop1
opcf $_obj_work_popnet_trail_popvop1
opwire -n $_obj_work_popnet_trail_popvop1_primuv1 -0 $_obj_work_popnet_trail_popvop1_geometryvopoutput1
opwire -n -o 20 $_obj_work_popnet_trail_popvop1_geometryvopglobal1 -0 $_obj_work_popnet_trail_popvop1_primuv1
opwire -n $_obj_work_popnet_trail_popvop1_bind1 -2 $_obj_work_popnet_trail_popvop1_primuv1
opwire -n $_obj_work_popnet_trail_popvop1_bind2 -3 $_obj_work_popnet_trail_popvop1_primuv1
opcf ..
opcf ..
opwire -n $_obj_work_file3 -0 $_obj_work_clean2
opwire -n $_obj_work_pid -0 $_obj_work_ray1
opwire -n $_obj_work_trail1 -1 $_obj_work_ray1
opwire -n $_obj_work_clean2 -0 $_obj_work_pid
opwire -n $_obj_work_pscale -0 $_obj_work_add2
opwire -n $_obj_work_add2 -0 $_obj_work_resample1
opwire -n $_obj_work_resample1 -0 $_obj_work_ray2
opwire -n $_obj_work_trail1 -1 $_obj_work_ray2
opwire -n $_obj_work_add3 -0 $_obj_work_particlefluidsurface1
opwire -n $_obj_work_ray2 -0 $_obj_work_clean3
opwire -n $_obj_work_clean3 -0 $_obj_work_add3
opwire -n $_obj_work_clean4 -0 $_obj_work_OUT_BaseSim
opwire -n $_obj_work_OUT_BaseSim -0 $_obj_work_file3
opwire -n $_obj_work_popnet -0 $_obj_work_clean4
opwire -n $_obj_work_file3 -0 $_obj_work_remove_by_dot
opwire -n $_obj_work_deform -0 $_obj_work_normal2
opwire -n $_obj_work_remove_by_dot -0 $_obj_work_remove_random
opwire -n $_obj_work_clean5 -0 $_obj_work_popnet_droplet
opwire -n $_obj_work_trail1 -2 $_obj_work_popnet_droplet
opwire -n $_obj_work_vdb -3 $_obj_work_popnet_droplet
opcf $_obj_work_popnet_droplet
opwire -n $_obj_work_popnet_droplet_merge2 -0 $_obj_work_popnet_droplet_output
opwire -n $_obj_work_popnet_droplet_popobject -0 $_obj_work_popnet_droplet_popsolver
opwire -n $_obj_work_popnet_droplet_set_bounce -2 $_obj_work_popnet_droplet_popsolver
opwire -n $_obj_work_popnet_droplet_source_first_input -0 $_obj_work_popnet_droplet_wire_pops_into_here
opwire -n $_obj_work_popnet_droplet_popfluid1 -1 $_obj_work_popnet_droplet_wire_pops_into_here
opwire -n $_obj_work_popnet_droplet_staticobject1 -0 $_obj_work_popnet_droplet_merge1
opwire -n $_obj_work_popnet_droplet_popsolver -1 $_obj_work_popnet_droplet_merge1
opwire -n $_obj_work_popnet_droplet_source_first_input -0 $_obj_work_popnet_droplet_popforce1
opwire -n $_obj_work_popnet_droplet_groundplane1 -0 $_obj_work_popnet_droplet_merge2
opwire -n $_obj_work_popnet_droplet_merge1 -1 $_obj_work_popnet_droplet_merge2
opwire -n $_obj_work_popnet_droplet_popforce1 -0 $_obj_work_popnet_droplet_set_bounce
opcf ..
opwire -n $_obj_work_set_weight -0 $_obj_work_clean5
opwire -n $_obj_work_remove_random -0 $_obj_work_copy1
opwire -n $_obj_work_copy1 -0 $_obj_work_pointjitter1
opwire -n $_obj_work_file5 -0 $_obj_work_pscale_by_weight
opwire -n $_obj_work_normal3 -0 $_obj_work_copytopoints1
opwire -n $_obj_work_attribrandomize1 -1 $_obj_work_copytopoints1
opwire -n $_obj_work_pointjitter1 -0 $_obj_work_set_weight
opwire -n $_obj_work_popnet_trail -0 $_obj_work_csSimClean1
opwire -n $_obj_work_csSimClean1 -0 $_obj_work_OUT_trail
opwire -n $_obj_work_OUT_trail -0 $_obj_work_file4
opwire -n $_obj_work_popnet_droplet -0 $_obj_work_csSimClean2
opwire -n $_obj_work_csSimClean2 -0 $_obj_work_OUT_droplet
opwire -n $_obj_work_OUT_droplet -0 $_obj_work_file5
opwire -n $_obj_work_particlefluidsurface1 -0 $_obj_work_OUT_trail_mesh
opwire -n $_obj_work_OUT_trail_mesh -0 $_obj_work_file6
opwire -n $_obj_work_file6 -0 $_obj_work_convert1
opwire -n $_obj_work_deform -0 $_obj_work_subdivide3
opwire -n $_obj_work_subdivide3 -0 $_obj_work_color5
opwire -n $_obj_work_color5 -0 $_obj_work_pointvop1
opwire -n $_obj_work_add3 -1 $_obj_work_pointvop1
opcf $_obj_work_pointvop1
opwire -n $_obj_work_pointvop1_multiply1 -3 $_obj_work_pointvop1_geometryvopoutput1
opwire -n -o 19 $_obj_work_pointvop1_geometryvopglobal1 -0 $_obj_work_pointvop1_pcopen1
opwire -n $_obj_work_pointvop1_geometryvopglobal1 -2 $_obj_work_pointvop1_pcopen1
opwire -n $_obj_work_pointvop1_pcopen1 -0 $_obj_work_pointvop1_Cd
opwire -n $_obj_work_pointvop1_pcopen1 -0 $_obj_work_pointvop1_pscale
opwire -n $_obj_work_pointvop1_pscale -0 $_obj_work_pointvop1_fit1
opwire -n $_obj_work_pointvop1_srcmax -2 $_obj_work_pointvop1_fit1
opwire -n $_obj_work_pointvop1_Cd -0 $_obj_work_pointvop1_multiply1
opwire -n $_obj_work_pointvop1_fit1 -1 $_obj_work_pointvop1_multiply1
opcf ..
opwire -n $_obj_work_pointvop1 -0 $_obj_work_attribblur1
opwire -n $_obj_work_MayaScale1 -0 $_obj_work_OUT_wetmask
opwire -n $_obj_work_attribute1 -0 $_obj_work_MayaScale1
opwire -n $_obj_work_attribblur1 -0 $_obj_work_attribute1
opwire -n $_obj_work_pscale_by_weight -0 $_obj_work_attribrandomize1
opwire -n $_obj_work_sphere2 -0 $_obj_work_attribnoise1
opwire -n $_obj_work_attribnoise1 -0 $_obj_work_matchsize1
opwire -n $_obj_work_matchsize1 -0 $_obj_work_normal3
opwire -n $_obj_work_normal4 -0 $_obj_work_clean6
opwire -n $_obj_work_convert1 -0 $_obj_work_normal4
opwire -n $_obj_work_file1 -0 $_obj_work_scatter3
opwire -n $_obj_work_scatter3 -0 $_obj_work_pscale2
opwire -n $_obj_work_attribrandomize2 -0 $_obj_work_attribinterpolate2
opwire -n $_obj_work_deform -1 $_obj_work_attribinterpolate2
opwire -n $_obj_work_pscale2 -0 $_obj_work_attribrandomize2
opwire -n $_obj_work_normal3 -0 $_obj_work_copytopoints2
opwire -n $_obj_work_clean7 -1 $_obj_work_copytopoints2
opwire -n $_obj_work_copytopoints2 -0 $_obj_work_OUT_droplet_fix
opwire -n $_obj_work_attribinterpolate2 -0 $_obj_work_clean7
opwire -n $_obj_work_clean6 -0 $_obj_work_OUT_droplet_trail
opwire -n $_obj_work_copytopoints1 -0 $_obj_work_OUT_droplet_fall
opcf ..

set oidx = 0
if ($argc >= 9 && "$arg9" != "") then
    set oidx = $arg9
endif

if ($argc >= 5 && "$arg4" != "") then
    set output = $_obj_work
    opwire -n $output -$arg5 $arg4
endif
if ($argc >= 6 && "$arg6" != "") then
    set input = $_obj_work
    if ($arg8) then
        opwire -n -i $arg6 -0 $input
    else
        opwire -n -o $oidx $arg6 -0 $input
    endif
endif
opcf $saved_path
'''
hou.hscript(h_preamble + h_extra_args + h_cmd)
