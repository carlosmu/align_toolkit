import bpy

##############################################
#    USER PREFERENCES 
##############################################

class ALI_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    show_in_3dview_main_menu : bpy.props.BoolProperty(name= "3d View Main Menu", default =True) 
    show_in_3dview_tool_header : bpy.props.BoolProperty(name= "3d View Tool Header", default =False) 

    default_align_by : bpy.props.EnumProperty( 
        name="Align By",
        description="Choose prefered 'align by' method",
        items=[
            ('origin', "Origin", "Align by object origin", 'OBJECT_ORIGIN', 0),
            ('bounding_box', "Bounding Box (Fast)", "Align by bounding boxes of every object. Fast but imprecise", 'MESH_CUBE', 1),
            ('mesh_bounds', "Mesh Bounds (Precise)", "Align by mesh bounds of every object. Precise but slow in high density meshes", 'MESH_MONKEY', 2)
        ],
        default='mesh_bounds'
    ) 

    default_align_target: bpy.props.EnumProperty(
        name="Align Target",
        description="Choose target",
        items=[
            ('selected_objects', "Selected Objects", "Align by selected objects", 'PIVOT_MEDIAN', 0),
            ('active_object', "Active Object", "Align by active object", 'PIVOT_ACTIVE', 1),
            ('3d_cursor', "3D Cursor", "Align by 3D cursor", 'CURSOR', 2)
        ],
        default= 'selected_objects'
    )
        
    ###################
    # UI          
    def draw(self, context):
        layout = self.layout 

        box = layout.box()        
        box.label(text="Show popover panel in:", icon='OPTIONS')
        box.prop(self, "show_in_3dview_main_menu")
        box.prop(self, "show_in_3dview_tool_header")
        box.separator()

        box = layout.box()        
        box.label(text="Default behaviour (will be used after restart blender):", icon='PREFERENCES')
        row = box.row()
        col = row.column(align=True)
        col.label(text="Align/Distribute by:")
        col.prop(self, "default_align_by", text="")
        
        col = row.column(align=True)
        col.label(text="Align target:")
        col.prop(self, "default_align_target", text="")

        box.separator()
        layout.separator()

####################################
# REGISTER/UNREGISTER
####################################
def register():
    bpy.utils.register_class(ALI_Preferences) 
        
def unregister():
    bpy.utils.unregister_class(ALI_Preferences)