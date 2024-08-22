import bpy
import os
from . import ui_icons

# Función para asignar íconos después de la carga
def assign_icons():
    global align_center, align_left, align_right
    global align_center_Z, align_left_Z, align_right_Z
    global distribute, distribute_Z

    if ui_icons.addon_icons:
        align_center = ui_icons.addon_icons["align_center"].icon_id
        align_left = ui_icons.addon_icons["align_left"].icon_id
        align_right = ui_icons.addon_icons["align_right"].icon_id

        align_center_Z = ui_icons.addon_icons["align_center_Z"].icon_id
        align_left_Z = ui_icons.addon_icons["align_left_Z"].icon_id
        align_right_Z = ui_icons.addon_icons["align_right_Z"].icon_id

        distribute = ui_icons.addon_icons["distribute"].icon_id
        distribute_Z = ui_icons.addon_icons["distribute_Z"].icon_id
    else:
        raise RuntimeError("addon_icons is not initialized")


# Panel class
class ALI_PT_Alignator_3D(bpy.types.Panel):
    bl_label = "Align Toolkit"
    bl_idname = "ALI_PT_Alignator_3D"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Item'
 
    # @classmethod
    # def poll(cls, context):
    #     if context.object.type in {'MESH', 'CURVE', 'FONT', 'SURFACE', 'LATTICE'}:
    #         return True

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
def popover_main_menu(self, context):
    prefs = bpy.context.preferences.addons[__package__].preferences
    if prefs.show_in_3dview_main_menu:
        self.layout.separator()
        if context.area.show_menus:
            self.layout.popover("ALI_PT_Alignator_3D", text="", icon_value=align_center)
        else:
            self.layout.popover("ALI_PT_Alignator_3D", text="Align Toolkit", icon_value=align_center)
        self.layout.separator()

def popover_tool_header(self, context):
    prefs = bpy.context.preferences.addons[__package__].preferences
    if prefs.show_in_3dview_tool_header:
        self.layout.popover("ALI_PT_Alignator_3D", text="", icon_value=align_center)

##############################################
# REGISTER/UNREGISTER
##############################################
def register():
    assign_icons()
    bpy.utils.register_class(ALI_PT_Alignator_3D)
    bpy.types.VIEW3D_MT_editor_menus.append(popover_main_menu)
    bpy.types.VIEW3D_HT_tool_header.append(popover_tool_header)
    
def unregister():
    bpy.utils.unregister_class(ALI_PT_Alignator_3D)
    bpy.types.VIEW3D_MT_editor_menus.remove(popover_main_menu)
    bpy.types.VIEW3D_HT_tool_header.remove(popover_tool_header)