import vtk
import math
import numpy as np

EPS = 1e-12

# --------- Helpers geométricos ---------
def polygon_area(points_list):
    """
    Calcula el área de un polígono en 3D proyectando al plano mejor definido.
    Funciona para triángulos, quads y polígonos convexos.
    """
    if len(points_list) < 3:
        return 0.0

    # Normal del polígono usando la primera triangulación
    normal = np.zeros(3)
    p0 = np.array(points_list[0])
    for i in range(1, len(points_list) - 1):
        v1 = np.array(points_list[i]) - p0
        v2 = np.array(points_list[i+1]) - p0
        normal += np.cross(v1, v2)
    norm_len = np.linalg.norm(normal)
    if norm_len < EPS:
        return 0.0

    # Área es 0.5 * |sum cross products|
    area = 0.0
    for i in range(1, len(points_list) - 1):
        v1 = np.array(points_list[i]) - p0
        v2 = np.array(points_list[i+1]) - p0
        area += 0.5 * np.linalg.norm(np.cross(v1, v2))
    return area

def edge_length(p1, p2):
    return float(np.linalg.norm(np.array(p1) - np.array(p2)))

def triangle_area(p0, p1, p2):
    # Área del triángulo en 3D (norma de 0.5 * cross)
    v1 = np.array(p1) - np.array(p0)
    v2 = np.array(p2) - np.array(p0)
    return 0.5 * np.linalg.norm(np.cross(v1, v2))

def tri_aspect_ratio(p0, p1, p2):
    a = edge_length(p1, p2)
    b = edge_length(p2, p0)
    c = edge_length(p0, p1)
    A = triangle_area(p0, p1, p2)
    if A < EPS:
        return float("inf")
    return (a*a + b*b + c*c) / (4.0 * math.sqrt(3.0) * A)

def poly_aspect_ratio(points_list):
    # Para quads/polígonos: razón de aristas (simple y estable)
    lengths = [edge_length(points_list[i], points_list[(i+1)%len(points_list)])
               for i in range(len(points_list))]
    mn = min(lengths)
    mx = max(lengths)
    if mn < EPS:
        return float("inf")
    return mx / mn

def angle_between(v1, v2):
    n1 = np.linalg.norm(v1)
    n2 = np.linalg.norm(v2)
    if n1 < EPS or n2 < EPS:
        return math.pi  # si hay arista degenerada, no castigamos con NaN
    v1u = v1 / n1
    v2u = v2 / n2
    dot = float(np.clip(np.dot(v1u, v2u), -1.0, 1.0))
    return math.acos(dot)

def min_angle_of_cell(cell, points):
    ids = cell.GetPointIds()
    n = ids.GetNumberOfIds()
    # Triángulos: podemos calcular ángulos por ley de cosenos (más estable)
    if n == 3:
        p0 = np.array(points.GetPoint(ids.GetId(0)))
        p1 = np.array(points.GetPoint(ids.GetId(1)))
        p2 = np.array(points.GetPoint(ids.GetId(2)))
        # vectores en torno a cada vértice
        vA1, vA2 = p1 - p0, p2 - p0
        vB1, vB2 = p0 - p1, p2 - p1
        vC1, vC2 = p0 - p2, p1 - p2
        angA = angle_between(vA1, vA2)
        angB = angle_between(vB1, vB2)
        angC = angle_between(vC1, vC2)
        return min(angA, angB, angC)
    # Polígonos generales
    min_ang = math.pi
    for i in range(n):
        pid_prev = ids.GetId((i-1) % n)
        pid_curr = ids.GetId(i)
        pid_next = ids.GetId((i+1) % n)
        p_prev = np.array(points.GetPoint(pid_prev))
        p_curr = np.array(points.GetPoint(pid_curr))
        p_next = np.array(points.GetPoint(pid_next))
        v1 = p_prev - p_curr
        v2 = p_next - p_curr
        ang = angle_between(v1, v2)
        if ang < min_ang:
            min_ang = ang
    return min_ang

# --------- Colores ---------
def interpolate_color(c1, c2, t):
    t = max(0.0, min(1.0, float(t)))
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def map_value_to_color(val, ref_value, step, base_color, end_color, max_bins):
    if val <= ref_value:
        return base_color
    bin_index = int((val - ref_value) // step)
    t = min(bin_index / max_bins, 1.0)
    return interpolate_color(base_color, end_color, t)

# --------- Función principal ---------
def colorear_celdas(
    input_path, output_path,
    metric="aspect",              
    base_color=(128, 0, 128),     
    end_color=(255, 0, 0),        
    bins=10                       # número de rangos
):
    """
    Lee un .vtk (UNSTRUCTURED_GRID 2D) y colorea celdas según:
      - metric="aspect": razón de aspecto
      - metric="angle" : ángulo interno mínimo (en grados)
      - metric="area"  : área de la celda
    Los rangos se calculan automáticamente usando 'bins'.
    """

    # Leer malla
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(input_path)
    reader.Update()
    ugrid = reader.GetOutput()
    points = ugrid.GetPoints()

    n_cells = ugrid.GetNumberOfCells()
    if n_cells == 0:
        raise RuntimeError("No hay celdas en el archivo VTK.")

    values = []
    for cid in range(n_cells):
        cell = ugrid.GetCell(cid)
        ids = cell.GetPointIds()
        n = ids.GetNumberOfIds()
        pts = [points.GetPoint(ids.GetId(i)) for i in range(n)]

        if metric == "aspect":
            if n == 3:
                val = tri_aspect_ratio(pts[0], pts[1], pts[2])
            else:
                val = poly_aspect_ratio(pts)
        elif metric == "angle":
            val = math.degrees(min_angle_of_cell(cell, points))
        elif metric == "area":
            val = polygon_area(pts)
        else:
            raise ValueError("metric debe ser 'aspect', 'angle' o 'area'.")

        if not np.isfinite(val):
            val = 1e9
        values.append(val)

    # Rango automático según valores
    min_val = min(values)
    max_val = max(values)
    if max_val <= min_val:
        max_val = min_val + 1e-6
    step = (max_val - min_val) / max(1, bins-1)

    print(f"✔ Métrica={metric} | rango=({min_val:.4f}, {max_val:.4f}) | bins={bins}")

    # Mapear a colores
    colors = vtk.vtkUnsignedCharArray()
    colors.SetNumberOfComponents(3)
    colors.SetName("CellColors")

    for val in values:
        rgb = map_value_to_color(val, min_val, step, base_color, end_color, bins)
        colors.InsertNextTuple3(*rgb)

    ugrid.GetCellData().SetScalars(colors)

    writer = vtk.vtkUnstructuredGridWriter()
    writer.SetFileName(output_path)
    writer.SetInputData(ugrid)
    writer.Write()

    print(f"✔ Archivo generado: {output_path} ({n_cells} celdas)")



