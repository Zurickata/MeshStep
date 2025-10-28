import os
import time
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QSpinBox, 
                            QPushButton, QMessageBox, QFileDialog, QDialog, QHBoxLayout,
                            QGroupBox, QRadioButton, QProgressDialog)
# --- CAMBIO: Importar QEvent ---
from PyQt5.QtCore import Qt, QEvent, QThread, pyqtSignal
from core.wrapper import QuadtreeWrapper, OctreeWrapper
from app.logic.scripts_historial.crear_historial import crear_historial
from app.logic.scripts_historial.historial_octree import crear_historial_octree

# --- CAMBIO: Definir Contexto ---
CONTEXTO = "MeshGeneratorController"

# 🧩 Worker del historial
# =============================
class HistorialWorker(QThread):
    finished = pyqtSignal(bool, str)

    def __init__(self, algoritmo, input_dir, name, tipo, max_refinement):
        super().__init__()
        self.algoritmo = algoritmo
        self.input_dir = input_dir
        self.name = name
        self.tipo = tipo
        self.max_refinement = max_refinement

    def run(self):
        try:
            os.chdir(self.input_dir)
            if self.algoritmo == "Quadtree":
                crear_historial(self.name, self.max_refinement, self.tipo)
            else:
                crear_historial_octree(self.name, self.max_refinement, self.tipo)

            self.finished.emit(True, f"{self.input_dir}/{self.name}_historial.txt")
        except Exception as e:
            self.finished.emit(False, str(e))

class MeshGeneratorController(QDialog):
    def __init__(self, parent=None, ignorar_limite=False):
        super().__init__(parent)
        self.mesher = None
        self.generated_files = []
        self.historial_status = False
        self.ruta_historial = ""
        self.ignorar_limite = ignorar_limite
        self.cargar_sin_generar = False
        self.historial_generandose = False
        self.historial_thread = None 
        self.setup_ui()
        self.retranslateUi() # Esta llamada ya estaba aquí, ¡perfecto!

    def setup_ui(self):
        self.setWindowTitle("") # Se establece en retranslateUi
        self.resize(400, 350)  
        
        self.archivos_seleccionados = []
        self.ruta_archivos = QLabel("") # Se establece en retranslateUi

        # Grupo para selección de tipo de refinamiento
        self.refinement_type_group = QGroupBox("") # Se establece en retranslateUi
        self.edge_refinement = QRadioButton("") # Se establece en retranslateUi
        self.full_refinement = QRadioButton("") # Se establece en retranslateUi
        self.edge_refinement.setChecked(True)  
        
        refinement_layout = QHBoxLayout()
        refinement_layout.addWidget(self.edge_refinement)
        refinement_layout.addWidget(self.full_refinement)
        self.refinement_type_group.setLayout(refinement_layout)

        # Grupo para selección de algoritmo
        self.algorithm_type_group = QGroupBox("") # Se establece en retranslateUi
        self.quadtree = QRadioButton("") # Se establece en retranslateUi
        self.octree = QRadioButton("") # Se establece en retranslateUi
        self.quadtree.setChecked(True)  
        
        algorithm_layout = QHBoxLayout()
        algorithm_layout.addWidget(self.quadtree)
        algorithm_layout.addWidget(self.octree)
        self.algorithm_type_group.setLayout(algorithm_layout)

        # Controles de generación
        self.refinement_label = QLabel("") # Se establece en retranslateUi
        self.refinement_spinbox = QSpinBox()
        self.refinement_spinbox.setRange(1, 6)
        if self.ignorar_limite:
            self.refinement_label = QLabel("") # Se establece en retranslateUi
            self.refinement_spinbox.setRange(1, 102)
        self.refinement_spinbox.setValue(3)
        self.refinement_spinbox.valueChanged.connect(self.verificar_refinamiento)

        self.input_file_button = QPushButton("") # Se establece en retranslateUi
        self.input_file_button.clicked.connect(self.select_input_file)

        # Botón para ejecutar
        self.run_button = QPushButton("") # Se establece en retranslateUi
        self.run_button.clicked.connect(self.run_mesh_generation)

        # Área de estado
        self.status_label = QLabel("") # Se establece en retranslateUi
        self.status_label.setWordWrap(True)
        
        # Etiqueta para mostrar tiempos
        self.time_label = QLabel("") # Se establece en retranslateUi
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
        # --- CAMBIO: Usar QApplication.translate ---
        if self.quadtree.isChecked():
            file_filter = QApplication.translate(CONTEXTO, "Archivos POLY (*.poly)")
        elif self.octree.isChecked():
            file_filter = QApplication.translate(CONTEXTO, "Archivos MDL (*.mdl);;Archivos POLY (*.poly);;Archivos VTK (*.vtk)")
        else:
            file_filter = QApplication.translate(CONTEXTO, "Archivos POLY (*.poly)")  

        archivos, _ = QFileDialog.getOpenFileNames(
            self,
            QApplication.translate(CONTEXTO, "Seleccionar archivo"),
            "",
            file_filter
        )
        if archivos:
            self.archivos_seleccionados = archivos
            self.ruta_archivos.setText(f"{QApplication.translate(CONTEXTO, 'Archivo seleccionado')}: {os.path.basename(archivos[0])}")

    def run_mesh_generation(self):
        if not self.archivos_seleccionados:
            # --- CAMBIO: Usar QApplication.translate ---
            QMessageBox.critical(self, 
                                 QApplication.translate(CONTEXTO, "Error"), 
                                 QApplication.translate(CONTEXTO, "Debes seleccionar al menos un archivo antes de confirmar."))
            return
        
        # Instanciar el wrapper según algoritmo seleccionado
        if self.quadtree.isChecked():
            self.mesher = QuadtreeWrapper()
            algoritmo = "Quadtree"
        elif self.octree.isChecked():
            self.mesher = OctreeWrapper()
            algoritmo = "Octree"
        else:
            # --- CAMBIO: Usar QApplication.translate ---
            QMessageBox.critical(self, 
                                 QApplication.translate(CONTEXTO, "Error"), 
                                 QApplication.translate(CONTEXTO, "Debes seleccionar un algoritmo de mallado."))
            return

        max_refinement = self.refinement_spinbox.value()
        input_file = self.archivos_seleccionados[0]
        refinement_type = "-a" if self.full_refinement.isChecked() else "-s"

        # 🔹 Barra de progreso
        progress = QProgressDialog("Generando mallas...", "Cancelar", 0, max_refinement, self)
        progress.setWindowTitle("Progreso de mallado")
        progress.setWindowModality(Qt.WindowModal)
        progress.setAutoClose(True)
        progress.show()

        start_time = time.time()
        level_times = []
        self.generated_files = []
        
        # --- CAMBIO: Usar QApplication.translate ---
        self.status_label.setText(f"[{algoritmo}] {QApplication.translate(CONTEXTO, 'Generando mallas desde nivel 1 hasta')} {max_refinement}...")
        self.time_label.setText(f"{QApplication.translate(CONTEXTO, 'Tiempo de ejecución')}: {QApplication.translate(CONTEXTO, 'calculando')}...")
        QApplication.processEvents()

        try:
            for level in range(1, max_refinement + 1):
                if progress.wasCanceled():
                    self.status_label.setText("Proceso cancelado por el usuario.")
                    return
                
                progress.setValue(level - 1)
                progress.setLabelText(f"[{algoritmo}] Generando nivel {level}/{max_refinement}...")
                QApplication.processEvents()

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
                # --- CAMBIO: Usar QApplication.translate ---
                self.status_label.setText(
                    f"{QApplication.translate(CONTEXTO, 'Nivel')} {level}/{max_refinement} {QApplication.translate(CONTEXTO, 'completado en')} {level_time:.2f}s\n"
                    f"{QApplication.translate(CONTEXTO, 'Archivo')}: {os.path.basename(result_file)}"
                )
                QApplication.processEvents()

            progress.setValue(max_refinement)

            # Tiempo total de generación de mallas
            mesh_time = time.time() - start_time
            print(self.generated_files)
            
            self.status_label.setText(f"Mallado completado en {mesh_time:.2f}s. Generando historial...")

            # 🔹 Lanzar el historial en un hilo separado
            last_output_path = self.generated_files[-1]
            input_dir = os.path.dirname(last_output_path)
            name = os.path.splitext(os.path.basename(last_output_path))[0]
            tipo = "borde" if self.edge_refinement.isChecked() else "completo"

            self.historial_generandose = True
            self.historial_thread = HistorialWorker(algoritmo, input_dir, name, tipo, max_refinement)
            self.historial_thread.finished.connect(self.on_historial_finished)
            self.historial_thread.start()

            QMessageBox.information(
                self, "Mallado completado",
                "Se generaron todas las mallas.\n"
                "El historial se está creando en segundo plano.\n"
                "Puedes seguir usando MeshStep mientras tanto."
            )
            self.accept()

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Ocurrió un error: {e}")

            # # Medir también la creación del historial
            # historial_start = time.time()

            # try:
            #     last_output_path = self.generated_files[-1] if self.generated_files else result_file
            #     input_dir = os.path.dirname(last_output_path)
            #     name = os.path.splitext(os.path.basename(last_output_path))[0]
            #     tipo = "borde" if self.edge_refinement.isChecked() else "completo"

            #     _cwd = os.getcwd()
            #     try:
            #         os.chdir(input_dir)
            #         if algoritmo == "Quadtree":
            #             crear_historial(name, max_refinement, tipo)
            #         else:
            #             crear_historial_octree(name, max_refinement, tipo)
            #         self.historial_status = True
            #         self.ruta_quads = f"{input_dir}/{name}_quads.vtk"
            #         self.ruta_historial = f"{input_dir}/{name}_historial.txt"
            #     finally:
            #         os.chdir(_cwd)

            #     print(f"[Historial] Generado en {self.ruta_historial}")
            #     # --- CAMBIO: Usar QApplication.translate ---
            #     self.status_label.setText(self.status_label.text() + f"\n{QApplication.translate(CONTEXTO, 'El historial se generó correctamente')}")
            # except Exception as e_hist:
            #     print(f"[Historial] Error al generar historial: {e_hist}")
            #     # --- CAMBIO: Usar QApplication.translate ---
            #     self.status_label.setText(self.status_label.text() + f"\n{QApplication.translate(CONTEXTO, 'Ocurrió un error al generar el historial')}")
            # historial_time = time.time() - historial_start

            # # 🔹 Tiempo total (mallado + historial)
            # total_time = mesh_time + historial_time
            # avg_time = total_time / max_refinement

            # # --- CAMBIO: Usar QApplication.translate ---
            # time_report = (
            #     f"{QApplication.translate(CONTEXTO, 'Tiempo total')}: {total_time:.2f} {QApplication.translate(CONTEXTO, 'segundos')}\n"
            #     f"{QApplication.translate(CONTEXTO, 'Tiempo promedio por nivel')}: {avg_time:.2f} {QApplication.translate(CONTEXTO, 'segundos')}\n"
            #     f"{QApplication.translate(CONTEXTO, 'Tiempo del Historial')}: {historial_time:.2f} {QApplication.translate(CONTEXTO, 'segundos')}"
            # )

            # self.time_label.setText(time_report)
            # self.status_label.setText(f"{QApplication.translate(CONTEXTO, 'Generación completada')}!\n{time_report}")

            # # --- CAMBIO: Usar QApplication.translate ---
            # msg_historial = QApplication.translate(CONTEXTO, 'Se generó el historial exitosamente') if self.historial_status else QApplication.translate(CONTEXTO, 'No se generó el historial')
            # QMessageBox.information(
            #     self, 
            #     QApplication.translate(CONTEXTO, "Proceso completado"), 
            #     f"{QApplication.translate(CONTEXTO, 'Se generaron')} {max_refinement} {QApplication.translate(CONTEXTO, 'mallas con')} {algoritmo} {QApplication.translate(CONTEXTO, 'en')} {total_time:.2f} {QApplication.translate(CONTEXTO, 'segundos')}\n{msg_historial}"
            # )
            # self.accept()
            
        # except Exception as e:
        #     elapsed_time = time.time() - start_time
        #     # --- CAMBIO: Usar QApplication.translate ---
        #     error_msg = (
        #         f"{QApplication.translate(CONTEXTO, 'Error después de')} {elapsed_time:.2f} {QApplication.translate(CONTEXTO, 'segundos')}:\n"
        #         f"{str(e)}"
        #     )
            
        #     print(f"ERROR: {error_msg}")
        #     self.time_label.setText(f"{QApplication.translate(CONTEXTO, 'Error después de')} {elapsed_time:.2f}s")
        #     self.status_label.setText(error_msg)
            
        #     # --- CAMBIO: Usar QApplication.translate ---
        #     QMessageBox.critical(
        #         self,
        #         QApplication.translate(CONTEXTO, "Error"),
        #         error_msg
        #     )

    def on_historial_finished(self, success, msg):
        self.historial_generandose = False
        self.historial_status = success
        self.ruta_historial = msg if success else ""

        # 🔹 Notificar al MainWindow si existe
        if self.parent() and hasattr(self.parent(), "mesh_generator_controller"):
            self.parent().mesh_generator_controller = self

        if success:
            print(f"[Historial] Generado correctamente en {msg}")
            QMessageBox.information(self.parent() or self, "Historial", "Historial generado correctamente.")
        else:
            print(f"[Historial] Error: {msg}")
            QMessageBox.critical(self.parent() or self, "Error al generar historial", msg)

    def verificar_refinamiento(self):
        valor = self.refinement_spinbox.value()
        if valor > 10:
            # --- CAMBIO: Usar QApplication.translate ---
            QMessageBox.warning(
                self,
                QApplication.translate(CONTEXTO, "Advertencia"),
                QApplication.translate(CONTEXTO, "Los niveles altos de refinamiento (>10) pueden requerir mucha memoria RAM.")
            )
    
    def cargar_sin_generar_accion(self):
        self.cargar_sin_generar = True
        self.accept()

    def retranslateUi(self):
        # --- CAMBIO: Usar QApplication.translate y mover texto de setup_ui aquí ---
        self.setWindowTitle(QApplication.translate(CONTEXTO, "Cargar archivos"))
        self.refinement_type_group.setTitle(QApplication.translate(CONTEXTO, "Tipo de refinamiento"))
        self.edge_refinement.setText(QApplication.translate(CONTEXTO, "Refinamiento de borde"))
        self.full_refinement.setText(QApplication.translate(CONTEXTO, "Refinamiento completo"))
        self.algorithm_type_group.setTitle(QApplication.translate(CONTEXTO, "Algoritmo"))
        self.quadtree.setText(QApplication.translate(CONTEXTO, "Quadtree (2D)"))
        self.octree.setText(QApplication.translate(CONTEXTO, "Octree (3D)"))
        
        if self.ignorar_limite:
            self.refinement_label.setText(QApplication.translate(CONTEXTO, "Nivel máximo (sin límite):"))
        else:
            self.refinement_label.setText(QApplication.translate(CONTEXTO, "Nivel máximo de refinamiento (1-6):"))
            
        self.input_file_button.setText(QApplication.translate(CONTEXTO, "Seleccionar archivo"))
        self.run_button.setText(QApplication.translate(CONTEXTO, "Generar Mallas"))
        
        # Textos iniciales
        if not self.archivos_seleccionados:
             self.ruta_archivos.setText(QApplication.translate(CONTEXTO, "Ningún archivo seleccionado"))
        self.status_label.setText(QApplication.translate(CONTEXTO, "Presiona 'Generar Mallas' para comenzar"))
        self.time_label.setText(f"{QApplication.translate(CONTEXTO, 'Tiempo de ejecución')}: -")

    # --- CAMBIO: Añadir changeEvent ---
    def changeEvent(self, event):
        """
        Escucha el evento de cambio de idioma para traducir este diálogo
        """
        if event.type() == QEvent.LanguageChange:
            self.retranslateUi()
        else:
            super().changeEvent(event)