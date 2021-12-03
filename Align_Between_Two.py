import bpy
from bpy.props import StringProperty, BoolProperty, EnumProperty, IntProperty, FloatProperty, FloatVectorProperty, PointerProperty


class Align_Between_Two_Properties(bpy.types.PropertyGroup):
    side_axis : bpy.props.EnumProperty(name='Horizontal', default='Y', description='Horizontal direction to align to other objects',
    items=[
    ('X', 'X', ''),
    ('Y', 'Y', ''),
    ('Z', 'Z', '')])

    up_axis : bpy.props.EnumProperty(name='Vertical', default='Z', description='Vertical direction to align to other objects',
    items=[
    ('X', 'X', ''),
    ('Y', 'Y', ''),
    ('Z', 'Z', '')])


def Align_between_two(self, context):
    scene = context.scene
    rot_vars = scene.align_between_two_vars

    if len(bpy.context.selected_objects) > 3: return
    if bpy.context.view_layer.objects.active in bpy.context.selected_objects:
        objTarget = bpy.context.view_layer.objects.active
        posA, posB = [ob.location for ob in bpy.context.selected_objects if ob != objTarget]
        midPoint = (posA + posB)/2
        objTarget.location = midPoint
        axis = posA - posB
        rotation_mode = objTarget.rotation_mode
        objTarget.rotation_mode = 'QUATERNION'
        if not rot_vars.up_axis == rot_vars.side_axis:
            objTarget.rotation_quaternion = axis.to_track_quat(str(rot_vars.side_axis), str(rot_vars.up_axis))
            objTarget.rotation_mode = rotation_mode
    else:
        return
    

class ALIGN_OT_Align_Active_To_Selected(bpy.types.Operator):
    bl_idname = 'wm.align_ot_align_active_to_selected'
    bl_label = 'Align To Selected'
    bl_description = 'Align rotation of active object to other selected objects.'
    bl_options = {'REGISTER'}
        
    def execute(self, context):
        if bpy.context.selected_objects:
            Align_between_two(self, context)

        return {'FINISHED'}
    

class ALIGN_PT_Align_Panel(bpy.types.Panel):
    bl_idname = 'ALIGN_PT_align_panel'
    bl_category = 'Align Panel'
    bl_label = 'OBJ Align Tools'
    bl_context = "objectmode"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'


    def draw(self, context):
        scene = context.scene
        rot_vars = scene.align_between_two_vars
       
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        # Not enough objects selected
        if len(bpy.context.selected_objects) < 2:
            row = layout.column(align=True)
            row.label(text='No objects selected')
            row.label(text='Select 2 objects')
            row.label(text='then select a 3rd object to align')

        # Active object is outside operator range
        elif len(bpy.context.selected_objects) == 2:
            row = layout.column(align=True)
            row.label(text='Select object to align')

        # Proper amount of objects selected for operator
        elif len(bpy.context.selected_objects) == 3 and bpy.context.view_layer.objects.active in bpy.context.selected_objects:
            row = layout.row(align=True)            
            row.operator('wm.align_ot_align_active_to_selected', icon='OBJECT_ORIGIN')

        # Active object is outside operator range
        elif len(bpy.context.selected_objects) == 3 and not bpy.context.view_layer.objects.active in bpy.context.selected_objects:
            row = layout.column(align=True)
            row.label(text='Active object not selected')
            row.label(text='Select object to align')

        # Too many objects selected
        elif len(bpy.context.selected_objects) > 3:
            row = layout.column(align=True)
            row.label(text='Too many objects selected')
            row.label(text='Select 2 objects')
            row.label(text='then select a 3rd object to align')

        # Axis Selector
        if len(bpy.context.selected_objects) == 3 and bpy.context.view_layer.objects.active in bpy.context.selected_objects:
            col = layout.column(align=True)
            col.prop(rot_vars, 'side_axis')
            col.prop(rot_vars, 'up_axis')

            # Both axis are the same, show warning message
            if rot_vars.up_axis == rot_vars.side_axis:
                row = layout.column(align=True)
                row.label(text='Both axis cant be the same')
        
