import os
import time
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QSpinBox, 
                            QPushButton, QMessageBox, QFileDialog, QDialog, QHBoxLayout,
                            QGroupBox, QRadioButton)
from core.wrapper import QuadtreeWrapper
from app.logic.scripts_historial.crear_historial import crear_historial

class MeshGeneratorController(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.mesher = QuadtreeWrapper()
        self.generated_files = []
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Cargar archivos")
        self.resize(400, 350)  # Aumentamos un poco el tamaño
        
        self.archivos_seleccionados = []
        self.ruta_archivos = QLabel("Ningún archivo seleccionado")

        # Grupo para selección de tipo de refinamiento
        self.refinement_type_group = QGroupBox("Tipo de refinamiento")
        self.edge_refinement = QRadioButton("Refinamiento de borde")
        self.full_refinement = QRadioButton("Refinamiento completo")
        self.edge_refinement.setChecked(True)  # Por defecto refinamiento de borde
        
        type_layout = QHBoxLayout()
        type_layout.addWidget(self.edge_refinement)
        type_layout.addWidget(self.full_refinement)
        self.refinement_type_group.setLayout(type_layout)

        # Controles de generación
        self.refinement_label = QLabel("Nivel máximo de refinamiento (1-15):")
        self.refinement_spinbox = QSpinBox()
        self.refinement_spinbox.setRange(1, 17)
        self.refinement_spinbox.setValue(3)
        self.refinement_spinbox.valueChanged.connect(self.verificar_refinamiento)

        self.input_file_button = QPushButton("Seleccionar archivo .poly")
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
        layout.addWidget(self.refinement_type_group)  # Agregamos el grupo de selección
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
        archivos, _ = QFileDialog.getOpenFileNames(
            self,
            "Seleccionar archivo .poly",
            "",
            "Archivos POLY (*.poly)"
        )
        if archivos:
            self.archivos_seleccionados = archivos
            self.ruta_archivos.setText(f"{len(archivos)} archivo(s) seleccionados")

    def run_mesh_generation(self):
        if not self.archivos_seleccionados:
            QMessageBox.critical(self, "Error", "Debes seleccionar al menos un archivo .poly antes de confirmar.")
            return
        
        max_refinement = self.refinement_spinbox.value()
        input_file = self.archivos_seleccionados[0]
        
        # Determinar tipo de refinamiento seleccionado
        refinement_type = "-a" if self.full_refinement.isChecked() else "-s"

        start_time = time.time()
        level_times = []
        self.generated_files = []
        
        self.status_label.setText(f"Generando mallas desde nivel 1 hasta {max_refinement}...")
        self.time_label.setText("Tiempo de ejecución: calculando...")
        QApplication.processEvents()

        try:
            for level in range(1, max_refinement + 1):
                level_start = time.time()

                poly_name = os.path.splitext(os.path.basename(input_file))[0]
                output_name = f"{poly_name}_output_{level}"
                
                result_file = self.mesher.generate_mesh(
                    input_file=input_file,
                    output_file=output_name,
                    refinement_level=level,
                    refinement_type=refinement_type,  # Pasamos el tipo de refinamiento
                    show_quality_metrics=True
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

            total_time = time.time() - start_time
            avg_time = total_time / max_refinement

            time_report = (
                f"Tiempo total: {total_time:.2f} segundos\n"
                f"Tiempo promedio por nivel: {avg_time:.2f} segundos"
            )

            self.time_label.setText(time_report)
            self.status_label.setText(f"Generación completada!\n{time_report}")

            print(self.generated_files)

            # Acá debería ir para generar el historial
            # No sé como se conecta cuando se genera solo uno
            try:
                last_output_path = self.generated_files[-1] if self.generated_files else result_file
                input_dir = os.path.dirname(last_output_path)
                name = os.path.splitext(os.path.basename(last_output_path))[0]
                tipo = "borde" if self.edge_refinement.isChecked() else "completo"

                _cwd = os.getcwd()
                try:
                    os.chdir(input_dir)
                    crear_historial(name, max_refinement, tipo)
                finally:
                    os.chdir(_cwd)

                print(f"[Historial] Generado en {input_dir}/historial_completo_new.txt")
            except Exception as e_hist:
                print(f"[Historial] Error al generar historial: {e_hist}")
                self.status_label.setText(self.status_label.text() + f"\n[Historial] Error: {e_hist}")

            QMessageBox.information(
                self, 
                "Proceso completado", 
                f"Se generaron {max_refinement} mallas en {total_time:.2f} segundos"
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