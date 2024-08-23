import bpy
import mathutils

def distribute_objects(axis="x", distribute_by="origin", distribute_target="selected_objects"):
    # Obtener los objetos seleccionados
    selected_objects = bpy.context.selected_objects
    
    if len(selected_objects) < 3:
        print("Need at least 3 objects to distribute")
        return
    
    # Obtener la posición en el eje especificado basado en el origen, bounding box o mesh bounds
    def get_position(obj, axis):
        if distribute_by == "origin":
            return getattr(obj.location, axis)
        elif distribute_by == "bounding_box":
            depsgraph = bpy.context.evaluated_depsgraph_get()
            obj_eval = obj.evaluated_get(depsgraph)
            bounds_world = [obj_eval.matrix_world @ mathutils.Vector(corner) for corner in obj_eval.bound_box]
            return min([getattr(v, axis) for v in bounds_world])
        elif distribute_by == "mesh_bounds":
            depsgraph = bpy.context.evaluated_depsgraph_get()
            obj_eval = obj.evaluated_get(depsgraph)
            mesh = obj_eval.to_mesh()
            vertices = [obj_eval.matrix_world @ v.co for v in mesh.vertices]
            min_pos = min([getattr(v, axis) for v in vertices])
            obj_eval.to_mesh_clear()  # Limpiar los datos de malla evaluados
            return min_pos
        else:
            raise ValueError("distribute_by must be 'origin', 'bounding_box', or 'mesh_bounds'")
    
    # Ordenar los objetos en base a su posición en el eje seleccionado
    selected_objects.sort(key=lambda obj: get_position(obj, axis))
    
    # Obtener las posiciones de los objetos en los extremos
    min_pos = get_position(selected_objects[0], axis)
    max_pos = get_position(selected_objects[-1], axis)
    
    # Calcular la distancia total y el espacio entre objetos
    total_distance = max_pos - min_pos
    gap = total_distance / (len(selected_objects) - 1)
    
    # Distribuir los objetos intermedios
    for i, obj in enumerate(selected_objects[1:-1], start=1):
        target_pos = min_pos + gap * i
        current_pos = get_position(obj, axis)
        offset = target_pos - current_pos
        setattr(obj.location, axis, getattr(obj.location, axis) + offset)