import vtk

# Controles básicos del interactor de VTK:
# - Botón izquierdo del mouse: Rotar la escena
# - Botón derecho del mouse: Zoom (acercar o alejar)
# - Botón central del mouse (o rueda): Pan (mover la escena)
# - Rueda del mouse: Zoom continuo
# - Tecla 'r': Resetear la cámara a la posición inicial
# - Tecla 'q' o 'e': Salir de la visualización
# - Tecla 'n': cambiar modelo
# - Tecla 'm': agregar modelo extra
# - Tecla 'w': wireframe

import math

def calcular_angulo(p1, p2, p3):
    # Calcula el ángulo en p2 formado por p1-p2-p3 (en radianes)
    v1 = [p1[i] - p2[i] for i in range(3)]
    v2 = [p3[i] - p2[i] for i in range(3)]
    def norma(v): return math.sqrt(sum(c*c for c in v))
    def dot(a, b): return sum(a[i]*b[i] for i in range(3))

    nv1 = norma(v1)
    nv2 = norma(v2)
    if nv1 == 0 or nv2 == 0:
            return 0
    cos_theta = dot(v1, v2) / (nv1 * nv2)
    cos_theta = max(-1.0, min(1.0, cos_theta))  # Evitar errores numéricos
    return math.acos(cos_theta)


class ModelSwitcher:
# ----------------------------- INIT -----------------------------
    def __init__(self, renderer, renderWindowInteractor, file_list):
        self.renderer = renderer
        self.interactor = renderWindowInteractor
        self.file_list = file_list
        self.current_index = 0

        # Actor y mapper del modelo actual (solo para 'n')
        self.reader = vtk.vtkUnstructuredGridReader()
        self.mapper = vtk.vtkDataSetMapper()
        self.actor = vtk.vtkActor()

        # Actor es un modelo .poly 
        self.renderer.AddActor(self.actor)
        # Lista para guardar actores añadidos con 'm' y las esferas que muestran los angulos extremos
        self.extra_actors = []
        self.load_model(self.file_list[self.current_index])


        # Escuchar eventos de tecla
        self.interactor.AddObserver("KeyPressEvent", self.keypress_callback)

#------------------------------------------Cargar/Leer modelo-----------------------------------------------------
    def load_model(self, filename):
        print(f"Cargando modelo (reemplazando): {filename}")
        self.reader.SetFileName(filename)
        self.reader.Update()
        self.mapper.SetInputConnection(self.reader.GetOutputPort())
        self.actor.SetMapper(self.mapper)
        self.renderer.ResetCamera()
        self.renderer.GetRenderWindow().Render()
        self.marcar_angulos_extremos()
#-------------------------------------------Calculo de angulos-----------------------------------------------------

    def marcar_angulos_extremos(self):
        grid = self.reader.GetOutput()
        if grid.GetNumberOfCells() == 0:
            return

        cell = grid.GetCell(0)
        puntos = [cell.GetPoints().GetPoint(i) for i in range(cell.GetNumberOfPoints())]

        if len(puntos) < 3:
            return

        angulos = []
        n = len(puntos)
        for i in range(n):
            ang = calcular_angulo(puntos[i - 1], puntos[i], puntos[(i + 1) % n])
            angulos.append((ang, puntos[i]))

        min_ang, min_pt = min(angulos, key=lambda x: x[0])
        max_ang, max_pt = max(angulos, key=lambda x: x[0])

        for angulo, punto, color in [(min_ang, min_pt, (1, 0, 0)), (max_ang, max_pt, (0, 1, 0))]:
            self._agregar_esfera(punto, color)

    # Generador de las esferas para marcar agulos extremos
    def _agregar_esfera(self, centro, color):
        esfera = vtk.vtkSphereSource()
        esfera.SetCenter(*centro)
        esfera.SetRadius(0.01)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(esfera.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(*color)

        self.renderer.AddActor(actor)
        self.extra_actors.append(actor)
#---------------------------------------------- Anadir modelos ----------------------------------------------------------

    # Anade un modelo, la diferencia a cargar/leer es que AQUI se MANTIENE el objeto principal.
    def add_model(self, filename):
        print(f"Añadiendo modelo: {filename}")
        reader = vtk.vtkUnstructuredGridReader()
        reader.SetFileName(filename)
        reader.Update()

        mapper = vtk.vtkDataSetMapper()
        mapper.SetInputConnection(reader.GetOutputPort())

        actor = vtk.vtkActor()
        actor.SetMapper(mapper)

        self.renderer.AddActor(actor)
        self.extra_actors.append(actor)
        self.renderer.ResetCamera() 
        self.renderer.GetRenderWindow().Render()

    # Borra todos los modelos extras (incluye las esferas), se mantiene el principal.
    def clear_extra_models(self):
        print("Borrando todos los modelos extra añadidos")
        for actor in self.extra_actors:
            self.renderer.RemoveActor(actor)
        self.extra_actors.clear()
        self.renderer.ResetCamera()
        self.renderer.GetRenderWindow().Render()

#-------------------------------------------------------- Llamado de funciones ---------------------------------------------
    def keypress_callback(self, obj, event):
        key = self.interactor.GetKeySym()
        if key == 'n':  # Cambiar modelo (reemplazar)
            self.current_index = (self.current_index + 1) % len(self.file_list)
            self.load_model(self.file_list[self.current_index])
        elif key == 'm':  # Añadir modelo al escenario (sin borrar)
            self.current_index = (self.current_index + 1) % len(self.file_list)
            self.add_model(self.file_list[self.current_index])
        elif key == 'b':  # Borrar todos los modelos extra
            self.clear_extra_models()


#------------------------------------------ Main ---------------------------------------------------------------------------

def visualizar_vtk_unstructured_con_cambio_y_anadir(filenames):
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0.1, 0.2, 0.4) # Color Fondo

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(800, 800) # tamano pantalla

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderWindow)

    switcher = ModelSwitcher(renderer, interactor, filenames)

    renderWindow.Render()
    interactor.Start()

# Archivos .vtk a cargar
archivos = ["output.vtk", "output2.vtk", "output3.vtk"]

visualizar_vtk_unstructured_con_cambio_y_anadir(archivos)
