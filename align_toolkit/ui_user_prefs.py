import bpy

##############################################
#    USER PREFERENCES 
##############################################

class ALI_Preferences(bpy.types.AddonPreferences):
    bl_idname = __package__

    show_in_3dview_main_menu : bpy.props.BoolProperty(name= "3d View Main Menu", default =True) 
    show_in_3dview_tool_header : bpy.props.BoolProperty(name= "3d View Tool Header", default =False) 
        
    ###################
    # UI          
    def draw(self, context):
        layout = self.layout 
        box = layout.box()        
        box.label(text="Show popover panel in:", icon='OPTIONS')
        box.prop(self, "show_in_3dview_main_menu")
        box.prop(self, "show_in_3dview_tool_header")

        box.separator()
        layout.separator()

####################################
# REGISTER/UNREGISTER
####################################
def register():
    bpy.utils.register_class(ALI_Preferences) 
        
def unregister():
    bpy.utils.unregister_class(ALI_Preferences)