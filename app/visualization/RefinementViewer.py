import os
import vtk
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import Qt, QTimer
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from app.visualization.FeriaVTK import ModelSwitcher, CustomInteractorStyle
from app.visualization.coloreo_metricas import colorear_celdas

def poly_to_vtk(filepath):

    points = vtk.vtkPoints()
    lines = vtk.vtkCellArray()

    with open(filepath, 'r') as f:
        lines_raw = f.readlines()

    # Buscar la línea con el número de puntos
    i = 0
    num_points = 0
    while i < len(lines_raw):
        line = lines_raw[i].strip()
        if line and not line.startswith('#'):
            parts = line.split()
            if len(parts) >= 2 and parts[0].isdigit():
                num_points = int(parts[0])
                i += 1
                break
        i += 1

    # Leer los puntos
    for _ in range(num_points):
        while i < len(lines_raw) and (not lines_raw[i].strip() or lines_raw[i].strip().startswith('#')):
            i += 1
        parts = lines_raw[i].strip().split()
        if len(parts) >= 3:
            x, y = float(parts[1]), float(parts[2])
            points.InsertNextPoint(x, y, 0)
        i += 1

    # Buscar la línea con el número de segmentos
    num_segments = 0
    while i < len(lines_raw):
        line = lines_raw[i].strip()
        if line and not line.startswith('#'):
            parts = line.split()
            if len(parts) >= 2 and parts[0].isdigit():
                num_segments = int(parts[0])
                i += 1
                break
        i += 1

    # Leer los segmentos y detectar el mínimo índice
    segment_indices = []
    segment_lines = []
    for _ in range(num_segments):
        while i < len(lines_raw) and (not lines_raw[i].strip() or lines_raw[i].strip().startswith('#')):
            i += 1
        parts = lines_raw[i].strip().split()
        if len(parts) >= 3:
            start_id = int(parts[1])
            end_id = int(parts[2])
            segment_indices.append(start_id)
            segment_indices.append(end_id)
            segment_lines.append((start_id, end_id))
        i += 1

    # Detecta si los índices empiezan en 1 (caso a.poly) o en 0 (caso pie.poly)
    min_index = min(segment_indices) if segment_indices else 0
    index_offset = 1 if min_index == 1 else 0

    # Agrega las líneas ajustando el offset
    for start_id, end_id in segment_lines:
        start_id_adj = start_id - index_offset
        end_id_adj = end_id - index_offset
        if 0 <= start_id_adj < points.GetNumberOfPoints() and 0 <= end_id_adj < points.GetNumberOfPoints():
            vtk_line = vtk.vtkLine()
            vtk_line.GetPointIds().SetId(0, start_id_adj)
            vtk_line.GetPointIds().SetId(1, end_id_adj)
            lines.InsertNextCell(vtk_line)

    polydata = vtk.vtkPolyData()
    polydata.SetPoints(points)
    polydata.SetLines(lines)
    return polydata

class RefinementViewer(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.panel_derecho = None
        self.vtk_widget = QVTKRenderWindowInteractor(self)
        self.renderer = vtk.vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)
        self.interactor = self.vtk_widget.GetRenderWindow().GetInteractor()
        self.interactor.SetInteractorStyle(CustomInteractorStyle(self.renderer))
        self.interactor.Initialize()
        self.switcher = None

        # Botones de navegación
        self.boton_anterior = QPushButton("Anterior")
        self.boton_siguiente = QPushButton("Siguiente")
        self.boton_play = QPushButton("Play")
        self.boton_pausa = QPushButton("Pausa")
        self.boton_reinicio = QPushButton("Reinicio")
        self.boton_overlay = QPushButton("Mostrar overlay")
        self.overlay_visible = False
        self.overlay_actor = None
        self.poly_path = None

        self.timer_animacion = QTimer(self)
        self.timer_animacion.setInterval(1500)
        self.timer_animacion.timeout.connect(self.avance_automatico)

        nav_layout = QHBoxLayout()
        nav_layout.addWidget(self.boton_anterior)
        nav_layout.addWidget(self.boton_siguiente)
        nav_layout.addWidget(self.boton_play)
        nav_layout.addWidget(self.boton_pausa)
        nav_layout.addWidget(self.boton_reinicio)
        nav_layout.addWidget(self.boton_overlay)

        layout = QVBoxLayout()
        layout.addWidget(self.vtk_widget)
        layout.addLayout(nav_layout)
        self.setLayout(layout)

        self.boton_anterior.clicked.connect(self.navegar_anterior)
        self.boton_siguiente.clicked.connect(self.navegar_siguiente)
        self.boton_play.clicked.connect(self.iniciar_animacion)
        self.boton_pausa.clicked.connect(self.detener_animacion)
        self.boton_reinicio.clicked.connect(self.reiniciar_secuencia)
        self.boton_overlay.clicked.connect(self.toggle_overlay)

    # def set_panel_derecho(self, panel):
    #     self.panel_derecho = panel

    def set_switcher(self, switcher, poly_path=None):
        self.switcher = switcher
        self.poly_path = poly_path
        self._load_overlay_poly()

    def _load_overlay_poly(self):
        # Cargar el poly original como overlay
        if self.poly_path and os.path.exists(self.poly_path):
            polydata = poly_to_vtk(self.poly_path)
            mapper = vtk.vtkPolyDataMapper()
            mapper.SetInputData(polydata)
            self.overlay_actor = vtk.vtkActor()
            self.overlay_actor.SetMapper(mapper)
            self.overlay_actor.GetProperty().SetColor(1, 1, 0)  # Amarillo
            self.overlay_actor.GetProperty().SetLineWidth(2)
            self.overlay_actor.GetProperty().SetOpacity(0.7)
            self.overlay_actor.VisibilityOff()
            self.renderer.AddActor(self.overlay_actor)

    def navegar_anterior(self):
        if not self.switcher:
            return
        archivos = self.switcher.file_dict.get(self.switcher.current_poly, [])
        if not archivos:
            return
        if self.switcher.current_index > 0:
            self.switcher.anterior_modelo()
            if self.panel_derecho:
                self.panel_derecho.actualizar_panel_derecho(archivos[self.switcher.current_index])
                self.panel_derecho.actualizar_estadisticas(self.switcher.metricas_actuales)
            self.switcher.toggle_load = False
            self.switcher.clear_extra_models()
        else:
            QMessageBox.information(self, "Inicio", "Ya estás en el primer modelo.")

    def navegar_siguiente(self):
        if not self.switcher:
            return
        archivos = self.switcher.file_dict.get(self.switcher.current_poly, [])
        if not archivos:
            return
        if self.switcher.current_index + 1 < len(archivos):
            self.switcher.siguiente_modelo()
            if self.panel_derecho:
                self.panel_derecho.actualizar_panel_derecho(archivos[self.switcher.current_index])
                self.panel_derecho.actualizar_estadisticas(self.switcher.metricas_actuales)
            self.switcher.toggle_load = False
            self.switcher.clear_extra_models()
        else:
            QMessageBox.information(self, "Fin", "Ya estás en el último modelo.")

    def iniciar_animacion(self):
        if self.switcher and self.switcher.file_dict:
            self.boton_play.setEnabled(False)
            self.boton_pausa.setEnabled(True)
            self.timer_animacion.start()

    def detener_animacion(self):
        self.timer_animacion.stop()
        self.boton_play.setEnabled(True)
        self.boton_pausa.setEnabled(False)

    def avance_automatico(self):
        if not self.switcher:
            self.detener_animacion()
            return
        archivos = self.switcher.file_dict.get(self.switcher.current_poly, [])
        if not archivos:
            self.detener_animacion()
            return
        if self.switcher.current_index + 1 >= len(archivos):
            self.reiniciar_secuencia()
        else:
            self.navegar_siguiente()

    def reiniciar_secuencia(self):
        if not self.switcher:
            return
        archivos = self.switcher.file_dict.get(self.switcher.current_poly, [])
        if archivos:
            self.switcher.current_index = 0
            self.switcher._load_current()
            if self.panel_derecho:
                self.panel_derecho.actualizar_panel_derecho(archivos[0])
                self.panel_derecho.actualizar_estadisticas(self.switcher.metricas_actuales)
            self.switcher.toggle_load = False
            self.switcher.clear_extra_models()

    def toggle_overlay(self):
        if self.overlay_actor:
            self.overlay_visible = not self.overlay_visible
            self.overlay_actor.SetVisibility(self.overlay_visible)
            self.boton_overlay.setText("Ocultar overlay" if self.overlay_visible else "Mostrar overlay")
            self.renderer.GetRenderWindow().Render()

    def update_overlay_poly(self, poly_path):
        self.poly_path = poly_path
        # Elimina el actor anterior si existe
        if self.overlay_actor:
            self.renderer.RemoveActor(self.overlay_actor)
            self.overlay_actor = None
        self._load_overlay_poly()
        self.overlay_visible = False
        self.boton_overlay.setText("Mostrar overlay")
        self.renderer.GetRenderWindow().Render()

    def accion_area(self):
        if not self.switcher:
            print("No hay modelo cargado.")
            return
        archivos = self.switcher.file_dict.get(self.switcher.current_poly, [])
        if archivos and 0 <= self.switcher.current_index < len(archivos):
            nombre = os.path.basename(archivos[self.switcher.current_index])
        else:
            print("No hay archivo actual.")
    # Métodos para cada acción
        input_path = "outputs/" + nombre
        output_path = "outputs/" + "color_" +nombre
        colorear_celdas(
            input_path, output_path,
            metric="area", bins=12,
            base_color=(0,255,0), end_color=(255,0,0)
        )   

        self.switcher.load_model(output_path)
        self.renderer.GetRenderWindow().Render()

    def accion_angulo_minimo(self):
        if not self.switcher:
            print("No hay modelo cargado.")
            return
        archivos = self.switcher.file_dict.get(self.switcher.current_poly, [])
        if archivos and 0 <= self.switcher.current_index < len(archivos):
            nombre = os.path.basename(archivos[self.switcher.current_index])
        else:
            print("No hay archivo actual.")
    # Métodos para cada acción
        input_path = "outputs/" +  nombre
        output_path = "outputs/" + "color_" + nombre
        colorear_celdas(
            input_path, output_path,
            metric="angle", bins=12,
            base_color=(0,255,0), end_color=(255,0,0)
        )

        self.switcher.load_model(output_path)
        self.renderer.GetRenderWindow().Render()

    def accion_relacion_aspecto(self):
        if not self.switcher:
            print("No hay modelo cargado.")
            return
        archivos = self.switcher.file_dict.get(self.switcher.current_poly, [])
        if archivos and 0 <= self.switcher.current_index < len(archivos):
            nombre = os.path.basename(archivos[self.switcher.current_index])
        else:
            print("No hay archivo actual.")
    # Métodos para cada acción
        input_path = "outputs/" + nombre
        output_path = "outputs/" + "color_" +nombre
        colorear_celdas(
            input_path, output_path,
            metric="aspect", bins=12,
            base_color=(0,255,0), end_color=(255,0,0)
        )

        self.switcher.load_model(output_path)
        self.renderer.GetRenderWindow().Render()

    def ajustar_velocidad(self, valor):
        """Ajusta la velocidad de la animación"""
        segundos = valor / 1000.0
        self.timer_animacion.setInterval(valor)
        self.panel_derecho.label_velocidad_valor.setText(f"{segundos:.1f}s")