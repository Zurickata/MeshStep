import sys
<<<<<<< HEAD

import os

# Añadir la ruta del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

=======
import os
>>>>>>> 0e18fd0544ffd6977e098ebd3592d57a4e8f298d
import qdarkstyle
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from app.interface.main_window import MainWindow

# Habilita el escalado DPI automático
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
os.environ["QT_SCALE_FACTOR"] = "1"
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"

def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    font = QFont("Ubuntu", 12)
    app.setFont(font)
    window = MainWindow()
    
    # Aplicar qdarkstyle DESPUÉS de que la ventana esté completamente inicializada
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    
    window.show()
    # window.vtk_widget.Start()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()