import sys
import os
import qdarkstyle
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QTranslator, QLocale
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

    app.translator = QTranslator()
    language_code = "es"
    path_opcion_1 = f"translations/meshstep_{language_code}.qm"
    path_opcion_2 = f"../translations/meshstep_{language_code}.qm"

    if app.translator.load(path_opcion_1) or app.translator.load(path_opcion_2):
        app.installTranslator(app.translator)
        print(f"Traducción por defecto '{language_code}' cargada exitosamente.")
    else:
        print(f"Error: No se pudo cargar la traducción. (Rutas probadas: {path_opcion_1}, {path_opcion_2})")

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