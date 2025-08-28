import vtk
import time

# (bug?) NOOO hacer click durante la animacion, hace que se congele.

def animar_vtk_unstructured(filename):
    # Leer el archivo .vtk
    reader = vtk.vtkUnstructuredGridReader()
    reader.SetFileName(filename)
    reader.Update()
    data = reader.GetOutput()

    # Obtener puntos del archivo original
    puntos = data.GetPoints()

    # Crear un nuevo UnstructuredGrid vacío para animar    <------ 
    anim_grid = vtk.vtkUnstructuredGrid()
    anim_grid.SetPoints(puntos)

    # Mapper y actor
    mapper = vtk.vtkDataSetMapper()
    mapper.SetInputData(anim_grid)
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)

    # Renderer, ventana e interactor
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0.1, 0.2, 0.4)
    renderer.AddActor(actor)
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(800, 800)
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderWindow)

    # Inicializar render
    renderWindow.Render()
    interactor.Initialize()

#------------------------------------------------- Animacion---------------------------------------
    # Agregar las celdas (conexiones) una a una
    num_cells = data.GetNumberOfCells()
    for i in range(num_cells):
        cell = data.GetCell(i)
        anim_grid.InsertNextCell(cell.GetCellType(), cell.GetPointIds())
        anim_grid.Modified()
        renderWindow.Render()
        time.sleep(0.1)  # pausa para ver la animación

    # Finalmente, lanzar la interacción
    interactor.Start()


#------------------------------------------------- main -------------------
# Usar la función con tu archivo
animar_vtk_unstructured("output.vtk")
