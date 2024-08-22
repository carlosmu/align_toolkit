import bpy.utils.previews
import os

# Addon icons inicialization
addon_icons = None

def load_icons():
    global addon_icons
    if addon_icons is None:
        addon_icons = bpy.utils.previews.new()
        addon_path = os.path.dirname(__file__)
        icons_dir = os.path.join(addon_path, "icons")

        addon_icons.load("align_left", os.path.join(icons_dir, "align_left.svg"), 'IMAGE')
        addon_icons.load("align_center", os.path.join(icons_dir, "align_center.svg"), 'IMAGE')
        addon_icons.load("align_right", os.path.join(icons_dir, "align_right.svg"), 'IMAGE')
        addon_icons.load("align_left_Z", os.path.join(icons_dir, "align_left_Z.svg"), 'IMAGE')
        addon_icons.load("align_center_Z", os.path.join(icons_dir, "align_center_Z.svg"), 'IMAGE')
        addon_icons.load("align_right_Z", os.path.join(icons_dir, "align_right_Z.svg"), 'IMAGE')
        addon_icons.load("distribute", os.path.join(icons_dir, "distribute.svg"), 'IMAGE')
        addon_icons.load("distribute_Z", os.path.join(icons_dir, "distribute_Z.svg"), 'IMAGE')

def unload_icons():
    global addon_icons
    if addon_icons is not None:
        bpy.utils.previews.remove(addon_icons)
        addon_icons = None