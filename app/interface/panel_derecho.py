from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QGroupBox, QScrollArea,
                            QSlider, QGridLayout)
from PyQt5.QtCore import Qt, QCoreApplication, QEvent

import os
import re
from app.visualization.FeriaVTK import CustomInteractorStyle
from app.logic.main_window_logic import (
    accion_w, accion_s
)
from app.visualization.FeriaVTK import notifier

class PanelDerecho(QScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.refinement_viewer = None
        self.parent = parent
        #self.modo_visualizacion = "solido"  # Estado inicial
        self.threshold_angulo = 30  # Valor inicial del threshold
        self.setup_ui()
        self.metricas_actuales = None
        
    def setup_ui(self):
        """Configura la interfaz del panel derecho"""
        self.setWidgetResizable(True)
        self.setMaximumWidth(480)
        self.setMinimumWidth(320)
        
        # Widget contenedor principal
        self.contenido = QWidget()
        self.layout_principal = QVBoxLayout(self.contenido)
        self.layout_principal.setSpacing(12)
        self.layout_principal.setContentsMargins(12, 12, 12, 12)
        
        # Crear secciones 
        self.crear_seccion_metricas()
        self.crear_seccion_coloreos()
        self.crear_seccion_acciones()
        self.crear_seccion_estadisticas()
        self.crear_seccion_threshold()
        self.crear_seccion_animacion()
        
        # Espaciador final
        self.layout_principal.addStretch()
        
        self.setWidget(self.contenido)
        self.aplicar_estilo_botones()
        
        self.actualizar_display_threshold()
       

        notifier.cell_selected.connect(self.mostrar_info_celda)
        notifier.cell_deselected.connect(self.limpiar_info_celda)

    def mostrar_info_celda(self, cell_id, num_points, min_angle):
        """Muestra información de la celda seleccionada"""
        # Determinar color basado en el ángulo mínimo
        if min_angle < 25:
            color_angle = "#ff6b6b"  # Rojo - crítico
            calidad = "Crítico"
        elif min_angle < 45:
            color_angle = "#ff9f43"  # Naranja - regular
            calidad = "Regular"
        else:
            color_angle = "#4ecdc4"  # Verde - bueno
            calidad = "Bueno"
        
        # Crear HTML para la información de la celda
        celda_html = f"""
        <div style='background-color: #3a3a3a; padding: 8px; border-radius: 4px; margin-top: 8px;'>
            <b style='color: #ffd700;'>Celda seleccionada:</b><br>
            ID: <span style='color:#4ecdc4;'>{cell_id}</span><br>
            Puntos: <span style='color:#ff9f43;'>{num_points}</span><br>
            Ángulo mínimo: <span style='color:{color_angle};'>{min_angle:.2f}°</span><br>
            Calidad: <span style='color:{color_angle};'>{calidad}</span>
        </div>
        """
        
    
        self.actualizar_metricas(self._contenido_base_sin_celda + celda_html)

    def limpiar_info_celda(self):
        
        if hasattr(self, '_contenido_base_sin_celda') and self._contenido_base_sin_celda:
            self.actualizar_metricas(self._contenido_base_sin_celda)
        else:
            # Fallback: mostrar solo el número de refinamiento
            base_path = getattr(self, '_archivo_actual', '')
            if base_path:
                base, _ = os.path.splitext(base_path)
                numero = base.split('_')[-1] if '_' in base else "?"
                contenido_html = f"""
                <div style='background-color: #2a2a2a; padding: 12px; border-radius: 6px;'>
                    <b style='color: #ffd700;'>Nivel de Refinamiento: {numero}</b><br><br>
                    <i style='color: #888;'>No hay celda seleccionada</i>
                </div>
                """
                self.actualizar_metricas(contenido_html)
                self._contenido_base_sin_celda = contenido_html

    
    def actualizar_panel_derecho(self, ruta_archivo):
        
        try:
            base, _ = os.path.splitext(ruta_archivo)
            numero = base.split('_')[-1]
            if self.refinement_viewer and self.refinement_viewer.switcher:
                switcher = self.refinement_viewer.switcher
                archivos = switcher.file_dict.get(switcher.current_poly, [])
                ultimo_archivo = archivos[-1] if archivos else "N/A"
                ultimo_archivo = ultimo_archivo.split('_')[-1] if '_' in ultimo_archivo else "N/A"
                ultimo_level_refinement = ultimo_archivo.split('.')[0] if '.' in ultimo_archivo else "N/A"
             # Plantilla traducible con placeholders %1 (actual) y %2 (máximo)
            tpl = QCoreApplication.translate(
                "PanelDerecho",
                "<div style='margin-top: 10px; padding: 8px; background-color: #3a3a3a; border-radius: 4px;'>"
                "<div style='background-color: #2a2a2a; padding: 12px; border-radius: 6px;'>"
                "<b style='color: #ffd700;'>Nivel de Refinamiento: %1/%2</b><br><br>"
                "</div>"
                "</div>"
            )
            contenido_html = (tpl
                              .replace("%1", str(numero))
                              .replace("%2", str(ultimo_level_refinement)))
            
            # Actualizar el panel derecho
            self.actualizar_metricas(contenido_html)
            # Guardar como contenido base limpio (SIN información de celda)
            self._contenido_base_sin_celda = contenido_html
            self._archivo_actual = ruta_archivo

        except Exception as e:
            error_html = f"""
            <div style='background-color: #2a2a2a; padding: 12px; border-radius: 6px; color: #ff6b6b;'>
                <b>Error al leer el archivo:</b><br>{str(e)}<br><br>
                <span style='font-size: 12px; color: #cccccc;'>Ruta:</span>
            </div>
            """
            self.actualizar_metricas(error_html)

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
        grupo = QGroupBox("Umbral de Ángulos Mínimos Críticos")
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
        
        # Label para mostrar los conteos bajo/encima del umbral
        self.label_threshold_counts = QLabel()
        self.label_threshold_counts.setWordWrap(True)
        self.label_threshold_counts.setTextFormat(Qt.RichText)
        self.label_threshold_counts.setStyleSheet(
            """
            QLabel {
                background-color: #2a2a2a;
                padding: 8px;
                border-radius: 4px;
                font-size: 13px;
                color: #ffffff;
            }
            """
        )
        # Placeholder inicial para que no se vea vacío
        self.label_threshold_counts.setText(
            "<div style='color:#cccccc;'>Cargue un archivo para ver conteos por umbral.</div>"
        )

        layout.addWidget(self.label_threshold)
        layout.addLayout(slider_layout)
        layout.addWidget(label_leyenda)
        layout.addWidget(self.label_threshold_counts)
        grupo.setLayout(layout)
        self.layout_principal.addWidget(grupo)

    def actualizar_threshold(self, valor):
        """Actualiza el umbral y refresca el conteo/visual."""
        try:
            self.threshold_angulo = int(valor)
        except Exception:
            try:
                self.threshold_angulo = float(valor)
            except Exception:
                pass
        self.actualizar_display_threshold()

    def actualizar_display_threshold(self):
        """Actualiza el display del threshold con colores (INVERTIDO)"""
        # Determinar color basado en el valor - ÁNGULOS BAJOS = MALOS = ROJO
        if self.threshold_angulo <= 25:
            color = "#ff6b6b"  # ROJO - ángulos muy bajos (críticos)
        elif self.threshold_angulo <= 45:
            color = "#ff9f43"  # NARANJA - ángulos medios (regulares)
        else:
            color = "#4ecdc4"  # VERDE AZULADO - ángulos altos (buenos)
        
        texto = f"Umbral actual: <span style='color: {color}; font-size: 16px;'><b>{self.threshold_angulo}°</b></span>"
        self.label_threshold.setText(texto)
        self.label_threshold.setTextFormat(Qt.RichText)

        # Si hay métricas cargadas, calcular conteos por debajo/encima del umbral
        try:
            conteo_html = self._construir_conteo_threshold_html()
        except Exception:
            conteo_html = (
                "<div style='color:#cccccc;'>Cargue un archivo para ver conteos por umbral.</div>"
            )
        if hasattr(self, 'label_threshold_counts') and self.label_threshold_counts:
            self.label_threshold_counts.setText(conteo_html)
            self.label_threshold_counts.setTextFormat(Qt.RichText)

    def _construir_conteo_threshold_html(self):
        """Construye HTML con conteos de ángulos mínimos por debajo/encima del umbral.

        Usa self.metricas_actuales['triangulos']['min_angle'] y
        self.metricas_actuales['cuadrilateros']['min_angle'] si existen.
        """
        if not self.metricas_actuales:
            raise ValueError("No hay métricas actuales")

        tri = self.metricas_actuales.get('triangulos', {}) or {}
        quad = self.metricas_actuales.get('cuadrilateros', {}) or {}

        tri_list = tri.get('min_angle', []) or []
        quad_list = quad.get('min_angle', []) or []

        # Asegurar que los valores sean numéricos
        def to_float_list(vals):
            out = []
            for v in vals:
                try:
                    out.append(float(v))
                except Exception:
                    continue
            return out

        tri_vals = to_float_list(tri_list)
        quad_vals = to_float_list(quad_list)

        T = float(self.threshold_angulo)
        tri_below = sum(1 for v in tri_vals if v < T)
        tri_total = len(tri_vals)
        tri_above = tri_total - tri_below

        quad_below = sum(1 for v in quad_vals if v < T)
        quad_total = len(quad_vals)
        quad_above = quad_total - quad_below

        total_below = tri_below + quad_below
        total_total = tri_total + quad_total
        total_above = total_total - total_below

        # Si no hay datos aún, devolver un mensaje amigable
        if total_total == 0:
            return (
                "<div style='color:#cccccc;'>"
                "Sin datos de ángulos mínimos en métricas. "
                "Genere/recargue métricas para ver el conteo por umbral."
                "</div>"
            )

        # Colores por categoría
        color_below = "#ff6b6b"  # rojo
        color_above = "#4ecdc4"  # verde-azulado

        return f"""
        <div>
            <b style='color:#ffffff;'>Conteo de ángulos por umbral ({T:.0f}°):</b><br>
            • Triángulos: <br> 
            <span style='color:{color_below};'>{tri_below}</span> &lt; {T:.0f}°&nbsp;<span style='color:#cccccc;'></span>
            &nbsp;|&nbsp;
            <span style='color:{color_above};'>{tri_above}</span> &ge; {T:.0f}°&nbsp;<span style='color:#cccccc;'></span>
            &nbsp;<span style='color:#888;'>(de {tri_total})</span><br>
            • Cuadriláteros: <br> 
            <span style='color:{color_below};'>{quad_below}</span> &lt; {T:.0f}°&nbsp;<span style='color:#cccccc;'></span>
            &nbsp;|&nbsp;
            <span style='color:{color_above};'>{quad_above}</span> &ge; {T:.0f}°&nbsp;<span style='color:#cccccc;'></span>
            &nbsp;<span style='color:#888;'>(de {quad_total})</span><br>
            • Total: <br> 
            <span style='color:{color_below};'>{total_below}</span> &lt; {T:.0f}°&nbsp;<span style='color:#cccccc;'></span>
            &nbsp;|&nbsp;
            <span style='color:{color_above};'>{total_above}</span> &ge; {T:.0f}°&nbsp;<span style='color:#cccccc;'></span>
            &nbsp;<span style='color:#888;'>(de {total_total})</span>
        </div>
        """
    
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
        self.slider_velocidad.valueChanged.connect(self._on_velocidad_cambiada)

        velocidad_layout.addWidget(label_velocidad)
        velocidad_layout.addWidget(self.slider_velocidad)
        velocidad_layout.addWidget(self.label_velocidad_valor)
        
        layout.addLayout(velocidad_layout)
        grupo.setLayout(layout)
        self.layout_principal.addWidget(grupo)
    

    
    def crear_seccion_acciones(self):
        """Sección de acciones rápidas"""
        grupo = QGroupBox("Acciones Rápidas")
        grupo.setStyleSheet("QGroupBox { font-weight: bold; color: #ffffff; }")
        layout = QGridLayout()
        layout.setSpacing(6)
        
        # Botones esenciales
        self.boton_puntos_criticos = QPushButton("Puntos Críticos")
        self.boton_reset_camara = QPushButton("Reset Cámara")
        self.boton_reload = QPushButton("Recargar") 

        self.boton_puntos_criticos.setToolTip("Shortcut: A")
        self.boton_reset_camara.setToolTip("Shortcut: R")
        self.boton_reload.setToolTip("Shortcut: L")

        self.boton_puntos_criticos.clicked.connect(self.toggle_puntos_criticos)
        self.boton_reset_camara.clicked.connect(self.resetear_camara)
        self.boton_reload.clicked.connect(self.reload_modelo)

        # Agregar al layout
        layout.addWidget(self.boton_puntos_criticos, 0, 0)
        layout.addWidget(self.boton_reset_camara, 0, 1)
        layout.addWidget(self.boton_reload, 1, 0, 1, 2)
        grupo.setLayout(layout)
        self.layout_principal.addWidget(grupo)

    def actualizar_estadisticas(self, metricas):
        # print("actualizar_estadisticas llamado", metricas)
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
            • Ángulo mínimo: <span style='color: #4ecdc4;'>{triangulos.get('min_angle_min', 'N/A'):.1f}°</span><br>
            • Ángulo máximo: <span style='color: #ff6b6b;'>{triangulos.get('max_angle_avg', 'N/A'):.1f}°</span><br>
            • Área promedio: <span style='color: #4ecdc4;'>{triangulos.get('area_avg', 'N/A'):.6f}</span><br>
            """
        
        # Añadir métricas de cuadriláteros si existen
        if metricas['cuadrilateros']:
            cuadrilateros = metricas['cuadrilateros']
            stats_html += f"""
            <b>Cuadriláteros:</b><br>
            • Relación aspecto: <span style='color: #4ecdc4;'>{cuadrilateros.get('aspect_ratio_avg', 'N/A'):.3f}</span><br>
            • Ángulo mínimo: <span style='color: #4ecdc4;'>{cuadrilateros.get('min_angle_min', 'N/A'):.1f}°</span><br>
            • Ángulo máximo: <span style='color: #ff6b6b;'>{cuadrilateros.get('max_angle_avg', 'N/A'):.1f}°</span><br>
            • Distorsión: <span style='color: #ff6b6b;'>{cuadrilateros.get('skew_avg', 'N/A'):.3f}</span><br>
            • Relación aristas: <span style='color: #4ecdc4;'>{cuadrilateros.get('edge_ratio_avg', 'N/A'):.3f}</span><br>
            """
        
        stats_html += "</div>"
        self.label_estadisticas.setText(stats_html)
        # Refrescar el conteo por threshold si la sección existe
        try:
            if hasattr(self, 'label_threshold') and self.label_threshold:
                self.actualizar_display_threshold()
        except Exception:
            pass
    
    
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
    

#---------------------------------------------- Esta es la seccion a modificar xiska ----------------------------------------------------------

    def crear_seccion_coloreos(self):
        """Sección de acciones Coloreo"""
        grupo = QGroupBox("Coloreo")
        grupo.setStyleSheet("QGroupBox { font-weight: bold; color: #ffffff; }")
        layout = QGridLayout()
        layout.setSpacing(6)
        
        # Botones esenciales
        self.boton_color = QPushButton("Por área")
        self.boton_color2 = QPushButton("Por ángulo mínimo")
        self.boton_color3 = QPushButton("Relación de aspecto")

        self.boton_color.setToolTip("Shortcut: 1")
        self.boton_color2.setToolTip("Shortcut: 2")

        self.boton_color.clicked.connect(
            lambda: self.refinement_viewer.accion_area() if self.refinement_viewer else None
        )
        self.boton_color2.clicked.connect(
            lambda: self.refinement_viewer.accion_angulo_minimo() if self.refinement_viewer else None
        )
        self.boton_color3.clicked.connect(
            lambda: self.refinement_viewer.accion_relacion_aspecto() if self.refinement_viewer else None
        )

        # Agregar al layout
        layout.addWidget(self.boton_color, 0, 0)
        layout.addWidget(self.boton_color2, 0, 1)
        layout.addWidget(self.boton_color3, 1 , 0 , 1, 2)
        grupo.setLayout(layout)
        self.layout_principal.addWidget(grupo)


    
    def activar_wireframe(self):
        """Activa modo wireframe"""
        #self.modo_visualizacion = "wireframe"
        #self.actualizar_estado_botones_visualizacion()
        # Obtener la ventana principal de forma robusta
        main_window = self.window()
        accion_w(main_window)
    
    def activar_solido(self):
        """Activa modo sólido"""
        #self.modo_visualizacion = "solido"
        #self.actualizar_estado_botones_visualizacion()
        # Obtener la ventana principal de forma robusta
        main_window = self.window()
        accion_s(main_window)
    
    

    
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

    

    def toggle_puntos_criticos(self):
        if self.refinement_viewer and self.refinement_viewer.switcher:
            self.refinement_viewer.switcher.toggle_load = not self.refinement_viewer.switcher.toggle_load
            if self.refinement_viewer.switcher.toggle_load:
                self.refinement_viewer.switcher.marcar_angulos_extremos()
            else:
                self.refinement_viewer.switcher.clear_extra_models()
            self.refinement_viewer.renderer.GetRenderWindow().Render()

    def resetear_camara(self):
        if self.refinement_viewer and self.refinement_viewer.switcher:
            self.refinement_viewer.switcher.actor.SetOrientation(0, 0, 0)
            self.refinement_viewer.switcher.actor.SetPosition(0, 0, 0)
            self.refinement_viewer.switcher.actor.SetScale(1, 1, 1)
            self.refinement_viewer.renderer.ResetCamera()
            if isinstance(self.refinement_viewer.interactor.GetInteractorStyle(), CustomInteractorStyle):
                self.refinement_viewer.interactor.GetInteractorStyle().reset_camera_and_rotation()
            self.refinement_viewer.renderer.GetRenderWindow().Render()

    def _on_velocidad_cambiada(self, valor):
        """Maneja el cambio de velocidad"""
        segundos = valor / 1000.0
        self.label_velocidad_valor.setText(f"{segundos:.1f}s")
        
        # Ajustar directamente en el refinement viewer si está disponible
        if self.refinement_viewer:
            self.refinement_viewer.ajustar_velocidad(valor)

    def reload_modelo(self):
        """Recarga el modelo actual desde el archivo"""
        if self.refinement_viewer and self.refinement_viewer.switcher:
            switcher = self.refinement_viewer.switcher
            archivos = switcher.file_dict.get(switcher.current_poly, [])
            
            if archivos and 0 <= switcher.current_index < len(archivos):
                archivo_actual = archivos[switcher.current_index]
                print(f"Recargando modelo: {archivo_actual}")

                # LIMPIAR HIGHLIGHTER
                style = switcher.interactor.GetInteractorStyle()
                if isinstance(style, CustomInteractorStyle):
                    if hasattr(style, "highlight_actor") and style.highlight_actor:
                        switcher.renderer.RemoveActor(style.highlight_actor)
                        style._remove_highlight()
                        style.highlight_actor = None
                        
                    style.last_selected_cell = None
                
                # Emitir deselección para limpiar panel
                notifier.cell_deselected.emit()
                
                # Forzar recarga del modelo
                switcher.load_model(archivo_actual)
                
                # Limpiar extras y resetear toggle
                switcher.clear_extra_models()
                switcher.toggle_load = False
                
                # Actualizar panel derecho si es necesario
                if hasattr(self, 'actualizar_panel_derecho'):
                    self.actualizar_panel_derecho(archivo_actual)
                
                print("✅ Modelo recargado exitosamente")
            else:
                print("⚠️ No hay modelo actual para recargar")
        else:
            print("⚠️ No hay refinement viewer o switcher disponible")

    def changeEvent(self, event):
        # Regenerar HTML traducible al cambiar el idioma de la app
        if event.type() == QEvent.LanguageChange:
            if hasattr(self, "_archivo_actual") and self._archivo_actual:
                try:
                    self.actualizar_panel_derecho(self._archivo_actual)
                except Exception:
                    pass
        super().changeEvent(event)