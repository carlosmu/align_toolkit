import bpy
from . import ui_icons

# Assign variables to icons
align_center = ui_icons.addon_icons["align_center"].icon_id
align_left = ui_icons.addon_icons["align_left"].icon_id
align_right = ui_icons.addon_icons["align_right"].icon_id

align_center_Z = ui_icons.addon_icons["align_center_Z"].icon_id
align_left_Z = ui_icons.addon_icons["align_left_Z"].icon_id
align_right_Z = ui_icons.addon_icons["align_right_Z"].icon_id

distribute = ui_icons.addon_icons["distribute"].icon_id
distribute_Z = ui_icons.addon_icons["distribute_Z"].icon_id

# Panel class

class ALI_PT_Alignator_3D(bpy.types.Panel):
    bl_label = "Align Toolkit"
    bl_idname = "ALI_PT_Alignator_3D"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Item'
 
    @classmethod
    def poll(cls, context):
        if context.object.type in {'MESH', 'CURVE', 'FONT', 'SURFACE', 'LATTICE'}:
            return True

    def draw(self,context):
        layout = self.layout
        layout.label(text="Align Objects:")
        row = layout.row(align=True)
        row.scale_x = 2.0
        row.operator("alignator.alignator_3d", text="", icon_value=align_left).option = 'X_MINIMUM'
        row.operator("alignator.alignator_3d", text="", icon_value=align_center).option = 'X_CENTER'
        row.operator("alignator.alignator_3d", text="", icon_value=align_right).option = 'X_MAXIMUM'
        row.separator()
        row.label(text="X")
        
        row = layout.row(align=True)
        row.scale_x = 2.0
        row.operator("alignator.alignator_3d", text="", icon_value=align_left).option = 'Y_MINIMUM'
        row.operator("alignator.alignator_3d", text="", icon_value=align_center).option = 'Y_CENTER'
        row.operator("alignator.alignator_3d", text="", icon_value=align_right).option = 'Y_MAXIMUM'
        row.separator()
        row.label(text="Y")

        row = layout.row(align=True)
        row.scale_x = 2.0
        row.operator("alignator.alignator_3d", text="", icon_value=align_left_Z).option = 'Z_MINIMUM'
        row.operator("alignator.alignator_3d", text="", icon_value=align_center_Z).option = 'Z_CENTER'
        row.operator("alignator.alignator_3d", text="", icon_value=align_right_Z).option = 'Z_MAXIMUM'
        row.separator()
        row.label(text="Z")
        
        # layout.separator()
        layout.label(text="Distribute Objects:")
        row = layout.row(align=False)
        row.operator("alignator.distribute_3d", text="X", icon_value=distribute).option = 'X'
        row.operator("alignator.distribute_3d", text="Y", icon_value=distribute).option = 'Y'
        row.operator("alignator.distribute_3d", text="Z", icon_value=distribute_Z).option = 'Z'

# Context menu popover
def popover_contextmenu(self, context):
    # prefs = context.preferences.addons[__package__].preferences
    # if prefs.pb_enable_context_menu:
    layout = self.layout
    layout.popover("ALI_PT_Alignator_3D", text="", icon_value=align_center)
    layout.separator()


##############################################
# REGISTER/UNREGISTER
##############################################
def register():
    bpy.utils.register_class(ALI_PT_Alignator_3D)
    bpy.types.VIEW3D_MT_editor_menus.append(popover_contextmenu)
    
def unregister():
    bpy.utils.unregister_class(ALI_PT_Alignator_3D)
    bpy.types.VIEW3D_MT_editor_menus.remove(popover_contextmenu)