import os
import re
import glob
import vtk
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QMenu, QLabel, QListWidget, QListWidgetItem, QSplitter, QMessageBox, QSizePolicy, QStyle, QTabWidget, QDialog)
from PyQt5.QtCore import Qt, QTimer
from app.visualization.RefinementViewer import RefinementViewer
from app.visualization.BaseViewer import BaseViewer
from app.visualization.FeriaVTK import ModelSwitcher, CustomInteractorStyle
from app.logic.mesh_generator import MeshGeneratorController
from app.interface.options_dialog import OpcionesDialog
from app.interface.panel_derecho import PanelDerecho
from app.visualization.vtkplayer import VTKPlayer

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MeshStep")
        self.resize(1280, 720)

        self.ignorar_limite_hardware = False

        self.boton_opciones = QPushButton("Opciones", self)
        self.boton_opciones.clicked.connect(self.abrir_opciones_dialog)

        self.boton_cargar = QPushButton("Cargar archivos", self)
        self.boton_cargar.clicked.connect(self.abrir_dialogo_carga)

        self.lista_archivos = QListWidget()
        self.lista_archivos.itemClicked.connect(self.mostrar_contenido)
        self.lista_archivos.setContextMenuPolicy(Qt.CustomContextMenu)
        self.lista_archivos.customContextMenuRequested.connect(self.mostrar_menu_contextual)

        self.panel_derecho = PanelDerecho(self)

        self.rutas_archivos = {}
        self.rutas_octree = {}

        # Panel central: pestañas
        self.refinement_viewer = RefinementViewer(self)
        self.vtk_player = VTKPlayer(self)
        self.tab_widget = QTabWidget()
        self.tab_widget.addTab(self.refinement_viewer, "Niveles de refinación")
        self.tab_widget.addTab(self.vtk_player, "Paso a paso")
        self.tab_widget.currentChanged.connect(self.cambiar_visualizador)

        self.panel_central = QWidget()
        central_layout = QVBoxLayout()
        central_layout.addWidget(self.tab_widget)
        self.panel_central.setLayout(central_layout)

        splitter = QSplitter(Qt.Horizontal)
        panel_izquierdo = QWidget()
        layout_izquierdo = QVBoxLayout()
        layout_izquierdo.addWidget(self.boton_opciones)
        layout_izquierdo.addWidget(self.boton_cargar)
        layout_izquierdo.addWidget(self.lista_archivos)
        panel_izquierdo.setLayout(layout_izquierdo)

        splitter.addWidget(panel_izquierdo)
        splitter.addWidget(self.panel_central)
        splitter.addWidget(self.panel_derecho)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        splitter.setStretchFactor(2, 1)

        layout = QVBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)
        self.setAcceptDrops(True)

        self.switcher = None
        self.refinement_viewer.actualizar_panel_derecho = self.panel_derecho.actualizar_panel
    # Este método se encarga de leer el archivo _histo.txt y actualizar el panel derecho con los ángulos

    # Métodos para cada acción

    # Moverse entre los poly
    # def accion_n(self):
    #     if not self.switcher:
    #         return
    #     polys_cargados = list(self.switcher.file_dict.keys())
    #     if not polys_cargados:
    #         return
        
    #     try:
    #         i = polys_cargados.index(self.switcher.current_poly)
    #         next_index = (i + 1) % len(polys_cargados)
    #         next_poly = polys_cargados[next_index]
    #     except ValueError:
    #         next_poly = polys_cargados[0]
        
    #     archivos = self.switcher.file_dict.get(next_poly, [])
    #     if archivos:
    #         self.switcher.current_poly = next_poly
    #         self.switcher.current_index = 0
    #         self.switcher._load_current()
    #         self.actualizar_panel_derecho(archivos[0])

    #         items = self.lista_archivos.findItems(next_poly, Qt.MatchExactly)
    #         if items:
    #             self.lista_archivos.setCurrentItem(items[0])
            
    #         # Eliminar los puntos críticos si están
    #         self.switcher.toggle_load = False
    #         self.switcher.clear_extra_models()

    #     # if self.switcher:
    #     #     self.switcher.current_index = (self.switcher.current_index + 1) % len(self.switcher.file_list)
    #     #     self.switcher.load_model(self.switcher.file_list[self.switcher.current_index])
    #     #     self.switcher.clear_extra_models()
    #     #     self.switcher.toggle_load = False

    # #Toggle puntos críticos
    # def accion_a(self):
    #     if self.switcher:
    #         self.switcher.toggle_load = not self.switcher.toggle_load
    #         if self.switcher.toggle_load:
    #             print("Cargando puntos criticos...")
    #             self.switcher.marcar_angulos_extremos()
    #             self.renderer.GetRenderWindow().Render()
    #         else:
    #             print("Toggle desactivado puntos criticos.")
    #             self.switcher.clear_extra_models()
    #             self.renderer.GetRenderWindow().Render()

    # def accion_b(self):
    #     if self.switcher:
    #         self.switcher.clear_extra_models()

    # def accion_r(self):
    #     if self.switcher:
    #         print("🔁 Reseteando cámara y modelo")
    #         self.switcher.actor.SetOrientation(0, 0, 0)
    #         self.switcher.actor.SetPosition(0, 0, 0)
    #         self.switcher.actor.SetScale(1, 1, 1)
    #         self.renderer.ResetCamera()
    #         if isinstance(self.interactor.GetInteractorStyle(), CustomInteractorStyle):
    #             self.interactor.GetInteractorStyle().reset_camera_and_rotation()
    #         self.renderer.GetRenderWindow().Render()

    # def accion_w(self):
    #     if self.switcher:
    #         self.switcher.actor.GetProperty().SetRepresentationToWireframe()
    #         self.renderer.GetRenderWindow().Render()

    # def accion_s(self):
    #     if self.switcher:
    #         self.switcher.actor.GetProperty().SetRepresentationToSurface()
    #         self.renderer.GetRenderWindow().Render()

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            # Acepta solo si todos los archivos son .poly
            if all(url.toLocalFile().endswith('.poly') for url in urls):
                event.acceptProposedAction()

    def dropEvent(self, event):
        archivos = [url.toLocalFile() for url in event.mimeData().urls()]
        for archivo in archivos:
            self.procesar_archivo_arrastrado(archivo)
    
    def procesar_archivo_arrastrado(self, ruta_archivo):
        dialogo = MeshGeneratorController(self)
        dialogo.archivos_seleccionados = [ruta_archivo]
        dialogo.ruta_archivos.setText(ruta_archivo)

        if not ruta_archivo.endswith('.poly'):
            QMessageBox.critical(self, "Error", "El archivo no es un archivo .poly válido.")
            return

        if dialogo.exec_() == QDialog.Accepted:
            try:
                with open(ruta_archivo, 'r', encoding='utf-8') as f:
                    contenido = f.read()
                # Agregar a lista lateral
                nombre = os.path.basename(ruta_archivo)
                if nombre not in self.rutas_archivos:
                    self.rutas_archivos[nombre] = ruta_archivo
                    self.lista_archivos.addItem(nombre)
                # Mostrar en el panel central directamente (opcional)
                self.vista_texto.setPlainText(contenido)
            except Exception as e:
                QMessageBox.critical(self, "Error al leer archivo", str(e))
  
    def _encontrar_serie_completa(self, base_name, extension):
        """Encuentra todos los archivos de la misma serie numérica"""
        print(f"DEBUG: Buscando serie completa para: {base_name}_*.{extension}")
        
        # Patrones a buscar
        patterns = [
            f"{base_name}_*.{extension}",
            f"{base_name}-*.{extension}",
            f"{os.path.basename(base_name)}_*.{extension}",
            f"{os.path.basename(base_name)}-*.{extension}"
        ]
        
        # Directorio donde buscar
        search_dir = os.path.dirname(base_name) if os.path.dirname(base_name) else "."
        print(f"DEBUG: Buscando en directorio: {search_dir}")
        
        # Encontrar todos los archivos que coincidan
        all_files = []
        for pattern in patterns:
            full_pattern = os.path.join(search_dir, pattern)
            print(f"DEBUG: Buscando con patrón: {full_pattern}")
            all_files.extend(glob.glob(full_pattern))
        
        # Eliminar duplicados
        unique_files = list(set(all_files))
        print(f"DEBUG: Archivos encontrados: {unique_files}")
        
        # Ordenar numéricamente
        def extract_number(filepath):
            filename = os.path.basename(filepath)
            match = re.search(r'(\d+)\.'+extension+'$', filename)
            return int(match.group(1)) if match else 0
        
        try:
            unique_files.sort(key=extract_number)
            print(f"DEBUG: Archivos ordenados: {unique_files}")
            return unique_files
        except:
            print("DEBUG: Error al ordenar archivos")
            return []

    def _descomponer_nombre_archivo(self, filepath):
        """Extrae las partes del nombre del archivo para detectar números"""
        filename = os.path.basename(filepath)
        base_dir = os.path.dirname(filepath)
        
        # Busca patrones como: nombre_X.ext o nombre-X.ext (X es el número)
        match = re.match(r'^(.*?)[-_](\d+)\.([^.]+)$', filename)
        if match:
            base_name = match.group(1)
            number = int(match.group(2))
            extension = match.group(3)
            return (os.path.join(base_dir, base_name), number, extension)
        
        # Si no encuentra el patrón, devuelve None para el número
        base, ext = os.path.splitext(filename)
        return (os.path.join(base_dir, base), None, ext[1:] if ext else '')

    def _encontrar_archivo_numerado(self, base_name, number, extension):
        """Busca un archivo con el número especificado"""
        possible_paths = [
            f"{base_name}_{number}.{extension}",
            f"{base_name}-{number}.{extension}",
            f"{base_name}{number}.{extension}"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                return path
        return None

    def _cargar_archivo_numerado(self, filepath):
        """Carga un archivo y actualiza la interfaz"""
        # Verificar si el archivo ya está en la lista
        filename = os.path.basename(filepath)
        
        if filename not in self.rutas_archivos:
            # Si no está en la lista, agregarlo
            self.rutas_archivos[filename] = filepath
            self.lista_archivos.addItem(filename)
            if self.switcher:
                self.switcher.add_model(filepath)
        
        # Cargar el archivo
        if self.switcher:
            try:
                self.switcher.load_model(filepath)
                self.actualizar_panel_derecho(filepath)
                # Actualizar el índice actual al nuevo archivo
                if filepath in self.switcher.file_list:
                    self.switcher.current_index = self.switcher.file_list.index(filepath)
                self.renderer.GetRenderWindow().Render()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo cargar el archivo:\n{str(e)}")
  

        # 0: Niveles de refinación, 1: Paso a paso
        if index == 0:
            self.central_layout.removeWidget(self.base_viewer)
            self.base_viewer.hide()
            self.central_layout.addWidget(self.feria_vtk_widget)
            self.feria_vtk_widget.show()
        else:
            self.central_layout.removeWidget(self.feria_vtk_widget)
            self.feria_vtk_widget.hide()
            self.central_layout.addWidget(self.base_viewer)
            self.base_viewer.show()
    
    def abrir_dialogo_carga(self):
        dialogo = MeshGeneratorController(self, ignorar_limite=self.ignorar_limite_hardware)
        if dialogo.exec_() == QDialog.Accepted:
            if dialogo.cargar_sin_generar:
                archivo = dialogo.archivos_seleccionados[0]
                self.tab_widget.setCurrentIndex(1)
                self.base_viewer.load_poly_or_mdl(archivo)
                return

            ruta_poly = dialogo.archivos_seleccionados[0]
            nombre_poly = os.path.basename(ruta_poly)
            if dialogo.quadtree.isChecked():
                diccionario = self.rutas_archivos
                tipo = "2D"
            elif dialogo.octree.isChecked():
                diccionario = self.rutas_octree
                tipo = "3D"
            else:
                diccionario = self.rutas_archivos
                tipo = "2D"

            item_text = f"{nombre_poly} ({tipo})"
            if nombre_poly not in diccionario:
                diccionario[nombre_poly] = dialogo.generated_files
                item = QListWidgetItem(item_text)
                item.setData(Qt.UserRole, tipo)
                self.lista_archivos.addItem(item)

            # Actualiza el diccionario global de archivos
            # Si ya existe, actualiza; si no, agrega
            if not self.switcher:
                self.switcher = ModelSwitcher(
                    self.refinement_viewer.renderer,
                    self.refinement_viewer.interactor,
                    {nombre_poly: dialogo.generated_files}
                )
                self.refinement_viewer.set_switcher(self.switcher, poly_path=ruta_poly)
            else:
                self.switcher.file_dict[nombre_poly] = dialogo.generated_files
                self.refinement_viewer.poly_path = ruta_poly
                self.refinement_viewer._load_overlay_poly()

            # Selecciona el archivo recién cargado
            self.switcher.current_poly = nombre_poly
            self.switcher.current_index = 0
            self.switcher._load_current()
            self.refinement_viewer.actualizar_panel_derecho(dialogo.generated_files[0])

    def mostrar_contenido(self, item):
        nombre_poly = item.text().split(" ")[0]
        archivos_vtk = self.rutas_archivos.get(nombre_poly) or self.rutas_octree.get(nombre_poly)
        poly_path = None
        if nombre_poly in self.rutas_archivos:
            # Si guardas el path original en el diccionario, úsalo
            poly_path = self.rutas_archivos.get(nombre_poly + "_path", None)
            # Si no, reconstruye el path a partir del nombre
            if not poly_path:
                # Busca en el directorio data
                posibles = [os.path.join("data", nombre_poly), os.path.join("data", nombre_poly.replace(" ", ""))]
                for p in posibles:
                    if os.path.exists(p):
                        poly_path = p
                        break
        elif nombre_poly in self.rutas_octree:
            poly_path = self.rutas_octree.get(nombre_poly + "_path", None)
        # Si tienes el path, actualiza el overlay
        if poly_path:
            self.refinement_viewer.update_overlay_poly(poly_path)
        if archivos_vtk and self.switcher:
            self.switcher.current_poly = nombre_poly
            self.switcher.current_index = 0
            self.switcher._load_current()
            self.refinement_viewer.actualizar_panel_derecho(archivos_vtk[0])

    def mostrar_menu_contextual(self, posicion):
        item = self.lista_archivos.itemAt(posicion)
        if item:
            menu = QMenu()
            accion_eliminar = menu.addAction("Eliminar archivo de la lista")
            accion = menu.exec_(self.lista_archivos.mapToGlobal(posicion))
            if accion == accion_eliminar:
                nombre = item.text().split(" ")[0]
                if nombre in self.rutas_archivos:
                    del self.rutas_archivos[nombre]
                self.lista_archivos.takeItem(self.lista_archivos.row(item))

    def actualizar_panel_derecho(self, ruta_archivo):
        self.panel_derecho.actualizar_panel(ruta_archivo)

    # Navegación y animación (puedes mover la lógica a RefinementViewer si lo prefieres)
    def navegar_anterior(self):
        if not self.switcher:
            return
        archivos = self.switcher.file_dict.get(self.switcher.current_poly, [])
        if not archivos:
            return
        if self.switcher.current_index > 0:
            self.switcher.anterior_modelo()
            self.actualizar_panel_derecho(archivos[self.switcher.current_index])
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
            self.actualizar_panel_derecho(archivos[self.switcher.current_index])
            self.switcher.toggle_load = False
            self.switcher.clear_extra_models()
        else:
            QMessageBox.information(self, "Fin", "Ya estás en el último modelo.")

    def iniciar_animacion(self):
        if self.switcher and self.switcher.file_dict:
            self.refinement_viewer.boton_play.setEnabled(False)
            self.refinement_viewer.boton_pausa.setEnabled(True)
            self.timer_animacion.start()

    def detener_animacion(self):
        self.timer_animacion.stop()
        self.refinement_viewer.boton_play.setEnabled(True)
        self.refinement_viewer.boton_pausa.setEnabled(False)

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
            self.actualizar_panel_derecho(archivos[0])
            self.switcher.toggle_load = False
            self.switcher.clear_extra_models()
            items = self.lista_archivos.findItems(self.switcher.current_poly, Qt.MatchExactly)
            if items:
                self.lista_archivos.setCurrentItem(items[0])

    def abrir_opciones_dialog(self):
        dialog = OpcionesDialog(self)
        dialog.checkbox.setChecked(self.ignorar_limite_hardware)
        if dialog.exec_() == QDialog.Accepted:
            self.ignorar_limite_hardware = dialog.checkbox.isChecked()

    def cambiar_visualizador(self, index):
        # 0: Niveles de refinación, 1: Paso a paso
        if index == 0:
            self.refinement_viewer.vtk_widget.show()
            self.refinement_viewer.vtk_widget.GetRenderWindow().Render()
        else:
            self.vtk_player.vtk_widget.show()
            self.vtk_player.vtk_widget.GetRenderWindow().Render()
            self.vtk_player.run_script("a_output_3_quads.vtk", "historial_completo_new.txt")
            # Inicializa el interactor si es necesario
            try:
                self.vtk_player.vtk_widget.GetRenderWindow().GetInteractor().Initialize()
            except Exception:
                pass