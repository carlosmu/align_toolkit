import bpy
import mathutils

def align_objects(alignment="center", align_by="origin", axis="x"):
    # Obtener los objetos seleccionados
    selected_objects = bpy.context.selected_objects
    
    if not selected_objects:
        print("No objects selected")
        return
    
    # Función para obtener la posición en el eje especificado basado en el origen, bounding box o mesh bounds
    def get_position(obj, axis):
        if align_by == "origin":
            return getattr(obj.location, axis)
        elif align_by == "bounding_box":
            obj.update_tag()  # Asegurarse de que el bounding box está actualizado
            bounds_world = [obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box]
            if axis == "x":
                min_pos = min([v.x for v in bounds_world])
                max_pos = max([v.x for v in bounds_world])
            elif axis == "y":
                min_pos = min([v.y for v in bounds_world])
                max_pos = max([v.y for v in bounds_world])
            elif axis == "z":
                min_pos = min([v.z for v in bounds_world])
                max_pos = max([v.z for v in bounds_world])
            return min_pos if alignment == "min" else max_pos if alignment == "max" else (min_pos + max_pos) / 2
        elif align_by == "mesh_bounds":
            mesh = obj.data
            vertices = [obj.matrix_world @ v.co for v in mesh.vertices]
            if axis == "x":
                min_pos = min([v.x for v in vertices])
                max_pos = max([v.x for v in vertices])
            elif axis == "y":
                min_pos = min([v.y for v in vertices])
                max_pos = max([v.y for v in vertices])
            elif axis == "z":
                min_pos = min([v.z for v in vertices])
                max_pos = max([v.z for v in vertices])
            return min_pos if alignment == "min" else max_pos if alignment == "max" else (min_pos + max_pos) / 2
        else:
            raise ValueError("align_by must be 'origin', 'bounding_box', or 'mesh_bounds'")
    
    # Alineación para un solo eje
    def align_single_axis(axis):
        positions = [get_position(obj, axis) for obj in selected_objects]
        min_pos = min(positions)
        max_pos = max(positions)
        
        if alignment == "min":
            target_pos = min_pos
        elif alignment == "max":
            target_pos = max_pos
        elif alignment == "center":
            target_pos = (min_pos + max_pos) / 2
        else:
            raise ValueError("Alignment must be 'min', 'center', or 'max'")
        
        for obj in selected_objects:
            if align_by == "origin":
                setattr(obj.location, axis, target_pos)
            elif align_by in {"bounding_box", "mesh_bounds"}:
                bounds_world = [obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box]
                if align_by == "bounding_box":
                    if axis == "x":
                        min_pos = min([v.x for v in bounds_world])
                        max_pos = max([v.x for v in bounds_world])
                    elif axis == "y":
                        min_pos = min([v.y for v in bounds_world])
                        max_pos = max([v.y for v in bounds_world])
                    elif axis == "z":
                        min_pos = min([v.z for v in bounds_world])
                        max_pos = max([v.z for v in bounds_world])
                elif align_by == "mesh_bounds":
                    vertices = [obj.matrix_world @ v.co for v in obj.data.vertices]
                    if axis == "x":
                        min_pos = min([v.x for v in vertices])
                        max_pos = max([v.x for v in vertices])
                    elif axis == "y":
                        min_pos = min([v.y for v in vertices])
                        max_pos = max([v.y for v in vertices])
                    elif axis == "z":
                        min_pos = min([v.z for v in vertices])
                        max_pos = max([v.z for v in vertices])
                obj_center = (min_pos + max_pos) / 2 if alignment == "center" else min_pos if alignment == "min" else max_pos
                offset = target_pos - obj_center
                setattr(obj.location, axis, getattr(obj.location, axis) + offset)
    
    # Alinear en uno o varios ejes
    if axis in {"x", "y", "z"}:
        align_single_axis(axis)
    elif axis == "xyz":
        for ax in "xyz":
            align_single_axis(ax)
    else:
        raise ValueError("Axis must be 'x', 'y', 'z', or 'xyz'")
