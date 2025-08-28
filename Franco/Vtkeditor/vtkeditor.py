import vtk
import numpy as np


# ------------------------------
# FUNCIONES DE MANIPULACIÓN
# ------------------------------
def mover_vertice(ugrid, vid, new_pos):
    puntos = ugrid.GetPoints()
    puntos.SetPoint(vid, new_pos)
    puntos.Modified()
    return ugrid


def borrar_caras(ugrid, cids_a_borrar):
    """
    Elimina caras/celdas por ID de un vtkUnstructuredGrid.
    """
    ids = vtk.vtkIdTypeArray()
    for cid in cids_a_borrar:
        ids.InsertNextValue(cid)

    selectionNode = vtk.vtkSelectionNode()
    selectionNode.SetFieldType(vtk.vtkSelectionNode.CELL)
    selectionNode.SetContentType(vtk.vtkSelectionNode.INDICES)
    selectionNode.SetSelectionList(ids)
    selectionNode.GetProperties().Set(vtk.vtkSelectionNode.INVERSE(), 1)  
    # INVERSE=1 → selecciona TODO MENOS esas caras

    selection = vtk.vtkSelection()
    selection.AddNode(selectionNode)

    extract = vtk.vtkExtractSelection()
    extract.SetInputData(0, ugrid)
    extract.SetInputData(1, selection)
    extract.Update()

    # Convertir de vtkDataSet a vtkUnstructuredGrid
    ugrid_out = vtk.vtkUnstructuredGrid.SafeDownCast(extract.GetOutput())
    return ugrid_out



def borrar_vertices(ugrid, vids_a_borrar):
    cell_ids_to_remove = []
    for cid in range(ugrid.GetNumberOfCells()):
        cell = ugrid.GetCell(cid)
        if any(v in vids_a_borrar for v in [cell.GetPointId(i) for i in range(cell.GetNumberOfPoints())]):
            cell_ids_to_remove.append(cid)

    return borrar_caras(ugrid, cell_ids_to_remove)



def merge_vertices(ugrid, tol=1e-6, ids_merge=None):
    clean = vtk.vtkCleanUnstructuredGrid()
    if ids_merge is None:
        # Automático
        clean.SetInputData(ugrid)
        clean.SetTolerance(tol)
    else:
        puntos = ugrid.GetPoints()
        arr = np.array([puntos.GetPoint(i) for i in range(puntos.GetNumberOfPoints())])
        for (i, j) in ids_merge:
            avg = (arr[i] + arr[j]) / 2
            arr[i] = avg
            arr[j] = avg

        new_points = vtk.vtkPoints()
        for p in arr:
            new_points.InsertNextPoint(p)
        ugrid.SetPoints(new_points)
        clean.SetInputData(ugrid)
        clean.SetTolerance(tol)

    clean.Update()
    return clean.GetOutput()

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

# ------------------------------
# EJEMPLO DE USO CON VISUALIZACIÓN
# ------------------------------
def visualizar_y_modificar(ugrid):
    mapper = vtk.vtkDataSetMapper()
    mapper.SetInputData(ugrid)

    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetEdgeVisibility(1)
    actor.GetProperty().SetColor(0.8, 0.8, 1.0)

    renderer = vtk.vtkRenderer()
    renderer.AddActor(actor)
    renderer.SetBackground(0.1, 0.1, 0.1)

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(800, 600)

    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renderWindow)

    # ------------------------------
    # Atajos de teclado
    # ------------------------------
    def keypress(obj, ev):
        key = obj.GetKeySym()
        nonlocal ugrid

        if key == "m":  # mover vértice
            print("Moviendo vértice 0 a (2,2,0)")
            ugrid = mover_vertice(ugrid, 0, (2, 2, 0))
            mapper.SetInputData(ugrid)
            renderWindow.Render()

        elif key == "c":  # borrar cara
            print("Borrando cara 0")
            ugrid = borrar_caras(ugrid, [0])
            mapper.SetInputData(ugrid)
            renderWindow.Render()

        elif key == "v":  # borrar vértices
            print("Borrando vértice 0")
            ugrid = borrar_vertices(ugrid, [0])
            mapper.SetInputData(ugrid)
            renderWindow.Render()

        elif key == "g":  # merge automático
            print("Merge automático con tol=1e-3")
            ugrid = merge_vertices(ugrid, tol=1e-3)
            mapper.SetInputData(ugrid)
            renderWindow.Render()

        elif key == "s":  # guardar archivo
            print("Guardando archivo en salida.vtk...")
            guardar_ugrid(ugrid, "salida.vtk")

        elif key == "q":
            print("Saliendo...")
            iren.TerminateApp()

    iren.AddObserver("KeyPressEvent", keypress)

    renderWindow.Render()
    iren.Start()
    

def cargar_ugrid(filename):
    """
    Carga un vtkUnstructuredGrid desde un archivo .vtk (formato clásico).
    """
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(filename)
    reader.Update()

    ugrid = reader.GetOutput()
    return ugrid

# ------------------------------
# EJEMPLO DE MALLA (cuadrado 2D extruido en 3D)
# ------------------------------
def ejemplo_malla():
    points = vtk.vtkPoints()
    points.InsertNextPoint(0, 0, 0)
    points.InsertNextPoint(1, 0, 0)
    points.InsertNextPoint(1, 1, 0)
    points.InsertNextPoint(0, 1, 0)

    quad = vtk.vtkQuad()
    for i in range(4):
        quad.GetPointIds().SetId(i, i)

    cells = vtk.vtkCellArray()
    cells.InsertNextCell(quad)

    ugrid = vtk.vtkUnstructuredGrid()
    ugrid.SetPoints(points)
    ugrid.InsertNextCell(quad.GetCellType(), quad.GetPointIds())

    return ugrid


if __name__ == "__main__":
    ugrid = cargar_ugrid("reordenado_total.vtk")
    print("Puntos:", ugrid.GetNumberOfPoints())
    print("Celdas:", ugrid.GetNumberOfCells())
    visualizar_y_modificar(ugrid)
