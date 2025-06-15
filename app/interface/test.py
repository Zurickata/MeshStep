import sys
import time
import vtk
import os
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QSpinBox, QPushButton, QMessageBox, 
                            QListWidget, QSplitter, QFileDialog)
from PyQt5.QtCore import Qt
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from app.visualization.FeriaVTK import ModelSwitcher, CustomInteractorStyle
from core.wrapper import QuadtreeWrapper

class MeshGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("MeshStep - Generador y Visualizador")
        self.resize(1280, 720)
        
        # Inicializar componentes
        self.mesher = QuadtreeWrapper()
        self.generated_files = []
        self.switcher = None
        
        # Configurar interfaz
        self.setup_ui()
        
    def setup_ui(self):
        # Layout principal
        main_layout = QHBoxLayout(self)
        splitter = QSplitter(Qt.Horizontal)
        
        # Panel izquierdo (controles)
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        
        # Controles de generación
        self.refinement_label = QLabel("Nivel máximo de refinamiento (1-10):")
        self.refinement_spinbox = QSpinBox()
        self.refinement_spinbox.setRange(1, 10)
        self.refinement_spinbox.setValue(3)
        
        self.input_file_button = QPushButton("Seleccionar archivo .poly")
        self.input_file_button.clicked.connect(self.select_input_file)
        
        self.run_button = QPushButton("Generar Mallas")
        self.run_button.clicked.connect(self.run_mesh_generation)
        
        # Lista de archivos generados
        self.file_list = QListWidget()
        self.file_list.itemClicked.connect(self.load_vtk_file)
        
        # Área de estado
        self.status_label = QLabel("Seleccione un archivo .poly y presione 'Generar Mallas'")
        self.status_label.setWordWrap(True)
        
        # Tiempos de ejecución
        self.time_label = QLabel("Tiempo de ejecución: -")
        self.time_label.setStyleSheet("font-weight: bold; color: #2E86C1;")
        
        # Agregar widgets al panel izquierdo
        left_layout.addWidget(self.refinement_label)
        left_layout.addWidget(self.refinement_spinbox)
        left_layout.addWidget(self.input_file_button)
        left_layout.addWidget(self.run_button)
        left_layout.addSpacing(20)
        left_layout.addWidget(self.status_label)
        left_layout.addWidget(self.time_label)
        left_layout.addWidget(QLabel("Archivos generados:"))
        left_layout.addWidget(self.file_list)
        left_panel.setLayout(left_layout)
        
        # Panel central (visualización VTK)
        self.vtk_widget = QVTKRenderWindowInteractor(self)
        self.renderer = self.vtk_widget.GetRenderWindow().AddRenderer(vtk.vtkRenderer())
        self.interactor = self.vtk_widget.GetRenderWindow().GetInteractor()
        self.interactor.SetInteractorStyle(CustomInteractorStyle(self.renderer))
        self.interactor.Initialize()
        
        # Panel derecho (controles de visualización)
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        
        # Botones de control (ejemplo)
        self.btn_wireframe = QPushButton("Wireframe (w)")
        self.btn_surface = QPushButton("Superficie (s)")
        self.btn_reset = QPushButton("Reset (r)")
        
        right_layout.addWidget(self.btn_wireframe)
        right_layout.addWidget(self.btn_surface)
        right_layout.addWidget(self.btn_reset)
        right_layout.addStretch()
        right_panel.setLayout(right_layout)
        
        # Conectar botones
        self.btn_wireframe.clicked.connect(self.set_wireframe)
        self.btn_surface.clicked.connect(self.set_surface)
        self.btn_reset.clicked.connect(self.reset_view)
        
        # Configurar splitter
        splitter.addWidget(left_panel)
        splitter.addWidget(self.vtk_widget)
        splitter.addWidget(right_panel)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 3)
        splitter.setStretchFactor(2, 1)
        
        main_layout.addWidget(splitter)
    
    def select_input_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo .poly",
            "",
            "Archivos POLY (*.poly)"
        )
        if file_path:
            self.input_file_path = file_path
            self.status_label.setText(f"Archivo seleccionado: {os.path.basename(file_path)}")
    
    def run_mesh_generation(self):
        if not hasattr(self, 'input_file_path'):
            QMessageBox.warning(self, "Advertencia", "Por favor seleccione un archivo .poly primero")
            return
            
        max_refinement = self.refinement_spinbox.value()
        input_file = self.input_file_path
        
        # Iniciar cronómetro
        start_time = time.time()
        level_times = []
        self.generated_files = []
        
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
                    f"Archivo: {os.path.basename(result_file)}"
                )
                QApplication.processEvents()
            
            # Calcular tiempos totales
            total_time = time.time() - start_time
            avg_time = total_time / max_refinement
            
            # Mostrar resultados
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
                f"Se generaron {max_refinement} mallas en {total_time:.2f} segundos"
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
    
    def initialize_switcher(self):
        """Inicializa el ModelSwitcher con los archivos generados"""
        if self.generated_files:
            self.switcher = ModelSwitcher(self.renderer, self.interactor, self.generated_files)
            # Cargar el primer archivo por defecto
            self.switcher.load_model(self.generated_files[0])
    
    def load_vtk_file(self, item):
        """Carga el archivo seleccionado en el visualizador"""
        if self.switcher:
            file_name = item.text()
            file_path = next((f for f in self.generated_files if os.path.basename(f) == file_name), None)
            if file_path:
                self.switcher.load_model(file_path)
    
    # Funciones de control de visualización
    def set_wireframe(self):
        if self.switcher:
            self.switcher.actor.GetProperty().SetRepresentationToWireframe()
            self.vtk_widget.GetRenderWindow().Render()
    
    def set_surface(self):
        if self.switcher:
            self.switcher.actor.GetProperty().SetRepresentationToSurface()
            self.vtk_widget.GetRenderWindow().Render()
    
    def reset_view(self):
        if self.switcher:
            self.switcher.actor.SetOrientation(0, 0, 0)
            self.switcher.actor.SetPosition(0, 0, 0)
            self.switcher.actor.SetScale(1, 1, 1)
            self.renderer.ResetCamera()
            if hasattr(self.interactor.GetInteractorStyle(), 'reset_camera_and_rotation'):
                self.interactor.GetInteractorStyle().reset_camera_and_rotation()
            self.vtk_widget.GetRenderWindow().Render()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MeshGeneratorApp()
    window.show()
    window.vtk_widget.Start()
    sys.exit(app.exec_())