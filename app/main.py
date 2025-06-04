import sys
from PySide6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from core.wrapper import QuadtreeWrapper

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Quadtree Visualizer")
        layout = QVBoxLayout()
        self.label = QLabel("Presiona para generar malla")
        layout.addWidget(self.label)
        self.setLayout(layout)
        
        # Ejemplo de uso
        # self.mesher = QuadtreeWrapper()
        # self.mesher.generate_mesh("core/quadtree/data/a.poly")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())