import bpy
from . import fn_distribute_objects as fn
# from mathutils import Vector

class ALI_OT_distribute_3d(bpy.types.Operator):
    """Distribute selected objects along selected world axis"""
    bl_idname = "alignator.distribute_3d"
    bl_label = "Distribute selected objects"
    # bl_options = {'REGISTER', 'UNDO'}
    bl_options = {'UNDO'}
    enum_items = (
        ('X', '', '', '', 0),
        ('Y', '', '', '', 1),
        ('Z', '', '', '', 2),
    )

    option: bpy.props.EnumProperty(items=enum_items) # type: ignore

    @classmethod
    def poll(cls, context):
        if (context.area.ui_type == 'VIEW_3D'):
            return True

    def execute(self, context):
        align_tool = context.scene.align_tool

        align_method = align_tool.align_by
        # target_method = align_tool.align_target


        if self.option == 'X':
            fn.distribute_objects(axis="x", distribute_by=align_method)
        elif self.option == 'Y':
            fn.distribute_objects(axis="y", distribute_by=align_method)
        else:
            fn.distribute_objects(axis="z", distribute_by=align_method)
         
        return{'FINISHED'}

##############################################
# REGISTER/UNREGISTER
##############################################

def register():
    bpy.utils.register_class(ALI_OT_distribute_3d)

def unregister():
    bpy.utils.unregister_class(ALI_OT_distribute_3d)