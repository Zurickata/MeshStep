import sys
import time
from PySide6.QtWidgets import (QApplication, QLabel, QVBoxLayout, QWidget, 
                              QSpinBox, QPushButton, QMessageBox)
from core.wrapper import QuadtreeWrapper

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quadtree Mesh Generator")
        self.setMinimumSize(400, 250)
        
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
        
        # Etiqueta para mostrar tiempos
        self.time_label = QLabel("Tiempo de ejecución: -")
        self.time_label.setStyleSheet("font-weight: bold; color: #2E86C1;")
        
        # Añadir widgets al layout
        layout.addWidget(self.refinement_label)
        layout.addWidget(self.refinement_spinbox)
        layout.addWidget(self.run_button)
        layout.addSpacing(20)
        layout.addWidget(self.status_label)
        layout.addWidget(self.time_label)
        self.setLayout(layout)
        
        # Inicializar el mesher
        self.mesher = QuadtreeWrapper()
    
    def run_mesh_generation(self):
        max_refinement = self.refinement_spinbox.value()
        input_file = "core/quadtree/data/a.poly"
        
        # Iniciar cronómetro
        start_time = time.time()
        level_times = []
        
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())