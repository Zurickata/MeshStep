import sys
from PySide6.QtWidgets import (QApplication, QLabel, QVBoxLayout, QWidget, 
                              QSpinBox, QPushButton, QMessageBox)
from core.wrapper import QuadtreeWrapper

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quadtree Mesh Generator")
        self.setMinimumSize(400, 200)
        
        # Configuración de la interfaz
        layout = QVBoxLayout()
        
        # Control para seleccionar el nivel máximo de refinamiento
        self.refinement_label = QLabel("Nivel máximo de refinamiento (1-10):")
        self.refinement_spinbox = QSpinBox()
        self.refinement_spinbox.setRange(1, 10)
        self.refinement_spinbox.setValue(3)
        
        # Botón para ejecutar
        self.run_button = QPushButton("Generar Mallas")
        self.run_button.clicked.connect(self.run_mesh_generation)
        
        # Área de estado
        self.status_label = QLabel("Presiona 'Generar Mallas' para comenzar")
        self.status_label.setWordWrap(True)
        
        # Añadir widgets al layout
        layout.addWidget(self.refinement_label)
        layout.addWidget(self.refinement_spinbox)
        layout.addWidget(self.run_button)
        layout.addWidget(self.status_label)
        self.setLayout(layout)
        
        # Inicializar el mesher
        self.mesher = QuadtreeWrapper()
    
    def run_mesh_generation(self):
        max_refinement = self.refinement_spinbox.value()
        input_file = "core/quadtree/data/a.poly"
        
        self.status_label.setText(f"Generando mallas desde nivel 1 hasta {max_refinement}...")
        QApplication.processEvents()  # Actualiza la UI
        
        try:
            for level in range(1, max_refinement + 1):
                output_name = f"output_{level}"  # Sufijo con nivel de refinamiento
                self.status_label.setText(f"Procesando nivel {level}...")
                QApplication.processEvents()
                
                # Ejecutar el mesher
                result_file = self.mesher.generate_mesh(
                    input_file=input_file,
                    output_file=output_name,
                    refinement_level=level,
                    show_quality_metrics=False  # Puedes hacer esto configurable también
                )
                
                self.status_label.setText(f"Nivel {level} completado. Archivo: {result_file}")
                QApplication.processEvents()
            
            QMessageBox.information(
                self, 
                "Proceso completado", 
                f"Se generaron {max_refinement} mallas exitosamente"
            )
            self.status_label.setText("Proceso completado con éxito")
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error",
                f"Ocurrió un error al generar las mallas:\n{str(e)}"
            )
            self.status_label.setText(f"Error: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())