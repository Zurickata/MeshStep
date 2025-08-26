import vtk
import numpy as np

def guardar_vtk_clasico(ugrid, filename, precision=8, puntos_por_linea=2):
    """Guardar vtkUnstructuredGrid en ASCII, formato clásico."""
    output_lines = []

    output_lines.append("# vtk DataFile Version 3.0\n")
    output_lines.append("VTK file formatted in classic ASCII\n")
    output_lines.append("ASCII\n")
    output_lines.append("DATASET UNSTRUCTURED_GRID\n")

    # POINTS
    npoints = ugrid.GetNumberOfPoints()
    output_lines.append(f"POINTS {npoints} float\n")
    for i in range(0, npoints, puntos_por_linea):
        line_coords = []
        for j in range(puntos_por_linea):
            idx = i + j
            if idx >= npoints:
                break
            pt = ugrid.GetPoint(idx)
            line_coords.extend([f"{c:+.{precision}E}" for c in pt])
        output_lines.append(" ".join(line_coords) + "\n")

    # CELLS
    ncells = ugrid.GetNumberOfCells()
    total_indices = sum(ugrid.GetCell(i).GetNumberOfPoints() + 1 for i in range(ncells))
    output_lines.append(f"CELLS {ncells} {total_indices}\n")
    for i in range(ncells):
        cell = ugrid.GetCell(i)
        ids = [str(cell.GetNumberOfPoints())] + [str(cell.GetPointId(j)) for j in range(cell.GetNumberOfPoints())]
        output_lines.append(" ".join(ids) + "\n")

    # CELL_TYPES
    output_lines.append(f"CELL_TYPES {ncells}\n")
    for i in range(ncells):
        output_lines.append(str(ugrid.GetCellType(i)) + "\n")

    with open(filename, "w") as f:
        f.writelines(output_lines)


def subdividir_cara(quad_points, subdivs, start_pid):
    """
    Subdivide una cara (quad) en una grilla de subdivs x subdivs.
    quad_points: 4x3 numpy array (p0,p1,p2,p3)
    """
    nx = ny = subdivs + 1
    pts = []
    pid_map = {}
    quads = []

    # Crear grilla de puntos internos
    for j in range(ny):
        t = j / subdivs
        for i in range(nx):
            s = i / subdivs
            pt = (1-s)*(1-t)*quad_points[0] + s*(1-t)*quad_points[1] + s*t*quad_points[2] + (1-s)*t*quad_points[3]
            pts.append(pt)
            pid_map[(i,j)] = start_pid
            start_pid += 1

    # Crear quads subdivididos
    for j in range(subdivs):
        for i in range(subdivs):
            q = (
                pid_map[(i,j)],
                pid_map[(i+1,j)],
                pid_map[(i+1,j+1)],
                pid_map[(i,j+1)]
            )
            quads.append(q)

    return pts, quads, start_pid


def subdividir_malla_por_caras(input_file, output_file, subdivs):
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(input_file)
    reader.Update()
    ugrid = reader.GetOutput()

    all_points = []
    all_quads = []
    pid_counter = 0

    # Subdividir cada cara por separado
    for cid in range(ugrid.GetNumberOfCells()):
        cell = ugrid.GetCell(cid)
        if cell.GetNumberOfPoints() != 4:
            raise ValueError("Sólo se soportan quads")
        quad_pts = np.array([ugrid.GetPoint(cell.GetPointId(k)) for k in range(4)])
        pts, quads, pid_counter = subdividir_cara(quad_pts, subdivs, pid_counter)
        all_points.extend(pts)
        all_quads.extend(quads)

    # Crear vtkPoints
    vtk_points = vtk.vtkPoints()
    vtk_points.SetDataTypeToDouble()
    for p in all_points:
        vtk_points.InsertNextPoint(p)

    # Crear celdas
    vtk_cells = vtk.vtkCellArray()
    for q in all_quads:
        quad = vtk.vtkQuad()
        for k in range(4):
            quad.GetPointIds().SetId(k, q[k])
        vtk_cells.InsertNextCell(quad)

    # Crear nuevo grid
    new_grid = vtk.vtkUnstructuredGrid()
    new_grid.SetPoints(vtk_points)
    new_grid.SetCells(vtk.VTK_QUAD, vtk_cells)

    # Guardar
    guardar_vtk_clasico(new_grid, output_file)
    print(f"Malla subdividida por caras guardada en {output_file}")


# EJEMPLO
nivel_refinamiento= 5
subdividir_malla_por_caras(
    "a_output_3_grid.vtk",
    "a_output_5_subdividida.vtk",
    subdivs=2**nivel_refinamiento
)
