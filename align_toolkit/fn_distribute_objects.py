import bpy
import mathutils

def distribute_objects(axis='x', distribute_by='origin', distribute_target='selected_objects'):
    selected_objects = bpy.context.selected_objects
    
    if len(selected_objects) < 3:
        print("At least 3 objects are required for distribution.")
        return

    def calculate_bounds(obj, axis):
        obj.update_tag()
        bounds_world = [obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box]
        min_bound = min(bounds_world, key=lambda v: getattr(v, axis))
        max_bound = max(bounds_world, key=lambda v: getattr(v, axis))
        return getattr(min_bound, axis), getattr(max_bound, axis)

    if distribute_by == 'origin':
        positions = [getattr(obj.location, axis) for obj in selected_objects]
        min_pos = min(positions)
        max_pos = max(positions)
        spacing = (max_pos - min_pos) / (len(selected_objects) - 1)
        
        for i, obj in enumerate(sorted(selected_objects, key=lambda o: getattr(o.location, axis))):
            new_pos = min_pos + i * spacing
            setattr(obj.location, axis, new_pos)
    
    elif distribute_by == 'bounding_box':
        bounds = [calculate_bounds(obj, axis) for obj in selected_objects]
        
        # Sort objects by their minimum bound in the selected axis
        sorted_objects = sorted(zip(selected_objects, bounds), key=lambda item: item[1][0])
        first_obj, first_bounds = sorted_objects[0]
        last_obj, last_bounds = sorted_objects[-1]
        
        # Distance between the bounding box of the first and last object
        total_distance = last_bounds[1] - first_bounds[0]
        
        # Calculate total space for objects (excluding gaps)
        total_object_size = sum(max_bound - min_bound for min_bound, max_bound in bounds)
        
        # Calculate the spacing between objects
        spacing = (total_distance - total_object_size) / (len(selected_objects) - 1)
        
        # Position each intermediate object
        current_position = first_bounds[1]  # Start at the max of the first object
        for obj, (min_bound, max_bound) in sorted_objects[1:-1]:
            current_position += spacing  # Add spacing before placing the object
            obj_offset = current_position - min_bound  # Offset to position the object correctly
            obj.location += mathutils.Vector((obj_offset if axis == 'x' else 0,
                                              obj_offset if axis == 'y' else 0,
                                              obj_offset if axis == 'z' else 0))
            current_position += max_bound - min_bound  # Move to the end of the current object
