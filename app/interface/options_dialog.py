from PyQt5.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QPushButton
from app.logic.export_utils import ExportManager

class OpcionesDialog(QDialog):
    def __init__(self, parent=None, poly_name=None, refinement_level=None):
        super().__init__(parent)
        self.setWindowTitle("Opciones avanzadas")
        self.setFixedSize(250, 140)
        self.checkbox = QCheckBox("Ignorar límite de hardware")
        self.checkbox.setChecked(False)
        btn_ok = QPushButton("Aceptar")
        btn_ok.clicked.connect(self.accept)

        self.export_manager = ExportManager(self)
        self.poly_name = poly_name
        self.refinement_level = refinement_level

        btn_exportar = QPushButton("Exportar historial de mallado")
        btn_exportar.clicked.connect(self.exportar_historial)

        layout = QVBoxLayout()
        layout.addWidget(self.checkbox)
        layout.addWidget(btn_exportar)
        layout.addWidget(btn_ok)
        self.setLayout(layout)

    def exportar_historial(self):
        success, message = self.export_manager.export_log_file(self.poly_name, self.refinement_level)
        if not success and message == "no_log_file":
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Error", "No se encontró ningún archivo de historial para exportar.")