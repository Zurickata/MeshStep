import sys
import time
import vtk
import os
from app.visualization.FeriaVTK import ModelSwitcher, CustomInteractorStyle
from core.wrapper import QuadtreeWrapper
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel,
    QFileDialog, QDialog, QSpinBox, QMessageBox, QListWidget, QSplitter, QListWidgetItem, QMenu, QFrame
)
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

class CargarArchivoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Cargar archivos")
        self.resize(400, 300)

        # variables para refinacion rutas labels y cosas
        self.archivos_seleccionados = []
        self.nivel_refinamiento = 1

        self.ruta_archivos = QLabel("Ningún archivo seleccionado")

        # Definir y conectar el boton pa abrir el exporador
        self.boton_seleccionar = QPushButton("Seleccionar archivos")
        self.boton_seleccionar.clicked.connect(self.abrir_explorador)

        self.label_refinamiento = QLabel("Nivel de refinamiento:")
        self.spin_refinamiento = QSpinBox()
        self.spin_refinamiento.setRange(1, 100)
        self.spin_refinamiento.setValue(1)
        self.spin_refinamiento.valueChanged.connect(self.verificar_refinamiento)

        self.boton_confirmar = QPushButton("Confirmar")
        # self.boton_confirmar.clicked.connect(self.confirmar_datos)
        self.boton_confirmar.clicked.connect(self.run_mesh_generation)

        self.status_label = QLabel("Presiona 'Generar Mallas' para comenzar")
        self.status_label.setWordWrap(True)

        self.time_label = QLabel("Tiempo de ejecución: -")
        self.time_label.setStyleSheet("font-weight: bold; color: #2E86C1;")

        layout = QVBoxLayout()
        layout.addWidget(self.boton_seleccionar)
        layout.addWidget(self.ruta_archivos)
        layout.addWidget(self.label_refinamiento)
        layout.addWidget(self.spin_refinamiento)
        layout.addWidget(self.boton_confirmar)
        layout.addSpacing(20)
        layout.addWidget(self.status_label)
        layout.addWidget(self.time_label)
        layout.addWidget(QLabel("Archivos generados:"))
        layout.addWidget(self.file_list)
        self.setLayout(layout)

        # Inicializar el mesher
        self.mesher = QuadtreeWrapper()
        self.generated_files = []

    def abrir_explorador(self):
        archivos, _ = QFileDialog.getOpenFileNames(
            self,
            "Selecciona archivos",
            "",
            "Archivos .poly (*.poly)"
        )
        if archivos:
            self.archivos_seleccionados = archivos
            self.ruta_archivos.setText(f"{len(archivos)} archivo(s) seleccionados")

    def verificar_refinamiento(self):
        valor = self.spin_refinamiento.value()
        if valor > 10:
            QMessageBox.warning(
                self,
                "Advertencia",
                "Los niveles altos de refinamiento (>10) pueden requerir mucha memoria RAM."
            )

    def confirmar_datos(self):
        if not self.archivos_seleccionados:
            QMessageBox.critical(self, "Error", "Debes seleccionar al menos un archivo .poly antes de confirmar.")
            return

        self.nivel_refinamiento = self.spin_refinamiento.value()

        QMessageBox.information(
            self,
            "Confirmación",
            f"Se cargaron {len(self.archivos_seleccionados)} archivo(s) con nivel de refinamiento: {self.nivel_refinamiento}"
        )
        self.accept()

    def run_mesh_generation(self):
        # Confirmación de Datos (Inputs)
        if not self.archivos_seleccionados:
            QMessageBox.critical(self, "Error", "Debes seleccionar al menos un archivo .poly antes de confirmar.")
            return

        max_refinement = self.refinement_spinbox.value()
        input_file = self.archivos_seleccionados

        QMessageBox.information(
            self,
            "Confirmación",
            f"Se cargaron {len(self.archivos_seleccionados)} archivo(s) con nivel de refinamiento: {self.nivel_refinamiento}"
        )

        # Iniciar cronómetro
        start_time = time.time()
        level_times = []
        self.generated_files = []

        # # input_file = "core/quadtree/data/a.poly"
        # input_file = self.archivos_seleccionados[0]
        # print(input_file[0])
        
        self.status_label.setText(f"Generando mallas desde nivel 1 hasta {max_refinement}...")
        self.time_label.setText("Tiempo de ejecución: calculando...")
        QApplication.processEvents()
        
        try:
            for level in range(1, max_refinement + 1):
                level_start = time.time()
                output_name = f"output_{level}"
                
                self.status_label.setText(f"Procesando nivel {level}/{max_refinement}...")
                QApplication.processEvents()
                
                # Ejecutar el mesher
                result_file = self.mesher.generate_mesh(
                    input_file=input_file,
                    output_file=output_name,
                    refinement_level=level,
                    show_quality_metrics=False
                )
                
                level_time = time.time() - level_start
                level_times.append(level_time)
                self.generated_files.append(result_file)
                
                print(f"Nivel {level} completado en {level_time:.2f} segundos")
                self.status_label.setText(
                    f"Nivel {level}/{max_refinement} completado en {level_time:.2f}s\n"
                    f"Archivo: {result_file}"
                )
                QApplication.processEvents()
            
            # Calcular tiempos totales
            total_time = time.time() - start_time
            avg_time = total_time / max_refinement
            
            # Mostrar resultados en terminal
            print("\n" + "="*50)
            print(f"RESUMEN DE TIEMPOS:")
            print(f"- Niveles completados: {max_refinement}")
            print(f"- Tiempo total: {total_time:.2f} segundos")
            print(f"- Tiempo promedio por nivel: {avg_time:.2f} segundos")
            print("="*50 + "\n")
            
            # Mostrar en la interfaz
            time_report = (
                f"Tiempo total: {total_time:.2f} segundos\n"
                f"Tiempo promedio por nivel: {avg_time:.2f} segundos"
            )
            
            self.time_label.setText(time_report)
            self.status_label.setText(
                f"Proceso completado para {max_refinement} niveles\n"
                f"{time_report}"
            )
            
            # Actualizar lista y visualizador
            self.update_file_list()
            self.initialize_switcher()

            QMessageBox.information(
                self, 
                "Proceso completado", 
                f"Se generaron {max_refinement} mallas en {total_time:.2f} segundos\n"
                f"({avg_time:.2f} segundos por nivel en promedio)"
            )
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            error_msg = (
                f"Error después de {elapsed_time:.2f} segundos:\n"
                f"{str(e)}"
            )
            
            print(f"ERROR: {error_msg}")
            self.time_label.setText(f"Error después de {elapsed_time:.2f}s")
            self.status_label.setText(error_msg)
            
            QMessageBox.critical(
                self,
                "Error",
                error_msg
            )
    
    def update_file_list(self):
        self.file_list.clear()
        for file_path in self.generated_files:
            file_name = os.path.basename(file_path)
            self.file_list.addItem(file_name)
    
    def load_vtk_file(self, item):
        """Carga el archivo seleccionado en el visualizador"""
        if self.switcher:
            file_name = item.text()
            file_path = next((f for f in self.generated_files if os.path.basename(f) == file_name), None)
            if file_path:
                self.switcher.load_model(file_path)

class AppPrincipal(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MeshStep")
        self.resize(1280, 720)

        self.boton_cargar = QPushButton("Cargar archivos", self)
        self.boton_cargar.clicked.connect(self.abrir_dialogo_carga)

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

        self.lista_archivos = QListWidget()
        self.lista_archivos.itemClicked.connect(self.mostrar_contenido)
        self.lista_archivos.setContextMenuPolicy(Qt.CustomContextMenu)
        self.lista_archivos.customContextMenuRequested.connect(self.mostrar_menu_contextual)

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
        
        # AGREGAR LOS NUEVOS BOTONES
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
        dialogo = CargarArchivoDialog(self)
        if dialogo.exec_() == QDialog.Accepted:
            if not self.switcher:
                self.switcher = ModelSwitcher(self.renderer, self.interactor, dialogo.archivos_seleccionados)
            else:
                for ruta in dialogo.archivos_seleccionados:
                    self.switcher.add_model(ruta)

            for ruta in dialogo.archivos_seleccionados:
                nombre = os.path.basename(ruta)
                if nombre not in self.rutas_archivos:
                    self.rutas_archivos[nombre] = ruta
                    self.lista_archivos.addItem(nombre)

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

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if all(url.toLocalFile().endswith('.vtk') for url in urls):
                event.acceptProposedAction()

    def dropEvent(self, event):
        archivos = [url.toLocalFile() for url in event.mimeData().urls() if url.toLocalFile().endswith('.vtk')]
        for ruta_archivo in archivos:
            self.procesar_archivo_arrastrado(ruta_archivo)

    def procesar_archivo_arrastrado(self, ruta_archivo):
        dialogo = CargarArchivoDialog(self)
        dialogo.archivos_seleccionados = [ruta_archivo]
        dialogo.ruta_archivos.setText(ruta_archivo)

        if not ruta_archivo.endswith('.vtk'):
            QMessageBox.critical(self, "Error", "El archivo no es un archivo .vtk válido.")
            return

        if dialogo.exec_() == QDialog.Accepted:
            nombre = os.path.basename(ruta_archivo)
            if nombre not in self.rutas_archivos:
                self.rutas_archivos[nombre] = ruta_archivo
                self.lista_archivos.addItem(nombre)

            if not self.switcher:
                self.switcher = ModelSwitcher(self.renderer, self.interactor, [ruta_archivo])
            else:
                self.switcher.add_model(ruta_archivo)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = AppPrincipal()
    ventana.show()
    sys.exit(app.exec_())
