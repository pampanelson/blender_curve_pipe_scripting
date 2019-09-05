import bpy
from bpy import context, data, ops
scene = context.scene

# def create_curve(name,startPointPos,endPointPos,curHeight,curLen,cornerRatio):
def create_curve(name='curpath0'):
    pathName = name
    # startPoint = (0.5,0.5,0.5)
    # add a new path
    bpy.ops.curve.primitive_nurbs_path_add(radius=1, enter_editmode=True, location=(0, 0, 0))
    #  move into a collection with name 
    bpy.ops.object.move_to_collection(collection_index=0, is_new=True, new_collection_name=pathName)
    # subdivide
    bpy.ops.curve.subdivide()

    # check curve control points number == 9
    pts = bpy.data.collections[pathName].objects[0].data.splines[0].points.values()
    if len(pts) == 9:
        # set each control points position with given values
        # default z-axis up 
        for i in range(9):
            pts[i].co.x = 0.5 + i
            pts[i].co.y = 0.5
            pts[i].co.z = 0.5


def donothing():
    # scene.frame_set(scene.frame_end)
    # camera_path.location = (0.0, 0.0, 0.0)
    # camera_path.keyframe_insert(data_path='location')


    return


def create_strip(curname='curpath0',name='strip0',location=(0,0,0),radius=0.1,size=4):
    # default z-axis up 
    rotation = (0,0,0)
    bpy.ops.mesh.primitive_cylinder_add(radius=radius, depth=2, enter_editmode=True, location=location,rotation=rotation)
    # more subdivide make transform along with curve more smooth 
    bpy.ops.mesh.subdivide()
    bpy.ops.mesh.subdivide()
    bpy.ops.mesh.subdivide()
    bpy.ops.mesh.subdivide()
    bpy.ops.mesh.subdivide()
    bpy.ops.object.editmode_toggle()

    bpy.data.objects['Cylinder'].name = name
    bpy.data.collections[curname].objects.link(bpy.data.objects[name])

    bpy.ops.transform.resize(value=(1, 1,size), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)

   
    # add modifier
    bpy.ops.object.modifier_add(type='CURVE')
    bpy.context.object.modifiers["Curve"].object = bpy.data.collections[curname].objects['NurbsPath']

    bpy.context.object.modifiers["Curve"].deform_axis = 'POS_Z'

    # get current cylinder object 
    obj = bpy.data.objects[name]
    # set frame start
    scene.frame_set(0)
    # set location
    obj.location = (0,0,-5)
    obj.keyframe_insert(data_path='location')

    # set frame end
    scene.frame_set(50)
    obj.location = (0,0,5)
    obj.keyframe_insert(data_path='location')





def create_strip_with_curpath(curname='curpath0',stripname='strip0'):
    create_curve(name=curname)
    create_strip(curname=curname,name=stripname)




create_strip_with_curpath()