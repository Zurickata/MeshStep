import vtk

# Controles básicos del interactor de VTK:
# - Botón izquierdo del mouse: Rotar la escena
# - Botón derecho del mouse: Zoom (acercar o alejar)
# - Botón central del mouse (o rueda): Pan (mover la escena)
# - Rueda del mouse: Zoom continuo
# - Tecla 'r': Resetear la cámara a la posición inicial
# - Tecla 'q' o 'e': Salir de la visualización
# - Tecla 'n': cambiar modelo
# - Tecla 'm': agregar modelo extra # deprecated
# - Tecla 'w': wireframe
# - Tecla 's': desactivar wireframe
# - Tecla 'a': Activar/Desactivar Angulos criticos
import math
import numpy as np
from collections import defaultdict
from .mesh_metrics import calcular_angulo, calcular_metricas_calidad




    


class ModelSwitcher:
# ----------------------------- INIT -----------------------------
    def __init__(self, renderer, renderWindowInteractor, file_dict):
        self.renderer = renderer
        self.interactor = renderWindowInteractor
        self.file_dict = file_dict
        self.current_poly = list(file_dict.keys())[0]
        self.current_index = 0
        self.toggle_load = False

        # Actor y mapper del modelo actual (solo para 'n')
        self.reader = vtk.vtkUnstructuredGridReader()
        self.mapper = vtk.vtkDataSetMapper()
        self.actor = vtk.vtkActor()

        self.metricas_actuales = None

        # Actor es un modelo .poly 
        self.renderer.AddActor(self.actor)
        # Lista para guardar actores añadidos con 'm' y las esferas que muestran los angulos extremos
        self.extra_actors = []
        self._load_current()

        # Escuchar eventos de tecla
        self.interactor.AddObserver("KeyPressEvent", self.keypress_callback)

    def _load_current(self):
        archivos = self.file_dict.get(self.current_poly, [])
        if 0 <= self.current_index < len(archivos):
            self.load_model(archivos[self.current_index])

#------------------------------------------Cargar/Leer modelo-----------------------------------------------------
    def load_model(self, filename):
        print(f"Cargando modelo (reemplazando): {filename}")
        self.reader.SetFileName(filename)
        self.reader.Update()
        self.mapper.SetInputConnection(self.reader.GetOutputPort())
        self.actor.SetMapper(self.mapper)
        # Calcular métricas al cargar el modelo
        self.metricas_actuales = calcular_metricas_calidad(self.reader.GetOutput())
        self.renderer.ResetCamera()
        self.renderer.GetRenderWindow().Render()

#-------------------------------------------Calculo de angulos-----------------------------------------------------

    def marcar_angulos_extremos(self): # Marca los angulos extremos de un Modelo ¯\_(ツ)_/¯, la puedes llamar.
        grid = self.reader.GetOutput()
        if grid.GetNumberOfCells() == 0:
            return

        angulos = []
        print(grid.GetNumberOfCells())

        cell = grid.GetCell(0)
        for i in range(grid.GetNumberOfCells()):
            cell = grid.GetCell(i)
            puntos = [cell.GetPoints().GetPoint(j) for j in range(cell.GetNumberOfPoints())]

            if len(puntos) < 3:
                continue  # Saltar celdas inválidas

            n = len(puntos)
            for j in range(n):
                ang = calcular_angulo(puntos[j - 1], puntos[j], puntos[(j + 1) % n])
            angulos.append((ang, puntos[j]))

        min_ang, min_pt = min(angulos, key=lambda x: x[0])
        max_ang, max_pt = max(angulos, key=lambda x: x[0])

        #Personalizar la detecion de los angulos
        for angulo, punto, color in [(min_ang, min_pt, (1, 0, 0)), (max_ang, max_pt, (0, 1, 0))]:
            self._agregar_esfera(punto, color)
            self._agregar_texto_angulo(punto, f"{np.degrees(angulo):.1f}°", color)

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

    # Generador de texto para mostrar el angulo
    def _agregar_texto_angulo(self, posicion, texto, color):
        text_actor = vtk.vtkBillboardTextActor3D()
        text_actor.SetPosition(*posicion)
        text_actor.SetInput(texto)
        text_actor.GetTextProperty().SetColor(*color)
        text_actor.GetTextProperty().SetFontSize(16)
        text_actor.GetTextProperty().SetBackgroundColor(0, 0, 0)  
        text_actor.GetTextProperty().SetBackgroundOpacity(0.6)
        
        self.renderer.AddActor(text_actor)
        self.extra_actors.append(text_actor)
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

    # Borra todos los modelos extras (incluye las ESFERAS), se mantiene el principal.
    def clear_extra_models(self):
        print("Borrando todos los modelos extra añadidos")
        for actor in self.extra_actors:
            self.renderer.RemoveActor(actor)
        self.extra_actors.clear()
        self.renderer.ResetCamera()
        self.renderer.GetRenderWindow().Render()
    
    def siguiente_modelo(self):
        archivos = self.file_dict.get(self.current_poly, [])
        if not archivos:
            return

        if self.current_index + 1 < len(archivos):
            self.current_index += 1
            self.load_model(archivos[self.current_index])
        else:
            print("Estás en el último modelo.")

    def anterior_modelo(self):
        archivos = self.file_dict.get(self.current_poly, [])
        if not archivos:
            return
        if self.current_index > 0:
            self.current_index -= 1
            self.load_model(archivos[self.current_index])
        elif self.current_index == 0:
            print("Estás en el primer modelo.")

#-------------------------------------------------------- Llamado de funciones/ intereacion ---------------------------------------------
    def keypress_callback(self, obj, event):
        key = self.interactor.GetKeySym()
        archivos = self.file_dict.get(self.current_poly, [])
        if key == 'n':  # Cambiar modelo (reemplazar)
            self.current_index = (self.current_index + 1) % len(self.file_list)
            self.load_model(self.file_list[self.current_index])
            self.clear_extra_models() # borra los puntos criticos pasados
            self.toggle_load = False # reiniciar los puntos criticos
        # elif key == 'm':  # Añadir modelo al escenario (sin borrar)                     # Deprecated
        #     self.current_index = (self.current_index + 1) % len(self.file_list)
        #     self.add_model(self.file_list[self.current_index])
        elif key == 'b':  # Borrar todos los modelos extra
            self.clear_extra_models()

        elif key == 'a':  # Toggle para Puntos Criticos
            self.toggle_load = not self.toggle_load
            if self.toggle_load:
                print("Cargando puntos criticos...")
                self.marcar_angulos_extremos()
                self.renderer.GetRenderWindow().Render()  # <--- FORZAR RENDER
            else:
                print("Toggle desactivado puntos criticos.")
                self.clear_extra_models()
                self.renderer.GetRenderWindow().Render()  # <--- FORZAR RENDER
        elif key == 'r':
            print("🔁 Reseteando cámara y modelo")
            self.actor.SetOrientation(0, 0, 0)
            self.actor.SetPosition(0, 0, 0)
            self.actor.SetScale(1, 1, 1)
            self.renderer.ResetCamera()
            
            # Reinicia también la rotación de cámara:
            if isinstance(self.interactor.GetInteractorStyle(), CustomInteractorStyle):
                self.interactor.GetInteractorStyle().reset_camera_and_rotation()

            self.renderer.GetRenderWindow().Render()


# ---------------------------------------------------------------------------Cambio en el estilo para el control de la camara!
class CustomInteractorStyle(vtk.vtkInteractorStyleTrackballCamera): #chatgpt
    def __init__(self, renderer, parent=None):
        self.AddObserver("MouseMoveEvent", self.mouse_move_event)
        self.AddObserver("LeftButtonPressEvent", self.left_button_press_event)
        self.AddObserver("LeftButtonReleaseEvent", self.left_button_release_event)
        self.AddObserver("MiddleButtonPressEvent", self.middle_button_press_event)
        self.AddObserver("MiddleButtonReleaseEvent", self.middle_button_release_event)
        self.renderer = renderer
        self.left_mouse_down = False
        self.last_pos = (0, 0)

    def left_button_press_event(self, obj, event):
        self.OnMiddleButtonDown()
        self.last_pos = self.GetInteractor().GetEventPosition()
        

    def left_button_release_event(self, obj, event):
        self.OnMiddleButtonUp()
        
        
    def middle_button_press_event(self, obj, event):
        # Ahora el botón del medio hará Rotación (lo que hacía el click izquierdo)
        self.OnLeftButtonDown()
    
    def middle_button_release_event(self, obj, event):
        self.OnLeftButtonUp()
       

    def mouse_move_event(self, obj, event):
        if self.left_mouse_down:
            x, y = self.GetInteractor().GetEventPosition()
            dx = x - self.last_pos[0]
            dy = y - self.last_pos[1]

            camera = self.renderer.GetActiveCamera()
            camera.Azimuth(-dx * 0.5)     # Rotación horizontal
            camera.Elevation(dy * 0.5)    # Rotación vertical
            camera.OrthogonalizeViewUp()

            self.renderer.ResetCameraClippingRange()
            self.GetInteractor().GetRenderWindow().Render()

            self.last_pos = (x, y)
        self.OnMouseMove()

    def reset_camera_and_rotation(self): #Funcion para reiniciar la rotacion
        self.renderer.GetActiveCamera().SetViewUp(0, 1, 0)
        self.renderer.GetActiveCamera().SetPosition(0, 0, 1)
        self.renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
        self.renderer.ResetCamera()
        self.GetInteractor().GetRenderWindow().Render()

#------------------------------------------ Main ---------------------------------------------------------------------------

def visualizar_vtk_unstructured_con_cambio_y_anadir(filenames):
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0.1, 0.2, 0.4) # Color Fondo

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(800, 800) # tamano pantalla

    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderWindow)
    custom_style = CustomInteractorStyle(renderer) #Estilo camara
    interactor.SetInteractorStyle(custom_style)

    switcher = ModelSwitcher(renderer, interactor, filenames)

    renderWindow.Render()
    interactor.Start()

# Archivos .vtk a cargar
# archivos = ["output.vtk", "output2.vtk", "output3.vtk"]

# visualizar_vtk_unstructured_con_cambio_y_anadir(archivos)