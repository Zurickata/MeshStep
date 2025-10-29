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
    cell_deselected = pyqtSignal()  # Nueva señal para deselección

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


class CustomInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):
    def __init__(self, renderer, parent=None):
        super().__init__()
        self.renderer = renderer
        self.left_mouse_down = False
        self.last_pos = (0, 0)
        self.AddObserver("MouseMoveEvent", self.mouse_move_event)
        self.AddObserver("LeftButtonPressEvent", self.left_button_press_event)
        self.AddObserver("LeftButtonReleaseEvent", self.left_button_release_event)
        self.AddObserver("MiddleButtonPressEvent", self.middle_button_press_event)
        self.AddObserver("MiddleButtonReleaseEvent", self.middle_button_release_event)
        self.AddObserver("KeyPressEvent", self.on_key_press)

        self.picker = vtk.vtkCellPicker()
        self.last_selected_cell = None

        # Actors
        self._original_actor = None
        self._clip_actor = None
        self.highlight_actor = None
        self.edge_actor = None

        # Estado de visualización
        self.modo_visualizacion = "solido"  # "solido", "wireframe", "rayosX"
        self.cut_enabled = False

    # -------------------- Interacción con teclado --------------------
    def on_key_press(self, obj, event):
        key = self.GetInteractor().GetKeySym()
        if key.lower() == "e":
            self.seleccionar_celda_mouse()
        elif key.lower() == "c":
            self.cut_enabled = not self.cut_enabled
            self.toggle_cut_plane(self.cut_enabled)
            # Aplicar el modo visual actual al nuevo actor
            self.aplicar_modo_visualizacion()
        elif key.lower() == "w":
            self.modo_visualizacion = "wireframe"
            self.aplicar_modo_visualizacion()
        elif key.lower() == "s":
            self.modo_visualizacion = "solido"
            self.aplicar_modo_visualizacion()
        elif key.lower() == "x":
            self.modo_visualizacion = "rayosX"
            self.aplicar_modo_visualizacion()

    # -------------------- Selección de celdas --------------------
    def seleccionar_celda_mouse(self):
        mouse_pos = self.GetInteractor().GetEventPosition()
        if self.picker.Pick(mouse_pos[0], mouse_pos[1], 0, self.renderer):
            actor = self.picker.GetActor()
            cell_id = self.picker.GetCellId()
            if actor and cell_id >= 0:
                self._handle_selection(actor, cell_id)

    def _handle_selection(self, actor, cell_id):
        # Deseleccionar si ya estaba seleccionada
        if self.last_selected_cell and self.last_selected_cell[0] == cell_id:
            self._remove_highlight()
            self.last_selected_cell = None
            return

        self._remove_highlight()

        dataset = actor.GetMapper().GetInput()
        cell = dataset.GetCell(cell_id)
        cell_type = cell.GetCellType()

        # Crear grid temporal con la celda seleccionada
        ug = vtk.vtkUnstructuredGrid()
        pts = vtk.vtkPoints()
        for i in range(cell.GetNumberOfPoints()):
            pts.InsertNextPoint(cell.GetPoints().GetPoint(i))
        ug.SetPoints(pts)

        ids = vtk.vtkIdList()
        for i in range(cell.GetNumberOfPoints()):
            ids.InsertNextId(i)
        ug.InsertNextCell(cell_type, ids)

        # 🔧 Convertir a PolyData (sirve tanto para 2D como 3D)
        geom_filter = vtk.vtkGeometryFilter()
        geom_filter.SetInputData(ug)
        geom_filter.Update()
        poly = geom_filter.GetOutput()

        if poly.GetNumberOfPoints() == 0:
            print("⚠️ Celda seleccionada sin geometría visible (2D/3D no válido)")
            return

        # --- Superficie amarilla semi-transparente ---
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(poly)
        self.highlight_actor = vtk.vtkActor()
        self.highlight_actor.SetMapper(mapper)
        prop = self.highlight_actor.GetProperty()
        prop.SetColor(1.0, 1.0, 0.0)
        prop.SetOpacity(0.25)
        prop.BackfaceCullingOff()  # 🔧 importante para 2D
        self.renderer.AddActor(self.highlight_actor)

        # --- Aristas en naranja ---
        edge_extractor = vtk.vtkExtractEdges()
        edge_extractor.SetInputData(poly)
        edge_extractor.Update()
        edge_mapper = vtk.vtkPolyDataMapper()
        edge_mapper.SetInputConnection(edge_extractor.GetOutputPort())
        self.edge_actor = vtk.vtkActor()
        self.edge_actor.SetMapper(edge_mapper)
        self.edge_actor.GetProperty().SetColor(1.0, 0.2, 0.0)
        self.edge_actor.GetProperty().SetLineWidth(3.0)
        self.renderer.AddActor(self.edge_actor)

        puntos = [cell.GetPoints().GetPoint(i) for i in range(cell.GetNumberOfPoints())]

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

        self.renderer.GetRenderWindow().Render()
        self.last_selected_cell = (cell_id, cell_type)
        notifier.cell_selected.emit(cell_id, len(puntos), min_angle_deg)



    def _remove_highlight(self):
        if self.highlight_actor:
            self.renderer.RemoveActor(self.highlight_actor)
            self.highlight_actor = None
        if self.edge_actor:
            self.renderer.RemoveActor(self.edge_actor)
            self.edge_actor = None
        self.renderer.GetRenderWindow().Render()

    # -------------------- Wireframe / Solido / Rayos X --------------------
    def aplicar_modo_visualizacion(self):
        actor = self._clip_actor if self.cut_enabled and self._clip_actor else self._original_actor
        if not actor:
            return
        if self.modo_visualizacion == "wireframe":
            actor.GetProperty().SetRepresentationToWireframe()
            actor.GetProperty().SetOpacity(1.0)
        elif self.modo_visualizacion == "solido":
            actor.GetProperty().SetRepresentationToSurface()
            actor.GetProperty().SetOpacity(1.0)
        elif self.modo_visualizacion == "rayosX":
            actor.GetProperty().SetRepresentationToSurface()
            actor.GetProperty().SetOpacity(0.3)
        self.renderer.GetRenderWindow().Render()

    # -------------------- Plano de corte --------------------
    def toggle_cut_plane(self, enable: bool):
        if enable:
            if not self._original_actor:
                actors = self.renderer.GetActors()
                actors.InitTraversal()
                self._original_actor = actors.GetNextActor()
            if not self._original_actor:
                return

            mapper = self._original_actor.GetMapper()
            input_data = mapper.GetInput()

            plane = vtk.vtkPlane()
            bounds = input_data.GetBounds()
            center = [(bounds[0]+bounds[1])/2, (bounds[2]+bounds[3])/2, (bounds[4]+bounds[5])/2]
            plane.SetOrigin(center)
            plane.SetNormal(0,0,1)

            clip_filter = vtk.vtkClipDataSet()
            clip_filter.SetInputData(input_data)
            clip_filter.SetClipFunction(plane)
            clip_filter.Update()

            clip_mapper = vtk.vtkDataSetMapper()
            clip_mapper.SetInputConnection(clip_filter.GetOutputPort())

            self._clip_actor = vtk.vtkActor()
            self._clip_actor.SetMapper(clip_mapper)

            self.renderer.RemoveActor(self._original_actor)
            self.renderer.AddActor(self._clip_actor)
        else:
            if self._clip_actor:
                self.renderer.RemoveActor(self._clip_actor)
            if self._original_actor:
                self.renderer.AddActor(self._original_actor)
        self.aplicar_modo_visualizacion()
        self.renderer.GetRenderWindow().Render()

    # -------------------- Rotación y cámara --------------------
    def left_button_press_event(self, obj, event):
        self.OnMiddleButtonDown()
        self.last_pos = self.GetInteractor().GetEventPosition()
    def left_button_release_event(self, obj, event):
        self.OnMiddleButtonUp()
    def middle_button_press_event(self, obj, event):
        self.OnLeftButtonDown()
    def middle_button_release_event(self, obj, event):
        self.OnLeftButtonUp()
    def mouse_move_event(self, obj, event):
        if self.left_mouse_down:
            x, y = self.GetInteractor().GetEventPosition()
            dx = x - self.last_pos[0]
            dy = y - self.last_pos[1]
            cam = self.renderer.GetActiveCamera()
            cam.Azimuth(-dx*0.5)
            cam.Elevation(dy*0.5)
            cam.OrthogonalizeViewUp()
            self.renderer.ResetCameraClippingRange()
            self.GetInteractor().GetRenderWindow().Render()
            self.last_pos = (x,y)
        self.OnMouseMove()
    def reset_camera_and_rotation(self):
        cam = self.renderer.GetActiveCamera()
        cam.SetViewUp(0,1,0)
        cam.SetPosition(0,0,1)
        cam.SetFocalPoint(0,0,0)
        self.renderer.ResetCamera()
        self.GetInteractor().GetRenderWindow().Render()


# En FeriaVTK.py
class AxesOverlay:
    def __init__(self, renderer, interactor):
        self.renderer = renderer
        self.interactor = interactor

        # Crear ejes
        self.axes_actor = vtk.vtkAxesActor()
        self.axes_actor.SetTotalLength(0.3, 0.3, 0.3)
        self.axes_actor.SetShaftTypeToCylinder()
        self.axes_actor.SetCylinderRadius(0.01)
        self.axes_actor.SetConeRadius(0.04)
        self.axes_actor.SetSphereRadius(0.02)

        # Crear widget
        self.widget = vtk.vtkOrientationMarkerWidget()
        self.widget.SetOrientationMarker(self.axes_actor)
        self.widget.SetViewport(0.0, 0.0, 0.25, 0.25)
        self.widget.SetInteractor(self.interactor)
        self.widget.EnabledOff()
        self.widget.InteractiveOff()

        # Bind tecla T
        self.interactor.AddObserver("KeyPressEvent", self.toggle_visibility)

    def toggle_visibility(self, obj=None, event=None):
        key = self.interactor.GetKeySym().lower()
        if key == "t":
            if self.widget.GetEnabled():
                print("❌ Ejes desactivados")
                self.widget.EnabledOff()
            else:
                print("✅ Ejes activados")
                self.widget.EnabledOn()
            self.renderer.GetRenderWindow().Render()


#------------------------------------------ Main ---------------------------------------------------------------------------

def visualizar_vtk_unstructured_con_cambio_y_anadir(filenames):
    import vtk

    # ----------------------------- Renderer y ventana -----------------------------
    renderer = vtk.vtkRenderer()
    renderer.SetBackground(0.1, 0.2, 0.4)
    renderer.SetLayer(0)

    renderWindow = vtk.vtkRenderWindow()
    renderWindow.SetNumberOfLayers(2)
    renderWindow.AddRenderer(renderer)
    renderWindow.SetSize(800, 800)

    # ----------------------------- Interactor -----------------------------
    interactor = vtk.vtkRenderWindowInteractor()
    interactor.SetRenderWindow(renderWindow)

    # ----------------------------- Ejes -----------------------------
    axes_actor = vtk.vtkAxesActor()
    axes_actor.SetTotalLength(0.3, 0.3, 0.3)
    axes_actor.SetShaftTypeToCylinder()
    axes_actor.SetCylinderRadius(0.01)
    axes_actor.SetConeRadius(0.04)
    axes_actor.SetSphereRadius(0.02)

    axes_widget = vtk.vtkOrientationMarkerWidget()
    axes_widget.SetOrientationMarker(axes_actor)
    axes_widget.SetDefaultRenderer(renderer)
    axes_widget.SetViewport(0.0, 0.0, 0.25, 0.25)
    axes_widget.SetInteractor(interactor)
    axes_widget.EnabledOff()  # Inicialmente oculto
    axes_widget.InteractiveOff()

    # ----------------------------- Estilo custom -----------------------------
    custom_style = CustomInteractorStyle(renderer)
    interactor.SetInteractorStyle(custom_style)

    # ----------------------------- Model Switcher -----------------------------
    switcher = ModelSwitcher(renderer, interactor, filenames)

    # ----------------------------- Evento de tecla 't' -----------------------------
    def toggle_axes(obj, event):
        key = interactor.GetKeySym().lower()
        if key == "t":
            if axes_widget.GetEnabled():
                print("❌ Ejes desactivados")
                axes_widget.EnabledOff()
            else:
                print("✅ Ejes activados")
                axes_widget.EnabledOn()
            renderWindow.Render()

    interactor.AddObserver("KeyPressEvent", toggle_axes)

    # ----------------------------- Inicialización -----------------------------
    interactor.Initialize()
    renderer.ResetCamera()
    renderWindow.Render()
    interactor.Start()
