import vtk
import math
import numpy as np
from collections import defaultdict
from .mesh_metrics import calcular_angulo, calcular_metricas_calidad
import time
from PyQt5.QtCore import pyqtSignal, QObject

# Crear el notificador al inicio del archivo
class CellSelectionNotifier(QObject):
    cell_selected = pyqtSignal(int, int, float)  # cell_id, num_points, min_angle

notifier = CellSelectionNotifier()

class ModelSwitcher:
# ----------------------------- INIT -----------------------------
    def __init__(self, renderer, renderWindowInteractor, file_dict):
        self.renderer = renderer
        self.interactor = renderWindowInteractor
        self.file_dict = file_dict
        self.current_poly = list(file_dict.keys())[0]
        self.current_index = 0
        self.toggle_load = False

        self.last_e_time = 0
        self.last_selected_cell = None
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

        for angulo, punto, color in [(min_ang, min_pt, (1, 0, 0)), (max_ang, max_pt, (0, 1, 0))]:
            self._agregar_esfera(punto, color)
            self._agregar_texto_angulo(punto, f"{np.degrees(angulo):.1f}°", color)

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
        elif key == 'b':  
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
            
            if isinstance(self.interactor.GetInteractorStyle(), CustomInteractorStyle):
                self.interactor.GetInteractorStyle().reset_camera_and_rotation()

            self.renderer.GetRenderWindow().Render()
        elif key == 'q':
            # Get the custom interactor style from the interactor
            interactor_style = self.interactor.GetInteractorStyle()
            
            # Check if it's the correct style and if a cell has been selected
            if isinstance(interactor_style, CustomInteractorStyle) and interactor_style.last_selected_cell:
                # Get the selected cell data from the interactor style
                puntos, cell_id = interactor_style.last_selected_cell
                
                # Calculate the center of the selected face
                xs, ys, zs = zip(*puntos)
                center = (
                    (min(xs) + max(xs)) / 2,
                    (min(ys) + max(ys)) / 2,
                    (min(zs) + max(zs)) / 2,
                )
                
                # Animate the camera
                self.animate_camera_to(center, distance=0.3)
                print(f"📸 Cámara animada hacia cara {cell_id}")
            else:
                print("⚠️ No hay cara seleccionada todavía. Presione 'e' sobre una cara primero.")

    def animate_camera_to(self, focal_point, distance=0.3, steps=15, delay=10):
        cam = self.renderer.GetActiveCamera()
        start_pos = np.array(cam.GetPosition())
        start_focal = np.array(cam.GetFocalPoint())
        view_dir = np.array(start_focal) - np.array(start_pos)
        view_dir /= np.linalg.norm(view_dir)
        target_focal = np.array(focal_point)
        target_pos = target_focal - view_dir * distance

        for i in range(1, steps + 1):
            t = i / steps
            new_pos = (1 - t) * start_pos + t * target_pos
            new_focal = (1 - t) * start_focal + t * target_focal
            cam.SetPosition(*new_pos)
            cam.SetFocalPoint(*new_focal)
            self.renderer.ResetCameraClippingRange()
            self.renderer.GetRenderWindow().Render()
            time.sleep(delay / 1000.0)


# ---------------------------------------------------------------------------Cambio en el estilo para el control de la camara!
class CustomInteractorStyle(vtk.vtkInteractorStyleTrackballCamera): #chatgpt
    def __init__(self, renderer, parent=None):
        super().__init__()
        self.AddObserver("MouseMoveEvent", self.mouse_move_event)
        self.AddObserver("LeftButtonPressEvent", self.left_button_press_event)
        self.AddObserver("LeftButtonReleaseEvent", self.left_button_release_event)
        self.AddObserver("MiddleButtonPressEvent", self.middle_button_press_event)
        self.AddObserver("MiddleButtonReleaseEvent", self.middle_button_release_event)
        self.renderer = renderer
        self.left_mouse_down = False
        self.last_pos = (0, 0)
        self.AddObserver("KeyPressEvent", self.on_key_press)
        self.renderer = renderer
        self.picker = vtk.vtkCellPicker()
        self.selected_actor = None
        self.selected_cell_id = None
        self.original_property = None
        self.focused = False  
        self.last_selected_cell = None

    def on_key_press(self, obj, event):
        key = self.GetInteractor().GetKeySym()
        if key.lower() == "e":
            # Si no hubo click previo, obtener siempre la posición actual del mouse
            mouse_pos = self.GetInteractor().GetEventPosition()
            if not mouse_pos:  
                # fallback: centro de la ventana
                size = self.GetInteractor().GetRenderWindow().GetSize()
                mouse_pos = (size[0] // 2, size[1] // 2)
            click_pos = mouse_pos
            if self.picker.Pick(click_pos[0], click_pos[1], 0, self.renderer):
                actor = self.picker.GetActor()
                cell_id = self.picker.GetCellId()
                if actor and cell_id >= 0:
                    self._handle_selection(actor, cell_id)

    def _handle_selection(self, actor, cell_id):
        # Caso: deseleccionar si ya estaba seleccionada la misma cara
        if self.last_selected_cell and self.last_selected_cell[1] == cell_id:
            print(f"❌ Cara (ID={cell_id}) deseleccionada.")
            if hasattr(self, "highlight_actor") and self.highlight_actor:
                self.renderer.RemoveActor(self.highlight_actor)
                self.highlight_actor = None                           ### aca se elimina el selecionado
                self.renderer.GetRenderWindow().Render()
            self.last_selected_cell = None
            return

        # Si había otra seleccionada, eliminar highlight previo
        if hasattr(self, "highlight_actor") and self.highlight_actor:
            self.renderer.RemoveActor(self.highlight_actor)

        dataset = actor.GetMapper().GetInput()
        cell = dataset.GetCell(cell_id)

        puntos = [cell.GetPoints().GetPoint(i) for i in range(cell.GetNumberOfPoints())]
        print(f"📌 Cara seleccionada (ID={cell_id}):")
        for p in puntos:
            print(f"   {p}")

        # Calcular ángulo mínimo de la celda

        angulos = []
        n = len(puntos)
        for i in range(n):
            p1 = puntos[i-1]  # Punto anterior
            p2 = puntos[i]    # Punto actual
            p3 = puntos[(i+1) % n]  # Punto siguiente
            angulo = calcular_angulo(p1, p2, p3)
            angulos.append(angulo)
        min_angle_rad = min(angulos)
        min_angle_deg = math.degrees(min_angle_rad)
        print(f"🔢 Ángulo mínimo de la celda: {min_angle_deg:.2f}°")

        # Crear highlight para la nueva selección
        poly = vtk.vtkPolyData()
        points = vtk.vtkPoints()
        ids = vtk.vtkIdList()

        for i, p in enumerate(puntos):
            points.InsertNextPoint(p)
            ids.InsertNextId(i)

        cells = vtk.vtkCellArray()
        cells.InsertNextCell(ids)

        poly.SetPoints(points)
        poly.SetPolys(cells)

        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(poly)

        highlight_actor = vtk.vtkActor()
        highlight_actor.SetMapper(mapper)
        highlight_actor.GetProperty().SetColor(1, 1, 0)
        highlight_actor.GetProperty().SetLineWidth(3)
        highlight_actor.GetProperty().EdgeVisibilityOn()

        self.renderer.AddActor(highlight_actor)
        self.highlight_actor = highlight_actor
        self.renderer.GetRenderWindow().Render()

        self.last_selected_cell = (puntos, cell_id)
          # Emitir la señal con los datos calculados
        notifier.cell_selected.emit(cell_id, len(puntos), min_angle_deg)
        print(f"📌 Cara seleccionada (ID={cell_id}) registrada para cámara.")

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
