from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt

class PanelDerecho(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.label = QLabel("Métricas de ángulos críticos")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def actualizar_panel(self, ruta_archivo):
        import os
        try:
            base, _ = os.path.splitext(ruta_archivo)
            ruta_modificada = f"{base}_histo.txt"
            numero = base.split('_')[-1]
            with open(ruta_modificada, 'r') as f:
                lineas = f.readlines()
            angulo_triangulo = None
            angulo_cuadrado = None
            for i, linea in enumerate(lineas):
                if "For Triangles:" in linea and i + 1 < len(lineas):
                    angulo_triangulo = lineas[i + 1].strip()
                if "For Quads:" in linea and i + 1 < len(lineas):
                    angulo_cuadrado = lineas[i + 1].strip()
            def formatear_angulo(label, linea):
                partes = linea.split('|')
                min_ang = partes[0].strip()
                max_ang = partes[1].strip() if len(partes) > 1 else ''
                return f"<b>- {label}:</b><br>{min_ang}<br>{max_ang}<br><br>"
            if angulo_triangulo or angulo_cuadrado:
                contenido_html = "<b>Nivel de Refinamiento: " + numero + "</b><br><br><br>"
                contenido_html += "<b>Ángulos Críticos:</b><br><br>"
                if angulo_triangulo:
                    contenido_html += formatear_angulo("Triángulos", angulo_triangulo)
                if angulo_cuadrado:
                    contenido_html += formatear_angulo("Cuadriláteros", angulo_cuadrado)
            else:
                contenido_html = "<b>No se encontraron líneas de ángulos para triángulos ni cuadriláteros.</b>"
            self.label.setText(contenido_html)
        except Exception as e:
            self.label.setText(f"<b>Error al leer el archivo:</b><br>{e}")