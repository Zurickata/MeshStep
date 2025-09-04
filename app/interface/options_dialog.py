from PyQt5.QtWidgets import QDialog, QVBoxLayout, QCheckBox, QPushButton

class OpcionesDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Opciones avanzadas")
        self.setFixedSize(250, 100)
        self.checkbox = QCheckBox("Ignorar límite de hardware")
        self.checkbox.setChecked(False)
        btn_ok = QPushButton("Aceptar")
        btn_ok.clicked.connect(self.accept)

        layout = QVBoxLayout()
        layout.addWidget(self.checkbox)
        layout.addWidget(btn_ok)
        self.setLayout(layout)