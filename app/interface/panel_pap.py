from PyQt5.QtWidgets import QScrollArea, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QEvent
import os

class PanelPAP(QScrollArea):
    """Panel para el modo Paso A Paso (PAP)."""
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWidgetResizable(True)
        self.setMinimumWidth(320)
        self.setMaximumWidth(480)

        self.container = QWidget()
        self.layout = QVBoxLayout(self.container)
        self.layout.setContentsMargins(12, 12, 12, 12)
        self.layout.setSpacing(8)

        self.ruta_archivo = None

        # Estado para regenerar textos (paso actual)
        self._step_current = 0
        self._step_total = 0

        # Título del panel (traducible)
        self.title_label = QLabel(self.tr("Paso a Paso"))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #ffffff;")

        # Label para mostrar estado del paso actual (ej: "Paso 3 de 20")
        self.step_label = QLabel("Paso: -")
        self.step_label.setAlignment(Qt.AlignCenter)
        self.step_label.setStyleSheet("font-size: 12px; color: #ffd700;")

        # CONTROLES: usar HTML para buen espaciado y sin sangrías
        self.info_label = QLabel()
        self.info_label.setTextFormat(Qt.RichText)
        self.info_label.setWordWrap(True)
        self.info_label.setStyleSheet("background-color: #2a2a2a; padding: 10px; border-radius: 6px; color: #eaeaea;")
        self.info_label.setText(self._build_controls_html())

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.step_label)
        self.layout.addWidget(self.info_label)

        self.layout.addStretch()
        self.setWidget(self.container)

    # API mínima para integrarlo con MainWindow
    def show_panel(self):
        self.show()

    def hide_panel(self):
        self.hide()

    def ruta_para_pap(self, ruta: str):
        """Establece la ruta del archivo asociado al modo PAP."""
        self.ruta_archivo = ruta


    def actualizar_info(self, texto: str):
        """Actualizar el texto del panel (placeholder)."""
        if hasattr(self, "info_label") and isinstance(self.info_label, QLabel):
            self.info_label.setText(texto)

    def actualizar_estado_pasos(self, current: int, total: int):
        """Actualiza la etiqueta de estado con el paso actual y el total."""
        try:
            cur = int(current) if current is not None else 0
            tot = int(total) if total is not None else 0
            # Guardar estado para poder re-traducir en changeEvent
            self._step_current, self._step_total = cur, tot
            # Texto traducible con placeholders
            tpl = self.tr("Paso %1 de %2")
            step_text = tpl.replace("%1", str(cur)).replace("%2", str(tot))
            self.step_label.setText(step_text)
            self.step_label.setStyleSheet("background-color: #2a2a2a; padding: 8px; border-radius: 6px;color: #f3a123")
        except Exception:
            self.step_label.setText("Paso: -")

    def _build_controls_html(self) -> str:
        """HTML de instrucciones con mejor espaciado. Todo traducible."""
        items = [
            self.tr("Con la rueda del ratón puedes rotar la figura"),
            self.tr("Con el botón derecho del ratón puedes acercar/alejar la vista"),
            self.tr("Con el botón izquierdo del ratón puedes desplazar la figura"),
            self.tr("Con la tecla 'N' puedes avanzar al siguiente paso"),
            self.tr("Con la tecla 'W' activas Wireframe"),
            self.tr("Con la tecla 'S' activas Sólido"),
            self.tr("Con la tecla 'G' guardas el modelo actual"),
        ]
        # Quitar '•' manual para evitar doble viñeta
        lis = "".join(f"<li style='margin:6px 0;'>{txt}</li>" for txt in items)
        return (
            "<div style='font-family: Consolas, Menlo, monospace;'>"
            "<ul style='margin:0; padding-left:1.2em; line-height:1.7;'>"
            f"{lis}"
            "</ul>"
            "</div>"
        )



    def changeEvent(self, event):
        """Re-traduce título, paso y controles cuando cambie el idioma."""
        try:
            if event.type() == QEvent.LanguageChange:
                # Título del panel
                if hasattr(self, "title_label") and self.title_label:
                    self.title_label.setText(self.tr("Paso a Paso"))
                # Paso X de Y (usar últimos valores)
                if hasattr(self, "step_label") and self.step_label:
                    tpl = self.tr("Paso %1 de %2")
                    step_text = tpl.replace("%1", str(self._step_current)).replace("%2", str(self._step_total))
                    self.step_label.setText(step_text if self._step_total else self.tr("Paso: -"))
                # Controles
                if hasattr(self, "info_label") and self.info_label:
                    self.info_label.setText(self._build_controls_html())
        except Exception:
            pass
        super().changeEvent(event)