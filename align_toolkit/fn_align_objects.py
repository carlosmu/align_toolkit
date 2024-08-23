import bpy
import mathutils

def align_objects(alignment="center", align_by="origin", axis="x", align_target="selected_objects"):
    # Obtener los objetos seleccionados
    selected_objects = bpy.context.selected_objects
    active_object = bpy.context.active_object
    cursor_location = bpy.context.scene.cursor.location
    
    if not selected_objects:
        print("No objects selected")
        return

    # Función para obtener la posición en el eje especificado basado en el origen, bounding box, mesh bounds o cursor 3D
    def get_position(obj, axis):
        if align_by == "origin":
            return getattr(obj.location, axis)
        elif align_by == "bounding_box":
            obj.update_tag()  # Asegurarse de que el bounding box está actualizado
            bounds_world = [obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box]
            axis_idx = "xyz".index(axis)
            min_pos = min([v[axis_idx] for v in bounds_world])
            max_pos = max([v[axis_idx] for v in bounds_world])
            return min_pos if alignment == "min" else max_pos if alignment == "max" else (min_pos + max_pos) / 2
        elif align_by == "mesh_bounds":
            # Crear una copia evaluada del objeto con los modificadores aplicados
            obj_eval = obj.evaluated_get(bpy.context.evaluated_depsgraph_get())
            mesh = obj_eval.to_mesh()
            vertices = [obj_eval.matrix_world @ v.co for v in mesh.vertices]
            axis_idx = "xyz".index(axis)
            min_pos = min([v[axis_idx] for v in vertices])
            max_pos = max([v[axis_idx] for v in vertices])
            # Eliminar la malla temporal para liberar memoria
            obj_eval.to_mesh_clear()
            return min_pos if alignment == "min" else max_pos if alignment == "max" else (min_pos + max_pos) / 2
        else:
            raise ValueError("align_by must be 'origin', 'bounding_box', or 'mesh_bounds'")

    # Alineación para un solo eje
    def align_single_axis(axis):
        if align_target == "3d_cursor":
            target_pos = getattr(cursor_location, axis)
        elif align_target == "active_object" and active_object:
            target_pos = get_position(active_object, axis)
        elif align_target == "selected_objects":
            positions = [get_position(obj, axis) for obj in selected_objects]
            min_pos = min(positions)
            max_pos = max(positions)
            target_pos = min_pos if alignment == "min" else max_pos if alignment == "max" else (min_pos + max_pos) / 2
        else:
            raise ValueError("align_target must be '3d_cursor', 'active_object', or 'selected_objects'")

        for obj in selected_objects:
            if align_by == "origin":
                setattr(obj.location, axis, target_pos)
            elif align_by in {"bounding_box", "mesh_bounds"}:
                obj_center = get_position(obj, axis)
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