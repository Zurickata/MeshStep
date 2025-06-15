import sys
from PyQt5.QtWidgets import QApplication
from app.interface.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    window.vtk_widget.Start()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()