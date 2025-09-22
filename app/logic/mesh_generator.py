import os
import time
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QSpinBox, 
                            QPushButton, QMessageBox, QFileDialog, QDialog, QHBoxLayout,
                            QGroupBox, QRadioButton)
from core.wrapper import QuadtreeWrapper, OctreeWrapper
from app.logic.scripts_historial.crear_historial import crear_historial

class MeshGeneratorController(QDialog):
    def __init__(self, parent=None, ignorar_limite=False):
        super().__init__(parent)
        self.mesher = None  # Ahora se instancia dinámicamente según algoritmo
        self.generated_files = []
        self.historial_status = False
        self.ruta_historial = ""
        self.ignorar_limite = ignorar_limite
        self.cargar_sin_generar = False
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Cargar archivos")
        self.resize(400, 350)  
        
        self.archivos_seleccionados = []
        self.ruta_archivos = QLabel("Ningún archivo seleccionado")

        # Grupo para selección de tipo de refinamiento
        self.refinement_type_group = QGroupBox("Tipo de refinamiento")
        self.edge_refinement = QRadioButton("Refinamiento de borde")
        self.full_refinement = QRadioButton("Refinamiento completo")
        self.edge_refinement.setChecked(True)  
        
        refinement_layout = QHBoxLayout()
        refinement_layout.addWidget(self.edge_refinement)
        refinement_layout.addWidget(self.full_refinement)
        self.refinement_type_group.setLayout(refinement_layout)

        # Grupo para selección de algoritmo
        self.algorithm_type_group = QGroupBox("Algoritmo")
        self.quadtree = QRadioButton("Quadtree (2D)")
        self.octree = QRadioButton("Octree (3D)")
        self.quadtree.setChecked(True)  
        
        algorithm_layout = QHBoxLayout()
        algorithm_layout.addWidget(self.quadtree)
        algorithm_layout.addWidget(self.octree)
        self.algorithm_type_group.setLayout(algorithm_layout)

        # Controles de generación
        self.refinement_label = QLabel("Nivel máximo de refinamiento (1-6):")
        self.refinement_spinbox = QSpinBox()
        self.refinement_spinbox.setRange(1, 6)
        if self.ignorar_limite:
            self.refinement_label = QLabel("Sin nivel máximo:")
            self.refinement_spinbox.setRange(1, 102)
        self.refinement_spinbox.setValue(3)
        self.refinement_spinbox.valueChanged.connect(self.verificar_refinamiento)

        self.input_file_button = QPushButton("Seleccionar archivo")
        self.input_file_button.clicked.connect(self.select_input_file)

        # Botón para ejecutar
        self.run_button = QPushButton("Generar Mallas")
        self.run_button.clicked.connect(self.run_mesh_generation)

        # Área de estado
        self.status_label = QLabel("Presiona 'Generar Mallas' para comenzar")
        self.status_label.setWordWrap(True)
        
        # Etiqueta para mostrar tiempos
        self.time_label = QLabel("Tiempo de ejecución: -")
        self.time_label.setStyleSheet("font-weight: bold; color: #2E86C1;")

        layout = QVBoxLayout(self)
        layout.addWidget(self.refinement_type_group)
        layout.addWidget(self.algorithm_type_group)   
        layout.addWidget(self.refinement_label)
        layout.addWidget(self.refinement_spinbox)
        layout.addWidget(self.input_file_button)
        layout.addWidget(self.run_button)
        layout.addWidget(self.ruta_archivos)
        layout.addSpacing(20)
        layout.addWidget(self.status_label)
        layout.addWidget(self.time_label)

        self.setLayout(layout)

    def select_input_file(self):
        if self.quadtree.isChecked():
            file_filter = "Archivos POLY (*.poly)"
        elif self.octree.isChecked():
            file_filter = "Archivos VTK (*.vtk);;Archivos POLY (*.poly);;Archivos MDL (*.mdl)"
        else:
            file_filter = "Archivos POLY (*.poly)"  

        archivos, _ = QFileDialog.getOpenFileNames(
            self,
            "Seleccionar archivo",
            "",
            file_filter
        )
        if archivos:
            self.archivos_seleccionados = archivos
            self.ruta_archivos.setText(f"Archivo seleccionado: {os.path.basename(archivos[0])}")

    def run_mesh_generation(self):
        if not self.archivos_seleccionados:
            QMessageBox.critical(self, "Error", "Debes seleccionar al menos un archivo antes de confirmar.")
            return
        
        # Instanciar el wrapper según algoritmo seleccionado
        if self.quadtree.isChecked():
            self.mesher = QuadtreeWrapper()
            algoritmo = "Quadtree"
        elif self.octree.isChecked():
            self.mesher = OctreeWrapper()
            algoritmo = "Octree"
        else:
            QMessageBox.critical(self, "Error", "Debes seleccionar un algoritmo de mallado.")
            return

        max_refinement = self.refinement_spinbox.value()
        input_file = self.archivos_seleccionados[0]
        refinement_type = "-a" if self.full_refinement.isChecked() else "-s"

        start_time = time.time()
        level_times = []
        self.generated_files = []
        
        self.status_label.setText(f"[{algoritmo}] Generando mallas desde nivel 1 hasta {max_refinement}...")
        self.time_label.setText("Tiempo de ejecución: calculando...")
        QApplication.processEvents()

        try:
            for level in range(1, max_refinement + 1):
                level_start = time.time()

                base_name = os.path.splitext(os.path.basename(input_file))[0]
                output_name = f"{base_name}_output_{level}"
                
                result_file = self.mesher.generate_mesh(
                    input_file=input_file,
                    output_file=output_name,
                    refinement_level=level,
                    refinement_type=refinement_type,
                    show_quality_metrics=True
                )
                
                level_time = time.time() - level_start
                level_times.append(level_time)
                self.generated_files.append(result_file)
            
                print(f"[{algoritmo}] Nivel {level} completado en {level_time:.2f} segundos")
                self.status_label.setText(
                    f"Nivel {level}/{max_refinement} completado en {level_time:.2f}s\n"
                    f"Archivo: {os.path.basename(result_file)}"
                )
                QApplication.processEvents()

            # Tiempo total de generación de mallas
            mesh_time = time.time() - start_time

            # Medir también la creación del historial
            historial_start = time.time()

            print(self.generated_files)

            try:
                if algoritmo == "Quadtree":
                    last_output_path = self.generated_files[-1] if self.generated_files else result_file
                    input_dir = os.path.dirname(last_output_path)
                    name = os.path.splitext(os.path.basename(last_output_path))[0]
                    tipo = "borde" if self.edge_refinement.isChecked() else "completo"

                    _cwd = os.getcwd()
                    try:
                        os.chdir(input_dir)
                        crear_historial(name, max_refinement, tipo)
                        self.historial_status = True
                        self.ruta_quads = f"{input_dir}/{name}_quads.vtk"
                        self.ruta_historial = f"{input_dir}/{name}_historial.txt"
                    finally:
                        os.chdir(_cwd)

                print(f"[Historial] Generado en {self.ruta_historial}")
                self.status_label.setText(self.status_label.text() + "\nEl historial se generó correctamente")
            except Exception as e_hist:
                print(f"[Historial] Error al generar historial: {e_hist}")
                self.status_label.setText(self.status_label.text() + "\nOcurrió un error al generar el historial")
            historial_time = time.time() - historial_start

            # 🔹 Tiempo total (mallado + historial)
            total_time = mesh_time + historial_time
            avg_time = total_time / max_refinement

            time_report = (
                f"Tiempo total: {total_time:.2f} segundos\n"
                f"Tiempo promedio por nivel: {avg_time:.2f} segundos\n"
                f"Tiempo del Historial: {historial_time:.2f} segundos"
            )

            self.time_label.setText(time_report)
            self.status_label.setText(f"Generación completada!\n{time_report}")

            QMessageBox.information(
                self, 
                "Proceso completado", 
                f"Se generaron {max_refinement} mallas con {algoritmo} en {total_time:.2f} segundos"
            )
            self.accept()
            
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

    def verificar_refinamiento(self):
        valor = self.refinement_spinbox.value()
        if valor > 10:
            QMessageBox.warning(
                self,
                "Advertencia",
                "Los niveles altos de refinamiento (>10) pueden requerir mucha memoria RAM."
            )
    
    def cargar_sin_generar_accion(self):
        self.cargar_sin_generar = True
        self.accept()
