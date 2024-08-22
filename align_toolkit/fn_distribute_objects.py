import bpy
import mathutils

def distribute_objects(axis="x", distribute_by="origin"):
    # Obtener los objetos seleccionados
    selected_objects = bpy.context.selected_objects
    
    if len(selected_objects) < 3:
        print("Need at least 3 objects to distribute")
        return
    
    # Ordenar los objetos en base a su posición en el eje seleccionado
    def sort_key(obj):
        if distribute_by == "origin":
            return getattr(obj.location, axis)
        elif distribute_by == "bounding_box":
            obj.update_tag()
            bounds_world = [obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box]
            if axis == "x":
                return min([v.x for v in bounds_world])
            elif axis == "y":
                return min([v.y for v in bounds_world])
            elif axis == "z":
                return min([v.z for v in bounds_world])
        else:
            raise ValueError("distribute_by must be 'origin' or 'bounding_box'")
    
    selected_objects.sort(key=sort_key)
    
    # Obtener las posiciones de los objetos en los extremos
    if distribute_by == "origin":
        min_pos = getattr(selected_objects[0].location, axis)
        max_pos = getattr(selected_objects[-1].location, axis)
    elif distribute_by == "bounding_box":
        selected_objects[0].update_tag()
        selected_objects[-1].update_tag()
        bounds_min = [selected_objects[0].matrix_world @ mathutils.Vector(corner) for corner in selected_objects[0].bound_box]
        bounds_max = [selected_objects[-1].matrix_world @ mathutils.Vector(corner) for corner in selected_objects[-1].bound_box]
        if axis == "x":
            min_pos = min([v.x for v in bounds_min])
            max_pos = max([v.x for v in bounds_max])
        elif axis == "y":
            min_pos = min([v.y for v in bounds_min])
            max_pos = max([v.y for v in bounds_max])
        elif axis == "z":
            min_pos = min([v.z for v in bounds_min])
            max_pos = max([v.z for v in bounds_max])
    
    # Calcular la distancia total y el espacio entre objetos
    total_distance = max_pos - min_pos
    gap = total_distance / (len(selected_objects) - 1)
    
    # Distribuir los objetos intermedios
    for i, obj in enumerate(selected_objects[1:-1], start=1):
        target_pos = min_pos + gap * i
        if distribute_by == "origin":
            setattr(obj.location, axis, target_pos)
        elif distribute_by == "bounding_box":
            obj.update_tag()
            bounds_world = [obj.matrix_world @ mathutils.Vector(corner) for corner in obj.bound_box]
            current_min_pos = min([getattr(v, axis) for v in bounds_world])
            offset = target_pos - current_min_pos
            setattr(obj.location, axis, getattr(obj.location, axis) + offset)