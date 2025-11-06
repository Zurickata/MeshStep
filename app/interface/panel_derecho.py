from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                            QLabel, QGroupBox, QScrollArea,
                            QSlider, QGridLayout, QMessageBox)
from PyQt5.QtCore import Qt, QCoreApplication, QEvent

import os
import re
from app.visualization.FeriaVTK import CustomInteractorStyle
from app.logic.metricas_jeans import (
    parse_jeans_output
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
        self.metricas_3d_actuales = None
        self.isMesh3D = False
        
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
        self.crear_seccion_metricas_3d()
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


    # -------------------FUNCIONES DEL HIGHLIGHTER -------------------

    def mostrar_info_celda(self, cell_id, num_points, min_angle):
        """Muestra información de la celda seleccionada"""
        # Determinar color basado en el ángulo mínimo
        if min_angle < 25:
            color_angle = "#ff6b6b"  # Rojo - crítico
            calidad_text = self.tr("Crítico")
        elif min_angle < 45:
            color_angle = "#ff9f43"  # Naranja - regular
            calidad_text = self.tr("Regular")
        else:
            color_angle = "#4ecdc4"  # Verde - bueno
            calidad_text = self.tr("Bueno")

        # Plantilla traducible con placeholders nombrados
        tpl = QCoreApplication.translate(
            "PanelDerecho",
            "<div style='background-color: #3a3a3a; padding: 8px; border-radius: 4px; margin-top: 8px;'>"
            "<b style='color: #ffd700;'>{sel_title}</b><br>"
            "{id_label} <span style='color:#4ecdc4;'>{cell_id}</span><br>"
            "{pts_label} <span style='color:#ff9f43;'>{num_points}</span><br>"
            "{min_label} <span style='color:{color_angle};'>{min_angle}°</span><br>"
            "{qual_label} <span style='color:{color_angle};'>{calidad}</span>"
            "</div>"
        )

        celda_html = tpl.format(
            sel_title=self.tr("Celda seleccionada:"),
            id_label=self.tr("ID:"),
            pts_label=self.tr("Puntos:"),
            min_label=self.tr("Ángulo mínimo:"),
            qual_label=self.tr("Calidad:"),
            cell_id=cell_id,
            num_points=num_points,
            min_angle=f"{min_angle:.2f}",
            color_angle=color_angle,
            calidad=calidad_text,
        )

        # Guardar estado de la última celda para reconstruir tras cambio de idioma
        self._ultima_celda = {
            "cell_id": cell_id,
            "num_points": num_points,
            "min_angle": float(min_angle),
        }
        
    
        self.actualizar_metricas(self._contenido_base_sin_celda + celda_html)

    def limpiar_info_celda(self):

        self._ultima_celda = None
        
        if hasattr(self, '_contenido_base_sin_celda') and self._contenido_base_sin_celda:
            self.actualizar_metricas(self._contenido_base_sin_celda)
        else:
            # Fallback: mostrar solo el número de refinamiento
            base_path = getattr(self, '_archivo_actual', '')
            if base_path:
                base, _ = os.path.splitext(base_path)
                numero = base.split('_')[-1] if '_' in base else "?"
                tpl = QCoreApplication.translate(
                    "PanelDerecho",
                    "<div style='background-color: #2a2a2a; padding: 12px; border-radius: 6px;'>"
                    "<b style='color: #ffd700;'>{ref_label} {numero}</b><br><br>"
                    "<i style='color: #888;'>{no_sel}</i>"
                    "</div>"
                )
                contenido_html = tpl.format(
                    ref_label=self.tr("Nivel de Refinamiento:"),
                    numero=numero,
                    no_sel=self.tr("No hay celda seleccionada"),
                )
                self.actualizar_metricas(contenido_html)
                self._contenido_base_sin_celda = contenido_html

# ------------------- FUNCIONES DEL PRIMER TEXTO, NIVELES DE REFINAMIENTO -------------------
    
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
            
            
            # --- visibilidad por prefijo del archivo (quadtree_ / octree_) ---
            fname = os.path.basename(ruta_archivo)
            name_no_ext = os.path.splitext(fname)[0]
            prefix = name_no_ext.split('_')[0].lower()
            if prefix not in ("quadtree", "octree"):
                print(f"[PanelDerecho] Prefijo desconocido en archivo: {fname}")

            is_3d = (prefix == "octree")
            self.isMesh3D = is_3d

            # 3D: ocultar threshold/estadísticas y mostrar Métricas 3D (prueba)
            if hasattr(self, "grupo_threshold") and self.grupo_threshold:
                self.grupo_threshold.setVisible(not is_3d)
            if hasattr(self, "grupo_estadisticas") and self.grupo_estadisticas:
                self.grupo_estadisticas.setVisible(not is_3d)
            if hasattr(self, "grupo_metricas_3d") and self.grupo_metricas_3d:
                self.grupo_metricas_3d.setVisible(is_3d)


            # Actualizar el panel derecho
            self.actualizar_metricas(contenido_html)
            if is_3d:
                self.actualizar_metricas_3d(ruta_archivo)

            # Guardar como contenido base limpio (SIN información de celda)
            self._contenido_base_sin_celda = contenido_html
            self._archivo_actual = ruta_archivo

        except Exception as e:
            tpl_err = QCoreApplication.translate(
                "PanelDerecho",
                "<div style='background-color: #2a2a2a; padding: 12px; border-radius: 6px; color: #ff6b6b;'>"
                "<b>%1</b><br>%2<br><br>"
                "<span style='font-size: 12px; color: #cccccc;'>%3</span><br>%4"
                "</div>"
            )
            error_label = QCoreApplication.translate("PanelDerecho", "Error al leer el archivo:")
            ruta_label = QCoreApplication.translate("PanelDerecho", "Ruta:")
            error_html = (tpl_err
                          .replace("%1", error_label)
                          .replace("%2", str(e))
                          .replace("%3", ruta_label)
                          .replace("%4", str(ruta_archivo)))
            self.actualizar_metricas(error_html)


    def crear_seccion_metricas(self):
        """Sección de métricas de calidad (ahora dinámica)"""
        titulo = QCoreApplication.translate("PanelDerecho", "Métricas de Calidad")
        self.grupo_metricas = QGroupBox(titulo)
        self.grupo_metricas.setStyleSheet("QGroupBox { font-weight: bold; color: #ffffff; }")
        layout = QVBoxLayout()
        
        # Label para mostrar las métricas (inicialmente vacío)
        placeholder = QCoreApplication.translate("PanelDerecho", "Cargue un archivo para ver las métricas")
        self.label_metricas = QLabel(placeholder)
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


# ------------------- FUNCIONES DEL THRESHOLD -------------------
    
    def crear_seccion_threshold(self):
        """Sección para controlar el threshold de ángulos críticos"""
        self.grupo_threshold = QGroupBox(self.tr("Umbral de Ángulos Mínimos Críticos"))
        self.grupo_threshold.setStyleSheet("QGroupBox { font-weight: bold; color: #ffffff; }")
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
        self.label_threshold_min = QLabel("10°")
        self.label_threshold_min.setStyleSheet("color: #ff6b6b;")  # ROJO para ángulos bajos (peores)

        self.slider_threshold = QSlider(Qt.Horizontal)
        self.slider_threshold.setRange(10, 80)
        self.slider_threshold.setValue(self.threshold_angulo)
        self.slider_threshold.valueChanged.connect(self.actualizar_threshold)

        self.label_threshold_max = QLabel("80°")
        self.label_threshold_max.setStyleSheet("color: #4ecdc4;")  # VERDE para ángulos altos (mejores)

        slider_layout.addWidget(self.label_threshold_min)
        slider_layout.addWidget(self.slider_threshold)
        slider_layout.addWidget(self.label_threshold_max)

        # Leyenda de colores
        self.label_leyenda = QLabel()
        self.label_leyenda.setTextFormat(Qt.RichText)

        self.label_threshold_counts = QLabel()
        self.label_threshold_counts.setWordWrap(True)
        self.label_threshold_counts.setTextFormat(Qt.RichText)
        self.label_threshold_counts.setStyleSheet(
            "QLabel { background-color: #2a2a2a; padding: 8px; border-radius: 4px; font-size: 13px; color: #ffffff; }"
        )
        self.label_threshold_counts.setText(
            "<div style='color:#cccccc;'>" + self.tr("Cargue un archivo para ver conteos por umbral.") + "</div>"
        )


        layout.addWidget(self.label_threshold)
        layout.addLayout(slider_layout)
        layout.addWidget(self.label_leyenda)
        layout.addWidget(self.label_threshold_counts)
        self.grupo_threshold.setLayout(layout)
        self.layout_principal.addWidget(self.grupo_threshold)

        self._rebuild_threshold_static_texts()

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

    def _rebuild_threshold_static_texts(self):
        """Textos estáticos de la sección threshold (dependen de idioma)."""
        # Leyenda traducible
        leyenda_html = (
            "<div style='background-color: #2a2a2a; padding: 8px; border-radius: 4px; font-size: 11px;'>"
            f"<span style='color: #ff6b6b;'>● {self.tr('Crítico')}</span> | "
            f"<span style='color: #ff9f43;'>● {self.tr('Regular')}</span> | "
            f"<span style='color: #4ecdc4;'>● {self.tr('Bueno')}</span>"
            "</div>"
        )
        self.label_leyenda.setText(leyenda_html)
        self.grupo_threshold.setTitle(self.tr("Umbral de Ángulos Mínimos Críticos"))
        self.label_threshold_min.setText("10°")
        self.label_threshold_max.setText("80°")

    def actualizar_display_threshold(self):
        """Actualiza el display del threshold con colores (INVERTIDO)"""
        # Determinar color basado en el valor - ÁNGULOS BAJOS = MALOS = ROJO
        if self.threshold_angulo <= 25:
            color = "#ff6b6b"  # ROJO - ángulos muy bajos (críticos)
        elif self.threshold_angulo <= 45:
            color = "#ff9f43"  # NARANJA - ángulos medios (regulares)
        else:
            color = "#4ecdc4"  # VERDE AZULADO - ángulos altos (buenos)
        
        tpl = self.tr("Umbral actual: <span style='color: {color}; font-size: 16px;'><b>{value}°</b></span>")
        texto = tpl.format(color=color, value=self.threshold_angulo)
        self.label_threshold.setText(texto)
        self.label_threshold.setTextFormat(Qt.RichText)

        # Si hay métricas cargadas, calcular conteos por debajo/encima del umbral
        try:
            conteo_html = self._construir_conteo_threshold_html()
        except Exception:
            conteo_html = (
                "<div style='color:#cccccc;'>" +
                self.tr("Cargue un archivo para ver conteos por umbral.") +
                "</div>"
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
                + self.tr("Sin datos de ángulos mínimos en métricas. Genere/recargue métricas para ver el conteo por umbral.")
                + "</div>"
            )
        
        lbl_header = self.tr("Conteo de ángulos por umbral ({T}°):").format(T=int(T))
        lbl_tris = self.tr("Triángulos:")
        lbl_quads = self.tr("Cuadriláteros:")
        lbl_total = self.tr("Total:")
        lbl_of = self.tr("de")

        color_below = "#ff6b6b"
        color_above = "#4ecdc4"
        # Colores por categoría
        color_below = "#ff6b6b"  # rojo
        color_above = "#4ecdc4"  # verde-azulado

        return f"""
        <div>
            <b style='color:#ffffff;'>{lbl_header}</b><br>
            • {lbl_tris}<br>
            <span style='color:{color_below};'>{tri_below}</span> &lt; {T:.0f}° &nbsp;|&nbsp;
            <span style='color:{color_above};'>{tri_above}</span> &ge; {T:.0f}° &nbsp;<span style='color:#888;'>({self.tr(lbl_of)} {tri_total})</span><br>
            • {lbl_quads}<br>
            <span style='color:{color_below};'>{quad_below}</span> &lt; {T:.0f}° &nbsp;|&nbsp;
            <span style='color:{color_above};'>{quad_above}</span> &ge; {T:.0f}° &nbsp;<span style='color:#888;'>({self.tr(lbl_of)} {quad_total})</span><br>
            • {lbl_total}<br>
            <span style='color:{color_below};'>{total_below}</span> &lt; {T:.0f}° &nbsp;|&nbsp;
            <span style='color:{color_above};'>{total_above}</span> &ge; {T:.0f}° &nbsp;<span style='color:#888;'>({self.tr(lbl_of)} {total_total})</span>
        </div>
        """
    
# ------------------- FUNCIONES DE LA VELOCIDAD -------------------
#     
    def crear_seccion_animacion(self):
        """Sección de control de animación"""
        self.grupo_animacion = QGroupBox(self.tr("Control de Animación"))
        self.grupo_animacion.setStyleSheet("QGroupBox { font-weight: bold; color: #ffffff; }")
        layout = QVBoxLayout()
        layout.setSpacing(8)
        
        # Control de velocidad
        velocidad_layout = QHBoxLayout()
        self.label_velocidad_title = QLabel(self.tr("Velocidad:"))
        self.slider_velocidad = QSlider(Qt.Horizontal)
        self.slider_velocidad.setRange(500, 3000)
        self.slider_velocidad.setValue(1500)
        self.label_velocidad_valor = QLabel("1.5s")
        self.slider_velocidad.valueChanged.connect(self._on_velocidad_cambiada)

        velocidad_layout.addWidget(self.label_velocidad_title)
        velocidad_layout.addWidget(self.slider_velocidad)
        velocidad_layout.addWidget(self.label_velocidad_valor)
        
        layout.addLayout(velocidad_layout)
        self.grupo_animacion.setLayout(layout)
        self.layout_principal.addWidget(self.grupo_animacion)


# ------------------- FUNCIONES ESTADISTICAS DETALLADAS -------------------


    def build_stats_html(self, metricas):
        """Construye el HTML de estadísticas usando textos traducibles."""
        stats = metricas.get('estadisticas_generales', {}) or {}
        total_triangulos = stats.get('total_triangulos', 0)
        total_cuadrilateros = stats.get('total_cuadrilateros', 0)
        total_caras = total_triangulos + total_cuadrilateros

        # Calcular porcentajes
        porc_triangulos = (total_triangulos / total_caras * 100) if total_caras > 0 else 0.0
        porc_cuadrilateros = (total_cuadrilateros / total_caras * 100) if total_caras > 0 else 0.0

        # Helper para formateo seguro
        def fmt(x, pattern="{:.3f}"):
            try:
                return pattern.format(float(x))
            except Exception:
                return "N/A"

        # Secciones traducibles
        titulo_topologia = self.tr("Topología:")
        lbl_caras = self.tr("Caras:")
        lbl_tris = self.tr("Triángulos:")
        lbl_quads = self.tr("Cuadriláteros:")
        titulo_calidad = self.tr("Calidad:")

        # Triángulos
        tri = metricas.get('triangulos', {}) or {}
        tri_aspect = fmt(tri.get('aspect_ratio_avg'), "{:.3f}")
        tri_min_ang_min = fmt(tri.get('min_angle_min'), "{:.1f}")
        tri_max_ang_max = fmt(tri.get('max_angle_max'), "{:.1f}")
        tri_area_avg = fmt(tri.get('area_avg'), "{:.6f}")

        lbl_tri = self.tr("Triángulos:")
        lbl_aspect = self.tr("Relación aspecto:")
        lbl_ang_min = self.tr("Ángulo mínimo:")
        lbl_ang_max = self.tr("Ángulo máximo:")
        lbl_area_avg = self.tr("Área promedio:")

        # Cuadriláteros
        quad = metricas.get('cuadrilateros', {}) or {}
        quad_aspect = fmt(quad.get('aspect_ratio_avg'), "{:.3f}")
        quad_min_ang_min = fmt(quad.get('min_angle_min'), "{:.1f}")
        quad_max_ang_max = fmt(quad.get('max_angle_max'), "{:.1f}")
        quad_skew = fmt(quad.get('skew_avg'), "{:.3f}")
        quad_edge_ratio = fmt(quad.get('edge_ratio_avg'), "{:.3f}")

        lbl_quad = self.tr("Cuadriláteros:")
        lbl_skew = self.tr("Distorsión:")
        lbl_edge_ratio = self.tr("Relación aristas:")

        # Construcción del HTML
        parts = []
        parts.append(f"""
        <div style='background-color: #2a2a2a; padding: 12px; border-radius: 6px; font-family: monospace;'>
            <b>{titulo_topologia}</b><br>
            • {lbl_caras} <span style='color: #4ecdc4;'>{total_caras}</span><br>
            • {lbl_tris} <span style='color: #ff9f43;'>{total_triangulos}</span> ({porc_triangulos:.1f}%)<br>
            • {lbl_quads} <span style='color: #ff9f43;'>{total_cuadrilateros}</span> ({porc_cuadrilateros:.1f}%)<br><br>
            <b>{titulo_calidad}</b><br>
        """)

        if tri:
            parts.append(f"""
            <b>{lbl_tri}</b><br>
            • {lbl_aspect} <span style='color: #4ecdc4;'>{tri_aspect}</span><br>
            • {lbl_ang_min} <span style='color: #4ecdc4;'>{tri_min_ang_min}°</span><br>
            • {lbl_ang_max} <span style='color: #ff6b6b;'>{tri_max_ang_max}°</span><br>
            • {lbl_area_avg} <span style='color: #4ecdc4;'>{tri_area_avg}</span><br>
            """)

        if quad:
            parts.append(f"""
            <b>{lbl_quad}</b><br>
            • {lbl_aspect} <span style='color: #4ecdc4;'>{quad_aspect}</span><br>
            • {lbl_ang_min} <span style='color: #4ecdc4;'>{quad_min_ang_min}°</span><br>
            • {lbl_ang_max} <span style='color: #ff6b6b;'>{quad_max_ang_max}°</span><br>
            • {lbl_skew} <span style='color: #ff6b6b;'>{quad_skew}</span><br>
            • {lbl_edge_ratio} <span style='color: #4ecdc4;'>{quad_edge_ratio}</span><br>
            """)

        parts.append("</div>")
        return "\n".join(parts)

    def actualizar_estadisticas(self, metricas):
        # print("actualizar_estadisticas llamado", metricas)
        """Actualiza la sección de estadísticas con métricas de calidad"""
        self.metricas_actuales = metricas
        
        if not metricas or 'error' in metricas:
            titulo = self.tr("No hay métricas disponibles")
            subt = self.tr("Carga un modelo primero o verifica el archivo.")
            stats_html = f"""
            <div style='background-color: #2a2a2a; padding: 12px; border-radius: 6px; font-family: monospace; color: #ff6b6b;'>
                <b>❌ {titulo}</b><br>
                {subt}
            </div>
            """
            self.label_estadisticas.setText(stats_html)
            return
        
        # Refrescar el conteo por threshold si la sección existe
        try:
            if hasattr(self, 'label_threshold') and self.label_threshold:
                self.actualizar_display_threshold()
        except Exception:
            pass

        stats_html = self.build_stats_html(metricas)
        self.label_estadisticas.setText(stats_html)

        
    
    
    def crear_seccion_estadisticas(self):
        """Sección de estadísticas detalladas - Ahora se actualiza dinámicamente"""
        self.grupo_estadisticas = QGroupBox(self.tr("Estadísticas Detalladas"))
        self.grupo_estadisticas.setStyleSheet("QGroupBox { font-weight: bold; color: #ffffff; }")
        layout = QVBoxLayout()
        
        # Label para estadísticas (ahora se actualizará dinámicamente)
        self.label_estadisticas = QLabel()
        self.label_estadisticas.setTextFormat(Qt.RichText)
        self.label_estadisticas.setWordWrap(True)
        
        # Mensaje inicial
        titulo_espera = self.tr("Esperando modelo...")
        subt_espera = self.tr("Carga un archivo para ver las estadísticas.")
        html_inicial = f"""
        <div style='background-color: #2a2a2a; padding: 12px; border-radius: 6px; font-family: monospace; color: #4ecdc4;'>
            <b>🔄 {titulo_espera}</b><br>
            {subt_espera}
        </div>
        """
        self.label_estadisticas.setText(html_inicial)
        
        layout.addWidget(self.label_estadisticas)
        self.grupo_estadisticas.setLayout(layout)
        self.layout_principal.addWidget(self.grupo_estadisticas)
    


# ------------------- FUNCIONES VIEJAS DE LOS BOTONES QUE AUN SE USAN -------------------

    
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
        """Mostrar/Ocultar el punto del ángulo mínimo global usando métricas."""
        if self.isMesh3D:
            msg = self.tr("La visualización de puntos críticos no está disponible para mallas 3D.")
            QMessageBox.warning(self, "Error al mostrar puntos críticos", msg)
            return  # No aplicar en mallas 3D

        if self.refinement_viewer and self.refinement_viewer.switcher:
            sw = self.refinement_viewer.switcher
            sw.toggle_load = not sw.toggle_load
            if sw.toggle_load:
                sw.marcar_min_y_max_desde_metricas()
            else:
                sw.clear_extra_models()
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


 # ------------------- MÉTRICAS 3D -------------------

    def crear_seccion_metricas_3d(self):
        """Sección de métricas 3D (placeholder hasta que se actualice la malla)."""
        self.grupo_metricas_3d = QGroupBox(self.tr("Métricas 3D"))
        self.grupo_metricas_3d.setStyleSheet("QGroupBox { font-weight: bold; color: #ffffff; }")
        layout = QVBoxLayout()

        self.label_metricas_3d = QLabel()
        self.label_metricas_3d.setWordWrap(True)
        self.label_metricas_3d.setTextFormat(Qt.RichText)
        self.label_metricas_3d.setStyleSheet("""
            QLabel {
                background-color: #2a2a2a;
                padding: 12px;
                border-radius: 6px;
                min-height: 120px;
            }
        """)

        # Placeholder traducible (tarjeta)
        titulo_espera = self.tr("Esperando modelo 3D...")
        subt_espera = self.tr("Carga un archivo 3D para ver las métricas.")
        html_inicial = f"""
        <div style='background-color: #2a2a2a; padding: 12px; border-radius: 6px; font-family: monospace; color: #4ecdc4;'>
            <b>🔄 {titulo_espera}</b><br>
            {subt_espera}
        </div>
        """
        self.label_metricas_3d.setText(html_inicial)

        layout.addWidget(self.label_metricas_3d)
        self.grupo_metricas_3d.setLayout(layout)
        self.layout_principal.addWidget(self.grupo_metricas_3d)

    def actualizar_metricas_3d(self, ruta_archivo):
        """Actualiza el contenido de la sección Métricas 3D con HTML externo."""

        base, _ = os.path.splitext(str(ruta_archivo))
        jeansinput = f"{base}_jeanss.txt"
        # Leer contenido del archivo jeansinput
        try:
            with open(jeansinput, "r", encoding="utf-8") as fh:
                contenido = fh.read()
        except Exception as e:
            error_html = (
                "<div style='background-color:#2a2a2a; padding:12px; border-radius:6px; color:#ff6b6b;'>"
                f"<b>{self.tr('Error al leer métricas 3D')}</b><br>{str(e)}</div>"
            )
            self.metricas_3d_actuales = error_html
            self.label_metricas_3d.setText(error_html)
            return

        try:
            data = parse_jeans_output(contenido)
        except Exception as e:
            error_html = (
                "<div style='background-color:#2a2a2a; padding:12px; border-radius:6px; color:#ff6b6b;'>"
                f"<b>{self.tr('Error al parsear métricas 3D')}</b><br>{str(e)}</div>"
            )
            self.metricas_3d_actuales = error_html
            self.label_metricas_3d.setText(error_html)
            return

        # Campos esperados del parser
        total = data.get("total")
        negativos = data.get("negative")
        promedio = data.get("average_quality")
        peor = data.get("worst_quality")
        por_tipo = data.get("by_type", {})

        def f(v, nd=3):
            return f"{float(v):.{nd}f}"

        # Encabezado + resumen
        header_html = (
            "<div style='color:#9ad; font-family:Consolas, Menlo, monospace; font-weight:bold;'>"
            "Jens (Scaled Jacobian)"
            "</div>"
            "<div style='margin-top:6px; font-family:Consolas, Menlo, monospace; color:#eaeaea; line-height:1.35;'>"
        )

        if total is not None:
            header_html += (
                f"<div><span style='color:#888;'>{self.tr("Total elementos")}:</span> "
                f"<span style='color:#ffd54f;'>{total}</span></div>"
            )
        if negativos is not None:
            header_html += (
                f"<div><span style='color:#888;'>{self.tr("Invertidos")}:</span> "
                f"<span style='color:#ff6b6b;'>{negativos}</span></div>"
            )
        if promedio is not None:
            header_html += (
                f"<div><span style='color:#888;'>{self.tr("Promedio")}:</span> "
                f"<span style='color:#4ecdc4;'>{float(promedio):.5f}</span></div>"
            )
        if peor is not None:
            header_html += (
                f"<div><span style='color:#888;'>{self.tr("Peor")}:</span> "
                f"<span style='color:#ff9f43;'>{float(peor):.5f}</span></div>"
            )
        header_html += "</div>"

        # Por tipo (alineado con columnas fijas en ch)
        filas = []
        label_tipo = {
            "Hex": self.tr("Hexaedros"),
            "Pri": self.tr("Prismas"),
            "Pyr": self.tr("Pirámides"),
            "Tet": self.tr("Tetraedros"),
        }
        count_lbl = self.tr("Total:")
        avg_lbl = self.tr("Promedio:")
        min_lbl = self.tr("Mínimo:")
        max_lbl = self.tr("Máximo:")
        for label in ["Hex", "Pri", "Pyr", "Tet"]:
            if label in por_tipo:
                d = por_tipo[label]
                cnt = d.get("count", 0)
                avg = f(d.get("avg", 0.0), 3)
                mn = f(d.get("min", 0.0), 3)
                mx = f(d.get("max", 0.0), 3)
                fila = (
                    "<div>"
                    f"<span style='display:inline-block; width:4ch; color:#eaeaea;'><span style='color:#37e9c2;'>{label_tipo[label]}<br></span></span>"
                    f"<span style='display:inline-block; width:12ch; color:#eaeaea;'>{count_lbl}<span style='color:#ffd54f;'>{cnt} </span><br></span>"
                    f"<span style='display:inline-block; width:14ch; color:#eaeaea;'>{avg_lbl}<span style='color:#4ecdc4;'>{avg} </span><br></span>"
                    f"<span style='display:inline-block; width:14ch; color:#eaeaea;'>{min_lbl}<span style='color:#ff6b6b;'>{mn} </span><br></span>"
                    f"<span style='display:inline-block; width:14ch; color:#eaeaea;'>{max_lbl}<span style='color:#8bc34a;'>{mx} </span></span>"
                    "</div>"
                )
                filas.append(fila)
        
        tipos_html = ""
        if filas:
            tipos_html = (
                f"<div style='margin-top:10px; color:#aaa; font-family:Consolas, Menlo, monospace;'>{self.tr('Por tipo')}:</div>"
                "<div style='margin-top:4px; font-family:Consolas, Menlo, monospace;'>"
                + "".join(filas)
                + "</div>"
            )

        # Tarjeta final (sin ruta de archivo)
        html = (
            "<div style='background-color:#2a2a2a; padding:12px; border-radius:6px; max-width:100%;'>"
            f"{header_html}"
            f"{tipos_html}"
            "</div>"
        )

        self.metricas_3d_actuales = html
        self.label_metricas_3d.setText(html)

    #def limpiar_metricas_3d(self):
    #    """Vuelve al placeholder traducible para Métricas 3D."""
    #    self.metricas_3d_actuales = None
    #    titulo_espera = self.tr("Esperando modelo 3D...")
    #    subt_espera = self.tr("Carga un archivo 3D para ver las métricas.")
    #    html_inicial = f"""
    #    <div style='background-color: #2a2a2a; padding: 12px; border-radius: 6px; font-family: monospace; color: #4ecdc4;'>
    #        <b>🔄 {titulo_espera}</b><br>
    #        {subt_espera}
    #    </div>
    #    """
    #    self.label_metricas_3d.setText(html_inicial)


    
# ------------------- FUNCIONES DE TRADUCCION -------------------

    def retranslate_ui(self):
        """Actualizar todos los textos del panel (sin ifs por control)."""
        # Títulos y placeholders estáticos
        if hasattr(self, "grupo_metricas") and self.grupo_metricas:
            self.grupo_metricas.setTitle(self.tr("Métricas de Calidad"))
        if hasattr(self, "label_metricas") and self.label_metricas and not self.metricas_actuales:
            self.label_metricas.setText(self.tr("Cargue un archivo para ver las métricas"))

        if hasattr(self, "grupo_estadisticas") and self.grupo_estadisticas:
            self.grupo_estadisticas.setTitle(self.tr("Estadísticas Detalladas"))
            if hasattr(self, "label_estadisticas") and self.label_estadisticas:
                if self.metricas_actuales and 'error' not in self.metricas_actuales:
                    try:
                        self.label_estadisticas.setText(self._build_stats_html(self.metricas_actuales))
                    except Exception:
                        pass
                else:
                    titulo_espera = self.tr("Esperando modelo...")
                    subt_espera = self.tr("Carga un archivo para ver las estadísticas.")
                    html_inicial = f"""
                    <div style='background-color: #2a2a2a; padding: 12px; border-radius: 6px; font-family: monospace; color: #4ecdc4;'>
                        <b>🔄 {titulo_espera}</b><br>
                        {subt_espera}
                    </div>
                    """
                    self.label_estadisticas.setText(html_inicial)

        # NUEVO: traducir la sección Métricas 3D
        if hasattr(self, "grupo_metricas_3d") and self.grupo_metricas_3d:
            self.grupo_metricas_3d.setTitle(self.tr("Métricas 3D"))
            if hasattr(self, "label_metricas_3d") and self.label_metricas_3d and not self.metricas_3d_actuales:
                titulo_espera = self.tr("Esperando modelo 3D...")
                subt_espera = self.tr("Carga un archivo 3D para ver las métricas.")
                html_inicial = f"""
                <div style='background-color: #2a2a2a; padding: 12px; border-radius: 6px; font-family: monospace; color: #4ecdc4;'>
                    <b>🔄 {titulo_espera}</b><br>
                    {subt_espera}
                </div>
                """
                self.label_metricas_3d.setText(html_inicial)
        # Textos de la sección de animación

        if hasattr(self, "grupo_animacion") and self.grupo_animacion:
            self.grupo_animacion.setTitle(self.tr("Control de Animación"))
            self.label_velocidad_title.setText(self.tr("Velocidad:"))

        if hasattr(self, "grupo_threshold") and self.grupo_threshold:
            self._rebuild_threshold_static_texts()
            # Recalcular display (valor y conteos)
            self.actualizar_display_threshold()

        # Regenerar el bloque de “Nivel de Refinamiento”
        if hasattr(self, "_archivo_actual") and self._archivo_actual:
            try:
                self.actualizar_panel_derecho(self._archivo_actual)
            except Exception:
                pass

        # Si hay una celda seleccionada previamente, reconstruir su HTML traducido
        if getattr(self, "_ultima_celda", None):
            try:
                data = self._ultima_celda
                self.mostrar_info_celda(data["cell_id"], data["num_points"], data["min_angle"])
            except Exception:
                pass

    def changeEvent(self, event):
        # Regenerar HTML traducible al cambiar el idioma de la app
        if event.type() == QEvent.LanguageChange:
            # Título y placeholder de la sección de métricas
            self.retranslate_ui()
        super().changeEvent(event)