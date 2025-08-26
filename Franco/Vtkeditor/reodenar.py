import vtk
import numpy as np

def leer_ugrid(path):
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(path)
    reader.Update()
    return reader.GetOutput()

def get_cells_with_coords(ugrid):
    """ Devuelve lista de celdas como listas de coordenadas de sus puntos """
    pts = ugrid.GetPoints()
    cells = []
    id_list = vtk.vtkIdList()
    for i in range(ugrid.GetNumberOfCells()):
        ugrid.GetCellPoints(i, id_list)
        coords = [np.array(pts.GetPoint(id_list.GetId(j))) for j in range(id_list.GetNumberOfIds())]
        cells.append(coords)
    return cells

def cell_in_cell(parent, child, tol=1e-6):
    """Verifica si todos los puntos de child están en parent (con tolerancia)."""
    parent = np.array(parent)
    for pt in child:
        pt = np.array(pt)
        if not np.any(np.all(np.isclose(pt, parent, atol=tol), axis=1)):
            return False
    return True

def guardar_ugrid(ugrid, filename, precision=8, puntos_por_linea=2):
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

def reordenar_por_incompleto(pathA, pathB, pathOut, tol=1e-6):
    uA = leer_ugrid(pathA)  # subdividida
    uB = leer_ugrid(pathB)  # incompleto

    cellsA = get_cells_with_coords(uA)
    cellsB = get_cells_with_coords(uB)

    # Clasificar celdas: primero no presentes en B, luego presentes en B
    no_en_B = []
    en_B = []

    for a in cellsA:
        match = False
        for b in cellsB:
            if cell_in_cell(a, b, tol):
                match = True
                break
        if match:
            en_B.append(a)
        else:
            no_en_B.append(a)

    ordenadas = no_en_B + en_B

    # reconstruir UGrid
    newUG = vtk.vtkUnstructuredGrid()
    newPts = vtk.vtkPoints()
    point_index_map = {}

    def get_or_insert_point(pt):
        if pt not in point_index_map:
            pid = newPts.InsertNextPoint(pt)
            point_index_map[pt] = pid
        return point_index_map[pt]

    newUG.SetPoints(newPts)

    for cell in ordenadas:
        idlist = vtk.vtkIdList()
        for pt in cell:
            pid = get_or_insert_point(tuple(pt))
            idlist.InsertNextId(pid)
        newUG.InsertNextCell(vtk.VTK_QUAD, idlist)

    guardar_ugrid(newUG, pathOut)
    print(f"Guardado en {pathOut} → no_en_B={len(no_en_B)}, en_B={len(en_B)}")

# Ejemplo de uso
if __name__ == "__main__":
    reordenar_por_incompleto(
        "a_output_5_ubdividida.vtk",
        "a_output_5_quads.vtk",
        "reordenado_ordenado.vtk"
    )
