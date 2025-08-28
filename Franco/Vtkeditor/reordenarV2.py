import vtk
import numpy as np
from scipy.spatial import cKDTree

def leer_ugrid(path):
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(path)
    reader.Update()
    return reader.GetOutput()

def get_cells_with_coords(ugrid):
    pts = ugrid.GetPoints()
    cells = []
    id_list = vtk.vtkIdList()
    for i in range(ugrid.GetNumberOfCells()):
        ugrid.GetCellPoints(i, id_list)
        coords = np.array([pts.GetPoint(id_list.GetId(j)) for j in range(id_list.GetNumberOfIds())])
        cells.append(coords)
    return cells

def guardar_ugrid(ugrid, filename, precision=8, puntos_por_linea=2):
    output_lines = []
    output_lines.append("# vtk DataFile Version 3.0\n")
    output_lines.append("VTK file formatted in classic ASCII\n")
    output_lines.append("ASCII\n")
    output_lines.append("DATASET UNSTRUCTURED_GRID\n")

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

    ncells = ugrid.GetNumberOfCells()
    total_indices = sum(ugrid.GetCell(i).GetNumberOfPoints() + 1 for i in range(ncells))
    output_lines.append(f"CELLS {ncells} {total_indices}\n")
    for i in range(ncells):
        cell = ugrid.GetCell(i)
        ids = [str(cell.GetNumberOfPoints())] + [str(cell.GetPointId(j)) for j in range(cell.GetNumberOfPoints())]
        output_lines.append(" ".join(ids) + "\n")

    output_lines.append(f"CELL_TYPES {ncells}\n")
    for i in range(ncells):
        output_lines.append(str(ugrid.GetCellType(i)) + "\n")

    with open(filename, "w") as f:
        f.writelines(output_lines)

def reordenar_ugrid_total(pathA, pathB, pathOut, tol=1e-6):
    uA = leer_ugrid(pathA)
    uB = leer_ugrid(pathB)

    cellsA = get_cells_with_coords(uA)
    cellsB = get_cells_with_coords(uB)

    # Construir KDTree con los puntos de B
    all_points_B = np.vstack(cellsB)
    tree_B = cKDTree(all_points_B)

    no_en_B = []
    en_B = []

    for cellA in cellsA:
        # Para cada punto de la celda, buscar vecino en B dentro de tol
        matches = [tree_B.query_ball_point(pt, tol) for pt in cellA]
        # Si cada punto encuentra al menos un match → está en B
        if all(len(m) > 0 for m in matches):
            en_B.append(cellA)
        else:
            no_en_B.append(cellA)

    ordenadas = no_en_B + en_B

    # Reconstrucción UGrid usando los puntos originales de A
    newUG = vtk.vtkUnstructuredGrid()
    newUG.SetPoints(uA.GetPoints())

    # Construir mapeo de punto->id
    points_array = np.array([uA.GetPoint(i) for i in range(uA.GetNumberOfPoints())])
    tree_A = cKDTree(points_array)
    point_id_map = {}

    for cell in ordenadas:
        idlist = vtk.vtkIdList()
        for pt in cell:
            key = tuple(np.round(pt / tol).astype(int))
            if key in point_id_map:
                pid = point_id_map[key]
            else:
                dist, pid = tree_A.query(pt)
                point_id_map[key] = pid
            idlist.InsertNextId(pid)
        newUG.InsertNextCell(vtk.VTK_QUAD, idlist)

    guardar_ugrid(newUG, pathOut)
    print(f"Guardado en {pathOut} → no_en_B={len(no_en_B)}, en_B={len(en_B)}")

if __name__ == "__main__":
    reordenar_ugrid_total(
        "a_output_5_ubdividida.vtk",
        "a_output_5_quads.vtk",
        "reordenado_total.vtk"
    )
