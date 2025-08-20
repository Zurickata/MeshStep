import sys

import os

# Añadir la ruta del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import qdarkstyle
from PyQt5.QtWidgets import QApplication
from app.interface.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    
    # Aplicar qdarkstyle DESPUÉS de que la ventana esté completamente inicializada
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    
    window.show()
    window.vtk_widget.Start()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()