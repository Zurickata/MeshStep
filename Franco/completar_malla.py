import vtk
import numpy as np

def guardar_vtk_clasico(ugrid, filename, precision=8, puntos_por_linea=2):
    output_lines = []
    output_lines.append("# vtk DataFile Version 3.0\n")
    output_lines.append("VTK file formatted in classic ASCII\n")
    output_lines.append("ASCII\n")
    output_lines.append("DATASET UNSTRUCTURED_GRID\n")

    # PUNTOS
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

def completar_malla_vtk_subdiv(input_file, output_file, subdiv=3):
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(input_file)
    reader.Update()
    ugrid = reader.GetOutput()

    puntos = np.array([ugrid.GetPoint(i) for i in range(ugrid.GetNumberOfPoints())])

    # Detectar límites
    x_min, x_max = puntos[:,0].min(), puntos[:,0].max()
    y_min, y_max = puntos[:,1].min(), puntos[:,1].max()

    # Cantidad de nodos por eje según subdivisiones
    nx = 2**subdiv + 1
    ny = 2**subdiv + 1
    print(f"Generando grilla uniforme: {nx} x {ny} nodos")

    xs = np.linspace(x_min, x_max, nx)
    ys = np.linspace(y_min, y_max, ny)

    # Crear puntos
    new_points = vtk.vtkPoints()
    punto2id = {}
    pid = 0
    for j in range(ny):
        for i in range(nx):
            pt = (xs[i], ys[j], 0.0)
            new_points.InsertNextPoint(pt)
            punto2id[(i,j)] = pid
            pid += 1

    # Crear quads
    new_cells = vtk.vtkCellArray()
    for j in range(ny-1):
        for i in range(nx-1):
            quad = vtk.vtkQuad()
            quad.GetPointIds().SetId(0, punto2id[(i,j)])
            quad.GetPointIds().SetId(1, punto2id[(i+1,j)])
            quad.GetPointIds().SetId(2, punto2id[(i+1,j+1)])
            quad.GetPointIds().SetId(3, punto2id[(i,j+1)])
            new_cells.InsertNextCell(quad)

    # Nuevo grid
    new_grid = vtk.vtkUnstructuredGrid()
    new_grid.SetPoints(new_points)
    new_grid.SetCells(vtk.VTK_QUAD, new_cells)

    # Guardar
    guardar_vtk_clasico(new_grid, output_file, precision=8, puntos_por_linea=2)
    print(f"Archivo completo guardado en {output_file}")

# Uso
completar_malla_vtk_subdiv(
    "a_output_3_quads.vtk",
    "a_output_3_quads_completo.vtk",
    subdiv=3
)
