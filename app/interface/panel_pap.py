from PyQt5.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class PanelPAP(QScrollArea):
    """Panel para el modo Paso A Paso (PAP).

    Esta es una implementación mínima/placeholder: diseño simple y métodos
    de actualización básicos para que puedas extenderlo luego.
    """
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setMinimumWidth(320)
        self.setMaximumWidth(480)

        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(12, 12, 12, 12)
        self.layout.setSpacing(8)

        # Placeholder content
        title = QLabel("Paso a Paso")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff;")

        info = QLabel("Aquí irán los controles y la información del modo Paso a Paso.")
        info.setWordWrap(True)
        info.setStyleSheet("background-color: #2a2a2a; padding: 8px; border-radius: 6px;")

        self.layout.addWidget(title)
        self.layout.addWidget(info)
        self.layout.addStretch()

        self.setWidget(self.container)

    # API mínima para integrarlo con MainWindow
    def show_panel(self):
        self.show()

    def hide_panel(self):
        self.hide()

    def actualizar_info(self, texto: str):
        """Actualizar el texto del panel (placeholder)."""
        # Reemplaza el segundo widget (info) contenido en layout
        if self.layout.count() >= 2:
            info_widget = self.layout.itemAt(1).widget()
            if isinstance(info_widget, QLabel):
                info_widget.setText(texto)

    # Puedes añadir más métodos luego para cargar historial, controles, etc.
