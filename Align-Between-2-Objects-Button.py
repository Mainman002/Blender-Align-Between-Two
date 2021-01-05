import bpy
from bpy.props import PointerProperty

bl_info = {
    "name": "Rotate_Between_Two",
    "author": "Ivan Agibalov, Sergey Kritskiy, Andreas Håkansson, Johnathan Mueller",
    "descrtion": "This script allows you to align any object along an axis between the centers of two other objects.",
    "blender": (2, 80, 0),
    "version": (0, 1, 0),
    "location": "View3D (ObjectMode) > Sidebar > Edit Tab",
    "warning": "",
    "category": "Object"
}

def rotate_between_two(self, context):
    if len(bpy.context.selected_objects) != 3: return
    objTarget = bpy.context.view_layer.objects.active
    posA, posB = [ob.location for ob in bpy.context.selected_objects if ob != objTarget]
    midPoint = (posA + posB)/2
    objTarget.location = midPoint
    axis = posA - posB
    rotation_mode = objTarget.rotation_mode
    objTarget.rotation_mode = 'QUATERNION'
    objTarget.rotation_quaternion = axis.to_track_quat('Z','Y')
    objTarget.rotation_mode = rotation_mode
    
#rotate_between_two(self, context)


class ALIGN_OT_Align_Active_To_Selected(bpy.types.Operator):
    bl_idname = 'wm.align_ot_align_active_to_selected'
    bl_label = 'Align To Selected'
    bl_description = 'Align rotation of active object to other selected objects.'
    bl_options = {'REGISTER'}
        
    def execute(self, context):
        
        if bpy.context.selected_objects:
            rotate_between_two(self, context)

        return {'FINISHED'}
    

class ALIGN_PT_Align_Panel(bpy.types.Panel):
    bl_idname = 'ALIGN_PT_align_panel'
    bl_category = 'Align Panel'
    bl_label = 'OBJ Align Tools'
    bl_context = "objectmode"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'


    def draw(self, context):
        myscene = context.scene
        layout = self.layout

        if bpy.context.selected_objects:
            row = layout.row(align=True)            
            row.operator('wm.align_ot_align_active_to_selected', icon='OBJECT_ORIGIN')
        else:
            row = layout.row(align=True)
            row.label(text='No objects selected')
        
        col = layout.column()
        
        

classes = (
    ALIGN_PT_Align_Panel,
    ALIGN_OT_Align_Active_To_Selected,
)



def register():
    for rsclass in classes:
        bpy.utils.register_class(rsclass)


def unregister():
    for rsclass in classes:
        bpy.utils.unregister_class(rsclass)


if __name__ == "__main__":
    register()
