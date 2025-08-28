from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QGroupBox, QScrollArea, QProgressBar,
                            QSlider, QComboBox, QGridLayout)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QStyle

from collections import defaultdict
import numpy as np


class PanelDerecho(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.modo_visualizacion = "solido"  # Estado inicial
        self.threshold_angulo = 30  # Valor inicial del threshold
        self.setup_ui()
        self.metricas_actuales = None
        
    def setup_ui(self):
        """Configura la interfaz del panel derecho"""
        self.setWidgetResizable(True)
        self.setMaximumWidth(320)
        self.setMinimumWidth(280)
        
        # Widget contenedor principal
        self.contenido = QWidget()
        self.layout_principal = QVBoxLayout(self.contenido)
        self.layout_principal.setSpacing(12)
        self.layout_principal.setContentsMargins(12, 12, 12, 12)
        
        # Crear secciones (quitamos crear_seccion_informacion)
        self.crear_seccion_metricas()
        self.crear_seccion_threshold()  # Nueva sección para threshold
        self.crear_seccion_animacion()
        self.crear_seccion_visualizacion()
        self.crear_seccion_acciones()
        self.crear_seccion_estadisticas()
        
        # Espaciador final
        self.layout_principal.addStretch()
        
        self.setWidget(self.contenido)
        self.aplicar_estilo_botones()
        self.actualizar_estado_botones_visualizacion()
        self.actualizar_display_threshold()
    
    def crear_seccion_metricas(self):
        """Sección de métricas de calidad (ahora dinámica)"""
        self.grupo_metricas = QGroupBox("Métricas de Calidad")
        self.grupo_metricas.setStyleSheet("QGroupBox { font-weight: bold; color: #ffffff; }")
        layout = QVBoxLayout()
        
        # Label para mostrar las métricas (inicialmente vacío)
        self.label_metricas = QLabel("Cargue un archivo para ver las métricas")
        self.label_metricas.setWordWrap(True)
        self.label_metricas.setTextFormat(Qt.RichText)
        self.label_metricas.setStyleSheet("""
            QLabel {
                background-color: #2a2a2a;
                padding: 12px;
                border-radius: 6px;
                min-height: 120px;
            }
        """)
        
        layout.addWidget(self.label_metricas)
        self.grupo_metricas.setLayout(layout)
        self.layout_principal.insertWidget(0, self.grupo_metricas)  # Insertar al principio
    
    def actualizar_metricas(self, contenido_html):
        """Actualiza el contenido de las métricas"""
        self.label_metricas.setText(contenido_html)
    
    def crear_seccion_threshold(self):
        """Sección para controlar el threshold de ángulos críticos"""
        grupo = QGroupBox("Umbral de Ángulos Críticos")
        grupo.setStyleSheet("QGroupBox { font-weight: bold; color: #ffffff; }")
        layout = QVBoxLayout()
        layout.setSpacing(8)
        
        # Display del valor actual con color (INVERTIDO)
        self.label_threshold = QLabel()
        self.label_threshold.setAlignment(Qt.AlignCenter)
        self.label_threshold.setStyleSheet("""
            QLabel {
                background-color: #2a2a2a;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 14px;
            }
        """)
        
        # Slider para el threshold (INVERTIR MIN/MAX)
        slider_layout = QHBoxLayout()
        label_min = QLabel("10°")
        label_min.setStyleSheet("color: #ff6b6b;")  # ROJO para ángulos bajos (peores)
        
        self.slider_threshold = QSlider(Qt.Horizontal)
        self.slider_threshold.setRange(10, 80)
        self.slider_threshold.setValue(self.threshold_angulo)
        self.slider_threshold.valueChanged.connect(self.actualizar_threshold)
        
        label_max = QLabel("80°")
        label_max.setStyleSheet("color: #4ecdc4;")  # VERDE para ángulos altos (mejores)
        
        slider_layout.addWidget(label_min)
        slider_layout.addWidget(self.slider_threshold)
        slider_layout.addWidget(label_max)
        
        # Leyenda de colores (CORREGIDA)
        leyenda_html = """
        <div style='background-color: #2a2a2a; padding: 8px; border-radius: 4px; font-size: 11px;'>
            <span style='color: #ff6b6b;'>● Crítico</span> | 
            <span style='color: #ff9f43;'>● Regular</span> | 
            <span style='color: #4ecdc4;'>● Bueno</span>
        </div>
        """
        label_leyenda = QLabel(leyenda_html)
        label_leyenda.setTextFormat(Qt.RichText)
        
        layout.addWidget(self.label_threshold)
        layout.addLayout(slider_layout)
        layout.addWidget(label_leyenda)
        grupo.setLayout(layout)
        self.layout_principal.addWidget(grupo)

    def actualizar_display_threshold(self):
        """Actualiza el display del threshold con colores (INVERTIDO)"""
        # Determinar color basado en el valor - ÁNGULOS BAJOS = MALOS = ROJO
        if self.threshold_angulo <= 25:
            color = "#f6b6fb"  # ROJO - ángulos muy bajos (críticos)
        elif self.threshold_angulo <= 45:
            color = "#ff9f43"  # NARANJA - ángulos medios (regulares)
        else:
            color = "#4ecdc4"  # VERDE AZULADO - ángulos altos (buenos)
        
        texto = f"Umbral actual: <span style='color: {color}; font-size: 16px;'><b>{self.threshold_angulo}°</b></span>"
        self.label_threshold.setText(texto)
        self.label_threshold.setTextFormat(Qt.RichText)
    
    def crear_seccion_animacion(self):
        """Sección de control de animación"""
        grupo = QGroupBox("Control de Animación")
        grupo.setStyleSheet("QGroupBox { font-weight: bold; color: #ffffff; }")
        layout = QVBoxLayout()
        layout.setSpacing(8)
        
        # Control de velocidad
        velocidad_layout = QHBoxLayout()
        label_velocidad = QLabel("Velocidad:")
        self.slider_velocidad = QSlider(Qt.Horizontal)
        self.slider_velocidad.setRange(500, 3000)
        self.slider_velocidad.setValue(1500)
        self.label_velocidad_valor = QLabel("1.5s")
        
        velocidad_layout.addWidget(label_velocidad)
        velocidad_layout.addWidget(self.slider_velocidad)
        velocidad_layout.addWidget(self.label_velocidad_valor)
        
        layout.addLayout(velocidad_layout)
        grupo.setLayout(layout)
        self.layout_principal.addWidget(grupo)
    
    def crear_seccion_visualizacion(self):
        """Sección específica para modos de visualización"""
        grupo = QGroupBox("Modo de Visualización")
        grupo.setStyleSheet("QGroupBox { font-weight: bold; color: #ffffff; }")
        layout = QHBoxLayout()
        
        # Botones de visualización
        self.boton_wireframe = QPushButton("Wireframe")
        self.boton_solido = QPushButton("Sólido")

        # Tooltips
        self.boton_wireframe.setToolTip("Shortcut: W")
        self.boton_solido.setToolTip("Shortcut: S")

        # Conectar señales
        self.boton_wireframe.clicked.connect(self.activar_wireframe)
        self.boton_solido.clicked.connect(self.activar_solido)
        
        layout.addWidget(self.boton_wireframe)
        layout.addWidget(self.boton_solido)
        grupo.setLayout(layout)
        self.layout_principal.addWidget(grupo)
    
    def crear_seccion_acciones(self):
        """Sección de acciones rápidas"""
        grupo = QGroupBox("Acciones Rápidas")
        grupo.setStyleSheet("QGroupBox { font-weight: bold; color: #ffffff; }")
        layout = QGridLayout()
        layout.setSpacing(6)
        
        # Botones esenciales
        self.boton_limpiar = QPushButton("Limpiar")
        self.boton_puntos_criticos = QPushButton("Puntos Críticos")
        self.boton_reset_camara = QPushButton("Reset Cámara")

        self.boton_limpiar.setToolTip("Shortcut: B")
        self.boton_puntos_criticos.setToolTip("Shortcut: A")
        self.boton_reset_camara.setToolTip("Shortcut: R")
        
        # Agregar al layout
        layout.addWidget(self.boton_limpiar, 0, 0)
        layout.addWidget(self.boton_reset_camara, 0, 1)
        layout.addWidget(self.boton_puntos_criticos, 1 , 0 , 1, 2)
        grupo.setLayout(layout)
        self.layout_principal.addWidget(grupo)

    def actualizar_estadisticas(self, metricas):
        """Actualiza la sección de estadísticas con métricas de calidad"""
        self.metricas_actuales = metricas
        
        if not metricas or 'error' in metricas:
            stats_html = """
            <div style='background-color: #2a2a2a; padding: 12px; border-radius: 6px; font-family: monospace; color: #ff6b6b;'>
                <b>❌ No hay métricas disponibles</b><br>
                Carga un modelo primero o verifica el archivo.
            </div>
            """
            self.label_estadisticas.setText(stats_html)
            return
        
        stats = metricas['estadisticas_generales']
        total_triangulos = stats.get('total_triangulos', 0)
        total_cuadrilateros = stats.get('total_cuadrilateros', 0)
        total_caras = total_triangulos + total_cuadrilateros
        
        # Calcular porcentajes
        porc_triangulos = (total_triangulos / total_caras * 100) if total_caras > 0 else 0
        porc_cuadrilateros = (total_cuadrilateros / total_caras * 100) if total_caras > 0 else 0
        
        # Construir HTML en el mismo estilo
        stats_html = f"""
        <div style='background-color: #2a2a2a; padding: 12px; border-radius: 6px; font-family: monospace;'>
            <b>Topología:</b><br>
            • Vértices: <span style='color: #4ecdc4;'>N/A</span><br>
            • Caras: <span style='color: #4ecdc4;'>{total_caras}</span><br>
            • Triángulos: <span style='color: #ff9f43;'>{total_triangulos}</span> ({porc_triangulos:.1f}%)<br>
            • Cuadriláteros: <span style='color: #ff9f43;'>{total_cuadrilateros}</span> ({porc_cuadrilateros:.1f}%)<br><br>
            
            <b>Calidad:</b><br>
        """
        
        # Añadir métricas de triángulos si existen
        if metricas['triangulos']:
            triangulos = metricas['triangulos']
            stats_html += f"""
            <b>Triángulos:</b><br>
            • Relación aspecto: <span style='color: #4ecdc4;'>{triangulos.get('aspect_ratio_avg', 'N/A'):.3f}</span><br>
            • Ángulo mínimo: <span style='color: #4ecdc4;'>{triangulos.get('min_angle_avg', 'N/A'):.1f}°</span><br>
            • Ángulo máximo: <span style='color: #ff6b6b;'>{triangulos.get('max_angle_avg', 'N/A'):.1f}°</span><br>
            • Área promedio: <span style='color: #4ecdc4;'>{triangulos.get('area_avg', 'N/A'):.6f}</span><br>
            """
        
        # Añadir métricas de cuadriláteros si existen
        if metricas['cuadrilateros']:
            cuadrilateros = metricas['cuadrilateros']
            stats_html += f"""
            <b>Cuadriláteros:</b><br>
            • Relación aspecto: <span style='color: #4ecdc4;'>{cuadrilateros.get('aspect_ratio_avg', 'N/A'):.3f}</span><br>
            • Distorsión: <span style='color: #ff6b6b;'>{cuadrilateros.get('skew_avg', 'N/A'):.3f}</span><br>
            • Relación aristas: <span style='color: #4ecdc4;'>{cuadrilateros.get('edge_ratio_avg', 'N/A'):.3f}</span><br>
            """
        
        stats_html += "</div>"
        self.label_estadisticas.setText(stats_html)
    
    
    def crear_seccion_estadisticas(self):
        """Sección de estadísticas detalladas - Ahora se actualiza dinámicamente"""
        grupo = QGroupBox("Estadísticas Detalladas")
        grupo.setStyleSheet("QGroupBox { font-weight: bold; color: #ffffff; }")
        layout = QVBoxLayout()
        
        # Label para estadísticas (ahora se actualizará dinámicamente)
        self.label_estadisticas = QLabel()
        self.label_estadisticas.setTextFormat(Qt.RichText)
        self.label_estadisticas.setWordWrap(True)
        
        # Mensaje inicial
        html_inicial = """
        <div style='background-color: #2a2a2a; padding: 12px; border-radius: 6px; font-family: monospace; color: #4ecdc4;'>
            <b>🔄 Esperando modelo...</b><br>
            Carga un archivo para ver las estadísticas.
        </div>
        """
        self.label_estadisticas.setText(html_inicial)
        
        layout.addWidget(self.label_estadisticas)
        grupo.setLayout(layout)
        self.layout_principal.addWidget(grupo)
    
    def actualizar_threshold(self, valor):
        """Actualiza el threshold y el display"""
        self.threshold_angulo = valor
        self.actualizar_display_threshold()
        print(f"Threshold actualizado: {valor}°")  # Solo para debug
    
    def actualizar_display_threshold(self):
        """Actualiza el display del threshold con colores"""
        # Determinar color basado en el valor
        if self.threshold_angulo <= 25:
            color = "#ff6b6b"  # Verde azulado - muy bajo
        elif self.threshold_angulo <= 45:
            color = "#ff9f43"  # Naranja - medio
        else:
            color = "#4ecdc4"  # Rojo - alto
        
        texto = f"Umbral actual: <span style='color: {color}; font-size: 16px;'><b>{self.threshold_angulo}°</b></span>"
        self.label_threshold.setText(texto)
        self.label_threshold.setTextFormat(Qt.RichText)
    
    def activar_wireframe(self):
        """Activa modo wireframe"""
        self.modo_visualizacion = "wireframe"
        self.actualizar_estado_botones_visualizacion()
        # Llamar a la función del parent si existe
        if self.parent and hasattr(self.parent, 'accion_w'):
            self.parent.accion_w()
    
    def activar_solido(self):
        """Activa modo sólido"""
        self.modo_visualizacion = "solido"
        self.actualizar_estado_botones_visualizacion()
        # Llamar a la función del parent si existe
        if self.parent and hasattr(self.parent, 'accion_s'):
            self.parent.accion_s()
    
    def actualizar_estado_botones_visualizacion(self):
        """Actualiza el aspecto visual de los botones según el modo activo"""
        estilo_activo = """
            QPushButton {
                background-color: #2e7d32;
                color: white;
                border: 2px solid #4caf50;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #3d8b40;
            }
        """
        
        estilo_inactivo = """
            QPushButton {
                background-color: #4a4a4a;
                color: white;
                border: 1px solid #666;
                padding: 8px;
                border-radius: 4px;
            }
            QPushButton:hover {
                background-color: #5a5a5a;
            }
        """
        
        if self.modo_visualizacion == "wireframe":
            self.boton_wireframe.setStyleSheet(estilo_activo)
            self.boton_solido.setStyleSheet(estilo_inactivo)
        else:
            self.boton_wireframe.setStyleSheet(estilo_inactivo)
            self.boton_solido.setStyleSheet(estilo_activo)
    
    def set_modo_visualizacion(self, modo):
        """Sincronizar el modo de visualización desde fuera"""
        if modo in ["wireframe", "solido"]:
            self.modo_visualizacion = modo
            self.actualizar_estado_botones_visualizacion()
    
    def aplicar_estilo_botones(self):
        """Aplica estilo consistente a todos los botones"""
        estilo_base = """
            QPushButton {
                background-color: #4a4a4a;
                color: white;
                border: 1px solid #666;
                padding: 8px;
                border-radius: 4px;
                margin: 2px;
            }
            QPushButton:hover {
                background-color: #5a5a5a;
            }
            QPushButton:disabled {
                background-color: #333333;
                color: #777777;
            }
            QPushButton:pressed {
                background-color: #3a3a3a;
            }
        """
        
        # Aplicar a todos los botones
        for btn in self.findChildren(QPushButton):
            btn.setStyleSheet(estilo_base)