import sys
import os
import qdarkstyle
from PyQt5.QtWidgets import QApplication, QSplashScreen
from PyQt5.QtCore import Qt, QTranslator, QTimer
from PyQt5.QtGui import QFont, QIcon, QPixmap
from app.interface.main_window import MainWindow
import time

# Habilita el escalado DPI automático
os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
os.environ["QT_SCALE_FACTOR"] = "1"
os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "1"

def main():
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)

    # --- Splash Screen ---
    splash_pix = QPixmap("./meshsteppng.svg")
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.setWindowFlag(Qt.FramelessWindowHint)  # sin bordes
    splash.setWindowOpacity(0.95)
    splash.showMessage("Cargando MeshStep...", Qt.AlignBottom | Qt.AlignCenter, Qt.white)
    splash.show()

    app.setWindowIcon(QIcon("./meshsteppng.svg"))

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
    
    def start_app():
        splash.finish(window)
        window.show()

    QTimer.singleShot(1800, start_app)
    
    # window.vtk_widget.Start()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()