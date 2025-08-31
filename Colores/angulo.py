import vtk
import math
import numpy as np



def angle_between(v1, v2):
    v1 = v1 / np.linalg.norm(v1)
    v2 = v2 / np.linalg.norm(v2)
    dot = np.clip(np.dot(v1, v2), -1.0, 1.0)
    return math.acos(dot)

def min_angle_of_cell(cell, points):
    """Calcula el ángulo mínimo de un polígono 2D (quad o tri)."""
    ids = cell.GetPointIds()
    npts = ids.GetNumberOfIds()
    min_angle = math.pi
    for i in range(npts):
        pid_prev = ids.GetId((i - 1) % npts)
        pid_curr = ids.GetId(i)
        pid_next = ids.GetId((i + 1) % npts)

        p_prev = np.array(points.GetPoint(pid_prev))
        p_curr = np.array(points.GetPoint(pid_curr))
        p_next = np.array(points.GetPoint(pid_next))

        v1 = p_prev - p_curr
        v2 = p_next - p_curr
        angle = angle_between(v1, v2)
        if angle < min_angle:
            min_angle = angle
    return min_angle

def interpolate_color(c1, c2, t):
    """Interpolación lineal entre dos colores RGB (0-255)."""
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))

def pintar_quads_por_angulo(input_path, output_path, step=10,
                            ref_angle=10,
                            base_color=(128, 0, 128),   # morado
                            end_color=(255, 0, 0)):     # rojo
    """
    Colorea cada celda según su ángulo mínimo.
    - Si el ángulo <= ref_angle → base_color
    - Si el ángulo > ref_angle → escala de colores hasta end_color en bins de 'step'
    """
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(input_path)
    reader.Update()
    ugrid = reader.GetOutput()
    points = ugrid.GetPoints()

    colors = vtk.vtkUnsignedCharArray()
    colors.SetNumberOfComponents(3)
    colors.SetName("CellColors")

    max_bins = max(1, int((180 - ref_angle) // step))

    for cid in range(ugrid.GetNumberOfCells()):
        cell = ugrid.GetCell(cid)
        if cell is None:
            continue

        min_angle = math.degrees(min_angle_of_cell(cell, points))

        if min_angle <= ref_angle:
            r, g, b = base_color
        else:
            # Calcular bin relativo
            bin_index = int((min_angle - ref_angle) // step)
            t = min(bin_index / max_bins, 1.0)
            r, g, b = interpolate_color(base_color, end_color, t)

        colors.InsertNextTuple3(r, g, b)

    ugrid.GetCellData().SetScalars(colors)

    writer = vtk.vtkUnstructuredGridWriter()
    writer.SetFileName(output_path)
    writer.SetInputData(ugrid)
    writer.Write()

    print(f"✔ Archivo generado: {output_path} con {ugrid.GetNumberOfCells()} quads coloreados.")

pintar_quads_por_angulo("a_output_5.vtk", "out1.vtk",
                        step=10, ref_angle=60,
                        base_color=(0,0,255), end_color=(255,0,0))
