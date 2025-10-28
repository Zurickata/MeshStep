import os
import time
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QLabel, QSpinBox, 
                            QPushButton, QMessageBox, QFileDialog, QDialog, QHBoxLayout,
                            QGroupBox, QRadioButton)
from PyQt5.QtCore import QEvent # <-- 1. IMPORTA QEVENT
from core.wrapper import QuadtreeWrapper, OctreeWrapper
from app.logic.scripts_historial.crear_historial import crear_historial
from app.logic.scripts_historial.historial_octree import crear_historial_octree

class MeshGeneratorController(QDialog):
    def __init__(self, parent=None, ignorar_limite=False):
        super().__init__(parent)
        self.mesher = None  
        self.generated_files = []
        self.historial_status = False
        self.ruta_historial = ""
        self.ignorar_limite = ignorar_limite
        self.cargar_sin_generar = False
        self.setup_ui()
        self.retranslateUi() # <-- Tu llamada existente (¡perfecto!)

    def setup_ui(self):
        self.setWindowTitle("")
        self.resize(400, 350)  
        
        self.archivos_seleccionados = []
        # 2. Mover texto inicial a retranslateUi
        self.ruta_archivos = QLabel("") 

        # Grupo para selección de tipo de refinamiento
        self.refinement_type_group = QGroupBox("")
        self.edge_refinement = QRadioButton("")
        self.full_refinement = QRadioButton("")
        self.edge_refinement.setChecked(True)  
        
        refinement_layout = QHBoxLayout()
        refinement_layout.addWidget(self.edge_refinement)
        refinement_layout.addWidget(self.full_refinement)
        self.refinement_type_group.setLayout(refinement_layout)

        # Grupo para selección de algoritmo
        self.algorithm_type_group = QGroupBox("")
        self.quadtree = QRadioButton("")
        self.octree = QRadioButton("")
        self.quadtree.setChecked(True)  
        
        algorithm_layout = QHBoxLayout()
        algorithm_layout.addWidget(self.quadtree)
        algorithm_layout.addWidget(self.octree)
        self.algorithm_type_group.setLayout(algorithm_layout)

        # Controles de generación
        self.refinement_label = QLabel("") # 2. Mover texto
        self.refinement_spinbox = QSpinBox()
        self.refinement_spinbox.setRange(1, 6)
        if self.ignorar_limite:
            self.refinement_label = QLabel("") # 2. Mover texto
            self.refinement_spinbox.setRange(1, 102)
        self.refinement_spinbox.setValue(3)
        self.refinement_spinbox.valueChanged.connect(self.verificar_refinamiento)

        self.input_file_button = QPushButton("")
        self.input_file_button.clicked.connect(self.select_input_file)

        # Botón para ejecutar
        self.run_button = QPushButton("")
        self.run_button.clicked.connect(self.run_mesh_generation)

        # Área de estado
        self.status_label = QLabel("") # 2. Mover texto
        self.status_label.setWordWrap(True)
        
        # Etiqueta para mostrar tiempos
        self.time_label = QLabel("") # 2. Mover texto
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
        # 3. TRADUCIR TEXTOS DINÁMICOS
        if self.quadtree.isChecked():
            file_filter = self.tr("Archivos POLY (*.poly)")
        elif self.octree.isChecked():
            file_filter = self.tr("Archivos MDL (*.mdl);;Archivos POLY (*.poly);;Archivos VTK (*.vtk)")
        else:
            file_filter = self.tr("Archivos POLY (*.poly)")  

        archivos, _ = QFileDialog.getOpenFileNames(
            self,
            self.tr("Seleccionar archivo"), # <-- Título del diálogo
            "",
            file_filter
        )
        if archivos:
            self.archivos_seleccionados = archivos
            # 3. TRADUCIR F-STRINGS (estilo Python)
            self.ruta_archivos.setText(f"{self.tr('Archivo seleccionado')}: {os.path.basename(archivos[0])}")

    def run_mesh_generation(self):
        if not self.archivos_seleccionados:
            # 3. TRADUCIR QMESSAGEBOX
            QMessageBox.critical(self, self.tr("Error"), self.tr("Debes seleccionar al menos un archivo antes de confirmar."))
            return
        
        if self.quadtree.isChecked():
            self.mesher = QuadtreeWrapper()
            algoritmo = "Quadtree"
        elif self.octree.isChecked():
            self.mesher = OctreeWrapper()
            algoritmo = "Octree"
        else:
            QMessageBox.critical(self, self.tr("Error"), self.tr("Debes seleccionar un algoritmo de mallado."))
            return

        max_refinement = self.refinement_spinbox.value()
        input_file = self.archivos_seleccionados[0]
        refinement_type = "-a" if self.full_refinement.isChecked() else "-s"

        start_time = time.time()
        level_times = []
        self.generated_files = []
        
        # 3. TRADUCIR F-STRINGS
        self.status_label.setText(f"[{algoritmo}] {self.tr('Generando mallas desde nivel 1 hasta')} {max_refinement}...")
        self.time_label.setText(f"{self.tr('Tiempo de ejecución')}: {self.tr('calculando')}...")
        QApplication.processEvents()

        try:
            for level in range(1, max_refinement + 1):
                level_start = time.time()
                # ... (lógica) ...
                result_file = self.mesher.generate_mesh(...)
                # ... (lógica) ...
            
                print(f"[{algoritmo}] Nivel {level} completado en {level_time:.2f} segundos")
                self.status_label.setText(
                    f"{self.tr('Nivel')} {level}/{max_refinement} {self.tr('completado en')} {level_time:.2f}s\n"
                    f"{self.tr('Archivo')}: {os.path.basename(result_file)}"
                )
                QApplication.processEvents()

            mesh_time = time.time() - start_time
            historial_start = time.time()

            try:
                # ... (lógica historial) ...
                if algoritmo == "Quadtree":
                    crear_historial(name, max_refinement, tipo)
                else:
                    crear_historial_octree(name, max_refinement, tipo)
                
                print(f"[Historial] Generado en {self.ruta_historial}")
                # 3. TRADUCIR TEXTOS CONCATENADOS
                self.status_label.setText(self.status_label.text() + f"\n{self.tr('El historial se generó correctamente')}")
            except Exception as e_hist:
                print(f"[Historial] Error al generar historial: {e_hist}")
                self.status_label.setText(self.status_label.text() + f"\n{self.tr('Ocurrió un error al generar el historial')}")
            historial_time = time.time() - historial_start

            total_time = mesh_time + historial_time
            avg_time = total_time / max_refinement

            time_report = (
                f"{self.tr('Tiempo total')}: {total_time:.2f} {self.tr('segundos')}\n"
                f"{self.tr('Tiempo promedio por nivel')}: {avg_time:.2f} {self.tr('segundos')}\n"
                f"{self.tr('Tiempo del Historial')}: {historial_time:.2f} {self.tr('segundos')}"
            )

            self.time_label.setText(time_report)
            self.status_label.setText(f"{self.tr('Generación completada')}!\n{time_report}")

            msg_historial = self.tr('Se generó el historial exitosamente') if self.historial_status else self.tr('No se generó el historial')
            QMessageBox.information(
                self, 
                self.tr("Proceso completado"), 
                f"{self.tr('Se generaron')} {max_refinement} {self.tr('mallas con')} {algoritmo} {self.tr('en')} {total_time:.2f} {self.tr('segundos')}\n{msg_historial}"
            )
            self.accept()
            
        except Exception as e:
            elapsed_time = time.time() - start_time
            error_msg = (
                f"{self.tr('Error después de')} {elapsed_time:.2f} {self.tr('segundos')}:\n"
                f"{str(e)}"
            )
            
            print(f"ERROR: {error_msg}")
            self.time_label.setText(f"{self.tr('Error después de')} {elapsed_time:.2f}s")
            self.status_label.setText(error_msg)
            
            QMessageBox.critical(
                self,
                self.tr("Error"),
                error_msg
            )

    def verificar_refinamiento(self):
        valor = self.refinement_spinbox.value()
        if valor > 10:
            QMessageBox.warning(
                self,
                self.tr("Advertencia"),
                self.tr("Los niveles altos de refinamiento (>10) pueden requerir mucha memoria RAM.")
            )
    
    def cargar_sin_generar_accion(self):
        self.cargar_sin_generar = True
        self.accept()

    def retranslateUi(self):
        # 2. MOVER TODO EL TEXTO ESTÁTICO E INICIAL AQUÍ
        self.setWindowTitle(self.tr("Cargar archivos"))
        
        self.refinement_type_group.setTitle(self.tr("Tipo de refinamiento"))
        self.edge_refinement.setText(self.tr("Refinamiento de borde"))
        self.full_refinement.setText(self.tr("Refinamiento completo"))
        
        self.algorithm_type_group.setTitle(self.tr("Algoritmo"))
        self.quadtree.setText(self.tr("Quadtree (2D)"))
        self.octree.setText(self.tr("Octree (3D)"))
        
        if self.ignorar_limite:
            self.refinement_label.setText(self.tr("Nivel máximo (sin límite):"))
        else:
            self.refinement_label.setText(self.tr("Nivel máximo de refinamiento (1-6):"))
        
        self.input_file_button.setText(self.tr("Seleccionar archivo"))
        self.run_button.setText(self.tr("Generar Mallas"))
        
        # Textos iniciales
        if not self.archivos_seleccionados:
            self.ruta_archivos.setText(self.tr("Ningún archivo seleccionado"))
        self.status_label.setText(self.tr("Presiona 'Generar Mallas' para comenzar"))
        self.time_label.setText(f"{self.tr('Tiempo de ejecución')}: -")

    # 1. AÑADIR CHANGEEVENT
    def changeEvent(self, event):
        """
        Escucha el evento de cambio de idioma para traducir este diálogo
        """
        if event.type() == QEvent.LanguageChange:
            self.retranslateUi()
        else:
            super().changeEvent(event)