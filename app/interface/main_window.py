import os
import vtk
from PyQt5.QtWidgets import (QApplication, QDialog, QWidget, QVBoxLayout, QHBoxLayout,
                            QPushButton, QMenu, QLabel, QListWidget, QSplitter,
                            QMessageBox)
from PyQt5.QtCore import Qt
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from app.visualization.FeriaVTK import ModelSwitcher, CustomInteractorStyle
from app.logic.mesh_generator import MeshGeneratorController

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MeshStep")
        self.resize(1280, 720)

        self.boton_cargar = QPushButton("Cargar archivos", self)
        self.boton_cargar.clicked.connect(self.abrir_dialogo_carga)

        self.lista_archivos = QListWidget()
        self.lista_archivos.itemClicked.connect(self.mostrar_contenido)
        self.lista_archivos.setContextMenuPolicy(Qt.CustomContextMenu)
        self.lista_archivos.customContextMenuRequested.connect(self.mostrar_menu_contextual)

        # NUEVOS BOTONES PARA ACCIONES
        self.boton_n = QPushButton("Siguiente modelo (n)", self)
        self.boton_n.clicked.connect(self.accion_n)

        self.boton_a = QPushButton("Toggle puntos críticos (a)", self)
        self.boton_a.clicked.connect(self.accion_a)

        self.boton_b = QPushButton("Borrar extras (b)", self)
        self.boton_b.clicked.connect(self.accion_b)

        self.boton_r = QPushButton("Reset cámara/modelo (r)", self)
        self.boton_r.clicked.connect(self.accion_r)

        self.boton_w = QPushButton("Wireframe (w)", self)
        self.boton_w.clicked.connect(self.accion_w)

        self.boton_s = QPushButton("Sólido (s)", self)
        self.boton_s.clicked.connect(self.accion_s)

        self.rutas_archivos = {}

        self.vtk_widget = QVTKRenderWindowInteractor(self)
        self.renderer = vtk.vtkRenderer()
        self.vtk_widget.GetRenderWindow().AddRenderer(self.renderer)
        self.interactor = self.vtk_widget.GetRenderWindow().GetInteractor()
        self.interactor.SetInteractorStyle(CustomInteractorStyle(self.renderer))
        self.interactor.Initialize()

        self.switcher = None

        splitter = QSplitter(Qt.Horizontal)

        panel_izquierdo = QWidget()
        layout_izquierdo = QVBoxLayout()
        layout_izquierdo.addWidget(self.boton_cargar)
        layout_izquierdo.addWidget(self.lista_archivos)
        panel_izquierdo.setLayout(layout_izquierdo)

        panel_central = self.vtk_widget

        panel_derecho = QWidget()
        layout_derecho = QVBoxLayout()
        label_derecho = QLabel("Soy el panel derecho onda\naqui van las metricas y eso :p\n\npero mira intenta arrastrar los bordes\nes bacan igual")
        label_derecho.setAlignment(Qt.AlignCenter)
        layout_derecho.addWidget(label_derecho)
        layout_derecho.addWidget(self.boton_n)
        layout_derecho.addWidget(self.boton_a)
        layout_derecho.addWidget(self.boton_b)
        layout_derecho.addWidget(self.boton_r)
        layout_derecho.addWidget(self.boton_w)
        layout_derecho.addWidget(self.boton_s)
        panel_derecho.setLayout(layout_derecho)

        splitter.addWidget(panel_izquierdo)
        splitter.addWidget(panel_central)
        splitter.addWidget(panel_derecho)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        splitter.setStretchFactor(2, 1)

        layout = QVBoxLayout()
        layout.addWidget(splitter)
        self.setLayout(layout)
        self.setAcceptDrops(True)

    # Métodos para cada acción
    def accion_n(self):
        if self.switcher:
            self.switcher.current_index = (self.switcher.current_index + 1) % len(self.switcher.file_list)
            self.switcher.load_model(self.switcher.file_list[self.switcher.current_index])
            self.switcher.clear_extra_models()
            self.switcher.toggle_load = False

    def accion_a(self):
        if self.switcher:
            self.switcher.toggle_load = not self.switcher.toggle_load
            if self.switcher.toggle_load:
                print("Cargando puntos criticos...")
                self.switcher.marcar_angulos_extremos()
                self.renderer.GetRenderWindow().Render()
            else:
                print("Toggle desactivado puntos criticos.")
                self.switcher.clear_extra_models()
                self.renderer.GetRenderWindow().Render()

    def accion_b(self):
        if self.switcher:
            self.switcher.clear_extra_models()

    def accion_r(self):
        if self.switcher:
            print("🔁 Reseteando cámara y modelo")
            self.switcher.actor.SetOrientation(0, 0, 0)
            self.switcher.actor.SetPosition(0, 0, 0)
            self.switcher.actor.SetScale(1, 1, 1)
            self.renderer.ResetCamera()
            if isinstance(self.interactor.GetInteractorStyle(), CustomInteractorStyle):
                self.interactor.GetInteractorStyle().reset_camera_and_rotation()
            self.renderer.GetRenderWindow().Render()

    def accion_w(self):
        if self.switcher:
            self.switcher.actor.GetProperty().SetRepresentationToWireframe()
            self.renderer.GetRenderWindow().Render()

    def accion_s(self):
        if self.switcher:
            self.switcher.actor.GetProperty().SetRepresentationToSurface()
            self.renderer.GetRenderWindow().Render()

    def abrir_dialogo_carga(self):
        dialogo = MeshGeneratorController(self)
        if dialogo.exec_() == QDialog.Accepted:
            if not self.switcher:
                self.switcher = ModelSwitcher(self.renderer, self.interactor, dialogo.generated_files)
            else:
                for ruta in dialogo.generated_files:
                    self.switcher.add_model(ruta)

            for ruta in dialogo.generated_files:
                nombre = os.path.basename(ruta)
                print("Ruta (dialog):", ruta)
                print("Nombre:", nombre)
                if nombre not in self.rutas_archivos:
                    self.rutas_archivos[nombre] = ruta
                    self.lista_archivos.addItem(nombre)
        print(dialogo.generated_files)

    def mostrar_contenido(self, item):
        nombre = item.text()
        ruta = self.rutas_archivos.get(nombre)
        if ruta and self.switcher:
            self.switcher.load_model(ruta)

    def mostrar_menu_contextual(self, posicion):
        item = self.lista_archivos.itemAt(posicion)
        if item:
            menu = QMenu()
            accion_eliminar = menu.addAction("Eliminar archivo de la lista")
            accion = menu.exec_(self.lista_archivos.mapToGlobal(posicion))
            if accion == accion_eliminar:
                nombre = item.text()
                if nombre in self.rutas_archivos:
                    del self.rutas_archivos[nombre]
                self.lista_archivos.takeItem(self.lista_archivos.row(item))
                
                # Limpiar el panel central si estaba mostrando el archivo eliminado
                if self.vista_texto.toPlainText():
                    self.vista_texto.clear()

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
    