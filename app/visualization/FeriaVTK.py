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

# ------------------------- NUEVAS FUNCIONES PARA MÉTRICAS DE CALIDAD USANDO VTK -------------------------

def calcular_metricas_calidad(grid):
    """
    Calcula métricas de calidad para triángulos y cuadriláteros usando filtros VTK
    Retorna un diccionario con estadísticas para cada tipo de elemento
    """
    if grid.GetNumberOfCells() == 0:
        return {"error": "No hay celdas en la malla"}
    
    resultados = {
        'triangulos': defaultdict(list),
        'cuadrilateros': defaultdict(list),
        'estadisticas_generales': {}
    }
    
    # Contar tipos de elementos y separar celdas por tipo
    triangulos = []
    cuadrilateros = []
    
    for i in range(grid.GetNumberOfCells()):
        cell = grid.GetCell(i)
        if cell.GetCellType() == vtk.VTK_TRIANGLE:
            triangulos.append(i)
        elif cell.GetCellType() == vtk.VTK_QUAD:
            cuadrilateros.append(i)
    
    resultados['estadisticas_generales']['total_triangulos'] = len(triangulos)
    resultados['estadisticas_generales']['total_cuadrilateros'] = len(cuadrilateros)
    
    # Métricas para triángulos
    if triangulos:
        triangulo_metrics = _calcular_metricas_triangulos(grid, triangulos)
        resultados['triangulos'] = triangulo_metrics
    
    # Métricas para cuadriláteros
    if cuadrilateros:
        quad_metrics = _calcular_metricas_cuadrilateros(grid, cuadrilateros)
        resultados['cuadrilateros'] = quad_metrics
    
    return resultados

def _calcular_metricas_triangulos(grid, triangulo_indices):
    """Calcula métricas de calidad específicas para triángulos"""
    metrics = defaultdict(list)
    
    if not triangulo_indices:
        return metrics
    
    # Crear un grid temporal solo con triángulos
    triangle_points = vtk.vtkPoints()
    triangle_cells = vtk.vtkCellArray()
    triangle_grid = vtk.vtkUnstructuredGrid()
    
    point_id_map = {}
    new_point_id = 0
    
    # Extraer triángulos y sus puntos
    for cell_id in triangulo_indices:
        cell = grid.GetCell(cell_id)
        triangle_cell = vtk.vtkTriangle()
        
        for i in range(cell.GetNumberOfPoints()):
            point_id = cell.GetPointId(i)
            point = grid.GetPoint(point_id)
            
            if point_id not in point_id_map:
                point_id_map[point_id] = new_point_id
                triangle_points.InsertNextPoint(point)
                new_point_id += 1
            
            triangle_cell.GetPointIds().SetId(i, point_id_map[point_id])
        
        triangle_cells.InsertNextCell(triangle_cell)
    
    triangle_grid.SetPoints(triangle_points)
    triangle_grid.SetCells(vtk.VTK_TRIANGLE, triangle_cells)
    
    # Calcular área
    area_filter = vtk.vtkMeshQuality()
    area_filter.SetInputData(triangle_grid)
    area_filter.SetTriangleQualityMeasureToArea()
    area_filter.Update()
    area_array = area_filter.GetOutput().GetCellData().GetArray("Quality")
    
    # Calcular aspect ratio
    aspect_filter = vtk.vtkMeshQuality()
    aspect_filter.SetInputData(triangle_grid)
    aspect_filter.SetTriangleQualityMeasureToAspectRatio()
    aspect_filter.Update()
    aspect_array = aspect_filter.GetOutput().GetCellData().GetArray("Quality")
    
    # Calcular ángulos mínimos y máximos
    min_angle_filter = vtk.vtkMeshQuality()
    min_angle_filter.SetInputData(triangle_grid)
    min_angle_filter.SetTriangleQualityMeasureToMinAngle()
    min_angle_filter.Update()
    min_angle_array = min_angle_filter.GetOutput().GetCellData().GetArray("Quality")
    
    max_angle_filter = vtk.vtkMeshQuality()
    max_angle_filter.SetInputData(triangle_grid)
    max_angle_filter.SetTriangleQualityMeasureToMaxAngle()
    max_angle_filter.Update()
    max_angle_array = max_angle_filter.GetOutput().GetCellData().GetArray("Quality")
    
    # Almacenar todas las métricas
    for i in range(len(triangulo_indices)):
        metrics['area'].append(area_array.GetValue(i))
        metrics['aspect_ratio'].append(aspect_array.GetValue(i))
        metrics['min_angle'].append(min_angle_array.GetValue(i))
        metrics['max_angle'].append(max_angle_array.GetValue(i))
    
    # Calcular estadísticas
    stats = {}
    for metric_name, values in metrics.items():
        if values:
            stats[f'{metric_name}_min'] = min(values)
            stats[f'{metric_name}_max'] = max(values)
            stats[f'{metric_name}_avg'] = sum(values) / len(values)
            stats[f'{metric_name}_std'] = np.std(values) if len(values) > 1 else 0
    
    # Combinar las métricas con las estadísticas
    metrics.update(stats)
    
    return metrics

def _calcular_metricas_cuadrilateros(grid, quad_indices):
    """Calcula métricas de calidad específicas para cuadriláteros"""
    metrics = defaultdict(list)
    
    if not quad_indices:
        return metrics
    
    # Crear un grid temporal solo con cuadriláteros
    quad_points = vtk.vtkPoints()
    quad_cells = vtk.vtkCellArray()
    quad_grid = vtk.vtkUnstructuredGrid()
    
    point_id_map = {}
    new_point_id = 0
    
    # Extraer cuadriláteros y sus puntos
    for cell_id in quad_indices:
        cell = grid.GetCell(cell_id)
        quad_cell = vtk.vtkQuad()
        
        for i in range(cell.GetNumberOfPoints()):
            point_id = cell.GetPointId(i)
            point = grid.GetPoint(point_id)
            
            if point_id not in point_id_map:
                point_id_map[point_id] = new_point_id
                quad_points.InsertNextPoint(point)
                new_point_id += 1
            
            quad_cell.GetPointIds().SetId(i, point_id_map[point_id])
        
        quad_cells.InsertNextCell(quad_cell)
    
    quad_grid.SetPoints(quad_points)
    quad_grid.SetCells(vtk.VTK_QUAD, quad_cells)
    
    # Calcular área
    area_filter = vtk.vtkMeshQuality()
    area_filter.SetInputData(quad_grid)
    area_filter.SetQuadQualityMeasureToArea()
    area_filter.Update()
    area_array = area_filter.GetOutput().GetCellData().GetArray("Quality")
    
    # Calcular aspect ratio
    aspect_filter = vtk.vtkMeshQuality()
    aspect_filter.SetInputData(quad_grid)
    aspect_filter.SetQuadQualityMeasureToAspectRatio()
    aspect_filter.Update()
    aspect_array = aspect_filter.GetOutput().GetCellData().GetArray("Quality")
    
    # Calcular distorsión (skew)
    skew_filter = vtk.vtkMeshQuality()
    skew_filter.SetInputData(quad_grid)
    skew_filter.SetQuadQualityMeasureToSkew()
    skew_filter.Update()
    skew_array = skew_filter.GetOutput().GetCellData().GetArray("Quality")
    
    # Calcular relación de aspecto (edge ratio)
    edge_ratio_filter = vtk.vtkMeshQuality()
    edge_ratio_filter.SetInputData(quad_grid)
    edge_ratio_filter.SetQuadQualityMeasureToEdgeRatio()
    edge_ratio_filter.Update()
    edge_ratio_array = edge_ratio_filter.GetOutput().GetCellData().GetArray("Quality")
    
    # Almacenar todas las métricas
    for i in range(len(quad_indices)):
        metrics['area'].append(area_array.GetValue(i))
        metrics['aspect_ratio'].append(aspect_array.GetValue(i))
        metrics['skew'].append(skew_array.GetValue(i))
        metrics['edge_ratio'].append(edge_ratio_array.GetValue(i))
    
    # Calcular estadísticas
    stats = {}
    for metric_name, values in metrics.items():
        if values:
            stats[f'{metric_name}_min'] = min(values)
            stats[f'{metric_name}_max'] = max(values)
            stats[f'{metric_name}_avg'] = sum(values) / len(values)
            stats[f'{metric_name}_std'] = np.std(values) if len(values) > 1 else 0
    
    # Combinar las métricas con las estadísticas
    metrics.update(stats)
    
    
    return metrics

def mostrar_metricas_calidad(metricas):
    """Muestra las métricas de calidad en el panel derecho en formato HTML"""
    
    if not metricas or 'error' in metricas:
        html = """
        <div style='background-color: #2a2a2a; padding: 12px; border-radius: 6px; font-family: monospace; color: #ff6b6b;'>
            <b>❌ No hay métricas disponibles</b><br>
            Carga un modelo primero o verifica el archivo.
        </div>
        """
        panel_label.setText(html)
        return
    
    stats = metricas['estadisticas_generales']
    total_triangulos = stats.get('total_triangulos', 0)
    total_cuadrilateros = stats.get('total_cuadrilateros', 0)
    total_caras = total_triangulos + total_cuadrilateros
    
    # Calcular porcentajes
    porc_triangulos = (total_triangulos / total_caras * 100) if total_caras > 0 else 0
    porc_cuadrilateros = (total_cuadrilateros / total_caras * 100) if total_caras > 0 else 0
    
    # Preparar HTML base
    html = f"""
    <div style='background-color: #2a2a2a; padding: 12px; border-radius: 6px; font-family: monospace;'>
        <b style='color: #ffffff;'>Topología:</b><br>
        • Vértices: <span style='color: #4ecdc4;'>N/A</span><br>
        • Caras: <span style='color: #4ecdc4;'>{total_caras}</span><br>
        • Triángulos: <span style='color: #ff9f43;'>{total_triangulos}</span> ({porc_triangulos:.1f}%)<br>
        • Cuadriláteros: <span style='color: #ff9f43;'>{total_cuadrilateros}</span> ({porc_cuadrilateros:.1f}%)<br><br>
        
        <b style='color: #ffffff;'>Calidad:</b><br>
    """
    
    # Añadir métricas de triángulos si existen
    if metricas['triangulos']:
        triangulos = metricas['triangulos']
        html += f"""
        <b>Triángulos:</b><br>
        • Relación aspecto: <span style='color: #4ecdc4;'>{triangulos.get('aspect_ratio_avg', 'N/A'):.3f}</span><br>
        • Ángulo mínimo: <span style='color: #4ecdc4;'>{triangulos.get('min_angle_avg', 'N/A'):.1f}°</span><br>
        • Ángulo máximo: <span style='color: #4ecdc4;'>{triangulos.get('max_angle_avg', 'N/A'):.1f}°</span><br>
        • Área promedio: <span style='color: #4ecdc4;'>{triangulos.get('area_avg', 'N/A'):.6f}</span><br>
        """
    
    # Añadir métricas de cuadriláteros si existen
    if metricas['cuadrilateros']:
        cuadrilateros = metricas['cuadrilateros']
        html += f"""
        <b>Cuadriláteros:</b><br>
        • Relación aspecto: <span style='color: #4ecdc4;'>{cuadrilateros.get('aspect_ratio_avg', 'N/A'):.3f}</span><br>
        • Distorsión: <span style='color: #ff6b6b;'>{cuadrilateros.get('skew_avg', 'N/A'):.3f}</span><br>
        • Relación aristas: <span style='color: #4ecdc4;'>{cuadrilateros.get('edge_ratio_avg', 'N/A'):.3f}</span><br>
        • Área promedio: <span style='color: #4ecdc4;'>{cuadrilateros.get('area_avg', 'N/A'):.6f}</span><br>
        """
    
    html += "</div>"
    


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
        mostrar_metricas_calidad(self.metricas_actuales)

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

        elif key == 'm':  # Nueva tecla para mostrar métricas
            print("\n" + "="*60)
            print("MOSTRANDO MÉTRICAS DE CALIDAD ACTUALES")
            print("="*60)
            if self.metricas_actuales:
                mostrar_metricas_calidad(self.metricas_actuales)
            else:
                print("No hay métricas disponibles. Carga un modelo primero.")


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