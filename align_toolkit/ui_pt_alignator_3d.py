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

class align_properties(bpy.types.PropertyGroup):
    align_by: bpy.props.EnumProperty( 
        name="Align By",
        description="Choose align by method",
        items=[
            ('origin', "Origin", "Align by object origin", 'OBJECT_ORIGIN', 0),
            ('bounding_box', "Bounding Box (Fast)", "Align by bounding boxes of every object. Fast but imprecise", 'MESH_CUBE', 1),
            ('mesh_bounds', "Mesh Bounds (Precise)", "Align by mesh bounds of every object. Precise but slow in high density meshes", 'MESH_MONKEY', 2)
        ],
        default='mesh_bounds'
    ) 
    
    align_target: bpy.props.EnumProperty(
        name="Align Target",
        description="Choose target",
        items=[
            ('selected_objects', "Selected Objects", "Align by selected objects", 'PIVOT_MEDIAN', 0),
            ('active_object', "Active Object", "Align by active object", 'PIVOT_ACTIVE', 1),
            ('3d_cursor', "3D Cursor", "Align by 3D cursor", 'CURSOR', 2)
        ],
        default='selected_objects'
    )


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
        scene = context.scene
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        align_tool = scene.align_tool

        col = layout.column(align=True)
        col.label(text="Align / Distribute by:")
        col.prop(align_tool, "align_by", text="")

        col = layout.column(align=True)
        col.label(text="Align target:")
        col.prop(align_tool, "align_target", text="")

        # col = layout.column(align=True)
        # col.prop(align_tool, "align_by", text="Align/Distribute by")
        # col.prop(align_tool, "align_target", text="Target")
        
        # layout.separator()
        layout.label(text="Align Objects:")
        row = layout.row(align=True)
        row.separator()
        row.label(text="X")
        row.scale_x = 2.0
        row.operator("alignator.alignator_3d", text="", icon_value=align_left).option = 'X_MINIMUM'
        row.operator("alignator.alignator_3d", text="", icon_value=align_center).option = 'X_CENTER'
        row.operator("alignator.alignator_3d", text="", icon_value=align_right).option = 'X_MAXIMUM'
        
        row = layout.row(align=True)
        row.separator()
        row.label(text="Y")
        row.scale_x = 2.0
        row.operator("alignator.alignator_3d", text="", icon_value=align_left).option = 'Y_MINIMUM'
        row.operator("alignator.alignator_3d", text="", icon_value=align_center).option = 'Y_CENTER'
        row.operator("alignator.alignator_3d", text="", icon_value=align_right).option = 'Y_MAXIMUM'

        row = layout.row(align=True)
        row.separator()
        row.label(text="Z")
        row.scale_x = 2.0
        row.operator("alignator.alignator_3d", text="", icon_value=align_left_Z).option = 'Z_MINIMUM'
        row.operator("alignator.alignator_3d", text="", icon_value=align_center_Z).option = 'Z_CENTER'
        row.operator("alignator.alignator_3d", text="", icon_value=align_right_Z).option = 'Z_MAXIMUM'
        
        layout.separator()
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
    # Icons assignation
    assign_icons()
    # Properties
    bpy.utils.register_class(align_properties)
    bpy.types.Scene.align_tool = bpy.props.PointerProperty(type=align_properties)
    # Panel
    bpy.utils.register_class(ALI_PT_Alignator_3D)
    # Popovers
    bpy.types.VIEW3D_MT_editor_menus.append(popover_main_menu)
    bpy.types.VIEW3D_HT_tool_header.append(popover_tool_header)
    
def unregister():
    # Properties
    bpy.utils.unregister_class(align_properties)
    del bpy.types.Scene.align_tool
    # Panel
    bpy.utils.unregister_class(ALI_PT_Alignator_3D)
    # Poppovers
    bpy.types.VIEW3D_MT_editor_menus.remove(popover_main_menu)
    bpy.types.VIEW3D_HT_tool_header.remove(popover_tool_header)