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

        # Label para mostrar estado del paso actual (ej: "Paso 3 de 20")
        self.step_label = QLabel("Paso: -")
        self.step_label.setAlignment(Qt.AlignCenter)
        self.step_label.setStyleSheet("font-size: 12px; color: #ffd700;")

        info = QLabel("Aquí irán los controles y la información del modo Paso a Paso.")
        info.setWordWrap(True)
        info.setStyleSheet("background-color: #2a2a2a; padding: 8px; border-radius: 6px;")

        self.layout.addWidget(title)
        self.layout.addWidget(self.step_label)
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

    def actualizar_estado_pasos(self, current: int, total: int):
        """Actualiza la etiqueta de estado con el paso actual y el total.

        current: índice actual (0-based o 1-based según convención). Aquí usamos 1-based para mostrar.
        total: número total de pasos/comandos.
        """
        print("se actualiza estado pasos PAP")
        try:
            # Mostrar como 1-based al usuario
            cur = int(current) if current is not None else 0
            tot = int(total) if total is not None else 0
            # Si el valor interno es 0-based (estado['i']), mostramos cur (0) como 0 de tot
            # Normalmente queremos mostrar "Paso 3 de 20" cuando cur==3
            # Si prefieres 1-based: usar cur_display = cur if cur > 0 else 0
            cur_display = cur
            self.step_label.setText(f"Paso {cur_display} de {tot}")
        except Exception:
            self.step_label.setText("Paso: -")

    # Puedes añadir más métodos luego para cargar historial, controles, etc.
