import bpy
from . import fn_align_objects as fn

class ALI_OT_align_3d(bpy.types.Operator):
    """Align selected objects along selected world axis"""
    bl_idname = "alignator.alignator_3d"
    bl_label = "Align selected objects"
    # bl_options = {'REGISTER', 'UNDO'}
    bl_options = {'UNDO'}
    enum_items = (
        ('X_MINIMUM', '', '', '', 0),
        ('X_CENTER', '', '', '', 1),
        ('X_MAXIMUM', '', '', '', 2),
        ('Y_MINIMUM', '', '', '', 3),
        ('Y_CENTER', '', '', '', 4),
        ('Y_MAXIMUM', '', '', '', 5),
        ('Z_MINIMUM', '', '', '', 6),
        ('Z_CENTER', '', '', '', 7),
        ('Z_MAXIMUM', '', '', '', 8),
    )

    option: bpy.props.EnumProperty(items=enum_items) # type: ignore

    @classmethod
    def poll(cls, context):
        if (context.area.ui_type == 'VIEW_3D'):
            return True


    def execute(self, context):
        align_tool = context.scene.align_tool

        align_method = align_tool.align_by
        target_method = align_tool.align_target

        ###############
        if self.option == 'X_MINIMUM':
            fn.align_objects(self, alignment="min",  align_by=align_method, axis="x", align_target=target_method)
        elif self.option == 'X_CENTER':
            fn.align_objects(self, alignment="center",  align_by=align_method, axis="x", align_target=target_method)
        elif self.option == 'X_MAXIMUM':
            fn.align_objects(self, alignment="max",  align_by=align_method, axis="x", align_target=target_method)
        elif self.option == 'Y_MINIMUM':
            fn.align_objects(self, alignment="min",  align_by=align_method, axis="y", align_target=target_method)
        elif self.option == 'Y_CENTER':
            fn.align_objects(self, alignment="center",  align_by=align_method, axis="y", align_target=target_method)
        elif self.option == 'Y_MAXIMUM':
            fn.align_objects(self, alignment="max",  align_by=align_method, axis="y", align_target=target_method)
        elif self.option == 'Z_MINIMUM':
            fn.align_objects(self, alignment="min",  align_by=align_method, axis="z", align_target=target_method)
        elif self.option == 'Z_CENTER':
            fn.align_objects(self, alignment="center",  align_by=align_method, axis="z", align_target=target_method)
        else:
            fn.align_objects(self, alignment="max",  align_by=align_method, axis="z", align_target=target_method)
        
        return{'FINISHED'}



##############################################
# REGISTER/UNREGISTER
##############################################

def register():
    bpy.utils.register_class(ALI_OT_align_3d)

def unregister():
    bpy.utils.unregister_class(ALI_OT_align_3d)